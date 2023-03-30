from pathlib import Path

import cv2
import numpy as np

from async_get_images import transform_image


RESOURCES = Path("./tests/unit/resources/")
BASE_IMAGE = RESOURCES / "272_ludicolo.png"  # 1160x1660p, scale 1.0
REF_IMAGE_1160X1160_2P0 = RESOURCES / "272_ludicolo_1160x1160_x2p0.png"
REF_IMAGE_1920X1080_1P0 = RESOURCES / "272_ludicolo_1920x1080_x1p0.png"
REF_IMAGE_1280X720P_2P5 = RESOURCES / "272_ludicolo_1280x720_x2p5.png"


class TestOutput():
    """Compares the image transform output to a set of human-verified images."""

    def load_image(self, path: Path) -> cv2.Mat:
        img = cv2.imread(str(path))
        assert img.any(), f"Failed to load image: {path}"
        return img

    def ref_compare(self, imgsrc_path: Path, imgref_path: Path, params: tuple[int, int, float]):
        imgsrc = self.load_image(imgsrc_path)
        imgref = self.load_image(imgref_path)
        transform = transform_image.create_wallpaper(imgsrc_path, None, *params)
        equal = np.array_equal(imgref, transform)
        assert equal, "Image does not match reference"

    def test_setup(self):
        assert BASE_IMAGE.is_file(), "The base image does not exist!"
        assert REF_IMAGE_1160X1160_2P0.is_file(), "Reference image 1 does not exist!"
        assert REF_IMAGE_1920X1080_1P0.is_file(), "Reference image 2 does not exist!"
        assert REF_IMAGE_1280X720P_2P5.is_file(), "Reference image 3 does not exist!"

    def test_scaling(self):
        params = (1160, 1160, 2.0)
        self.ref_compare(BASE_IMAGE, REF_IMAGE_1160X1160_2P0, params)

    def test_tiling(self):
        params = (1920, 1080, 1.0)
        self.ref_compare(BASE_IMAGE, REF_IMAGE_1920X1080_1P0, params)

    def test_all(self):
        params = (1280, 720, 2.5)
        self.ref_compare(BASE_IMAGE, REF_IMAGE_1280X720P_2P5, params)
