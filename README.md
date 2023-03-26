# async_get_images
A simple asynchronous image fetcher. Download a set of images from a set of URLs using coroutines.

## Motivation: 
This program was built as:
- a way to bulk download the latest [Original Stitch Pokémon patterns](https://originalstitch.com/pokemon). These are tileable and make for some nice wallpapers or lock screen images.
- a simple test project for async (and threads, in an earlier version).

Some considerations were taken regarding mimetypes, as the default image URLs don't match the actual content type received (ex. 444.jpg returns a .png).

Run the main script (`./src/main`) to download all images (default download location: `./out/`).
