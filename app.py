from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def startpage():  # put application's code here
    print("Ja, es wurde wirklich diese Methode aufgerufen!")
    antwort = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>AGWI 15.5.25</title>
            </head>
            <body>

                <h1>AGWI ist super</h1>
                <h2>Erster Grund</h2>
                <p>Ist nicht kompliziert.</p>
                <p>Zweiter Absatz. </p>
                <h2>Zweiter Grund</h2>
                <p>Weil halt! 
                    <a href="/test0815">Hier</a> 
                   geht es zur Testseite
                </p>
                <p>Und 
                    <a href="http://www.zalando.de">Zalando</a> 
                    ist auch aufrufbar.
                </p>

                <p>
                    <a href="http://de.wikipedia.org/wiki/Katzen">
                        <img src="https://wallpapers.com/images/hd/cute-cat-pictures-cd92rtzsrel4rtwm.jpg" width="150px"></img>
                    </a>

                    <img src="static/tree.jpg"></img>
                </p>

                <p>
                    <a href="/produkte">Hier geht es zu den Produkten</a>
                </p>

                <p>
                    <a href="/user">Hier neu registrieren</a>
                </p>

            </body>
        </html>
    """
    return antwort


@app.route('/user')
def user_form():
    html = """
    <form action="/do_user_registrierung" method="POST">
        <label for="un">Username:</label><br>
        <input type="text" id="un" name="username_" value="Bitte geben Sie Ihren Namen ein"><br>

        <label for="pw">Passwort:</label><br>
        <input type="password" id="pw" name="password_"><br><br>

        <input type="submit" value="Jetzt registrieren">
    </form> 
    """

    return html


@app.route('/do_user_registrierung', methods=['POST'])
def user_anlegen():
    username = request.form.get("username_")  # alternative Syntax: request.form['username_']
    password = request.form.get("password_")
    return f"User {username} angelegt (Passwort:{password})"


@app.route("/produkte")
def produkte_anzeigen():
    html = """
    <h1>Produkte</h1>
      <ul>
      """

    html_end = """
    </ul>
    """

    # z. B. aus Datenbank die Produkte/Kategorien/... holen
    produkt_ids = (1, 2, 3, 77, 432, 9, 200, 89756434, 45637)
    for id in produkt_ids:
        html += f"<li><a href=\"/produkte/{id}\">Produkt {id}</a></li>"

    html += html_end
    return html


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
