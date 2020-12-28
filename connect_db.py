import pymysql, os, json

con = pymysql.connect(host = 'localhost',
                      user = 'root',
                      passwd =  '',
                      db = 'pokemondb')

cursor = con.cursor()