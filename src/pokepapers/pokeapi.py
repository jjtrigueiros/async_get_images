import requests

from .lib import settings


class PokeAPI:
    def __init__(self):
        self.api_url = settings.app.POKEAPI_URL

    def get_id(self, name: str) -> int:
        return (
            requests.get(f"{self.api_url}/pokemon-species/{name}").json().get("order")
        )

    def get_name(self, id: int) -> str:
        return requests.get(f"{self.api_url}/pokemon-species/{id}").json().get("name")

    def list_pokemon(self, limit: int = 0) -> list[str]:
        """
        Returns an ordered (by national pokédex number) list of pokémon names.
        If this list is kept in memory, we can query a certain nat. dex ID
        with list[id-1].
        """
        if not limit:
            limit = settings.app.NUMBER_OF_POKEMON
        url = f"{self.api_url}/pokemon-species/?limit={limit}"
        api_data = requests.get(url).json()
        return [pkmn["name"] for pkmn in api_data["results"]]
