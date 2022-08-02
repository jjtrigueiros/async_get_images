import os
import concurrent.futures
from .download_image import download_image


def download_images_sequentially(url_iterator: iter, dl_folder: str):
    """
    A simple script to sequentially download a list of images to the specified folder.
    The original filename is kept.

    :param url_iterator: An iterable sequence of URLs
    :param dl_folder: The target folder for the image downloads
    :return:
    """
    for url in url_iterator:
        filename = url.split("/")[-1]
        dl_target = os.path.join(dl_folder, filename)
        yield download_image(url, dl_target)


def download_images_concurrently(url_iterator: iter, dl_folder: str, max_workers=32):
    """
    A simple script to concurrently download a list of images to the specified folder.
    The original filename is kept.

    :param url_iterator: An iterable sequence of URLs
    :param dl_folder: The target folder for the image downloads
    :param max_workers: The maximum number of threads used for this operation
    :return:
    """

    file_iterator = [
        os.path.join(dl_folder, url.split("/")[-1])
        for url in url_iterator
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(download_image, url_iterator, file_iterator)
    return results
