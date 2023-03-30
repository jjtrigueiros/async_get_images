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


# source resolution -> TILE -> CROP -> RESIZE -> target resolution
# TILE: tile ceil(target/source) times
# CROP: crop to scale_factor * target
# RESIZE: resize (shrink) to target resolution
def create_wallpaper(
    input_path: Union[str, Path],
    output_path: Optional[Union[str, Path]],
    width: int,
    height: int,
    scaling: float,
) -> cv2.Mat:
    if input_path:
        input_path = str(input_path)
    if output_path:
        output_path = str(output_path)
    img = cv2.imread(input_path)
    source_resolution = np.array(img.shape)
    target_resolution = np.array((height, width, 3))
    resolution_scaler = np.array((scaling, scaling, 1))

    crop_size = (target_resolution * resolution_scaler).astype(int)
    tile_factor = np.ceil((crop_size / source_resolution)).astype(int)

    img = np.tile(img, tile_factor)
    img = img[: crop_size[0], : crop_size[1], :]  # crop
    img = cv2.resize(img, target_resolution[-2::-1])
    if output_path:  # TODO: refactor for single responsibility
        cv2.imwrite(output_path, img)
    return img


if __name__ == "__main__":
    wp = create_wallpaper(IMAGE, "./out/result.png", *RESOLUTION, SCALE_FACTOR)
    cv2.imshow("Output", wp)
    cv2.waitKey(0)
    cv2.destroyAllWindows
