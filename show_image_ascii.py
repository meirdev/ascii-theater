import sys

from PIL import Image


ASCII_CHARS = "@%#*+=-:. "


def write_image(path: str, width: int = 90, scale_factor: int = 2) -> None:
    image = Image.open(path)

    aspect_ratio = image.height / image.width

    height = int(width * aspect_ratio / scale_factor)

    image = image.resize((width, height)).convert("L")

    ascii_image = "".join(ASCII_CHARS[int(pixel / 255 * (len(ASCII_CHARS) - 1))] for pixel in image.getdata())

    print("\n".join(ascii_image[i:i + width] for i in range(0, len(ascii_image), width)))


if __name__ == "__main__":
    write_image(sys.argv[1])
