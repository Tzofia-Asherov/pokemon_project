-- create database pokemonDB;

USE pokemonDB;

/* drop table Owners;
drop table Pokemon;
drop table Types;
drop table Trainer;
drop table Towns; */


CREATE TABLE Types
(
    id  INT NOT NULL  PRIMARY KEY,
    name VARCHAR(20) NOT NULL
);


CREATE TABLE Pokemon
(
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    height FLOAT(2), 
    weight FLOAT(2),
    id_type INT,
   
    FOREIGN KEY(id_type) REFERENCES Types(id)
);


CREATE TABLE Towns
(
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(20) NOT NULL
);


CREATE TABLE Trainer
(
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    id_town INT,

    FOREIGN KEY(id_town) REFERENCES Towns(id)
);


CREATE TABLE Owners
(
    id_pokemon INT NOT NULL,
    id_trainer INT NOT NULL,

    FOREIGN KEY(id_pokemon) REFERENCES Pokemon(id),
    FOREIGN KEY(id_trainer) REFERENCES Trainer(id),
    PRIMARY KEY (id_pokemon,id_trainer)
);


create table id_counters
(
    trainer_counter INT NOT NULL,
    town_counter INT NOT NULL,
    type_counter INT NOT NULL
);

insert into id_counters(trainer_counter, town_counter, type_counter) values (0,0,0);



