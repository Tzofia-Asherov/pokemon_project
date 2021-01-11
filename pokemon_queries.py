import pandas as pd
from connect_db import cursor, con


def execute_query(query, params = ()):
    cursor.execute(query, params)
    return cursor.fetchall()


def get_pokemon_details_by_name(pokemon_name):
    cursor.execute("SELECT id, name , weight, height  \
                    FROM Pokemon \
                    WHERE name = %s", pokemon_name)
    details = cursor.fetchone()
    return details

def get_types_by_id(id_pokemon):
    cursor.execute("SELECT name_Type   \
                    FROM PokemonTypes \
                    WHERE id_pokemon = %s", id_pokemon)
    details = cursor.fetchall()
    return details

def get_pokemon_with_types(pokemon_name):
    pokemon_details= get_pokemon_details_by_name(pokemon_name)
    type_list = get_types_by_id([pokemon_details[0]])
    return pokemon_details, type_list

def get_pokemon_id_by_name(name):
    cursor.execute("SELECT Pokemon.id \
                            FROM Pokemon \
                            WHERE Pokemon.name = %s", name)
    record1 = cursor.fetchone()
    return record1[0]

def get_pokemons_id_by_type(type_name):
    cursor.execute("SELECT id_pokemon    \
                    FROM PokemonTypes \
                    WHERE name_Type = %s", type_name)
    details = cursor.fetchall()
    return details

def get_town_id_by_its_name(town_name):
    cursor.execute("SELECT id \
                    FROM Towns \
                    WHERE name = %s", town_name)
    town_id = cursor.fetchone()
    return town_id[0]



def get_trainer_id_by_name(trainer_name):
    cursor.execute("SELECT id \
                    FROM trainer \
                    WHERE name = %s", trainer_name)
    trainer_id = cursor.fetchone()
    return trainer_id[0]

def get_max_id_trainer():
    cursor.execute("""SELECT max(id) 
                    FROM trainer""")
    trainer_id = cursor.fetchone()
    return trainer_id[0]


def add_trainer(trainer_name, town_id):
    max_id_tainer = get_max_id_trainer()
    cursor.execute("INSERT INTO trainer (id, name, id_town) VALUES (%s, %s,%s)",(max_id_tainer+1, trainer_name, town_id))
    con.commit()


def delete_pokemon_trainer(trainer_name, pokemon_name):
    trainer_id = get_trainer_id_by_name(trainer_name)
    pokemon_id = get_pokemon_id_by_name(pokemon_name)
    cursor.execute("DELETE FROM owners WHERE id_pokemon =%s AND id_trainer = %s",(pokemon_id, trainer_id))
    con.commit()

def update_pokemon_trainer(trainer_name, pokemon_name, evolve_name):
    trainer_id = get_trainer_id_by_name(trainer_name)
    pokemon_id = get_pokemon_id_by_name(pokemon_name)
    evolve_id = get_pokemon_id_by_name(evolve_name)
    cursor.execute("UPDATE owners set id_pokemon =%s where id_trainer = %s and id_pokemon = %s",(evolve_id, trainer_id, pokemon_id ))
    con.commit()


def evolve_pokemon_species(pokemon_name, trainer_name, evolve_name):
    pokemon_id= get_pokemon_id_by_name(pokemon_name)
    trainer_id = get_trainer_id_by_name(trainer_name)

    evolve_to_id = get_pokemon_id_by_name(evolve_name)
    owner_list = get_owner(pokemon_name)
    if trainer_name in owner_list:
        evolve_owner_list = get_owner(evolve_name)
        if trainer_name in evolve_owner_list:
            delete_pokemon_trainer(trainer_name, pokemon_name)
        else:
            update_pokemon_trainer(trainer_name, pokemon_name, evolve_name)
        return 1
    return 0

def get_heaviest_pokemon():
    return execute_query("SELECT name, weight \
                    FROM pokemon \
                    WHERE weight =\
                    (SELECT max(weight) FROM pokemon) LIMIT 1")[0][0]


def find_by_type(type_name):
    tuple_pokemons = execute_query("SELECT Pokemon.name \
                            FROM Pokemon JOIN Types on pokemon.id_type = Types.id \
                            and Types.name = %s", type_name)
    return [pokemon[0] for pokemon in tuple_pokemons]


def get_owner(poke_name):
    cursor.execute('SELECT Trainer.name \
    from Pokemon join Owners on Pokemon.id = Owners.id_pokemon \
    join Trainer on Owners.id_trainer = Trainer.id \
        WHERE  Pokemon.name = %s', poke_name)
    records = cursor.fetchall()
    return [pokemon[0] for pokemon in records]


def find_roster(trainer_name):
    tuple_pokemons = execute_query("select Pokemon.name \
                                        from Pokemon join Owners on Pokemon.id = Owners.id_pokemon \
                                        join Trainer on Owners.id_trainer = Trainer.id\
                                        where Trainer.name = %s", (trainer_name))
    return [pokemon[0] for pokemon in tuple_pokemons]
    
def most_owned_pokemon():
    cursor.execute('select Types.name as type_name, Pokemon.name as pokemon_name, weight, height \
                    from Types,Pokemon, Owners \
                    where Pokemon.id = Owners.id_pokemon and Pokemon.id_type = Types.id \
                    group by Types.id, Owners.id_pokemon \
                    having  count(1) = \
                    (\
                    select  count(1) \
                    from  Owners \
                    group by  Owners.id_pokemon \
                    order by  count(Owners.id_pokemon) Desc \
                    limit 1)')
    df = pd.DataFrame(cursor.fetchall())
    df.columns = [x[0] for x in cursor.description]
    return df

if __name__ == "__main__":
    print("heavies pokemon:", get_heaviest_pokemon())
    print("grass pokemons:", find_by_type('grass'))
    print("gengar's trainers:", get_owner('gengar'))
    print("loga's pokemons:", find_roster('loga'))
    print("most owned pokemon: \n", most_owned_pokemon())

