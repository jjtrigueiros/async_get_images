from typing import Union

import requests
from pydantic import BaseModel

from . import settings


class PokemonSpecies:
    def __init__(self, json):
        self.json: dict = json
        self.id = self.json.get("order")
        self.name = self.json.get("name")

    def get_proper_name(self, language: str = "en") -> str:

        names: list[dict] = self.json.get("names")
        try:
            return next(
                element["name"] for element in names 
                if element.get("language").get("name") == language
            )
        except StopIteration:
            # fallback to english name
            return next(
                element["name"] for element in names 
                if element.get("language").get("name") == "en"
            )


class Language(BaseModel):
    """
    supported languages:
        ja-Hrkt
        roomaji
        ko
        zh-Hant
        fr
        de
        es
        it
        en
        ja
        pt-BR
    """
    id: int
    iso3166: str
    iso639: str
    name: str
    names: list[dict]

    def name_in(self, language) -> str:
        """
        Return this language's name in a given language.

        Examples: 
            - Language(es).name_in(Language(es)) -> Español
            - Language(es).name_in(Language(en)) -> Spanish
        """
        raise NotImplementedError()


class PokeAPI:
    def __init__(self):
        self.api_url = settings.app.POKEAPI_URL

    def get_pokemon_species(self, id_or_name: Union[int, str]) -> PokemonSpecies:
        json = requests.get(f"{self.api_url}/pokemon-species/{id_or_name}").json()
        return PokemonSpecies(json)

    def list_pokemon_species(self, limit: int = 0) -> list[str]:
        """
        Returns an ordered (by national pokédex number) list of Pokémon names.
        """
        if not limit:
            limit = settings.app.NUMBER_OF_POKEMON
        url = f"{self.api_url}/pokemon-species/?limit={limit}"
        api_data = requests.get(url).json()
        return [pkmn["name"] for pkmn in api_data["results"]]
