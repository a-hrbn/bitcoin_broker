# Bitcoin Broker

Bitcoin Broker sammelt monatlich die meistdiskutierten Beiträge aus `r/Bitcoin`, lässt diese per Gemini zusammenfassen und sendet die Auswertung in eine Telegram-Gruppe.

## Funktionen

- Abruf der Top-Posts des Monats aus Reddit
- Extraktion relevanter Beitragsinhalte
- KI-Auswertung (Stimmung, Hauptpunkte, Empfehlung)
- Versand der Auswertung per Telegram
- Geplanter Lauf am 1. Tag des Monats (08:00 Uhr)

## Voraussetzungen

- Python 3.11+
- Reddit API Zugang
- Google Gemini API Key
- Telegram Bot Token
- Telegram Chat/Group ID

## Konfiguration

Die Zugangsdaten werden aktuell direkt in `app.py` gesetzt:

- `REDDIT_API_KEY`
- `GEMINI_API_KEY`
- `BOT_TOKEN`
- `GROUP_TOKEN`

> Hinweis: Für produktive Nutzung sollten Secrets nicht im Code hinterlegt werden.

## Lokaler Start

1. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
2. API-Keys und Tokens in `app.py` eintragen.
3. Anwendung starten:
   ```bash
   python app.py
   ```

## Start mit Docker Compose

```bash
docker compose up --build -d
```

Logs anzeigen:

```bash
docker compose logs -f
```

## Projektstruktur

- `/app.py` – Hauptlogik (Datenabruf, KI-Auswertung, Scheduler, Telegram-Versand)
- `/requirements.txt` – Python-Abhängigkeiten
- `/Dockerfile` – Container-Definition
- `/docker-compose.yml` – Container-Orchestrierung
