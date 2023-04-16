# PokéPapers

[![Github Actions](https://github.com/jjtrigueiros/pokepapers/actions/workflows/python-app.yml/badge.svg)](https://github.com/jjtrigueiros/pokepapers/actions)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
$ ppp generate lotad -w 1440 -h 3120 -s 1.5
# Some resolution presets are supported, ex.: 4k desktop wallpaper
$ ppp generate scizor --resolution 4k
```
Please see `ppp generate --help` for more information.
