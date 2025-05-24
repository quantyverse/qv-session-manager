# QV Session Manager

A simple, efficient session manager for persistent storage and management of conversations from [qv-ollama-sdk](https://github.com/quantyverse/qv-ollama-sdk) in an SQLite database.

## ✨ Features

- 💾 **Persistent storage** of conversations and messages in SQLite
- 🔍 **Full-text search** in conversation contents and titles
- ⏰ **Time-based search** by creation/update date
- 🔄 **Conversation resumption** at any point
- 📋 **Conversation management** (list, delete, load)
- 🎯 **Minimal dependencies** (only Python stdlib + qv-ollama-sdk)
- 🚀 **Simple API** with clear, intuitive methods

## 🛠️ Installation

### From PyPI 
```bash
pip install qv-session-manager

or

uv add qv-session-manager
```

### Development installation
```bash
git clone https://github.com/quantyverse/qv-session-manager.git
cd qv-session-manager
pip install -e .
```

### Dependencies
- Python 3.10+
- qv-ollama-sdk

## 🚀 Quickstart

```python
from qv_session_manager import SessionManager
from qv_ollama_sdk.domain.models import Conversation

# Initialize SessionManager
mgr = SessionManager(db_path="my_sessions.db")

# Create new conversation
conv = Conversation(title="Python Help", model_name="llama3")
conv.add_user_message("Explain Python lists to me!")
conv.add_assistant_message("Lists are ordered, mutable collections...")

# Save
mgr.save_conversation(conv, conv.messages)

# Load
loaded = mgr.load_conversation(str(conv.id))
print(f"Loaded: {loaded.title} with {len(loaded.messages)} messages")

# Search
results = mgr.search_conversations("lists")
print(f"Found: {len(results)} conversations")
```

## 📚 API Documentation

### SessionManager

#### Initialization
```python
SessionManager(db_path: str = "session_manager.db")
```
- `db_path`: Path to the SQLite database file

#### Methods

##### `save_conversation(conversation, messages)`
Saves a conversation and its messages.
- `conversation`: Conversation object (with `to_db_dict()` method)
- `messages`: List of Message objects (with `to_db_dict()` methods)

```python
mgr.save_conversation(conv, conv.messages)
```

##### `load_conversation(conversation_id: str) -> Conversation | None`
Loads a conversation with all messages.
- `conversation_id`: UUID of the conversation as a string
- **Returns**: Conversation object or None

```python
conv = mgr.load_conversation("550e8400-e29b-41d4-a716-446655440000")
```

##### `list_conversations() -> List[Dict[str, Any]]`
Lists all conversations (without messages).
- **Returns**: List of conversation dicts with metadata

```python
all_convs = mgr.list_conversations()
for conv in all_convs:
    print(f"{conv['title']} - {conv['created_at']}")
```

##### `search_conversations(query: str) -> List[Dict[str, Any]]`
Full-text search in titles and message contents.
- `query`: Search term
- **Returns**: List of found conversation dicts

```python
results = mgr.search_conversations("Python")
```

##### `search_by_time(start: str = None, end: str = None) -> List[Dict[str, Any]]`
Time-based search for conversations.
- `start`: Start date (ISO format, e.g. "2025-01-20")
- `end`: End date (ISO format)
- **Returns**: List of conversation dicts

```python
# Conversations from today
today = datetime.now().strftime("%Y-%m-%d")
recent = mgr.search_by_time(start=today)

# Conversations from a period
results = mgr.search_by_time(start="2025-01-01", end="2025-01-31")
```

##### `resume_conversation(conversation_id: str) -> Dict[str, Any] | None`
Prepares conversation resumption.
- `conversation_id`: UUID of the conversation
- **Returns**: Dict with `conversation` and `last_message`

```python
resumed = mgr.resume_conversation(str(conv.id))
last_msg = resumed["last_message"]
print(f"Last message: {last_msg['content']}")
```

##### `delete_conversation(conversation_id: str)`
Deletes a conversation and all associated messages.
- `conversation_id`: UUID of the conversation

```python
mgr.delete_conversation(str(conv.id))
```

## 💡 Advanced Examples

### Conversation management with metadata

```python
from datetime import datetime
from qv_session_manager import SessionManager
from qv_ollama_sdk.domain.models import Conversation

mgr = SessionManager()

# Conversation with metadata
conv = Conversation(
    title="JavaScript Tutorial",
    model_name="llama3",
    metadata={
        "topic": "web-development", 
        "difficulty": "beginner",
        "language": "javascript"
    }
)

# Add messages
conv.add_system_message("You are an experienced web developer.")
conv.add_user_message("Explain closures in JavaScript.")

# Save
mgr.save_conversation(conv, conv.messages)

# Search by topic
web_convs = [c for c in mgr.list_conversations() 
             if c.get('metadata', {}).get('topic') == 'web-development']
```

### Batch operations

```python
# Delete all conversations from a specific day
target_date = "2025-01-20"
old_convs = mgr.search_by_time(start=target_date, end=target_date)

for conv in old_convs:
    mgr.delete_conversation(conv['id'])
    print(f"Deleted: {conv['title']}")
```

### Conversation continuation

```python
# Load and extend an existing conversation
conv = mgr.load_conversation("existing-conversation-id")

if conv:
    # Add new messages
    conv.add_user_message("Can you explain that again?")
    conv.add_assistant_message("Sure! Let me rephrase that...")
    
    # Save updated version
    mgr.save_conversation(conv, conv.messages)
```

## 🧪 Development & Testing

### Run tests
```bash
# All tests
pytest

# Specific test
pytest tests/test_session_manager.py

# With output
pytest -v -s
```

### Run demo
```bash
python examples/basic_usage.py
```

### Project structure
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

## 🗄️ Database Schema

The SQLite database uses the following schema:

```sql
-- Conversations table
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,           -- UUID
    title TEXT,                    -- Conversation title
    created_at TEXT,              -- ISO timestamp
    updated_at TEXT,              -- ISO timestamp  
    metadata TEXT                 -- JSON metadata
);

-- Messages table
CREATE TABLE messages (
    id TEXT PRIMARY KEY,          -- UUID
    conversation_id TEXT,         -- Reference to conversations.id
    role TEXT,                    -- "system", "user", "assistant"
    content TEXT,                 -- Message content
    created_at TEXT,             -- ISO timestamp
    metadata TEXT,               -- JSON metadata
    FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
```

## 🤝 Integration with qv-ollama-sdk

```python
from qv_ollama_sdk.client import OllamaClient
from qv_session_manager import SessionManager

# Initialize clients
ollama = OllamaClient()
session_mgr = SessionManager()

# New conversation
conv = ollama.create_conversation(model="gemma3:1b")
conv.title = "Code Review Session"

# Chat with Ollama
response = ollama.chat(conv, "Explain Clean Code principles to me")
print(response.content)

# Persist session
session_mgr.save_conversation(conv, conv.messages)

# Later: load and continue session
loaded_conv = session_mgr.load_conversation(str(conv.id))
next_response = ollama.chat(loaded_conv, "Which tools do you recommend?")
```

## 📋 Roadmap

- [ ] Advanced search/filter functions (e.g. by metadata)
- [ ] Optional encryption of stored data
- [ ] Export/import of conversations (JSON, CSV)
- [ ] Performance optimizations for large datasets
- [ ] Async support for high-performance applications

## 🐛 Error Handling

```python
try:
    conv = mgr.load_conversation("invalid-id")
    if conv is None:
        print("Conversation not found")
except Exception as e:
    print(f"Error loading: {e}")
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.


## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/quantyverse/qv-session-manager/issues)
- **Documentation**: This README
- **Examples**: See the `examples/` directory
