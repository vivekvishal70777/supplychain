#!/usr/bin/env python3
"""Render an educational looping GIF of DataWeave map."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 880, 500
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

ITEMS = [1, 2, 3]
MAPPED = [n * 2 for n in ITEMS]

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "dataweave-map.gif"

FONT_DIR = Path("/usr/share/fonts/truetype/macos")
MONO_DIR = Path("/usr/share/fonts/truetype/jetbrains-mono")


def load(name: str, size: int, mono: bool = False) -> ImageFont.FreeTypeFont:
    path = (MONO_DIR if mono else FONT_DIR) / name
    return ImageFont.truetype(str(path), size)


F_TITLE = load("Inter-Bold.ttf", 32)
F_SUB = load("Inter-Medium.ttf", 15)
F_LABEL = load("Inter-SemiBold.ttf", 12)
F_BODY = load("Inter-Medium.ttf", 15)
F_NUM = load("Inter-Bold.ttf", 26)
F_CODE = load("JetBrainsMono-Medium.ttf", 14, mono=True)


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
    rounded(draw, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 14, fill, outline, 3)
    text_center(draw, (cx, cy + 1), str(value), F_NUM, text_fill)


def layout():
    ys = [178, 256, 334]
    return {
        "input_x": 168,
        "map_x": 440,
        "output_x": 712,
        "chip_w": 86,
        "chip_h": 54,
        "map_box": (352, 148, 528, 364),
        "ys": ys,
    }


def render_frame(state: dict) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 5), fill=CYAN)
    L = layout()

    draw.text((36, 22), "DataWeave", font=F_TITLE, fill=CYAN)
    dw_w = draw.textbbox((0, 0), "DataWeave ", font=F_TITLE)[2]
    draw.text((36 + dw_w, 22), "map", font=F_TITLE, fill=WHITE)
    draw.text(
        (38, 64),
        "Iterate over each item in an array, perform an operation, and return an array",
        font=F_SUB,
        fill=MUTED,
    )

    for x, label in (
        (L["input_x"], "INPUT ARRAY"),
        (L["map_x"], "MAP  ((n) -> n * 2)"),
        (L["output_x"], "OUTPUT ARRAY"),
    ):
        text_center(draw, (x, 112), label, F_LABEL, MUTED)

    rounded(draw, L["map_box"], 22, PANEL, CYAN, 3)
    text_center(draw, (L["map_x"], 246), "n × 2", F_TITLE, WHITE)
    text_center(draw, (L["map_x"], 292), "one result per item", F_SUB, MUTED)

    chip_w, chip_h = L["chip_w"], L["chip_h"]
    pad_x, pad_y = 22, 16
    for x in (L["input_x"], L["output_x"]):
        top = L["ys"][0] - chip_h / 2 - pad_y
        bot = L["ys"][-1] + chip_h / 2 + pad_y
        rounded(
            draw,
            (x - chip_w / 2 - pad_x, top, x + chip_w / 2 + pad_x, bot),
            20,
            (12, 30, 46),
            PANEL_EDGE,
            2,
        )

    active = state.get("active", -1)

    for i, val in enumerate(ITEMS):
        y = L["ys"][i]
        hi = state["input_hi"][i]
        fill = mix(PANEL, AMBER, hi * 0.6)
        outline = mix(PANEL_EDGE, AMBER, hi)
        draw_chip(draw, L["input_x"], y, L["chip_w"], L["chip_h"], val, fill, outline, WHITE, 1 + 0.07 * hi)
        # row connector
        y_line = y
        left = L["input_x"] + 50
        right = L["map_x"] - 96
        col = mix(PANEL_EDGE, AMBER, hi)
        if active == i:
            col = AMBER
        draw.line((left, y_line, right, y_line), fill=col, width=3 if active == i else 2)
        draw.polygon([(right + 10, y_line), (right - 2, y_line - 6), (right - 2, y_line + 6)], fill=col)

        left2 = L["map_x"] + 96
        right2 = L["output_x"] - 50
        col2 = mix(PANEL_EDGE, GREEN, state["out_fill"][i])
        if active == i:
            col2 = GREEN
        draw.line((left2, y_line, right2 - 10, y_line), fill=col2, width=3 if active == i else 2)
        draw.polygon([(right2, y_line), (right2 - 12, y_line - 6), (right2 - 12, y_line + 6)], fill=col2)

    for i, val in enumerate(MAPPED):
        y = L["ys"][i]
        fill_a = state["out_fill"][i]
        if fill_a <= 0:
            draw_chip(draw, L["output_x"], y, L["chip_w"], L["chip_h"], "", DIM, PANEL_EDGE, MUTED)
        else:
            fill = mix(DIM, (16, 70, 52), fill_a)
            edge = mix(PANEL_EDGE, GREEN, fill_a)
            draw_chip(
                draw,
                L["output_x"],
                y,
                L["chip_w"],
                L["chip_h"],
                val,
                fill,
                edge,
                WHITE,
                1 + 0.1 * (1 - fill_a) * fill_a * 4,
            )

    fly = state.get("fly")
    if fly:
        x, y, val, t = fly
        glow = mix(AMBER, GREEN, t)
        draw_chip(draw, x, y, 70, 44, val, mix(PANEL, glow, 0.4), glow, WHITE, 1.06)

    status = state.get("status") or ""
    if status:
        text_center(draw, (W / 2, 392), status, F_BODY, mix(MUTED, GREEN, state.get("status_hi", 0)))

    rounded(draw, (28, 418, W - 28, 478), 14, NAVY, PANEL_EDGE, 2)
    result = state.get("code_result", "[ ?,  ?,  ? ]")
    code = f"[1, 2, 3]  map  ((n) -> n * 2)     //  {result}"
    draw.text((48, 436), code, font=F_CODE, fill=CYAN)

    return img


def timeline() -> list[dict]:
    frames: list[dict] = []
    L = layout()
    ready = {
        "input_hi": [0.0, 0.0, 0.0],
        "out_fill": [0.0, 0.0, 0.0],
        "fly": None,
        "status": "Start with an array. map visits every element.",
        "status_hi": 0.0,
        "active": -1,
        "code_result": "[ ?,  ?,  ? ]",
    }
    for _ in range(10):
        frames.append(deepcopy(ready))

    built = ["?", "?", "?"]

    for idx, (src, dst) in enumerate(zip(ITEMS, MAPPED)):
        x0, y0 = L["input_x"], L["ys"][idx]
        xm, ym = L["map_x"], L["ys"][idx]
        x1, y1 = L["output_x"], L["ys"][idx]

        for i in range(5):
            s = deepcopy(frames[-1])
            hi = list(s["input_hi"])
            hi[idx] = ease((i + 1) / 5)
            s["input_hi"] = hi
            s["active"] = idx
            s["status"] = f"Item {idx + 1} of 3: take {src}"
            s["status_hi"] = 0.15
            s["fly"] = None
            frames.append(s)

        for i in range(7):
            t = ease((i + 1) / 7)
            s = deepcopy(frames[-1])
            s["fly"] = (lerp(x0, xm, t), y0, src, t * 0.35)
            s["status"] = f"Apply the operation: {src} × 2"
            frames.append(s)

        for i in range(6):
            t = ease((i + 1) / 6)
            s = deepcopy(frames[-1])
            shown = src if t < 0.4 else dst
            s["fly"] = (xm, ym, shown, 0.35 + 0.4 * t)
            s["status"] = f"{src} × 2  =  {dst}"
            s["status_hi"] = t
            frames.append(s)

        for i in range(7):
            t = ease((i + 1) / 7)
            s = deepcopy(frames[-1])
            s["fly"] = (lerp(xm, x1, t), y1, dst, 0.75 + 0.25 * t)
            frames.append(s)

        built[idx] = str(dst)
        result = "[ " + ",  ".join(built) + " ]"
        for i in range(4):
            t = ease((i + 1) / 4)
            s = deepcopy(frames[-1])
            fill = list(s["out_fill"])
            fill[idx] = t
            s["out_fill"] = fill
            s["fly"] = None
            hi = list(s["input_hi"])
            hi[idx] = 1 - t * 0.85
            s["input_hi"] = hi
            s["code_result"] = result
            s["status"] = f"Write {dst} into the result array"
            frames.append(s)

        for _ in range(3):
            frames.append(deepcopy(frames[-1]))

    for i in range(6):
        s = deepcopy(frames[-1])
        s["status"] = "map returns a new array — same length, transformed items"
        s["status_hi"] = ease((i + 1) / 6)
        s["active"] = -1
        s["fly"] = None
        s["input_hi"] = [0.0, 0.0, 0.0]
        frames.append(s)

    for _ in range(18):
        frames.append(deepcopy(frames[-1]))

    return frames


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    states = timeline()
    rgb = [render_frame(s) for s in states]
    # Shared palette keeps GIF smaller and colors stable.
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
