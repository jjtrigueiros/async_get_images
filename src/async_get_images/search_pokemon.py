import requests

from lib.constants import NUMBER_OF_POKEMON

class PokeAPI():
    def __init__(self):
        self.url = 'https://pokeapi.co/api/v2/'

    def get_id(self, name: str) -> int:
        return requests.get(f"{self.url}/pokemon/{name}").json().get('id')
    
    def get_name(self, id: int) -> str:
        return requests.get(f"{self.url}/pokemon/{id}").json().get('name')
    
    def list_pokemon(self) -> set[str]:
        api_data = requests.get(f"{self.url}/pokemon/?limit={NUMBER_OF_POKEMON}").json()
        return {pkmn['name'] for pkmn in api_data['results']}


if __name__ == '__main__':
    pokemon = 'finneon'

    pa = PokeAPI()
    if pokemon in pa.list_pokemon():
        print(pa.get_id(pokemon))
    print('bye')