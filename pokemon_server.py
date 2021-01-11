from flask import Flask, Response, request
import pokemon_queries as queries
import external_api_queries as external
import json


app = Flask(__name__)



@app.route('/pokemons') 
def get_pokemons_details():

    trainer_name = request.args.get("trainer_name")
    if trainer_name:
        pokenon_list = queries.find_roster(trainer_name)
        return { ""+trainer_name+ " pokemons" :pokenon_list}
    
    pokemon_name =  request.args.get("pokemon_name")
    if pokemon_name:
        pokemon_details, pokemon_types = queries.get_pokemon_with_types(pokemon_name)
        return {"id" : pokemon_details[0],
                            "name": pokemon_details[1],
                             "weight" : pokemon_details[2],
                             "height" : pokemon_details[3],
                             "types": pokemon_types}

    type_name =  request.args.get("type_name")
    if type_name:
        pokemons_id_list = queries.get_pokemons_id_by_type(type_name)
        return {"pokemons by "+ type_name : pokemons_id_list}

    return {"error" : "no key trainer_name/pokemon_name/type_name"}, 400
    
    



@app.route('/trainers/<pokemon_name>') 
def get_trainers_of_pokemon(pokemon_name):
    trainers_list = queries.get_owner(pokemon_name)
    if trainers_list:
        return json.dumps({ ""+pokemon_name+ " trainers" :trainers_list})
    return json.dumps({ ""+pokemon_name+ " trainers" :"no trainers to pokemon"})
    



@app.route('/trainers', methods=['POST']) 
def add_new_trainer():
    response = request.get_json()
    trainer_name = response["trainer_name"]
    if trainer_name == None:
        return {"error" : "no key name trainer_name"}, 400 
    town_name = response["town_name"]
    if town_name== None:
        return {"error" : "no key name town_name"}, 400 
    town_id = queries.get_town_id_by_its_name(town_name)
    if town_id== None:
        return {"error" : "no "+ town_name + " in db"}, 400 
    queries.add_trainer(trainer_name, town_id)
    return {"added new trainer" : trainer_name}
              

@app.route('/pokemons', methods=['DELETE']) 
def delete_ownership():
    response = request.get_json()

    trainer_name = response["trainer_name"]
    if trainer_name == None:
        return {"error" : "no key name trainer_name"}, 400

    pokemon_name = response["pokemon_name"]
    if pokemon_name== None:
        return {"error" : "no key name pokemon_name"}, 400 

    queries.delete_pokemon_trainer(trainer_name, pokemon_name)
    return {"delete pokemon "+pokemon_name+ " in trainer" : trainer_name},204
 
 

@app.route('/pokemons', methods=['PUT']) 
def evolve():
    response = request.get_json()
    trainer_name = response["trainer_name"]
    if trainer_name == None:
        return {"error" : "no key name trainer_name"}, 400 

    pokemon_name = response["pokemon_name"]
    if pokemon_name == None:
        return {"error" : "no key name pokemon_name"}, 400 

    species_url = external.get_species_url(pokemon_name)
    evolution_chain_url = external.get_evolution_chain_url(species_url)
    chain_item = external.get_chain_item(evolution_chain_url)
    if chain_item["evolves_to"] != []:
        chain_item = chain_item["evolves_to"]
        evolve_name = chain_item[0]["species"]["name"]
    else:
        return {"warning" : "no where to evolve"}, 202


    # while(chain_item[0]["evolves_to"] != []):
    #     chain_item = chain_item[0]["evolves_to"]

    
    #if evolve_name == pokemon_name:
        
    res = queries.evolve_pokemon_species(pokemon_name, trainer_name, evolve_name)
    if res:
        return {"evolve pokemon "+pokemon_name : evolve_name }
    return {"error" : "no relation between the pokemon: " + pokemon_name + " and the trainer " + trainer_name}, 404
    
if __name__ == '__main__':
    app.run(port=3000)
