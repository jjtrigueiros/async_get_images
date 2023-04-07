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

log_queue: queue.Queue = queue.Queue()
queue_handler = logging.handlers.QueueHandler(log_queue)
logger = logging.getLogger(__name__)
logger.addHandler(queue_handler)
logger.setLevel("INFO")

queue_listener = logging.handlers.QueueListener(log_queue, logging.StreamHandler())
queue_listener.start()


def download_image_sync(
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
    return await asyncio.to_thread(
        download_image_sync, image_url, dest_path, preferred_stem
    )


async def download_image_set_async(
    urls: list[str], download_folder, preferred_stems: Optional[list[str]] = None
):
    if not preferred_stems:
        tasks = [
            download_image_async(url, download_folder)
            for url in urls
        ]
    else:
        tasks = [
            download_image_async(url, download_folder, preferred_stem)
            for (url, preferred_stem) in zip(urls, preferred_stems)
        ]
    return await asyncio.gather(*tasks)
