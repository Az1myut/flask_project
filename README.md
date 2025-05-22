# AGWI Beispielprojekt

Stand 22.05.2025

## Cascading Style Sheets (CSS)

Mit Hilfe der erstellten [css-Datei](static/css/style.css) werden Layout-Informationen (Farben, Schrift, Rahmen, Position, ...)
den Elementen in HTML zugeordnet.

Grundsätzlich im Format `<SELECTOR> { <PROPERTY>:<VALUE>; ... }` mit folgenden drei genutzten *Selektoren* (Beispiele):
- `h1 { color:rgb(30,45,129); backgroud-color:blue; font-family:Arial; }` --> legt das Layout für alle `<h1>`-Elemente fest
- `#xyz { ... }` --> legt das Layout für das Element `<div id="xyz">...</div>` fest (und für die enthaltenen Unter-Elemente)
- `.abc { ... }` --> legt das Layout für Elemente fest, die der Klasse `abc` zugeordnet werden, z. B. `<p class="abc">`

## Frontend-Toolkit 'Bootstrap'

Das Frontend-Toolkit [Bootstrap](https://www.getbootstrap.com) definiert ein eine große Menge an CSS-Klassen und gibt viele Beispiele, 
wie diese genutzt werden können. Die HTML-Beispiele in [Docs](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
wie *Tables*, *Forms*, *Cards* u. v. m. können einfach für die eigenen HTML-Templates genutzt und angepasst werden.

Einzige Voraussetzung ist, dass die CSS-Datei von Bootstrap im HTML-Header des eigenen HTML-Templates eingebunden wurde.
Dies geschieht mit dem Element `<link rel="stylesheet" href="...">` im HTML-Element `<head>`.
In diesem Beispielprojekt z. B. in [base.html](templates/base.html) zu finden.

## Template-Engine

Mit `from flask import render_template` kann die Methode `render_template("mein_template.html", ...)` genutzt werden.
Hierfür werden HTML-Dateien im Ordner [/templates](templates) als Templates erstellt, deren Inhalt dann von der Methode
geladen und zurückgegeben wird.

Für variable Anteile im Template werden diese mit `{{ variablen_name }}` definiert.
Fallunterscheidungen und Wiederholungen (Schleifen) sind im Template ebenfalls möglich mit `{% if ... %}...{% endif %}` 
und `{% for ...%}...{% endfor %}`. Siehe dazu die Beispiele in den Templates!

## Besprochene HTML-Elemente

```html
<a href=""></a>

<form action="">...
   <input ...>
   <label ...>
</form>

<h1>, <h2>, ...
<p>
<img src="">
<ul> <li></li> ... </ul>
<ol> <li></li> ... </ol>

```

## Besprochene Python- und Flask-Features

- Templates mit render_template()-Methode
- Methodendefinition mit `def` und Routendefinition (Link) zur Methode mit `@app.route`
- Variablen, Listen, Maps
- foreach-Schleife `for ... in ...`
- Strings `+= f".....{var}..."` und Multi-Line-Strings mit `""" ... """`
- Variable Pfadinformationen mit `@app.route(".../<var>")` und `def methode(var)`
- Formulardaten und Variable `request.form.get("input_name")`
- ...