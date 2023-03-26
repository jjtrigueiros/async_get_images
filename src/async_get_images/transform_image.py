import cv2
import numpy as np


SCALE_FACTOR: float = 1.5
RESOLUTION: tuple[int, int] = (1080, 1920)
IMAGE = './out/227.jpg'

# source resolution -> TILE -> CROP -> RESIZE -> target resolution
# TILE: tile ceil(target/source) times
# CROP: crop to scale_factor * target
# RESIZE: resize (shrink) to target resolution

img = cv2.imread(IMAGE)
source_resolution = np.array(img.shape)
target_resolution = np.array((*RESOLUTION, 3))
resolution_scaler = np.array((SCALE_FACTOR, SCALE_FACTOR, 1))

crop_size = (target_resolution * resolution_scaler).astype(int)
tile_factor = np.ceil((crop_size / source_resolution)).astype(int)


img = np.tile(img, tile_factor)
img = img[:crop_size[0], :crop_size[1], :] # crop
img = cv2.resize(img, np.flip(target_resolution[:2]))
print(img.shape)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()