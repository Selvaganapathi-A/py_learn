import math

import numpy
from PIL import Image, ImageDraw


def function_HexagonalMask(radius: int = 10):
    width = radius
    height = int(math.sin(math.radians(60)) * width) + 1
    image = Image.new("1", size=(width, height), color="black")
    draw = ImageDraw.Draw(image)
    draw.polygon(
        tuple((
            round(
                (width / 2) + math.cos(math.radians(value * 60)) * (radius / 2),
                2,
            ),
            round(
                (height / 2) + math.sin(math.radians(value * 60)) *
                (radius / 2),
                2,
            ),
        ) for value in range(6)),
        fill=(1,),
    )
    mask = numpy.array(image).astype(bool)
    del draw, image
    return mask


def hexgonFilter(imagePath: str, savePath: str, pixel_diameter: int):
    # maskWidth = 16
    mask = function_HexagonalMask(pixel_diameter)
    maskHeight, maskWidth = mask.shape
    maskCenterY, maskCenterX = int(maskHeight / 2), int(maskWidth / 2)
    image = Image.open(imagePath, "r")
    imageArray = numpy.array(image).astype(numpy.float64)
    image.close()
    del image
    imageHeight, imageWidth, noOfChannels = imageArray.shape
    imageCenterX, imageCenterY = int(imageWidth / 2), int(imageHeight / 2)
    # Top-Right Corner
    i = 0
    tempXPointer = imageCenterX - maskCenterX
    while True:
        tempYPointer = (imageCenterY - maskCenterY if i %
                        2 == 0 else imageCenterY - maskHeight)
        startWidth, endWidth = tempXPointer, tempXPointer + maskWidth
        startWidth = 0 if startWidth < 0 else startWidth
        endWidth = imageWidth if imageWidth < endWidth else endWidth
        while True:
            startHeight, endHeight = (
                tempYPointer,
                tempYPointer + maskHeight,
            )
            startHeight = 0 if startHeight < 0 else startHeight
            endHeight = (imageHeight if imageHeight < endHeight else endHeight)
            cutImageArray = imageArray[startHeight:endHeight,
                                       startWidth:endWidth, :]
            cutImageArrayHeight, cutImageArrayWidth, _ = (cutImageArray.shape)
            cutMask = mask[
                maskHeight - cutImageArrayHeight:maskHeight,
                0:cutImageArrayWidth,
            ]
            uniqueValues, counts = numpy.unique(cutMask, return_counts=True)
            Trues = 0
            for bools, count in zip(uniqueValues, counts):
                if bools:
                    Trues = count
            if 0 < Trues:
                cutImageArray2 = numpy.zeros(shape=cutImageArray.shape)
                cutImageArray2[cutMask] = cutImageArray[cutMask]
                cutImageArray[cutMask] = tuple(
                    numpy.sum(cutImageArray2[:, :, counter]) / Trues
                    for counter in range(noOfChannels))
            tempYPointer = tempYPointer - maskHeight
            if tempYPointer <= (0 - maskHeight):
                break
        i += 1
        tempXPointer = tempXPointer + int(maskWidth * 0.75)
        if imageWidth <= tempXPointer:
            break
    # Bottom-Right Corner
    i = 0
    tempXPointer = imageCenterX - maskCenterX
    while True:
        tempYPointer = (imageCenterY + maskCenterY if i %
                        2 == 0 else imageCenterY)
        startWidth, endWidth = tempXPointer, tempXPointer + maskWidth
        startWidth = 0 if startWidth < 0 else startWidth
        endWidth = imageWidth if imageWidth < endWidth else endWidth
        while True:
            startHeight, endHeight = (
                tempYPointer,
                tempYPointer + maskHeight,
            )
            startHeight = 0 if startHeight < 0 else startHeight
            endHeight = (imageHeight if imageHeight < endHeight else endHeight)
            cutImageArray = imageArray[startHeight:endHeight,
                                       startWidth:endWidth, :]
            cutImageArrayHeight, cutImageArrayWidth, _ = (cutImageArray.shape)
            cutMask = mask[
                :cutImageArrayHeight,
                :cutImageArrayWidth,
            ]
            uniqueValues, counts = numpy.unique(cutMask, return_counts=True)
            Trues = 0
            for bools, count in zip(uniqueValues, counts):
                if bools:
                    Trues = count
            if 0 < Trues:
                cutImageArray2 = numpy.zeros(shape=cutImageArray.shape)
                cutImageArray2[cutMask] = cutImageArray[cutMask]
                cutImageArray[cutMask] = tuple(
                    numpy.sum(cutImageArray2[:, :, counter]) / Trues
                    for counter in range(noOfChannels))
            tempYPointer = tempYPointer + maskHeight
            if imageHeight <= tempYPointer:
                break
        i += 1
        tempXPointer = tempXPointer + int(maskWidth * 0.75)
        if imageWidth <= tempXPointer:
            break
    # Bottom Left
    i = 1
    tempXPointer = imageCenterX - int(0.75 * maskWidth) - maskCenterX
    while True:
        tempYPointer = (imageCenterY + maskCenterY if i %
                        2 == 0 else imageCenterY)
        startWidth, endWidth = tempXPointer, tempXPointer + maskWidth
        startWidth = 0 if startWidth < 0 else startWidth
        endWidth = imageWidth if imageWidth < endWidth else endWidth
        while True:
            startHeight, endHeight = (
                tempYPointer,
                tempYPointer + maskHeight,
            )
            startHeight = 0 if startHeight < 0 else startHeight
            endHeight = (imageHeight if imageHeight < endHeight else endHeight)
            cutImageArray = imageArray[startHeight:endHeight,
                                       startWidth:endWidth, :]
            cutImageArrayHeight, cutImageArrayWidth, _ = (cutImageArray.shape)
            cutMask = mask[
                :cutImageArrayHeight,
                maskWidth - cutImageArrayWidth:,
            ]
            uniqueValues, counts = numpy.unique(cutMask, return_counts=True)
            Trues = 0
            for bools, count in zip(uniqueValues, counts):
                if bools:
                    Trues = count
            if 0 < Trues:
                cutImageArray2 = numpy.zeros(shape=cutImageArray.shape)
                cutImageArray2[cutMask] = cutImageArray[cutMask]
                cutImageArray[cutMask] = tuple(
                    numpy.sum(cutImageArray2[:, :, counter]) / Trues
                    for counter in range(noOfChannels))
            tempYPointer = tempYPointer + maskHeight
            if imageHeight <= tempYPointer:
                break
        i += 1
        tempXPointer = tempXPointer - int(maskWidth * 0.75)
        if tempXPointer <= (0 - maskWidth):
            break
    # Top-Left Corner
    i = 1
    tempXPointer = imageCenterX - int(0.75 * maskWidth) - maskCenterX
    while True:
        tempYPointer = (imageCenterY - maskCenterY if i %
                        2 == 0 else imageCenterY - maskHeight)
        startWidth, endWidth = tempXPointer, tempXPointer + maskWidth
        startWidth = 0 if startWidth < 0 else startWidth
        endWidth = imageWidth if imageWidth < endWidth else endWidth
        while True:
            startHeight, endHeight = (
                tempYPointer,
                tempYPointer + maskHeight,
            )
            startHeight = 0 if startHeight < 0 else startHeight
            endHeight = (imageHeight if imageHeight < endHeight else endHeight)
            cutImageArray = imageArray[startHeight:endHeight,
                                       startWidth:endWidth, :]
            cutImageArrayHeight, cutImageArrayWidth, _ = (cutImageArray.shape)
            cutMask = mask[
                maskHeight - cutImageArrayHeight:,
                maskWidth - cutImageArrayWidth:,
            ]
            uniqueValues, counts = numpy.unique(cutMask, return_counts=True)
            Trues = 0
            for bools, count in zip(uniqueValues, counts):
                if bools:
                    Trues = count
            if 0 < Trues:
                cutImageArray2 = numpy.zeros(shape=cutImageArray.shape)
                cutImageArray2[cutMask] = cutImageArray[cutMask]
                cutImageArray[cutMask] = tuple(
                    numpy.sum(cutImageArray2[:, :, counter]) / Trues
                    for counter in range(noOfChannels))

            tempYPointer = tempYPointer - maskHeight
            if tempYPointer <= (0 - maskHeight):
                break
        i += 1
        tempXPointer = tempXPointer - int(maskWidth * 0.75)
        if tempXPointer <= (0 - maskWidth):
            break

    image = Image.fromarray(imageArray.astype(numpy.uint8))
    image.save(savePath)
    image.close()
    return None


def main():
    hexgonFilter(
        imagePath=r"./images/001.jpg",
        savePath=r"./images/001-001.jpg",
        pixel_diameter=128,
    )


if __name__ == "__main__":
    main()
