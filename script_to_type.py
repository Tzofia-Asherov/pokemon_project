import requests
import json
import pokemon_queries as queries
from connect_db import cursor, con

api = "https://pokeapi.co/api/v2/"
def update_types(name):
    res = requests.get(api+'pokemon/'+name)
    poke_data = res.json()
    types = poke_data["types"]
    poke_id =  queries.get_id_by_name(name)
    for t in types:
        queries.execute_query("INSERT INTO PokemonTypes (id_pokemon, name_Type) VALUES (%s, %s)",(poke_id, t["type"]["name"]))
    con.commit()
    
def pokes_names():
    cursor.execute("SELECT name FROM pokemon")
    response = cursor.fetchall()
    for l in response:
        update_types(l[0])

pokes_names()