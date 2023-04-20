from pathlib import Path

from PIL import Image
import numpy as np

from pokepapers.model import transform_image


RESOURCES = Path("./tests/unit/resources/")
BASE_IMAGE = RESOURCES / "272_ludicolo.png"  # 1160x1660p, scale 1.0
REF_IMAGE_1160X1160_2P0 = RESOURCES / "272_ludicolo_1160x1160_2p00.png"
REF_IMAGE_1920X1080_1P0 = RESOURCES / "272_ludicolo_1920x1080_1p00.png"
REF_IMAGE_1280X720P_2P5 = RESOURCES / "272_ludicolo_1280x720_2p50.png"


class TestOutput:
    """Compares the image transform output to a set of human-verified images."""

    def load_image(self, path: Path) -> Image:
        try:
            img = Image.open(path)
        except Exception as e:
            assert img, f"Failed to load image: {path}. Exception: {e}"
        return img

    def ref_compare(
        self, imgsrc_path: Path, imgref_path: Path, params: tuple[int, int, float]
    ) -> bool:
        imgsrc = self.load_image(imgsrc_path)
        imgref = self.load_image(imgref_path)
        transform = transform_image.transform_image(imgsrc, *params)
        equal = np.array_equal(imgref, transform)
        assert equal, "Image does not match reference"

    def test_scaling(self):
        params = (1160, 1160, 2.0)
        self.ref_compare(BASE_IMAGE, REF_IMAGE_1160X1160_2P0, params)

    def test_tiling(self):
        params = (1920, 1080, 1.0)
        self.ref_compare(BASE_IMAGE, REF_IMAGE_1920X1080_1P0, params)

    def test_all(self):
        params = (1280, 720, 2.5)
        self.ref_compare(BASE_IMAGE, REF_IMAGE_1280X720P_2P5, params)
