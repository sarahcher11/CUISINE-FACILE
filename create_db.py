import sqlite3
import json
from werkzeug.security import generate_password_hash


JSONFILENAME = 'recipes.json'
DBFILENAME = 'recipes.sqlite'

def db_run(query, args=(),db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur= conn.execute(query,args)
    conn.execute

def load(fname=JSONFILENAME, db_name=DBFILENAME):
  # possible improvement: do whole thing as a single transaction
  db_run('DROP TABLE IF EXISTS recipe')
  db_run('DROP TABLE IF EXISTS ingredient')
  db_run('DROP TABLE IF EXISTS stage')
  db_run('DROP TABLE IF EXISTS user')

  db_run('CREATE TABLE recipe (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, img TEXT, description TEXT, duration TEXT)')
  db_run('CREATE TABLE ingredient (recipe INT, rank INT, name TEXT)')
  db_run('CREATE TABLE stage (recipe INT, rank INT, description TEXT)')
  db_run('CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password_hash  TEXT)')

  insert1 = 'INSERT INTO recipe VALUES (:id, :title, :img, :description, :duration)'
  insert2 = 'INSERT INTO ingredient VALUES (:recipe, :rank, :name)'
  insert3 = 'INSERT INTO stage VALUES (:recipe, :rank, :description)'


  with open('recipes.json', 'r') as fh:
    recipes = json.load(fh)
  for id, recipe in enumerate(recipes):
    recipe['id'] = id
    db_run(insert1, recipe)
    for r, ingredient in enumerate(recipe['ingredients']):
      db_run(insert2, {'recipe': id, 'rank': r, 'name': ingredient['name']})
    for r, stage in enumerate(recipe['stages']):
      db_run(insert3, {'recipe': id, 'rank': r, 'description': stage['description']})
  

def add_user(username,password):
  insert = 'INSERT INTO user (name, password_hash) VALUES (?, ?)'
  password_hash=generate_password_hash(password)
  db_run(insert,(username,password_hash))

load()
add_user("sarah","12345")
add_user("ines","hamiche")
add_user("souso","azerty")


