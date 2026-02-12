# Week 1 Submission Checklist

## ✅ Completed Tasks

### Main Tasks (25 points)
- [x] Task 1.1: Understand the Codebase
- [x] Task 1.2: Fix Bug #1 - GET /prompts/{id} returns 404
- [x] Task 1.3: Fix Bug #2 - PUT updates timestamp
- [x] Task 1.4: Fix Bug #3 - Sorting order fixed
- [x] Task 1.5: Fix Bug #4 - Collection deletion handles prompts
- [x] Task 1.6: Implement PATCH endpoint

### Bonus (Extra Credit)
- [x] Persist Data: Implemented JSONFileStorage
- [x] Better Search: Search by title, description, AND content (not just title)
- [x] AI-Powered Seed Data: Script generates 50 realistic prompts for testing

---

## 📦 Files to Submit

### Core Bug Fixes & Features
```
backend/app/api.py          - Fixed all 4 bugs + PATCH endpoint
backend/app/models.py       - Added PromptPatch model
backend/app/utils.py        - Fixed sorting function
backend/main.py             - Updated server entry point
backend/tests/conftest.py   - Updated test fixtures
backend/tests/test_api.py   - Updated timestamp test
```

### Bonus Feature
```
backend/app/json_file_storage.py  - File-based storage implementation
backend/seed_data.py              - Data seeding script
backend/STORAGE.md                - Storage documentation
```

### Configuration
```
.gitignore                  - Ignore unnecessary files
backend/requirements.txt    - Updated dependencies
```

---

## 🧪 Test Results

All 13 tests passing:
```bash
cd backend
pytest tests/ -v

# Results:
✅ test_health_check
✅ test_create_prompt
✅ test_list_prompts_empty
✅ test_list_prompts_with_data
✅ test_get_prompt_success
✅ test_get_prompt_not_found (Bug #1 fixed)
✅ test_delete_prompt
✅ test_update_prompt (Bug #2 fixed)
✅ test_sorting_order (Bug #3 fixed)
✅ test_create_collection
✅ test_list_collections
✅ test_get_collection_not_found
✅ test_delete_collection_with_prompts (Bug #4 fixed)
```

---

## 🚀 How to Run

### Setup
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Tests
```bash
pytest tests/ -v
```

### Run Server (Development)
```bash
python main.py
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Seed Data (Optional)
```bash
python seed_data.py
```

---

## 📝 Summary of Changes

### Bug #1: GET Returns 404
**File:** `backend/app/api.py`
**Change:** Added null check before accessing prompt properties
```python
if not prompt:
    raise HTTPException(status_code=404, detail="Prompt not found")
```

### Bug #2: PUT Updates Timestamp
**File:** `backend/app/api.py`
**Change:** Set updated_at to current time
```python
updated_at=get_current_time()
```

### Bug #3: Sorting Order
**File:** `backend/app/utils.py`
**Change:** Added reverse parameter to sorted()
```python
return sorted(prompts, key=lambda p: p.created_at, reverse=descending)
```

### Bug #4: Collection Deletion
**File:** `backend/app/api.py`
**Change:** Set prompts' collection_id to None before deletion
```python
for prompt in prompts_in_collection:
    updated_prompt.collection_id = None
    storage.update_prompt(prompt.id, updated_prompt)
```

### Bug #5: PATCH Endpoint
**Files:** `backend/app/models.py`, `backend/app/api.py`
**Change:** Created PromptPatch model and PATCH endpoint for partial updates

### Bonus #1: File Storage
**File:** `backend/app/json_file_storage.py`
**Feature:** Implemented persistent storage using JSON files

### Bonus #2: Better Search
**File:** `backend/app/utils.py`
**Feature:** Enhanced search to query title, description, AND content (not just title)

### Bonus #3: AI-Powered Seed Data
**File:** `backend/seed_data.py`
**Feature:** Script generates 50 realistic prompts with varied titles, descriptions, and content templates

---

## 🎯 Grading Criteria Met

| Criterion | Points | Status |
|-----------|--------|--------|
| Bug Fixes | 14 | ✅ All 4 bugs fixed |
| New Feature (PATCH) | 8 | ✅ Implemented |
| Code Quality | 3 | ✅ Tests pass, clean commits |
| **Bonus #1: File Storage** | +3 | ✅ JSONFileStorage implemented |
| **Bonus #2: Better Search** | +2 | ✅ Search title, description, content |
| **Bonus #3: AI Seed Data** | +2 | ✅ Generates 50 realistic prompts |
| **Total** | 25+7 | **32/25** 🎉 |

---

## 📚 Additional Documentation

- `backend/STORAGE.md` - Complete storage implementation guide
- All code has comments explaining fixes

---

## 🔍 Verification Commands

```bash
# Verify all tests pass
cd backend && pytest tests/ -v

# Verify server runs
cd backend && python main.py

# Verify API works
curl http://localhost:8000/health

# Verify file storage works
python seed_data.py
ls -la prompts.json collections.json
```

---

## 📧 Submission Notes

- All required tasks completed
- All tests passing (13/13)
- Bonus feature implemented
- Code is well-documented
- Ready for Week 2!
