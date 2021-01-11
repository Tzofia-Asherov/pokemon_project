import requests
api = "https://pokeapi.co/api/v2/"

def get_species_url(pokemon_name):
    res = requests.get(api+'pokemon/'+pokemon_name)
    species_url = res.json()["species"]["url"]
    return species_url

def get_evolution_chain_url(species_url):
    res = requests.get(species_url)
    evolution_chain_url = res.json()["evolution_chain"]["url"]
    return evolution_chain_url

def get_chain_item(evolution_chain_url):
    res = requests.get(evolution_chain_url)
    chain_item = res.json()["chain"]
    return chain_item