import os
from typing import Any

from common.module_os import function_new_filename
from PIL import Image, ImageDraw


def func_image_type(pathlike: str) -> str | None:
    image_type = None
    image = Image.open(pathlike, "r")
    image_type = image.format
    image.close()
    return image_type


def getColors(
    imagePath: str,
    noOfColors: int = 6,
    reSize: int = 256,
) -> list[Any]:
    image = Image.open(imagePath, "r")
    imageCopy = image.copy()
    imageCopy.resize(
        (
            reSize,
            reSize,
        ),
    )
    image.close()

    # Reduce Palette
    imagePalette = imageCopy.convert(
        "P",
        palette=Image.WEB,
        colors=noOfColors,
    )

    # Find Dominant Colors in Image
    palette = imagePalette.getpalette()
    colorCounts = sorted(
        imagePalette.getcolors(),
        reverse=True,
    )
    colors = list()
    for i in range(noOfColors):
        paletteIndex = colorCounts[i][1]
        dominanColor = palette[
            paletteIndex * 3 : paletteIndex * 3 + 3
        ]
        colors.append(
            tuple(
                dominanColor,
            ),
        )
    return colors


def save_palette(colors, swatchsize=128, outfile="palette.png"):
    num_colors = len(colors)
    palette = Image.new(
        "RGB",
        (
            swatchsize * num_colors,
            swatchsize,
        ),
    )
    draw = ImageDraw.Draw(palette)
    posx: int = 0
    posy: int = 0

    for color in colors:
        draw.rectangle(
            (
                posx,
                posy,
                posx + swatchsize,
                posy + swatchsize,
            ),
            fill=color,
        )
        posx = posx + swatchsize
    del (
        draw,
        posx,
        posy,
        num_colors,
    )
    palette.save(
        function_new_filename(
            outfile, "output", makedirs=True, filetype_alt=".png"
        ),
        "PNG",
    )


def main() -> None:
    pathlike = os.path.join(os.path.dirname(__file__), "AppData")
    if not os.path.exists(pathlike):
        os.makedirs(pathlike)
    for root, _, files in os.walk(os.path.abspath(pathlike)):
        for filename in files:
            filepath = os.path.join(root, filename)
            print(filepath, func_image_type(filepath))
            colors = getColors(
                filepath,
                27,
            )
            print(colors)
            # save_palette(
            #     colors,
            #     outfile=filepath,
            # )
            break
        break


if __name__ == "__main__":
    src = (
        r"C:\Users\Tesla\Pictures\SpotLight\1920 x 1080\01fe7d49e20a3936896924062a504c837cfe08d54915b8390fa359074a75441d.jpeg",
    )
    print(
        getColors(
            src,
            8,
            512,
        )
    )
