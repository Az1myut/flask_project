# Flask Movie & User Management App

Dies ist eine voll funktionsfähige Web-Anwendung, die mit dem Python-Framework **Flask** und **MongoDB** als Datenbank erstellt wurde. Sie demonstriert fortgeschrittene Web-Entwicklungsprinzipien, einschließlich eines mehrstufigen Berechtigungssystems, Benutzer-Interaktionen und zentralisiertem Content-Management über ein Admin-Panel.

## ✨ Key Features

*   ✅ **Benutzer-Interaktion:**
    *   **Authentifizierung:** Vollständiger Registrierungs-, Login- und Logout-Workflow mit Flask-Sessions.
    *   **Likes & Favoriten:** Eingeloggte Benutzer können Filme "liken" und zu ihrer persönlichen Favoritenliste hinzufügen.

*   ✅ **Admin-Verwaltung & Berechtigungen:**
    *   **Zentrales Admin-Panel:** Eine dedizierte Admin-Seite ermöglicht alle CRUD-Operationen (Create, Read, Update, Delete) für die Kern-Objekte der Anwendung (z.B. Filme, Profile).
    *   **Klare Rollen-Hierarchie:** Das Projekt implementiert ein zweistufiges Berechtigungssystem:
        *   **Admin:** Hat volle Kontrolle über die Inhalte der Seite.
        *   **Superuser:** Eine übergeordnete Rolle, die zusätzlich die Berechtigungen von Admins verwalten kann.

*   ✅ **Saubere Architektur:**
    *   **Repository-Pattern:** Klare Trennung von Anwendungslogik und Datenzugriff durch eine wiederverwendbare Repository-Klasse.
    *   **Modernes Frontend:** Gestaltet mit dem Bootstrap-Framework für ein sauberes und responsives Design.

## 🏛️ Entitäten & Datenmodell

Das Projekt basiert auf drei zentralen Datenklassen (`dataclasses`), die in `models.py` definiert sind, um eine klare Struktur zu gewährleisten:

*   **User:** Repräsentiert einen Benutzeraccount und ist für die Authentifizierung zuständig. Enthält Login-Daten und die zugewiesene Rolle (z.B. User, Admin, Superuser).
*   **Profile:** Erweitert das User-Modell um persönliche Daten. Hier werden nutzerspezifische Informationen wie die Liste der favorisierten Filme gespeichert. Jeder User hat ein zugehöriges Profil.
*   **Movie:** Stellt einen Film mit Attributen wie Titel, Beschreibung und Erscheinungsjahr dar. Dient als primäres Inhaltsobjekt, mit dem Benutzer interagieren.

## 🛠️ Technologie-Stack

*   **Backend:** Flask
*   **Datenbank:** [MongoDB] mit [PyMongo])
*   **Datenmodellierung:** Python `dataclasses` mit `dataclasses_json`
*   **Frontend-Styling:** [Bootstrap 5](https://getbootstrap.com/)
*   **Abhängigkeiten:**  `requirements.txt`

## 🚀 Setup und lokale Installation

Folge diesen Schritten, um das Projekt lokal auf deinem macOS- oder Linux-Computer auszuführen.

1.  **Erstelle und aktiviere eine virtuelle Umgebung:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Installiere die Abhängigkeiten und starte die Anwendung:**
    ```bash
    pip install -r requirements.txt
    python3 app.py
    ```
   
## 💡 Projektstruktur
.
├── 📄 app.py           → Einstiegspunkt der App: Flask-Anwendung, Routen & Logik
├── 📄 entity.py        → Dataclasses für 🎞️ Movie, 👤 User, 🧾 Profile usw.
├── 📄 repository.py    → Datenzugriffsschicht (CRUD-Operationen)
├── 📁 templates/       → HTML-Templates (Jinja2) für das Web-Frontend
├── 📁 static/          → Statische Dateien wie 🎨 CSS, 🖼️ Bilder, 📜 JS
├── 📄 requirements.txt → Python-Abhängigkeiten (pip)
└── 📁 venv/            → Virtuelle Umgebung (🔒 lokal, nicht tracken!)

---
## 💡 Hinweis zur Verwendung von KI

Ein großer Teil der Frontend-Struktur, einschließlich der **HTML-Templates** und der **CSS-Stile**, wurde unter Verwendung von Vorschlägen und Code-Beispielen von **ChatGPT** entwickelt und verfeinert. Ebenso wurde die Implementierung der **Session-basierten Berechtigungsprüfung** (role_required) in den Routen durch Konzepte und Beispiele von ChatGPT inspiriert.

