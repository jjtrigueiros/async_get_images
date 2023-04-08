<p align="left">
<a href="https://github.com/jjtrigueiros/async_get_images/actions"><img alt="Actions status" src="https://github.com/jjtrigueiros/async_get_images/actions/workflows/python-app.yml/badge.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# PokéPapers
Download a list of tileable Pokémon-themed patterns and make wallpapers.

## Motivation: 
This program was built as:
- a way to bulk download the latest [Original Stitch Pokémon patterns](https://originalstitch.com/pokemon). These are tileable and make for some nice wallpapers or lock screen images.
- a simple test project for async/coroutines and trying out CLI app development with Typer.

Some considerations were taken regarding mimetypes, as the default image URLs don't match the actual content type received (ex. 444.jpg returns a .png).


## Usage:
Install the module with Poetry and run it:
```shell
$ ppp --help
```

The main workflow is calling `ppp download` to pull all tileable images to the output folder and then generating an appropriate wallpaper with `ppp generate`.

Pull all tileable images to a local folder:
```shell
$ ppp download
```

Generate a 1080p desktop wallpaper of your favorite image:
```shell
$ ppp generate lotad
```

Generate a wallpaper with a custom resolution or scale factor:
```shell
# ex.: 1440x3120p, vertical aspect ratio, scale factor 1.5
$ ppp generate lotad 1440 3120 1.5
```