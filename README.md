# QV Session Manager

Ein einfacher, effizienter Session Manager zur persistenten Speicherung und Verwaltung von Konversationen aus [qv-ollama-sdk](https://github.com/quantyverse/qv-ollama-sdk) in einer SQLite-Datenbank.

## ✨ Features

- 💾 **Persistente Speicherung** von Conversations und Messages in SQLite
- 🔍 **Volltextsuche** in Conversation-Inhalten und Titeln
- ⏰ **Zeit-basierte Suche** nach Erstellungs-/Aktualisierungsdatum
- 🔄 **Conversation-Wiederaufnahme** an beliebigen Punkten
- 📋 **Conversation-Management** (Listen, Löschen, Laden)
- 🎯 **Minimale Abhängigkeiten** (nur Python stdlib + qv-ollama-sdk)
- 🚀 **Einfache API** mit klaren, intuitiven Methoden

## 🛠️ Installation

### Aus PyPI (empfohlen)
```bash
pip install qv-session-manager
```

### Entwicklungsinstallation
```bash
git clone https://github.com/quantyverse/qv-session-manager.git
cd qv-session-manager
pip install -e .
```

### Abhängigkeiten
- Python 3.8+
- qv-ollama-sdk

## 🚀 Schnellstart

```python
from qv_session_manager import SessionManager
from qv_ollama_sdk.domain.models import Conversation

# SessionManager initialisieren
mgr = SessionManager(db_path="my_sessions.db")

# Neue Conversation erstellen
conv = Conversation(title="Python Hilfe", model_name="llama3")
conv.add_user_message("Erkläre mir Python-Listen!")
conv.add_assistant_message("Listen sind geordnete, veränderbare Sammlungen...")

# Speichern
mgr.save_conversation(conv, conv.messages)

# Laden
loaded = mgr.load_conversation(str(conv.id))
print(f"Geladen: {loaded.title} mit {len(loaded.messages)} Messages")

# Suchen
results = mgr.search_conversations("Listen")
print(f"Gefunden: {len(results)} Conversations")
```

## 📚 API-Dokumentation

### SessionManager

#### Initialisierung
```python
SessionManager(db_path: str = "session_manager.sqlite3")
```
- `db_path`: Pfad zur SQLite-Datenbankdatei

#### Methoden

##### `save_conversation(conversation, messages)`
Speichert eine Conversation und ihre Messages.
- `conversation`: Conversation-Objekt (mit `to_db_dict()` Methode)
- `messages`: Liste von Message-Objekten (mit `to_db_dict()` Methoden)

```python
mgr.save_conversation(conv, conv.messages)
```

##### `load_conversation(conversation_id: str) -> Conversation | None`
Lädt eine Conversation mit allen Messages.
- `conversation_id`: UUID der Conversation als String
- **Rückgabe**: Conversation-Objekt oder None

```python
conv = mgr.load_conversation("550e8400-e29b-41d4-a716-446655440000")
```

##### `list_conversations() -> List[Dict[str, Any]]`
Listet alle Conversations auf (ohne Messages).
- **Rückgabe**: Liste von Conversation-Dicts mit Metadaten

```python
all_convs = mgr.list_conversations()
for conv in all_convs:
    print(f"{conv['title']} - {conv['created_at']}")
```

##### `search_conversations(query: str) -> List[Dict[str, Any]]`
Volltextsuche in Titeln und Message-Inhalten.
- `query`: Suchbegriff
- **Rückgabe**: Liste gefundener Conversation-Dicts

```python
results = mgr.search_conversations("Python")
```

##### `search_by_time(start: str = None, end: str = None) -> List[Dict[str, Any]]`
Zeit-basierte Suche nach Conversations.
- `start`: Start-Datum (ISO-Format, z.B. "2025-01-20")
- `end`: End-Datum (ISO-Format)
- **Rückgabe**: Liste von Conversation-Dicts

```python
# Conversations von heute
today = datetime.now().strftime("%Y-%m-%d")
recent = mgr.search_by_time(start=today)

# Conversations aus einem Zeitraum
results = mgr.search_by_time(start="2025-01-01", end="2025-01-31")
```

##### `resume_conversation(conversation_id: str) -> Dict[str, Any] | None`
Bereitet Conversation-Wiederaufnahme vor.
- `conversation_id`: UUID der Conversation
- **Rückgabe**: Dict mit `conversation` und `last_message`

```python
resumed = mgr.resume_conversation(str(conv.id))
last_msg = resumed["last_message"]
print(f"Letzte Nachricht: {last_msg['content']}")
```

##### `delete_conversation(conversation_id: str)`
Löscht eine Conversation und alle zugehörigen Messages.
- `conversation_id`: UUID der Conversation

```python
mgr.delete_conversation(str(conv.id))
```

## 💡 Erweiterte Beispiele

### Conversation-Management mit Metadaten

```python
from datetime import datetime
from qv_session_manager import SessionManager
from qv_ollama_sdk.domain.models import Conversation

mgr = SessionManager()

# Conversation mit Metadaten
conv = Conversation(
    title="JavaScript Tutorial",
    model_name="llama3",
    metadata={
        "topic": "web-development", 
        "difficulty": "beginner",
        "language": "javascript"
    }
)

# Messages hinzufügen
conv.add_system_message("Du bist ein erfahrener Web-Entwickler.")
conv.add_user_message("Erkläre mir Closures in JavaScript.")

# Speichern
mgr.save_conversation(conv, conv.messages)

# Nach Topic suchen
web_convs = [c for c in mgr.list_conversations() 
             if c.get('metadata', {}).get('topic') == 'web-development']
```

### Batch-Operationen

```python
# Alle Conversations eines Tages löschen
target_date = "2025-01-20"
old_convs = mgr.search_by_time(start=target_date, end=target_date)

for conv in old_convs:
    mgr.delete_conversation(conv['id'])
    print(f"Gelöscht: {conv['title']}")
```

### Conversation-Fortsetzung

```python
# Bestehende Conversation laden und erweitern
conv = mgr.load_conversation("existing-conversation-id")

if conv:
    # Neue Messages hinzufügen
    conv.add_user_message("Kannst du das nochmal erklären?")
    conv.add_assistant_message("Gerne! Lass mich das anders formulieren...")
    
    # Aktualisierte Version speichern
    mgr.save_conversation(conv, conv.messages)
```

## 🧪 Entwicklung & Testing

### Tests ausführen
```bash
# Alle Tests
pytest

# Spezifischer Test
pytest tests/test_session_manager.py

# Mit Ausgabe
pytest -v -s
```

### Demo ausführen
```bash
python examples/basic_usage.py
```

### Projektstruktur
```
qv-session-manager/
├── src/qv_session_manager/
│   ├── __init__.py
│   └── session_manager.py
├── tests/
│   └── test_session_manager.py
├── examples/
│   └── basic_usage.py
├── README.md
└── pyproject.toml
```

## 🗄️ Datenbankschema

Die SQLite-Datenbank verwendet folgendes Schema:

```sql
-- Conversations-Tabelle
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,           -- UUID
    title TEXT,                    -- Conversation-Titel
    created_at TEXT,              -- ISO-Timestamp
    updated_at TEXT,              -- ISO-Timestamp  
    metadata TEXT                 -- JSON-Metadaten
);

-- Messages-Tabelle
CREATE TABLE messages (
    id TEXT PRIMARY KEY,          -- UUID
    conversation_id TEXT,         -- Referenz zu conversations.id
    role TEXT,                    -- "system", "user", "assistant"
    content TEXT,                 -- Message-Inhalt
    created_at TEXT,             -- ISO-Timestamp
    metadata TEXT,               -- JSON-Metadaten
    FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
```

## 🤝 Integration mit qv-ollama-sdk

```python
from qv_ollama_sdk.client import OllamaClient
from qv_session_manager import SessionManager

# Clients initialisieren
ollama = OllamaClient()
session_mgr = SessionManager()

# Neue Conversation
conv = ollama.create_conversation(model="llama3")
conv.title = "Code Review Session"

# Mit Ollama chatten
response = ollama.chat(conv, "Erkläre mir Clean Code Prinzipien")
print(response.content)

# Session persistent speichern
session_mgr.save_conversation(conv, conv.messages)

# Später: Session wieder laden und fortsetzen
loaded_conv = session_mgr.load_conversation(str(conv.id))
next_response = ollama.chat(loaded_conv, "Welche Tools empfiehlst du?")
```

## 📋 Roadmap

- [ ] Erweiterte Such-/Filterfunktionen (z.B. nach Metadaten)
- [ ] Optionale Verschlüsselung der gespeicherten Daten
- [ ] Export/Import von Conversations (JSON, CSV)
- [ ] Performance-Optimierungen für große Datenmengen
- [ ] Async-Support für high-performance Anwendungen

## 🐛 Fehlerbehandlung

```python
try:
    conv = mgr.load_conversation("invalid-id")
    if conv is None:
        print("Conversation nicht gefunden")
except Exception as e:
    print(f"Fehler beim Laden: {e}")
```

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## 🚀 Beitragen

1. Fork des Repositories
2. Feature-Branch erstellen (`git checkout -b feature/amazing-feature`)
3. Änderungen committen (`git commit -m 'Add amazing feature'`)
4. Branch pushen (`git push origin feature/amazing-feature`)
5. Pull Request erstellen

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/quantyverse/qv-session-manager/issues)
- **Dokumentation**: Diese README
- **Beispiele**: Siehe `examples/` Verzeichnis
