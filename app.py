from flask import Flask, request, render_template
from entity import User, Product
from repository import save, find_all, find_by_id

app = Flask(__name__)


@app.route('/')
def startpage():  # put application's code here
    print("Ja, es wurde wirklich diese Methode aufgerufen!")

    return render_template('start.html')


@app.route('/user')
def user_form():
    return render_template('user_formular.html')


@app.route('/do_user_registrierung', methods=['POST'])
def user_anlegen():
    neuer_user = User(request.form.get("username_"), request.form.get("password_"))
    save("users", neuer_user.username, neuer_user)
    return render_template('user_angelegt.html', user=neuer_user)


@app.route("/produkte")
def produkte_anzeigen():

    # z. B. aus Datenbank die Produkte/Kategorien/... holen
    produkte = find_all("products")

    return render_template('produkt_liste.html', products=produkte)


@app.route("/produkte/<produkt_id>")
def produkt_details(produkt_id):
    # über Repository (import!) aus Datenbank auslesen
    produkt = find_by_id("products", int(produkt_id))
    return render_template("produkt_details.html", product=produkt)


@app.route('/test0815')
def test():
    return "Das ist ein Test."


if __name__ == '__main__':
    app.run()
