

# table_renderer.py


from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from typing import List, cast


def render_table(table_data: List[List[str]]) -> BytesIO:
    font_size = 20
    padding = 12

    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            font_size
        )
    except Exception:
        font = ImageFont.load_default()

    # Figure out column widths
    col_count = max(len(row) for row in table_data)
    col_widths = [80] * col_count  # default width
    dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for row in table_data:
        for i, cell in enumerate(row):
            w = dummy.textbbox((0, 0), cell, font=font)[2] + padding * 2
            col_widths[i] = cast(int, max(col_widths[i], w))

    row_height = font_size + padding * 2
    img = Image.new("RGB", (sum(col_widths), row_height *
                    len(table_data)), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    y = 0
    for r, row in enumerate(table_data):
        x = 0
        for c, cell in enumerate(row):
            bg = (200, 200, 200) if r == 0 else (255, 255, 255)
            draw.rectangle([x, y, x + col_widths[c], y +
                           row_height], fill=bg, outline=(0, 0, 0))
            draw.text((x + padding, y + padding),
                      cell, font=font, fill=(0, 0, 0))
            x += col_widths[c]
        y += row_height

    out = BytesIO()
    img.save(out, format="PNG")
    out.seek(0)
    return out
