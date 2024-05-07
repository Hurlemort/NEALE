from flask import Flask, render_template, request, url_for, redirect, session
import pymongo # Connexion avec MangoDB
import os # os = environnement sécurisé
import bcrypt 
from bson.objectid import ObjectId # Pour gérer les OcbjectId

# Connextion à la BDD 
mongo = pymongo.MongoClient(os.getenv("MONGO_KEY"))

# Création de l'application.
app = Flask("NEALE")

# Cookie de session d'utilisateur
app.secret_key = os.getenv("COOKIES_KEY")



# Route de la page d'accueil
@app.route('/')
def index():
  '''
  db_memes = mongo.NEALE.memes
  memes = db_memes.find({})
  if 'user' in session:
    return render_template('index.html', memes=memes, username=session['user'])
  else:
    return render_template('index.html', memes=memes)'''
  return render_template('index.html')

################
# UTILISATEURS #
################

# Route settings
@app.route('/settings')
def settings():
  '''
  if 'user' in session:
    if request.method=='POST':
      return render_template("settings.html")
    else:
      return render_template("settings.html")
  else:
    return render_template("signup.html", error="You must be logged in to access your settings")'''
  return render_template("settings.html")
  

# Route signup
@app.route('/signup', methods=['POST', 'GET'])
def signup():
  # Si on essaye de soummetre le formulaire
  if request.method == 'POST':
    # On vérifie qu'un utilisateur du même nom n'existe pas déjà
    db_users = mongo.NEALE.users
    # Si l'utilisateur existe déjà, on invalide l'envoi du formulaire
    if (db_users.find_one({'username': request.form['username']})):
      return render_template('signup.html', error = "Sorry, this username is already in use")
    # Sinon, on crée l'utilisateur
    else:
      if (request.form['password'] == request.form['password_verif']):
        # On hash le mot de passe
        password_hash = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # On ajoute l'utilisateur à la BDD
        db_users.insert_one({
          'username': request.form['username'],
          'password': password_hash,
        })
        # On connecte l'utilisateur
        session['user'] = request.form['username']
        # On renvoie l'utilisateur à la page d'accueil
        return redirect(url_for('index'))
      else:
        return render_template('signup.html', error = "Passwords don't match")
  else:
    return render_template('signup.html')

# Route login
@app.route('/login', methods=['POST', 'GET'])
def login():
  # Si on essaie de se connecter
  if request.method == 'POST':
    db_users = mongo.NEALE.users
    # Trouver si l'utilisateur correspond à celui entré
    user = db_users.find_one({'username': request.form['username']})
    # Si l'utilisateur existe
    if user:
      # On vérifie si le mot de passe est bon
      if bcrypt.checkpw(request.form['password'].encode('utf-8'), user['password']):
        session['user'] = request.form['username']
        return redirect(url_for('index'))
      # On renvoie un message d'erreur si le mdp ne marche pas   
      else:
        return render_template('login.html', error = "Invalid password")
    # On renvoie un message d'erreur si le nom d'utilisateur ne marche pas   
    else:
      return render_template('login.html', error = "Invalid username")
  else:
    return render_template('login.html')

# Route logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Route compte spécifique 
app.route('/user')
def user():
  return render_template('user.html')

#########
# MEMES #
#########

#menu des memes
@app.route('/memes')
def memes():
  db_memes = mongo.NEALE.memes
  memes = db_memes.find({})
  '''if 'user' in session:
    return render_template("memes.html", memes=memes, user=session['user'])
  else:'''
  return render_template("memes.html", memes=memes)

# Route pour "mieux voir" un meme + comments
@app.route('/memes/one_meme/<id>', methods=['POST', 'GET'])
def meme(id):
  db_memes = mongo.NEALE.memes
  meme = db_memes.find_one({"_id":ObjectId(id)})
  db_comments = mongo.NEALE.comments
  comments = db_comments.find({"MemeID":id})
  print(comments)
  if request.method == 'POST':
    if 'user' not in session:
      return redirect(url_for('login'))
    else:
      user = session['user']
      db_comments.insert_one({
        "MemeID":id,
        "author":user,
        "comment":request.form['comment']
      })
      return render_template("one_meme.html", meme=meme, Comments=comments)
  else:
    db_memes = mongo.NEALE.memes
    meme = db_memes.find_one({'_id': ObjectId(id)})
    return render_template('one_meme.html', meme=meme, Comments=comments)
    


# Route pour créer un nouveau meme
@app.route('/memes/new', methods=['POST', 'GET'])
def newmeme():
  # Si l'utilisateur n'est pas connecté 
  if 'user' not in session: 
    return render_template("login.html", erreur="You must log in to post a meme")
  # si on essaye d'envoyer le formulaire

  if request.method == 'POST':
    # on appelle la table "annonces" de la bdd
    db_memes = mongo.NEALE.memes
    # On récupère ce que l'utilisateur a rempli dans le formulaire
    title = request.form['title']
    description = request.form['description']
    image = request.form['image']
    # Si les champs titre et description sont remplis
    if (title and description and image):
      # On insère dans la bdd les nouvelles données
      db_memes.insert_one({
        'title': title,
        'description': description,
        'image': image,
        'user':session['user']
      })
      return render_template("newmeme.html", erreur="Your meme has been successfully posted")
    else:
      return render_template("newmeme.html", erreur="Please fill in a title, image and description")
  return render_template("newmeme.html") 






#########
# GAMES #
#########

@app.route('/games')
def games():
  return render_template("games.html")



#########
# ADMIN #
#########

@app.route('/admin/backmemes')
def adminmemes():
  db_memes = mongo.NEALE.memes
  memes = db_memes.find({})
  return render_template("admin/backmemes.html", memes = memes)

@app.route('/admin/backusers')
def adminusers():
    db_users = mongo.NEALE.users
    users = db_users.find({})
    return render_template("admin/backmemes.html", users = users)

#Execution du code
app.run(host='0.0.0.0', port=81)