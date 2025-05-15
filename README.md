# AGWI Beispielprojekt

Stand 15.05.2025

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

- Methodendefinition mit `def` und Routendefinition (Link) zur Methode mit `@app.route`
- Variablen, Listen, Maps
- foreach-Schleife `for ... in ...`
- Strings `+= f".....{var}..."` und Multi-Line-Strings mit `""" ... """`
- Variable Pfadinformationen mit `@app.route(".../<var>")` und `def methode(var)`
- Formulardaten und Variable `request.form.get("input_name")`
- ...