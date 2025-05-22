from flask import Flask, request, render_template

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
    username = request.form.get("username_")  # alternative Syntax: request.form['username_']
    password = request.form.get("password_")
    return render_template('user_angelegt.html', user=username, pw=password)


@app.route("/produkte")
def produkte_anzeigen():

    # z. B. aus Datenbank die Produkte/Kategorien/... holen
    produkt_ids = (1, 2, 3, 77, 432, 9, 200, 89756434, 45637)

    return render_template('produkt_liste.html', products=produkt_ids)


@app.route("/produkte/<produkt_id>")
def produkt_details(produkt_id):
    detail = f"""
    <h1>Produkt {produkt_id}</h1>
    <p>Titel: Produkt_{produkt_id}</p>
    <p>Preis: {produkt_id} Euro</p>
    """
    return detail


@app.route('/test0815')
def test():
    return "Das ist ein Test."


if __name__ == '__main__':
    app.run()
