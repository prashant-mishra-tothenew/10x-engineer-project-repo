# Storage Options

PromptLab supports two storage backends with automatic switching for tests.

## Current Implementation

**Development:** Always uses **JSONFileStorage** (data persists)  
**Testing:** Automatically uses **in-memory storage** (clean slate, fast)

---

## 1. JSON File Storage (Default)

**Used for:** Development, Production

**Characteristics:**
- ✅ Data persists across restarts
- ✅ Human-readable JSON format
- ✅ Easy to backup/restore
- ✅ No database setup required
- ❌ Slower than in-memory
- ❌ Not suitable for high traffic

**How it works:**
```python
# In api.py
from app.json_file_storage import JSONFileStorage
storage = JSONFileStorage()
```

**Data location:** 
- `backend/prompts.json` - All prompts
- `backend/collections.json` - All collections

**Features:**
- Automatic save on every operation (create, update, delete)
- Loads existing data on startup
- Thread-safe operations
- Atomic writes (prevents data corruption)

---

## 2. In-Memory Storage (Tests Only)

**Used for:** Automated tests

**Characteristics:**
- ✅ Fast (no disk I/O)
- ✅ Isolated (each test starts clean)
- ✅ No cleanup needed
- ❌ Data lost on restart

**How it works:**
```python
# In tests/conftest.py
@pytest.fixture(autouse=True)
def use_memory_storage():
    # Replace file storage with in-memory for tests
    test_storage = Storage()
    api_module.storage = test_storage
    yield
    # Cleanup happens automatically
```

**Why this approach?**
- Tests run fast (no file I/O)
- Tests are isolated (no shared state)
- No need to clean up test data files
- Production code uses file storage by default

---

## How Tests Override Storage

### The Pattern: Dependency Injection

**Development (api.py):**
```python
# Always uses file storage
from app.json_file_storage import JSONFileStorage
storage = JSONFileStorage()
```

**Tests (conftest.py):**
```python
# Replaces storage with in-memory version
from app import api as api_module
from app.storage import Storage

@pytest.fixture(autouse=True)
def use_memory_storage():
    original_storage = api_module.storage
    api_module.storage = Storage()  # In-memory
    yield
    api_module.storage = original_storage
```

---

## Running the Application

### For Development (File Storage):
```bash
cd backend
python main.py
# Uses JSONFileStorage
# Data saved to prompts.json and collections.json
```

### For Testing (In-Memory):
```bash
cd backend
pytest tests/ -v
# Automatically uses in-memory storage
# No data files created
```

### Seeding Data:
```bash
cd backend
python seed_data.py
# Creates sample prompts and collections
# Saved to prompts.json and collections.json
```

---

## Viewing Persisted Data

If using file storage, you can view the data:

```bash
# Pretty print the prompts file
cat backend/prompts.json | python -m json.tool

# Pretty print the collections file
cat backend/collections.json | python -m json.tool

# Or use jq (if installed)
cat backend/prompts.json | jq
cat backend/collections.json | jq

# Check file sizes
ls -lh backend/*.json
```

**Example data structure:**

`prompts.json`:
```json
[
  {
    "id": "uuid-123",
    "title": "Code Review",
    "content": "Review: {{code}}",
    "description": "A prompt for code review",
    "collection_id": "uuid-456",
    "created_at": "2026-02-12T10:00:00",
    "updated_at": "2026-02-12T10:00:00"
  }
]
```

`collections.json`:
```json
[
  {
    "id": "uuid-456",
    "name": "Development",
    "description": "Development prompts",
    "created_at": "2026-02-12T10:00:00"
  }
]
```

---

## Backup and Restore

### Backup:
```bash
# Copy the data files
cp backend/prompts.json backend/backup_prompts_$(date +%Y%m%d).json
cp backend/collections.json backend/backup_collections_$(date +%Y%m%d).json

# Or use git
git add backend/prompts.json backend/collections.json
git commit -m "Backup data"
```

### Restore:
```bash
# Restore from backup
cp backend/backup_prompts_20260212.json backend/prompts.json
cp backend/backup_collections_20260212.json backend/collections.json

# Or use git
git checkout HEAD -- backend/prompts.json backend/collections.json
```

---

## Comparison Table

| Feature | In-Memory | JSON File | Database |
|---------|-----------|-----------|----------|
| **Speed** | ⚡ Very Fast | 🐢 Slow | 🚀 Fast |
| **Persistence** | ❌ No | ✅ Yes | ✅ Yes |
| **Setup** | ✅ None | ✅ None | ❌ Complex |
| **Scalability** | ❌ Low | ❌ Low | ✅ High |
| **Best for** | Tests | Development | Production |
| **Current use** | Tests only | Development | Not yet |

---

## Troubleshooting

### Tests are slow
**Cause:** Tests might be using file storage  
**Fix:** Check that `conftest.py` has the `use_memory_storage` fixture

### Data not persisting
**Cause:** Using in-memory storage in development  
**Fix:** Check that `api.py` imports `JSONFileStorage`

### File permission errors
**Cause:** No write access to backend directory  
**Fix:** `chmod 755 backend/`

### Corrupted data file
**Cause:** Server crashed during write  
**Fix:** Delete `prompts.json` and `collections.json`, then restart (or restore from backup)

---

## Bonus: Implemented! ✅

This implementation completes TWO Week 1 bonus challenges:

### Bonus #1: Persist Data ✅
> "Try implementing `JSONFileStorage` or `SQLiteStorage` to save data to disk."

**Features implemented:**
- ✅ Automatic persistence to JSON files
- ✅ Loads existing data on startup
- ✅ Thread-safe operations
- ✅ Tests use in-memory storage (no cleanup needed)
- ✅ Easy to backup and restore
- ✅ Human-readable format

### Bonus #2: Better Search ✅
> "Improve the `search` parameter in `GET /prompts` to filter by tags or description, not just title."

**Features implemented:**
- ✅ Search by title
- ✅ Search by description
- ✅ Search by content
- ✅ Case-insensitive matching

**Files:**
- `backend/app/json_file_storage.py` - File storage implementation
- `backend/app/utils.py` - Enhanced search function
- `backend/app/api.py` - Uses file storage by default
- `backend/tests/conftest.py` - Overrides with in-memory for tests
- `backend/seed_data.py` - Populates with sample data
