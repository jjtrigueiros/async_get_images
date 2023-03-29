#!usr/bin/env python3

import asyncio

from pathlib import Path
from time import perf_counter

import typer

from download_image import download_image_set_async
from lib import settings

app = typer.Typer()


# STORE_PAGE_URL = 'https://originalstitch.com/pokemon/order/'
DOWNLOAD_FROM_URLS = {
    f'{settings.app.IMAGES_SOURCE_URL}{pokemon_id}.jpg'
    for pokemon_id in range(1, settings.app.NUMBER_OF_POKEMON+1)
}
TARGET_FOLDER = Path('./out/')

@app.command()
def download():

    urls = DOWNLOAD_FROM_URLS

    # create output directory (prompt)
    dl_folder = Path(TARGET_FOLDER)
    if not dl_folder.is_dir():
        if input(f'Create directory on "{dl_folder}" ? (y/N)') in {'y', 'Y'}:
            dl_folder.mkdir(parents=True, exist_ok=True)
        else:
            raise Exception('Could not create download directory.')

    start_time = perf_counter()
    asyncio.run(download_image_set_async(urls, dl_folder))
    print(f'Finished in {round(perf_counter() - start_time, 2)} seconds!')



if __name__ == '__main__':
    app()
