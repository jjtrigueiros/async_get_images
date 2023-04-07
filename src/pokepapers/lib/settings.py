"""Set configuration via environment variables."""

from pathlib import Path

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    class Config:
        case_sensitive = True

    PATTERNS_DIRECTORY: Path = Path("./out/patterns/")
    WALLPAPER_DIRECTORY: Path = Path("./out/wallpapers/")
    POKEAPI_URL: str = "https://pokeapi.co/api/v2/"
    IMAGES_SOURCE_URL: str = (
        "https://os-cdn.ec-ffmt.com/gl/pokemon/dedicate/pattern-flat/"
    )
    NUMBER_OF_POKEMON = 493
    # Gen 1 - #151 Mew
    # ...
    # Gen 4 - #493 Arceus
    # Gen 5 - #649 Genesect
    # ...
    # Gen 8 - #905 Enamorus
    # Gen 9 - #1010 Iron Leaves


app = AppSettings()
