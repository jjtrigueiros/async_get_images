from pydantic import BaseModel
from pokepapers.lib.pokeapi import PokeAPI
from pokepapers.lib import settings


client = PokeAPI()


class Pokemon(BaseModel):
    national_id: int
    name: str


ALL_POKEMON = [
    Pokemon(national_id=index + 1, name=name)
    for (index, name) in enumerate(
        client.list_pokemon_species(settings.app.NUMBER_OF_POKEMON)
    )
]
