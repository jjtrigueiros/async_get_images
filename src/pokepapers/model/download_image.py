#!usr/bin/env python3

import asyncio
import logging
import logging.handlers
import mimetypes
import queue
import shutil
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests
from pokepapers.lib import settings
from pokepapers.model.pokemon import Pokemon, ALL_POKEMON

log_queue: queue.Queue = queue.Queue()
queue_handler = logging.handlers.QueueHandler(log_queue)
logger = logging.getLogger(__name__)
logger.addHandler(queue_handler)
logger.setLevel("INFO")

queue_listener = logging.handlers.QueueListener(log_queue, logging.StreamHandler())
queue_listener.start()


def prompt_create_directory(directory: Path) -> None:
    if not directory.is_dir():
        if input(f'Create directory on "{directory}" ? (y/N)') in {"y", "Y"}:
            directory.mkdir(parents=True, exist_ok=True)
        else:
            raise Exception(f"Failed to create {directory}")


def download_image(
    image_url: str, save_to_directory: Path, preferred_stem: str = ""
) -> bool:
    """
    Download and save an image to the provided directory using the image's default
    filename.
    """

    try:
        r = requests.get(image_url, stream=True)
    except requests.ConnectionError as conn_err:
        logger.error("connection error downloading %s: %s", image_url, conn_err)
        return False

    if r.status_code == 200:
        # needed to properly calculate file size before saving
        r.raw.decode_content = True

        # Get file extension from headers
        url_path = Path(urlparse(image_url).path)
        if (mimetype := r.headers.get("content-type")) and (
            extension := mimetypes.guess_extension(mimetype)
        ):
            filename = url_path.with_suffix(extension).name
        else:
            filename = url_path.name

        dl_target = save_to_directory / filename
        if preferred_stem:
            dl_target = dl_target.with_stem(preferred_stem)

        with open(dl_target, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        logger.info(f"Successfully downloaded {dl_target}.")
        return True
    else:
        logger.error(f"Image not found: {image_url} (status code {r.status_code})")
        return False


async def download_image_async(
    image_url: str, dest_path: Path, preferred_stem: str = ""
):
    return await asyncio.to_thread(download_image, image_url, dest_path, preferred_stem)


async def download_image_set_async(
    urls: list[str], download_folder, preferred_stems: Optional[list[str]] = None
):
    if not preferred_stems:
        tasks = [download_image_async(url, download_folder) for url in urls]
    else:
        tasks = [
            download_image_async(url, download_folder, preferred_stem)
            for (url, preferred_stem) in zip(urls, preferred_stems)
        ]
    return await asyncio.gather(*tasks)


def download_from_original_stitch(
    pkmn_list: Optional[list[Pokemon]] = None, to_directory: Optional[Path] = None
):
    """
    Downloads a list of images from Original Stitch.
    If no list is provided, downloads all images.
    """
    original_stitch_url = "https://os-cdn.ec-ffmt.com/gl/pokemon/dedicate/pattern-flat/"
    if not pkmn_list:
        pkmn_list = ALL_POKEMON
    if not to_directory:
        to_directory = settings.app.PATTERNS_DIRECTORY / "original_stitch"

    # filename and url generation strategies
    filenames = [f"{pkmn.national_id}_{pkmn.name}" for pkmn in pkmn_list]
    url_list = [f"{original_stitch_url}{pkmn.national_id}.jpg" for pkmn in pkmn_list]

    prompt_create_directory(to_directory)
    asyncio.run(download_image_set_async(url_list, to_directory, filenames))
