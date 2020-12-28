import json
from connect_db import cursor, con


dic_type = dict()
counter_type = 0

dic_town = dict()
counter_town = 0

counter_trainer = 0


def load_file(file):
    json_data=open(file).read()
    json_obj = json.loads(json_data)
    return json_obj


def load_counters():
    cursor.execute("SELECT * FROM id_counters")
    row = cursor.fetchone()
    return row


def save_counters():
    cursor.execute("UPDATE id_counters \
    SET trainer_counter=%s, town_counter=%s, type_counter=%s",
    (counter_trainer, counter_town, counter_type) )


def insert_type_and_get_id(type_name):
    if dic_type.get(type_name, None) == None:
        global counter_type
        counter_type  += 1 
        dic_type[type_name] = counter_type
        cursor.execute("INSERT INTO Types (id, name) VALUES (%s, %s)", (counter_type, type_name))
    return  dic_type[type_name] 


def insert_pokemon(poke_id, poke_name, weight, height, type_id):
    cursor.execute("INSERT INTO Pokemon (id, name, height, weight, id_type) VALUES (%s, %s, %s, %s, %s)", (poke_id, poke_name,height, weight, type_id))


def insert_town(town_name):
    if dic_town.get(town_name, None) == None:
        global counter_town
        counter_town  += 1 
        dic_town[town_name] = counter_town
        cursor.execute("INSERT INTO Towns (id, name) VALUES (%s, %s)", (counter_town, town_name))
    return dic_town[town_name] 


def insert_trainer(owner_name, town_id):
    cursor.execute("SELECT  id \
        FROM Trainer \
        WHERE Name = %s and id_town = %s", (owner_name,town_id))
  
    row_count = cursor.rowcount
    if row_count == 0:
        global counter_trainer
        counter_trainer += 1
        cursor.execute("INSERT INTO Trainer (id, name, id_town) VALUES (%s, %s, %s)",
         (counter_trainer, owner_name, town_id))
        return counter_trainer
    trainer = cursor.fetchone()  
    return trainer[0]
    

def insert_trainers(owner_list):
    id_trainer_list = []
    for owner in owner_list:
        owner_name = owner.get("name")
        town_name = owner.get("town")
        town_id = insert_town(town_name)
        trainer_id = insert_trainer(owner_name, town_id)
        id_trainer_list.append(trainer_id)
    return id_trainer_list


def insert_owners(poke_id, id_trainer_list):
    for trainer_id in id_trainer_list:
        cursor.execute("INSERT INTO owners (id_pokemon, id_trainer) VALUES (%s, %s)",
         (poke_id, trainer_id))


def insert_to_db(json_obj):
    for item in json_obj:
        poke_id = item.get("id")
        poke_name = item.get("name")
        type_name = item.get("type")
        weight = item.get("weight")
        height = item.get("height")
        owned_by_list = item.get("ownedBy", None)

        type_id = insert_type_and_get_id(type_name)
        insert_pokemon(poke_id, poke_name, weight, height, type_id)
        id_trainer_list = insert_trainers(owned_by_list)
        insert_owners(poke_id, id_trainer_list)
    con.commit()


def main():
    global counter_trainer
    global counter_town
    global counter_type
    counter_trainer, counter_town, counter_type = load_counters()
    json_obj = load_file("pokemon/poke_data.json")
    insert_to_db(json_obj)
    save_counters()
    con.close()


main()
