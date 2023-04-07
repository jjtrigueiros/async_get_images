import cv2
import numpy as np


# common resolutions (height x width):
# 9:16
# 1080 x 1920
# 1440 x 2560
# 3840 x 2160
# 7680 x 4320


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
