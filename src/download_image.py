import requests
import shutil
import logging


def download_image(url, dl_target):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        # Open a local file with wb ( write binary ) permission.
        with open(dl_target, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        logging.info(f'{url} successfully downloaded to {dl_target}.')
        # print("ok")
        return 0
    else:
        logging.info(f'{url} not found : status code {r.status_code}')
        return -1
