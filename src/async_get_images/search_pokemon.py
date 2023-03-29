import requests

from lib import settings


class PokeAPI():
    def __init__(self):
        self.url = settings.app.POKEAPI_URL

    def get_id(self, name: str) -> int:
        return requests.get(f"{self.url}/pokemon/{name}").json().get('id')
    
    def get_name(self, id: int) -> str:
        return requests.get(f"{self.url}/pokemon/{id}").json().get('name')
    
    def list_pokemon(self) -> list[str]:
        """
        Returns an ordered (by national pokédex number) list of pokémon names.
        If this list is kept in memory, we can query a certain nat. dex ID with list[id-1].
        """
        api_data = requests.get(f"{self.url}/pokemon/?limit={settings.app.NUMBER_OF_POKEMON}").json()
        return {pkmn['name'] for pkmn in api_data['results']}


if __name__ == '__main__':
    pokemon = 'finneon'

    pa = PokeAPI()
    if pokemon in pa.list_pokemon():
        print(pa.get_id(pokemon))
    print('bye')