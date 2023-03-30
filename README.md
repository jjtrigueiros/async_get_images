<p align="left">
<a href="https://github.com/jjtrigueiros/async_get_images/actions"><img alt="Actions status" src="https://github.com/jjtrigueiros/async_get_images/actions/workflows/python-app.yml/badge.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# PokéPapers
Download a list of tileable Pokémon-themed patterns and make wallpapers.

## Motivation: 
This program was built as:
- a way to bulk download the latest [Original Stitch Pokémon patterns](https://originalstitch.com/pokemon). These are tileable and make for some nice wallpapers or lock screen images.
- a simple test project for async/coroutines and trying out CLI app developmnt with Typer.

Some considerations were taken regarding mimetypes, as the default image URLs don't match the actual content type received (ex. 444.jpg returns a .png).

Run the module help (`python -m pokepapers --help`) to get started.
Documentation will be expanded when core features are stabilized!
