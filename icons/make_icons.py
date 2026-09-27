"""Make the small-size icons from the original logo files.

Run from the repository root:  uv run --with pillow python icons/make_icons.py

What it does, and why:
- Starts from the "sem nome (sem azul)" versions: at icon sizes the name and
  Urania can't be read.
- Crops close around the spiral and its stars, leaving out the lone star
  below them, so the drawing fills the icon.
- For the light-theme icon (black drawing), makes the spiral twice as opaque:
  as drawn (13% opacity) it disappears on light backgrounds at small sizes.
  Shapes and colours are unchanged.
- The dark-theme icon (white drawing) is only cropped.
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "icons"

SPIRAL = (715, 618, 3108, 2742)  # spiral and its stars in the 3832 px originals
PADDING = 0.04                   # margin around the drawing, as a fraction of its size
SPIRAL_OPACITY = 2.0             # light-theme icon only
SIZE = 512


def square_crop(im, box, pad):
    x0, y0, x1, y1 = box
    side = int(max(x1 - x0, y1 - y0) * (1 + 2 * pad))
    left, top = (x0 + x1) // 2 - side // 2, (y0 + y1) // 2 - side // 2
    return im.crop((left, top, left + side, top + side))


def strengthen(im, factor):
    """Multiply the opacity of the faint parts; opaque stars stay as they are."""
    r, g, b, a = im.split()
    return Image.merge("RGBA", (r, g, b, a.point(lambda v: max(v, min(255, round(v * factor))))))


def make(source, target, factor=None):
    im = Image.open(ROOT / source).convert("RGBA")
    im = square_crop(im, SPIRAL, PADDING)
    if factor:
        im = strengthen(im, factor)
    im.resize((SIZE, SIZE), Image.LANCZOS).save(OUT / target, optimize=True)
    print(f"{source} -> icons/{target}")


make("pleiad logo preto sem nome (sem azul).png", "pleiad-icon-light.png", SPIRAL_OPACITY)
make("pleiad logo branco sem nome (sem azul).png", "pleiad-icon-dark.png")
