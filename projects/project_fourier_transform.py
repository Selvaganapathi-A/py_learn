import os

import numpy as np
from PIL import Image, ImageDraw


def get_samples(frequency: int,
                amplitude: int = 100) -> list[tuple[float, float]]:
    m: list[tuple[float, float]] = list()

    samples = 2160

    graph_length = 2160

    step_increase = graph_length // samples

    cut_off_angle = graph_length * frequency / (2880)

    # print(cut_off_angle)
    # print(step_increase)

    for x in range(0, graph_length + 1, step_increase):
        angle = np.radians(x * cut_off_angle)
        y = np.sin(angle) * amplitude
        m.append((x, y))

    return m


def main():
    my_img = Image.new("RGBA", size=(3000, 2280), color="#ccccccee")
    imdraw = ImageDraw.Draw(my_img, "RGBA")

    signals = [
        get_samples(1, 400),
    ]

    for x in range(3, 8, 2):
        signals.append(get_samples(x, 100))

    for i, (signal) in enumerate(signals, start=1):
        for co_ords in signal:
            x = int(co_ords[0]) + 30
            y = int(co_ords[1]) + 425
            imdraw.ellipse((x - 1, y - 1, x + 1, y + 1), fill="black")

    for j in range(2160):
        x = int(signals[0][j][0]) + 30
        y = int(signals[0][j][1]) + 425
        imdraw.ellipse((x - 1, y - 1, x + 1, y + 1), fill="black")

        ysum: list[float] = []
        for i in range(1, len(signals)):
            ysum.append(signals[i][j][1] / ((i - 1) * 2 + 1))
            # if i % 2 == 0:
            #     ysum.append(signals[i][j][1] / i)
            # else:
            #     ysum.append(0 - signals[i][j][1] / i)
        ysum.append(signals[0][j][1])
        x = int(signals[0][j][0]) + 30
        y = int(sum(ysum) / len(signals)) + 425

        imdraw.ellipse((x - 2, y - 2, x + 2, y + 2), fill="red")

    # my_img.save("hello sawtooth wave.png")
    my_img.save("hello square wave.png")
    my_img.close()


if __name__ == "__main__":
    os.system("clear")
    main()
    pass
