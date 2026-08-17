from PIL import Image, ImageDraw


def make_icon_image():
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((2, 2, size - 2, size - 2), fill=(30, 30, 40, 255), outline=(255, 200, 0, 255), width=3)
    draw.polygon(
        [(32, 12), (44, 30), (38, 30), (46, 48), (24, 26), (30, 26), (20, 12)],
        fill=(255, 200, 0, 255),
    )
    return img
