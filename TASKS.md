# Session Manager Implementation

Ein Session Manager zur persistenten Speicherung und Verwaltung von Konversationen (aus qv-ollama-sdk) in einer SQLite-Datenbank. Ziel ist eine einfache, effiziente und minimalistische Lösung.

## Completed Tasks

- [x] Analyse der Anforderungen und Abgleich mit bestehendem Code (qv-ollama-sdk, qv-ollama-simple-ui)
- [x] Entwurf des Datenmodells für SQLite (Konversationen, Nachrichten, Metadaten)
- [x] Implementierung der SessionManager-Klasse (save, load, list, delete, search)
- [x] Integration von Zeit-/ID-Suche und Wiederaufnahme-Funktionalität
- [x] Testfälle für die wichtigsten Funktionen
- [x] Ergänze Conversation und Message um Methoden zur vollständigen Serialisierung/Deserialisierung für die Datenbankspeicherung (z.B. to_db_dict, from_db_dict)
- [x] Erstelle ein praktisches Demo/Beispiel für die Nutzung mit qv-ollama-sdk
- [x] README.md mit Installationsanleitung und Verwendungsbeispielen

## In Progress Tasks

- [ ] README.md mit Installationsanleitung und Verwendungsbeispielen

## Future Tasks

- [ ] Erweiterung um weitere Such-/Filterfunktionen
- [ ] Optionale Verschlüsselung der gespeicherten Daten
- [ ] Export/Import von Konversationen (z.B. als JSON)

## Implementation Plan

- Das Datenmodell orientiert sich an den Conversation- und Message-Objekten aus qv-ollama-sdk.
- Nachrichten werden einzeln in der Datenbank abgelegt, um eine flexible Anzeige und Suche zu ermöglichen (analog zur UI-Logik in qv-ollama-simple-ui).
- Die SessionManager-Klasse kapselt alle Datenbankoperationen und bietet Methoden zum Speichern, Laden, Auflisten, Suchen und Löschen von Konversationen.
- Die Implementierung nutzt ausschließlich Python-Standardbibliothek (sqlite3).
- Fokus auf Klarheit, Effizienz und Erweiterbarkeit.

### Relevant Files

- session_manager.py - Enthält die SessionManager-Klasse und das Datenbankmodell. (✅)
- tests/test_session_manager.py - Testfälle für die SessionManager-Funktionen. (✅)
- examples/basic_usage.py - Vollständiges Demo der SessionManager-Funktionalität. (✅)
- README.md - Umfassende Dokumentation mit Installation, API-Docs und Beispielen. (✅) 