#!usr/bin/env python3

import concurrent.futures
import logging
import requests
import shutil

from functools import partial
from mimetypes import guess_extension
from pathlib import Path
from urllib.parse import urlparse

def download_image(url: str, dl_folder: Path):
    """
    Download and save an image to the provided directory using the image's default filename.
    """

    try:
        r = requests.get(url, stream=True)
    except requests.ConnectionError as conn_err:
        logging.error("connection error downloading %s", conn_err)
    if r.status_code == 200:
        r.raw.decode_content = True # needed to properly calculate file size before saving

        # Get file extension from headers
        url_path = Path(urlparse(url).path)
        if mimetype := r.headers.get('content-type'):
            filename = url_path.with_suffix(guess_extension(mimetype)).name
        else:
            filename = url_path.name

        dl_target = dl_folder / filename

        with open(dl_target, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        logging.info(f'{url} successfully downloaded to {dl_target}.')
        return 0
    else:
        logging.error(f'{url} not found : status code {r.status_code}')
        return -1


def download_images_concurrently(url_iterator: iter, dl_folder: Path, max_workers=32):
    """
    A simple script to concurrently download a list of images to the specified folder.
    The original filename is kept.

    :param url_iterator: An iterable sequence of URLs
    :param dl_folder: The target folder for the image downloads
    :param max_workers: The maximum number of threads used for this operation
    :return:
    """

    download_image_to_output_dir = partial(download_image, dl_folder=dl_folder)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(download_image_to_output_dir, url_iterator)
    return results


if __name__ == '__main__':
    download_image('https://os-cdn.ec-ffmt.com/gl/pokemon/dedicate/pattern-flat/444.jpg', Path('./out/'))