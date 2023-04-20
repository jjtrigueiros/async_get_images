from pydantic import BaseModel


class Resolution(BaseModel):
    identifiers: list[str]
    width: int
    height: int


def autocomplete_resolution_name(incomplete: str):
    "Method to autocomplete a resolution name"
    accepted_names: list[str] = [
        name for resolution in PRESET_RESOLUTIONS for name in resolution.identifiers
    ]
    for name in accepted_names:
        if name.startswith(incomplete):
            yield name


def get_resolution_by_name(name: str) -> Resolution:
    "Retrieve a Resolution preset object"
    for resolution in PRESET_RESOLUTIONS:
        if name in resolution.identifiers:
            return resolution


PRESET_RESOLUTIONS: list[Resolution] = [
    Resolution(
        identifiers=["full-hd", "fhd", "1080p", "1920x1080p"],
        width=1920,
        height=1080,
    ),
    Resolution(
        identifiers=["quad-hd", "qhd", "1440p", "2560x1440p"],
        width=2560,
        height=1440,
    ),
    Resolution(
        identifiers=["ultra-hd-4k", "uhd-4k", "4k", "3840x2160p"],
        width=3840,
        height=2160,
    ),
    Resolution(
        identifiers=["ultra-hd-8k", "uhd-8k", "8k", "7680x4320p"],
        width=7680,
        height=4320,
    ),
    Resolution(
        identifiers=["pixel-7-pro", "phone-pixel-7-pro"],
        width=1440,
        height=3120,
    ),
    Resolution(
        identifiers=["iphone-14-pro", "phone-iphone-14-pro"],
        width=1179,
        height=2556,
    ),
    Resolution(
        identifiers=["samsung-galaxy-s23", "phone-samsung-galaxy-s23"],
        width=1080,
        height=2340,
    ),
]
