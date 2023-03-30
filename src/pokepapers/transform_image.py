from pathlib import Path
from typing import Optional, Union
import cv2
import numpy as np

SCALE_FACTOR: float = 1.5
RESOLUTION: tuple[int, int] = (1440, 2560)  # height x width
IMAGE = "./out/131.jpg"

# common resolutions (height x width):
# 9:16
# 1080 x 1920
# 1440 x 2560
# 3840 x 2160
# 7680 x 4320


def load_image(self, path: Union[str, Path]) -> cv2.Mat:
    return cv2.imread(str(path))


# source resolution -> TILE -> CROP -> RESIZE -> target resolution
# TILE: tile ceil(target/source) times
# CROP: crop to scale_factor * target
# RESIZE: resize (shrink) to target resolution
def transform_image(
    img: cv2.Mat, width: int, height: int, scaling: float = 1.0
) -> cv2.Mat:
    """
    Tile an image `img` up to the size `width`x`height`.
    The `scaling` factor, which should always be >1.0, allows downscaling of the
    original tile image, which can hide undesirable visual artifacts.
    """

    source_resolution = np.array(img.shape)
    target_resolution = np.array((height, width, 3))
    resolution_scaler = np.array((scaling, scaling, 1))

    crop_size = (target_resolution * resolution_scaler).astype(int)
    tile_factor = np.ceil((crop_size / source_resolution)).astype(int)

    img = np.tile(img, tile_factor)
    img = img[: crop_size[0], : crop_size[1], :]  # crop
    img = cv2.resize(img, target_resolution[1::-1])

    return img


def create_wallpaper(
    input_path: Union[str, Path],
    output_path: Optional[Union[str, Path]],
    width: int,
    height: int,
    scaling: float,
) -> cv2.Mat:
    input_path = str(input_path)
    input_img = cv2.imread(input_path)

    output_img = transform_image(input_img, width, height, scaling)

    if output_path:
        output_path = str(output_path)
        cv2.imwrite(output_path, output_img)
    return output_img
