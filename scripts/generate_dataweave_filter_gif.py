#!/usr/bin/env python3
"""Render an educational looping GIF of DataWeave filter."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 880, 520
FPS_MS = 80

BG = (8, 22, 36)
PANEL = (16, 38, 56)
PANEL_EDGE = (36, 72, 98)
MUTED = (138, 163, 181)
WHITE = (236, 244, 250)
CYAN = (0, 176, 232)
AMBER = (255, 196, 72)
GREEN = (61, 220, 151)
NAVY = (10, 28, 44)
DIM = (24, 52, 74)
RED = (232, 92, 104)

ITEMS = [1, 2, 3, 4]


def keep(n: int) -> bool:
    return n % 2 == 0


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "dataweave-filter.gif"

FONT_DIR = Path("/usr/share/fonts/truetype/macos")
MONO_DIR = Path("/usr/share/fonts/truetype/jetbrains-mono")


def load(name: str, size: int, mono: bool = False) -> ImageFont.FreeTypeFont:
    path = (MONO_DIR if mono else FONT_DIR) / name
    return ImageFont.truetype(str(path), size)


F_TITLE = load("Inter-Bold.ttf", 32)
F_SUB = load("Inter-Medium.ttf", 15)
F_LABEL = load("Inter-SemiBold.ttf", 12)
F_BODY = load("Inter-Medium.ttf", 15)
F_NUM = load("Inter-Bold.ttf", 24)
F_CODE = load("JetBrainsMono-Medium.ttf", 14, mono=True)
F_GATE = load("Inter-Bold.ttf", 22)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def clamp(t: float) -> float:
    return 0.0 if t < 0 else 1.0 if t > 1 else t


def ease(t: float) -> float:
    t = clamp(t)
    return t * t * (3 - 2 * t)


def mix(c1, c2, t: float):
    t = clamp(t)
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


def rounded(draw, xy, r, fill, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def text_center(draw, xy, text, fnt, fill):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x - tw / 2, y - th / 2), text, font=fnt, fill=fill)


def draw_chip(draw, cx, cy, w, h, value, fill, outline, text_fill, scale=1.0):
    w, h = w * scale, h * scale
    rounded(draw, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 12, fill, outline, 3)
    if value != "":
        text_center(draw, (cx, cy + 1), str(value), F_NUM, text_fill)


def layout():
    ys = [172, 236, 300, 364]
    return {
        "input_x": 158,
        "gate_x": 440,
        "output_x": 722,
        "chip_w": 78,
        "chip_h": 48,
        "gate_box": (348, 150, 532, 386),
        "ys": ys,
        "out_ys": [204, 292],
    }


def render_frame(state: dict) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 5), fill=CYAN)
    L = layout()

    draw.text((36, 20), "DataWeave", font=F_TITLE, fill=CYAN)
    dw_w = draw.textbbox((0, 0), "DataWeave ", font=F_TITLE)[2]
    draw.text((36 + dw_w, 20), "filter", font=F_TITLE, fill=WHITE)
    draw.text(
        (38, 62),
        "Filter keeps some items and returns an array",
        font=F_SUB,
        fill=MUTED,
    )

    for x, label in (
        (L["input_x"], "INPUT ARRAY"),
        (L["gate_x"], "FILTER  isEven(n)"),
        (L["output_x"], "OUTPUT ARRAY"),
    ):
        text_center(draw, (x, 108), label, F_LABEL, MUTED)

    gate_edge = mix(CYAN, GREEN, state.get("gate_keep", 0))
    gate_edge = mix(gate_edge, RED, state.get("gate_drop", 0))
    rounded(draw, L["gate_box"], 22, PANEL, gate_edge, 3)
    text_center(draw, (L["gate_x"], 248), "keep?", F_GATE, WHITE)
    text_center(draw, (L["gate_x"], 282), "even → keep", F_SUB, GREEN)
    text_center(draw, (L["gate_x"], 306), "odd  → drop", F_SUB, mix(MUTED, RED, 0.7))

    chip_w, chip_h = L["chip_w"], L["chip_h"]
    pad_x, pad_y = 20, 14
    in_top = L["ys"][0] - chip_h / 2 - pad_y
    in_bot = L["ys"][-1] + chip_h / 2 + pad_y
    rounded(
        draw,
        (L["input_x"] - chip_w / 2 - pad_x, in_top, L["input_x"] + chip_w / 2 + pad_x, in_bot),
        18,
        (12, 30, 46),
        PANEL_EDGE,
        2,
    )

    kept_n = max(1, len(state.get("kept", [])) or 2)
    out_top = L["out_ys"][0] - chip_h / 2 - pad_y
    out_bot = L["out_ys"][min(kept_n, 2) - 1] + chip_h / 2 + pad_y if state.get("kept") else L["out_ys"][1] + chip_h / 2 + pad_y
    # Output box is shorter: only kept items, so size to two slots (typical result length here).
    out_bot = L["out_ys"][1] + chip_h / 2 + pad_y
    rounded(
        draw,
        (L["output_x"] - chip_w / 2 - pad_x, out_top, L["output_x"] + chip_w / 2 + pad_x, out_bot),
        18,
        (12, 30, 46),
        PANEL_EDGE,
        2,
    )

    active = state.get("active", -1)
    rejected = state.get("rejected", [0.0, 0.0, 0.0, 0.0])

    for i, val in enumerate(ITEMS):
        y = L["ys"][i]
        hi = state["input_hi"][i]
        rej = rejected[i]
        fill = mix(PANEL, AMBER, hi * 0.6)
        fill = mix(fill, mix(PANEL, RED, 0.35), rej)
        outline = mix(PANEL_EDGE, AMBER, hi)
        outline = mix(outline, RED, rej)
        text = mix(WHITE, mix(MUTED, RED, 0.5), rej)
        draw_chip(draw, L["input_x"], y, L["chip_w"], L["chip_h"], val, fill, outline, text, 1 + 0.07 * hi)

        left = L["input_x"] + 46
        right = L["gate_x"] - 100
        col = mix(PANEL_EDGE, AMBER, hi)
        if active == i:
            col = AMBER if not keep(val) or hi > 0 else GREEN
            if state.get("decided_keep") is True and active == i:
                col = GREEN
            if state.get("decided_keep") is False and active == i:
                col = RED
        if rej > 0.4:
            col = mix(col, RED, 0.8)
        draw.line((left, y, right, y), fill=col, width=3 if active == i else 2)
        draw.polygon([(right + 10, y), (right - 2, y - 6), (right - 2, y + 6)], fill=col)

    kept = state.get("kept") or []
    for k, val in enumerate(kept):
        y = L["out_ys"][k]
        fill_a = state["out_fill"][k] if k < len(state["out_fill"]) else 1.0
        fill = mix(DIM, (16, 70, 52), fill_a)
        edge = mix(PANEL_EDGE, GREEN, fill_a)
        draw_chip(draw, L["output_x"], y, L["chip_w"], L["chip_h"], val, fill, edge, WHITE, 1 + 0.08 * (1 - fill_a) * fill_a * 4)

    # Placeholder slots when nothing kept yet
    if not kept:
        for y in L["out_ys"]:
            draw_chip(draw, L["output_x"], y, L["chip_w"], L["chip_h"], "", DIM, PANEL_EDGE, MUTED)
    elif len(kept) == 1:
        draw_chip(draw, L["output_x"], L["out_ys"][1], L["chip_w"], L["chip_h"], "", DIM, PANEL_EDGE, MUTED)

    fly = state.get("fly")
    if fly:
        x, y, val, t, mode = fly
        if mode == "drop":
            glow = mix(AMBER, RED, t)
        else:
            glow = mix(AMBER, GREEN, t)
        alpha_fade = 1.0
        if mode == "drop" and t > 0.7:
            # fade by mixing toward background
            glow = mix(glow, BG, (t - 0.7) / 0.3)
            fill = mix(PANEL, glow, 0.35)
            fill = mix(fill, BG, (t - 0.7) / 0.3)
            text = mix(WHITE, BG, (t - 0.7) / 0.3)
            draw_chip(draw, x, y, 66, 40, val, fill, glow, text, 1.0)
        else:
            draw_chip(draw, x, y, 66, 40, val, mix(PANEL, glow, 0.4), glow, WHITE, 1.05)
        _ = alpha_fade

    # Keep path arrow from gate to output (shown when a keep is in flight or any kept exists)
    if state.get("show_keep_arrow"):
        y = state.get("keep_arrow_y", L["out_ys"][min(len(kept), 1)])
        left2 = L["gate_x"] + 100
        right2 = L["output_x"] - 48
        draw.line((left2, y, right2 - 10, y), fill=GREEN, width=3)
        draw.polygon([(right2, y), (right2 - 12, y - 6), (right2 - 12, y + 6)], fill=GREEN)

    status = state.get("status") or ""
    if status:
        col = mix(MUTED, GREEN, state.get("status_hi", 0))
        if state.get("status_drop"):
            col = mix(MUTED, RED, state.get("status_hi", 0.8))
        text_center(draw, (W / 2, 410), status, F_BODY, col)

    rounded(draw, (28, 436, W - 28, 498), 14, NAVY, PANEL_EDGE, 2)
    result = state.get("code_result", "[  ]")
    code = f"[1, 2, 3, 4]  filter  ((n) -> isEven(n))     //  {result}"
    draw.text((44, 454), code, font=F_CODE, fill=CYAN)

    return img


def timeline() -> list[dict]:
    frames: list[dict] = []
    L = layout()
    ready = {
        "input_hi": [0.0, 0.0, 0.0, 0.0],
        "out_fill": [],
        "kept": [],
        "rejected": [0.0, 0.0, 0.0, 0.0],
        "fly": None,
        "status": "Start with an array. filter tests every element.",
        "status_hi": 0.0,
        "status_drop": False,
        "active": -1,
        "code_result": "[  ]",
        "gate_keep": 0.0,
        "gate_drop": 0.0,
        "decided_keep": None,
        "show_keep_arrow": False,
        "keep_arrow_y": L["out_ys"][0],
    }
    for _ in range(10):
        frames.append(deepcopy(ready))

    for idx, src in enumerate(ITEMS):
        x0, y0 = L["input_x"], L["ys"][idx]
        xm, ym = L["gate_x"], L["ys"][idx]
        will_keep = keep(src)
        next_slot = len(frames[-1]["kept"])
        x1 = L["output_x"]
        y1 = L["out_ys"][next_slot] if will_keep else y0 + 70

        for i in range(5):
            s = deepcopy(frames[-1])
            hi = list(s["input_hi"])
            hi[idx] = ease((i + 1) / 5)
            s["input_hi"] = hi
            s["active"] = idx
            s["status"] = f"Item {idx + 1} of 4: test {src}"
            s["status_hi"] = 0.15
            s["status_drop"] = False
            s["fly"] = None
            s["decided_keep"] = None
            s["gate_keep"] = 0.0
            s["gate_drop"] = 0.0
            s["show_keep_arrow"] = False
            frames.append(s)

        for i in range(7):
            t = ease((i + 1) / 7)
            s = deepcopy(frames[-1])
            s["fly"] = (lerp(x0, xm, t), y0, src, t * 0.3, "test")
            s["status"] = f"isEven({src}) ?"
            frames.append(s)

        for i in range(6):
            t = ease((i + 1) / 6)
            s = deepcopy(frames[-1])
            mode = "keep" if will_keep else "drop"
            s["fly"] = (xm, ym, src, 0.35 + 0.25 * t, mode)
            s["decided_keep"] = will_keep
            if will_keep:
                s["gate_keep"] = t
                s["gate_drop"] = 0.0
                s["status"] = f"{src} is even  →  keep"
                s["status_hi"] = t
                s["status_drop"] = False
            else:
                s["gate_drop"] = t
                s["gate_keep"] = 0.0
                s["status"] = f"{src} is odd  →  drop"
                s["status_hi"] = t
                s["status_drop"] = True
            frames.append(s)

        if will_keep:
            for i in range(8):
                t = ease((i + 1) / 8)
                s = deepcopy(frames[-1])
                s["fly"] = (lerp(xm, x1, t), lerp(ym, y1, t), src, 0.7 + 0.3 * t, "keep")
                s["show_keep_arrow"] = True
                s["keep_arrow_y"] = lerp(ym, y1, t)
                frames.append(s)

            for i in range(4):
                t = ease((i + 1) / 4)
                s = deepcopy(frames[-1])
                kept = list(s["kept"])
                fills = list(s["out_fill"])
                if src not in kept:
                    kept.append(src)
                    fills.append(0.0)
                fills[-1] = t
                s["kept"] = kept
                s["out_fill"] = fills
                s["fly"] = None
                s["show_keep_arrow"] = t < 1
                hi = list(s["input_hi"])
                hi[idx] = 1 - t * 0.85
                s["input_hi"] = hi
                s["code_result"] = "[ " + ",  ".join(str(v) for v in kept) + " ]"
                s["status"] = f"Write {src} into the result array"
                s["status_drop"] = False
                s["gate_keep"] = 1 - t
                frames.append(s)
        else:
            for i in range(8):
                t = ease((i + 1) / 8)
                s = deepcopy(frames[-1])
                s["fly"] = (xm, lerp(ym, ym + 90, t), src, 0.55 + 0.45 * t, "drop")
                s["show_keep_arrow"] = False
                frames.append(s)

            for i in range(4):
                t = ease((i + 1) / 4)
                s = deepcopy(frames[-1])
                s["fly"] = None
                rej = list(s["rejected"])
                rej[idx] = t
                s["rejected"] = rej
                hi = list(s["input_hi"])
                hi[idx] = 1 - t
                s["input_hi"] = hi
                s["status"] = f"{src} is not in the result array"
                s["gate_drop"] = 1 - t
                frames.append(s)

        for _ in range(3):
            frames.append(deepcopy(frames[-1]))

    for i in range(6):
        s = deepcopy(frames[-1])
        s["status"] = "filter returns a new array — only the items that passed"
        s["status_hi"] = ease((i + 1) / 6)
        s["status_drop"] = False
        s["active"] = -1
        s["fly"] = None
        s["input_hi"] = [0.0, 0.0, 0.0, 0.0]
        s["gate_keep"] = 0.0
        s["gate_drop"] = 0.0
        s["show_keep_arrow"] = False
        frames.append(s)

    for _ in range(18):
        frames.append(deepcopy(frames[-1]))

    return frames


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    states = timeline()
    rgb = [render_frame(s) for s in states]
    palette = rgb[len(rgb) // 2].quantize(colors=64, method=Image.Quantize.MEDIANCUT)
    images = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in rgb]
    images[0].save(
        OUT,
        save_all=True,
        append_images=images[1:],
        duration=FPS_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )
    size_kb = OUT.stat().st_size / 1024
    print(f"Wrote {OUT} ({len(images)} frames, {size_kb:.1f} KiB)")


if __name__ == "__main__":
    main()
