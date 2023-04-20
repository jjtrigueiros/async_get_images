#!usr/bin/env python3

from time import perf_counter

from PIL import Image
import typer

from .lib import settings
from .lib.pokeapi import PokeAPI
from .model.download_image import download_from_original_stitch
from .model.pokemon import ALL_POKEMON
from .model.transform_image import transform_image
from .resolutions import autocomplete_resolution_name, get_resolution_by_name


app = typer.Typer()
client = PokeAPI()

# STORE_PAGE_URL = 'https://originalstitch.com/pokemon/order/'


@app.command()
def download():
    """
    Downloads all Pokémon patterns into the configured output folder.
    Default: download from Original Stitch.
    Planned: download from Serebii or Bulbapedia.
    Planned (future): download from self-hosted API/DB.
    """
    start_time = perf_counter()
    download_from_original_stitch()
    print(f"Finished in {round(perf_counter() - start_time, 2)} seconds!")


def autocomplete_pkmn_name(incomplete: str):
    for pkmn in ALL_POKEMON:
        if pkmn.name.startswith(incomplete):
            yield pkmn.name


@app.command()
def search(
    id_or_name: str = typer.Argument(
        default=None,
        autocompletion=autocomplete_pkmn_name,
    ),
    language: str = typer.Option(default="en"),
):
    """Returns the pokémon National ID for a given pokémon name."""

    client = PokeAPI()
    species = client.get_pokemon_species(id_or_name)
    print(f"#{species.id} - {species.get_proper_name(language)}")


@app.command()
def generate(
    pokemon: str = typer.Argument(None, autocompletion=autocomplete_pkmn_name),
    width: int = typer.Option(1920, "--width", "-w"),
    height: int = typer.Option(1080, "--height", "-h"),
    resolution_name: str = typer.Option(
        None, "--resolution", "-r", autocompletion=autocomplete_resolution_name
    ),
    scaling: float = typer.Option(1.0, "--scaling", "-s"),
):
    """
    Generates a wallpaper featuring the Pokémon with chosen ID,
    with the set width, height and scaling factor (default 1920x1080 at x1.0 scale).
    """
    if resolution_name:  # override width and height
        resolution = get_resolution_by_name(resolution_name)
        width = resolution.width
        height = resolution.height

    img_local_matches = settings.app.PATTERNS_DIRECTORY.glob(f"**/*_{pokemon}*.*")
    if not (input_file := next(img_local_matches, None)):
        print("Image not found locally.")
        return

    # generate output filename
    i, r = divmod(scaling, 1)
    i = int(i)
    r = round(100 * r)
    output_file = (
        settings.app.WALLPAPER_DIRECTORY
        / input_file.with_stem(f"{input_file.stem}_{width}x{height}_{i}p{r}").name
    )

    input_image = Image.open(input_file)
    output_image = transform_image(input_image, width, height, scaling)
    print(output_file)
    output_file.parent.mkdir(exist_ok=True)
    output_image.save(output_file)
