import numpy as np
from PIL import Image


def transform_image(img: Image, width: int, height: int, scaling: float = 1.0) -> Image:
    """
    Tile and crop an image `img` up to the resolution given by `width`x`height`.

    The `scaling` factor allows downscaling of the original tile image, to allow hiding
    undesirable visual artifacts, ex. due to compression.
    Since there is no benefit in upscaling, `scaling` should always be `>=1.0`.
    """

    img_array = np.array(img)
    source_resolution = np.array(img_array.shape)
    target_resolution = np.array((height, width, 3))
    resolution_scaler = np.array((scaling, scaling, 1))

    crop_size = (target_resolution * resolution_scaler).astype(int)
    tile_factor = np.ceil((crop_size / source_resolution)).astype(int)

    img_array = np.tile(img_array, tile_factor)
    img_array = img_array[: crop_size[0], : crop_size[1], :]
    img = Image.fromarray(img_array)
    img = img.resize(target_resolution[1::-1])

    return img
