from flask import Flask

app = Flask(__name__)


@app.route('/')
def startpage():  # put application's code here
    print("Ja, es wurde wirklich diese Methode aufgerufen!")
    antwort = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>AGWI 8.5.25</title>
        </head>
        <body>
        
        <h1>AGWI ist super</h1>
        <h2>Erster Grund</h2>
        <p>Ist nicht kompliziert.</p>
        <p>Zweiter Absatz. </p>
        <h2>Zweiter Grund</h2>
        <p>Weil halt! <a href="/test0815">Hier</a> geht es zur Testseite</p>
        <p>Und <a href="http://www.zalando.de">Zalando</a> ist auch aufrufbar.</p>
        </body>
        </html>
    """
    return antwort

@app.route('/test0815')
def test():
    return "Das ist ein Test."

if __name__ == '__main__':
    app.run()
