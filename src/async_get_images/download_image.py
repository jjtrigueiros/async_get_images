#!usr/bin/env python3

import asyncio
import logging
import logging.handlers
import mimetypes
import queue
import shutil
from pathlib import Path
from urllib.parse import urlparse

import requests

log_queue = queue.Queue()
queue_handler = logging.handlers.QueueHandler(log_queue)
logger = logging.getLogger(__name__)
logger.addHandler(queue_handler)
logger.setLevel("INFO")

queue_listener = logging.handlers.QueueListener(log_queue, logging.StreamHandler())
queue_listener.start()


def download_image_sync(image_url: str, save_to_directory: Path) -> int:
    """
    Download and save an image to the provided directory using the image's default filename.
    """

    try:
        r = requests.get(image_url, stream=True)
    except requests.ConnectionError as conn_err:
        logger.error("connection error downloading %s: %s", image_url, conn_err)

    if r.status_code == 200:
        r.raw.decode_content = True # needed to properly calculate file size before saving

        # Get file extension from headers
        url_path = Path(urlparse(image_url).path)
        if mimetype := r.headers.get('content-type'):
            extension = mimetypes.guess_extension(mimetype)
            filename = url_path.with_suffix(extension).name
        else:
            filename = url_path.name

        dl_target = save_to_directory / filename

        with open(dl_target, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        logger.info(f'Successfully downloaded {dl_target}.')
        return 0
    else:
        logger.error(f'Image not found: {image_url} (status code {r.status_code})')
        return -1


async def download_image_async(image_url: str, save_to_directory: Path):
    return await asyncio.to_thread(download_image_sync, image_url, save_to_directory)


async def download_image_set_async(url_iterator: iter, save_to_directory: Path):
    return await asyncio.gather(*[download_image_async(url, save_to_directory) for url in url_iterator])


if __name__ == '__main__':
    # test downloading one image (URL is for a .jpg but return should be a .png)
    asyncio.run(download_image_async('https://os-cdn.ec-ffmt.com/gl/pokemon/dedicate/pattern-flat/444.jpg', Path('./out/')), debug=True)