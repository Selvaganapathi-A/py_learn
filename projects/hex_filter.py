import math

import numpy as np
from PIL import Image


def hex_mask(diameter: int, /) -> np.ndarray:
    """
    Create a boolean hexagonal mask inside a bounding box.

    Args:
        diameter: Approximate width of the hexagon in pixels

    Returns:
        2D boolean numpy array
    """
    r = diameter / 2
    h = int(math.sin(math.radians(60)) * diameter)

    y, x = np.ogrid[:h, :diameter]
    cx, cy = diameter / 2, h / 2

    x = np.abs(x - cx)
    y = np.abs(y - cy)

    mask = (
        (x <= r) & (y <= (math.sqrt(3) * r / 2)) & ((math.sqrt(3) * x + y) <= (math.sqrt(3) * r))
    )

    return mask


def apply_hex(
    image: np.ndarray,
    mask: np.ndarray,
    x0: int,
    y0: int,
) -> None:
    """
    Apply hex averaging at a given top-left position.
    """
    h, w = mask.shape
    H, W, C = image.shape

    x1 = min(x0 + w, W)
    y1 = min(y0 + h, H)

    sub = image[y0:y1, x0:x1]
    sub_mask = mask[: y1 - y0, : x1 - x0]

    if not sub_mask.any():
        return

    mean_color = sub[sub_mask].mean(axis=0)
    sub[sub_mask] = mean_color


def hex_pixelate(
    image_path: str,
    save_path: str,
    diameter: int,
) -> None:
    """
    Apply honeycomb-style hex pixelation to an image.
    """
    image = np.asarray(Image.open(image_path)).astype(np.float64)
    mask = hex_mask(diameter)

    mask_h, mask_w = mask.shape
    step_x = int(mask_w * 0.75)
    step_y = mask_h

    H, W, _ = image.shape

    for col, x in enumerate(range(0, W, step_x)):
        y_offset = 0 if col % 2 == 0 else mask_h // 2

        for y in range(y_offset, H, step_y):
            apply_hex(image, mask, x, y)

    Image.fromarray(image.astype(np.uint8)).save(save_path)


def main():
    hex_pixelate(
        "C://Pictures/063.jpg",
        "C://Pictures/63 - Copy (63).jpg",
        64,
    )


if __name__ == "__main__":
    main()
