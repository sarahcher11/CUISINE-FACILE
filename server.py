from functools import wraps
from flask import Flask, abort, session, Response, request, redirect, url_for, render_template
import data_model as model

app = Flask(__name__)

app.secret_key = 'gghyednejcn'  

########################################
# Routes des pages principales du site #
########################################


def login_required(f):
  @wraps(f)
  def decorated_function(*args,**kwargs):
    if 'user_id' not in session :
      return Response('Unauthorized', 401)
    return f(*args,**kwargs)
  return decorated_function

@app.get('/ma_route')
@login_required
def ma_route():
    # Le code de la route ici
    pass



@app.get('/logout')
def logout():
 
  session.clear()
  return redirect ('/')

@app.get('/new_user')
def signup_form():
  return render_template('new_user.html')

@app.post('/new_user')
def signup():
    name = request.form['name']
    password = request.form['password']
    confirmed_password = request.form['confirm_password']
    if password != confirmed_password:
        erreur = 'Passwords do not match'
        return render_template("new_user.html", error=erreur)
    user_id = model.new_user(name, password)
    if user_id == None:
        session['user_id'] = user_id
        session['username'] = name
        return redirect('/')
    else:
        erreur = 'This username already exists'
        return render_template('new_user.html', error=erreur)

  


@app.get('/login')
def login_form():
  return render_template('login.html')

@app.post('/login')
def login():
  username=request.form['name']
  password=request.form['password']

  user_id=model.login(username,password)
  if user_id!=-1:
    session['user_id']=user_id
    session['username']=username
    session['auth_success']=True
    return redirect('/')
  else:
    erreur='Failed authentification'
    return render_template("login.html", error=erreur)

# Retourne une page principale avec le nombre de recettes
@app.get('/')
def home():
  session['auth_success']=False
  return render_template('index.html')


# Retourne les résultats de la recherche à partir de la requête "query"
@app.get('/search')
def search():
  if 'page' in request.args:
    page = int(request.args["page"])
  else:
    page = 1
  if 'query' in request.args:
    query = request.args["query"]
  else:
    query = ""
  found = model.search(query, page)
  return render_template('search.html', found=found)

# Retourne le contenu d'une recette d'identifiant "id"
@app.get('/read/<id>')
def read(id):
  recipe = model.read(int(id))
  return render_template('read.html', recipe=recipe)


@app.get('/create')
def create_form():
  return render_template('create.html')

@app.get('/update/<id>')
def update_form(id):
  recipe = model.read(int(id))
  return render_template('update.html', recipe=recipe)


@app.get('/delete/<id>')
def delete_form(id):
  entry = model.read(int(id))
  return render_template('delete.html', id=id, title=entry['title'])


############################################
# Routes pour modifier les données du site #
############################################


def parse_user_list(user_list):
  l = user_list.strip().split("-")
  l = [e.strip() for e in l]
  l = [e for e in l if len(e)> 0]
  return l
# Fonction qui facilite la création d'une recette
def post_data_to_recipe(form_data):
  ingredients = parse_user_list(form_data['ingredients'])
  stages = parse_user_list(form_data['stages'])
  return {
    'title': form_data['title'], 
    'description': form_data['description'],
    'img': form_data['img'],
    'duration': form_data['duration'],
    'ingredients': ingredients,
    'stages': stages
  }

@app.post('/create')
def create_post():
  id = model.create(post_data_to_recipe(request.form))
  return redirect(url_for('read', id=str(id)))


@app.post('/update/<id>')
def update_post(id):
  id = int(id)
  model.update(id, post_data_to_recipe(request.form))
  return redirect(url_for('read', id=str(id)))


@app.post('/delete/<id>')
def delete_post(id):
  model.delete(int(id))
  return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
