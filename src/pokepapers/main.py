#!usr/bin/env python3

import asyncio

from pathlib import Path
from time import perf_counter

import cv2
import typer

from .download_image import download_image_set_async
from .lib import settings
from .pokeapi import PokeAPI
from .transform_image import transform_image

app = typer.Typer()
client = PokeAPI()

# STORE_PAGE_URL = 'https://originalstitch.com/pokemon/order/'
LIST_OF_POKEMON: list[str] = client.list_pokemon()
DOWNLOAD_FROM_URLS: list[str] = [
    f"{settings.app.IMAGES_SOURCE_URL}{pokemon_id}.jpg"
    for pokemon_id in range(1, settings.app.NUMBER_OF_POKEMON + 1)
]


@app.command()
def download():
    """Downloads all Pokémon patterns into the configured output folder."""
    urls = DOWNLOAD_FROM_URLS
    filenames = [f"{i+1}_{LIST_OF_POKEMON[i]}" for i in range(len(LIST_OF_POKEMON))]

    # create output directory (prompt)
    dl_folder = Path(settings.app.PATTERNS_DIRECTORY)
    if not dl_folder.is_dir():
        if input(f'Create directory on "{dl_folder}" ? (y/N)') in {"y", "Y"}:
            dl_folder.mkdir(parents=True, exist_ok=True)
        else:
            raise Exception("Could not create download directory.")

    start_time = perf_counter()
    asyncio.run(download_image_set_async(urls, dl_folder, filenames))
    print(f"Finished in {round(perf_counter() - start_time, 2)} seconds!")


def complete_name(incomplete: str):
    for name in LIST_OF_POKEMON:
        if name.startswith(incomplete):
            yield name


@app.command()
def search(
    pkmn: str = typer.Argument(
        "",
        autocompletion=complete_name,
    )
):
    """Returns the pokémon National ID for a given pokémon name."""

    client = PokeAPI()
    id: int = client.get_id(pkmn)
    print(id)


@app.command()
def generate(
    pkid: int = typer.Argument(""),
    width: int = typer.Argument(1920),
    height: int = typer.Argument(1080),
    scaling: float = typer.Argument(1.0),
):
    """
    Generates a wallpaper featuring the Pokémon with chosen ID,
    with the set width, height and scaling factor (default 1920x1080 at x1.0 scale).
    """
    input_file = settings.app.PATTERNS_DIRECTORY / str(pkid)
    if input_file.with_suffix(".png").is_file():
        input_file = input_file.with_suffix(".png")
    elif input_file.with_suffix(".jpg").is_file():
        input_file = input_file.with_suffix(".jpg")
    else:
        raise Exception("Image not found")

    # generate output filename
    i, r = divmod(scaling, 1)
    i = int(i)
    r = round(100 * r)
    output_file = (
        settings.app.WALLPAPER_DIRECTORY
        / input_file.with_stem(f"{input_file.stem}_{width}x{height}_{i}p{r}").name
    )

    input_image = cv2.imread(str(input_file))
    output_image = transform_image(input_image, width, height, scaling)
    print(output_file)
    output_file.parent.mkdir(exist_ok=True)
    cv2.imwrite(str(output_file), output_image)
    print(output_file.is_file())
