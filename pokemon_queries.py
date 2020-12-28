import pandas as pd
from connect_db import cursor


def execute_query(query, params = ()):
    cursor.execute(query, params)
    return cursor.fetchall()


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

