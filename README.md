# Der Flaneur

Kulturveranstaltungen im Saarland

## Projekt-Übersicht

Dieses Projekt wurde von Pelican (Python static site generator) zu Jekyll (Ruby-basiert) migriert. Die Website wird automatisch mit GitHub Pages gebaut und deployed.

## Lokale Entwicklung

### Anforderungen

- Ruby 3.0+
- Bundler (wird mit Ruby installiert)
- Git

### Installation

1. **Repository klonen**
   ```bash
   git clone https://github.com/saschamarkus/flaneur.git
   cd flaneur
   ```

2. **Ruby-Dependencies installieren**
   ```bash
   bundle install
   ```

3. **Website lokal starten**
   ```bash
   bundle exec jekyll serve
   ```

   Die Website ist dann unter `http://localhost:4000/flaneur` erreichbar.

### Website bauen

```bash
bundle exec jekyll build
```

Dies erstellt die statische Website im Ordner `_site/`.

## Projekt-Struktur

```
.
├── _config.yml              # Jekyll-Konfiguration
├── _posts/                  # Blog-Beiträge (Markdown)
├── _layouts/                # HTML-Templates
├── _includes/               # Wiederverwendbare HTML-Komponenten
├── assets/
│   ├── css/                 # Stylesheets
│   └── images/              # Bilder
├── Gemfile                  # Ruby-Dependencies
├── Gemfile.lock             # Gesperrte Dependency-Versionen
└── .github/workflows/       # GitHub Actions für CI/CD
```

## Neue Beiträge hinzufügen

### Beitrag erstellen

1. Neue Datei in `_posts/` erstellen mit dem Namen:
   ```
   YYYY-MM-DD-title-slug.md
   ```

   Beispiel: `2024-02-26-neue-ausstellung.md`

2. Datei mit folgendem Front Matter beginnen:
   ```yaml
   ---
   layout: post
   title: Titel des Beitrags
   date: 2024-02-26 19:30
   category: Ausgehen
   ---
   ```

3. Inhalt in Markdown schreiben:
    ```markdown
    # Überschrift

    Text mit **Fettdruck** und *Kursiv*.

    ![Bildtext](/assets/images/bild.jpg)

    - Punkt 1
    - Punkt 2
    ```

### Bilder hinzufügen

Bilder sollten in `assets/images/` abgelegt werden und können einfach mit:
```markdown
![Beschreibung](/assets/images/dateiname.jpg)
```

eingebunden werden.

## GitHub Pages Deployment

Die Website wird automatisch bei jedem Push zum `master` oder `main` Branch mit GitHub Actions gebaut und zu GitHub Pages deployed.

### Workflow-Datei

Der Build-Prozess ist in `.github/workflows/build.yml` definiert:
- Läuft auf jeden Push zum `master`/`main` Branch
- Führt `jekyll build` durch
- Deployed zu GitHub Pages

### Pages-Einstellungen

In den Repository-Settings unter "Pages":
- Source sollte auf "GitHub Actions" eingestellt sein
- Die Website wird unter `https://saschamarkus.github.io/flaneur` erreichbar sein

## Konfiguration

### _config.yml anpassen

Die wichtigsten Einstellungen in `_config.yml`:

```yaml
title: Der Flaneur              # Website-Titel
description: ...               # Website-Beschreibung
author: Sascha Markus          # Autor
baseurl: /flaneur              # Basis-URL (für Subpath-Hosting)
url: https://saschamarkus.github.io
timezone: Europe/Berlin        # Zeitzone
```

## Styling

Die Website nutzt ein eigenes CSS in `assets/css/style.css`. Das Design basiert auf:
- Serif-Schrift (Libre Baskerville)
- Primärfarbe: #4267b2 (Blau)
- Responsive Design für Mobile-Geräte

## Migration von Pelican

Diese Projekt wurde erfolgreich von Pelican migriert:
- ✅ Alle Beiträge von `content/` nach `_posts/` konvertiert
- ✅ Pelican-Theme durch Jekyll-Layouts ersetzt
- ✅ `pelicanconf.py` und alte Python-Dateien können entfernt werden
- ✅ GitHub Actions Workflow konfiguriert

Alte Pelican-Dateien:
- `pelicanconf.py` (kann gelöscht werden)
- `publishconf.py` (kann gelöscht werden)
- `content/` Ordner (Beiträge wurden migriert)
- `m.css/` Theme (nicht mehr benötigt)

## Troubleshooting

### Build schlägt fehl?

1. Überprüfe die `Gemfile` auf Fehler
2. Führe `bundle update` aus
3. Lösche `_site/` und `.jekyll-cache/` Ordner
4. Versuche den Build erneut

### Website wird nicht korrekt angezeigt?

1. Überprüfe die `baseurl` Einstellung in `_config.yml`
2. Überprüfe die relativen Pfade zu Assets
3. Kontrolliere die Browser-Console auf JavaScript-Fehler

## Lizenz und Links

- **Webseite**: https://saschamarkus.github.io/flaneur
- **Repository**: https://github.com/saschamarkus/flaneur
- **Autor**: Sascha Markus

## Weitere Ressourcen

- [Jekyll Dokumentation](https://jekyllrb.com/docs/)
- [GitHub Pages Dokumentation](https://docs.github.com/en/pages)
- [Markdown Guide](https://www.markdownguide.org/)
