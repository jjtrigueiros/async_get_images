import os
from time import perf_counter
from src import download_images_concurrently, download_images_sequentially


NUMBER_OF_POKEMON = 493
# Gen 1 - #151 Mew
# ...
# Gen 4 - #493 Arceus
# Gen 5 - #649 Genesect
# ...
# Gen 8 - #890 Eternatus
#         #905 Enamorus
# Gen 9 - #??? Miraidon

# STORE_PAGE_URL = 'https://originalstitch.com/pokemon/order/'
SHIRT_PATTERN_URL = 'https://os-cdn.ec-ffmt.com/gl/pokemon/dedicate/pattern-flat/{pokemon_number:.0f}.jpg'
TARGET_FOLDER = os.path.abspath('./out/')
N_THREADS = 32


def main():

    # generate list of URLs
    base_url = SHIRT_PATTERN_URL
    urls = [
        base_url.format(pokemon_number=i+1)
        for i in range(NUMBER_OF_POKEMON)
    ]

    # check if target folder exists, and if not, prompt to create it
    base_dl_folder = os.path.abspath(TARGET_FOLDER)
    if not os.path.isdir(base_dl_folder):
        if input(f'Folder not found. Create new directory on "{base_dl_folder}" ? (y/N)') in {'y', 'Y'}:
            os.mkdir(base_dl_folder)
        else:
            raise Exception('No valid target destination')

    dl_folder = os.path.abspath(base_dl_folder)

    #    # Sequential download approach
    #    start_time = perf_counter()
    #    status_sequential = download_images_sequentially(urls, dl_folder)
    #    sequential_download_results = list(status_sequential)
    #    print(f'Finished in {round(perf_counter() - start_time, 2)} seconds!')

    # Concurrent download approach
    start_time = perf_counter()
    status_concurrent = download_images_concurrently(urls, dl_folder)
    concurrent_download_results = list(status_concurrent)
    print(f'Finished in {round(perf_counter() - start_time, 2)} seconds!')

#    assert sequential_download_results == concurrent_download_results, 'download results do not match!'


if __name__ == '__main__':
    main()
