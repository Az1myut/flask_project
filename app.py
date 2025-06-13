import atexit
import flask
from flask import Flask, request, render_template, session, redirect
from entity import User, Product
from repository import save, find_all, find_by_id
from repository_db import Repository
from pymongo import MongoClient
import math

app = Flask(__name__)

#Für session notwendig:
app.secret_key = "i7tbiuztifuertlbjh234qat"

#Verbindung zur Datenbank
username = "abc22222"
password = username + "_secret"
auth_source = username
host = "im-vm-005"
port = 27017

try:
    client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_source}", serverSelectionTimeoutMS=3000)
    client.admin.command("ping")
    print("Verbindung zu MongoDB aufgebaut")
    db = client[f"{auth_source}"]
except:
    print("Keine Verbindung zur Datenbank (VPN-Verbindung an?!?)")
    exit(0)

#Erzeugen der Repo-Objekte
user_repo = Repository[User](db["users"], User, primary_key="username")
product_repo = Repository[Product](db["products"], Product, primary_key="product_id")


@app.route('/')
def startpage():  # put application's code here
    if 'logout' in request.args:
        session.pop('eingeloggter_user') # entfernt Eintrag 'eingeloggter_user' aus dem session-dict --> das ist der "Logout"

    return render_template('start.html')

@app.route('/do_user_registrierung', methods=['POST'])
def user_anlegen():
    neuer_user = User(request.form.get("username_"), request.form.get("password_"))

    #save("users", neuer_user.username, neuer_user)
    user_repo.save(neuer_user)

    session["eingeloggter_user"] = neuer_user

    return render_template('user_angelegt.html', user=neuer_user)


@app.route('/register')
def user_form():
    return render_template('user_formular.html')

@app.route('/login')
def user_login():
    return render_template('login_formular.html')

@app.route('/do_login', methods=['POST'])
def user_einloggen():

    user_from_db = user_repo.find_by_id(request.form.get("username"))
    if user_from_db != None:
        if user_from_db.password == request.form.get("password"):
            session["eingeloggter_user"] = user_from_db
            return render_template('start.html', name=user_from_db.username)

    flask.flash("Username oder Passwort falsch", category="error")
    return render_template('start.html')

@app.route('/search', methods=['GET'])
def search():
    # Bei Methode 'GET' ist der Parameter in 'request.args'...
    # ...bei 'POST' in 'request.form'
    produkte = product_repo.find({ "$or": [
            {"title" : {"$regex": request.args.get("keyword"), "$options": "i"} },
            {"description" : {"$regex": request.args.get("keyword"), "$options": "i"} }
        ]
    })

    return render_template('produkt_liste.html', products=produkte)

@app.route("/produkte")
def produkte_anzeigen():
    produkte_je_seite = 2
    anzahl_produkte = db["products"].count_documents({})
    seite = 1
    if 'page' in request.args:
        seite = int(request.args.get("page"))
    print("anzahl produkte")
    print(anzahl_produkte)
    print("max")
    max = math.ceil(anzahl_produkte/produkte_je_seite)
    print(max)
    produkte = product_repo.find_all(skip=(seite-1)*produkte_je_seite, limit=produkte_je_seite)

    return render_template('produkt_liste.html', products=produkte, page=seite, max=max)


@app.route("/produkte/<produkt_id>")
def produkt_details(produkt_id):
    # Achtung, Pfad-Parameter sind immer Strings - hier <produkt_id>
    # muss erst in ein int umgewandelt werden!
    produkt = product_repo.find_by_id( int(produkt_id) )
    return render_template("produkt_details.html", product=produkt)


@atexit.register
def shutdown_hook():
    print("Schließe MongoDB-Verbindung...")
    client.close()

if __name__ == '__main__':
    app.run()
