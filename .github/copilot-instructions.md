# PromptLab AI Coding Instructions

This document guides AI assistants on how to write code for the PromptLab project.

## Project Overview

PromptLab is an AI prompt engineering platform built with Python/FastAPI backend. The developer is transitioning from Node.js/PHP, so explanations should reference those ecosystems when helpful.

## 1. Coding Standards

### Naming Conventions

- **Functions and variables**: `snake_case` (Python standard)
  - Example: `get_prompt()`, `user_id`, `created_at`
  - Like: JavaScript/PHP but with underscores instead of camelCase
  
- **Classes**: `PascalCase`
  - Example: `PromptCreate`, `CollectionResponse`, `StorageManager`
  - Same as: JavaScript classes, PHP classes
  
- **Constants**: `UPPER_SNAKE_CASE`
  - Example: `MAX_CONTENT_LENGTH`, `DEFAULT_SORT_ORDER`
  
- **Private attributes**: Prefix with underscore
  - Example: `_prompts`, `_collections`
  - Like: Private fields in TypeScript/PHP

### Type Hints (Required)

Always include type hints for function parameters and return values:

```python
# Good
def get_prompt(prompt_id: str) -> Prompt | None:
    return storage.get_prompt(prompt_id)

# Bad
def get_prompt(prompt_id):
    return storage.get_prompt(prompt_id)
```

Think of type hints like TypeScript types or PHP type declarations - they're not just documentation, they enable IDE autocomplete and catch errors early.

### Import Organization

Group imports in this order with blank lines between:

```python
# 1. Standard library
from datetime import datetime
from typing import List, Optional

# 2. Third-party packages
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 3. Local imports
from app.models import Prompt, PromptCreate
from app.storage import storage
```

## 2. Preferred Patterns and Conventions

### FastAPI Patterns

- **Dependency Injection**: Use FastAPI's DI system for shared resources
  ```python
  # Storage is a singleton, accessed directly
  @app.get("/prompts/{prompt_id}")
  def get_prompt(prompt_id: str):
      prompt = storage.get_prompt(prompt_id)
  ```

- **Response Models**: Always specify response_model
  ```python
  @app.get("/prompts/{prompt_id}", response_model=PromptResponse)
  def get_prompt(prompt_id: str):
      # FastAPI auto-validates response matches PromptResponse
  ```

- **Status Codes**: Use explicit status codes for non-200 responses
  ```python
  @app.post("/prompts", status_code=201, response_model=PromptResponse)
  @app.delete("/prompts/{prompt_id}", status_code=204)
  ```

### Pydantic Models

Use Pydantic for all data validation (similar to Zod in Node.js or DTOs in PHP):

```python
class PromptCreate(BaseModel):
    title: str
    content: str
    collection_id: str | None = None
    tags: List[str] = []
```

- Separate models for Create/Update/Response operations
- Use `Field()` for validation constraints
- Auto-validation happens at API boundary

### Storage Layer Pattern

- **Singleton pattern**: One global `storage` instance
- **Return None for not found**: Don't raise exceptions in storage layer
- **Simple CRUD operations**: Keep storage logic minimal

```python
# Storage layer returns None
def get_prompt(self, prompt_id: str) -> Prompt | None:
    return self._prompts.get(prompt_id)

# API layer converts to HTTP error
@app.get("/prompts/{prompt_id}")
def get_prompt(prompt_id: str):
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt
```

### Utils Layer Pattern

- **Pure functions only**: No side effects, no state modification
- **Single responsibility**: Each function does one thing
- **Composable**: Functions can be combined

```python
# Good - pure function
def sort_prompts(prompts: List[Prompt], sort_by: str) -> List[Prompt]:
    return sorted(prompts, key=lambda p: getattr(p, sort_by))

# Bad - modifies input
def sort_prompts(prompts: List[Prompt], sort_by: str) -> List[Prompt]:
    prompts.sort(key=lambda p: getattr(p, sort_by))
    return prompts
```

## 3. File Naming and Organization

### File Structure

```
backend/
├── app/
│   ├── __init__.py      # Package marker (minimal content)
│   ├── api.py           # FastAPI routes (like routes/ in Express)
│   ├── models.py        # Pydantic schemas (like types/ in TypeScript)
│   ├── storage.py       # Data layer (like repositories/ in PHP)
│   └── utils.py         # Helper functions (like utils/ in Node.js)
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # pytest fixtures (like jest.setup.js)
│   └── test_api.py      # API tests (like *.test.js)
├── main.py              # Entry point (like index.js or server.php)
└── requirements.txt     # Dependencies (like package.json)
```

### Naming Rules

- Test files: `test_*.py` (pytest convention)
- No `index.py` - Python doesn't use index files like Node.js
- Use `__init__.py` only for package initialization, keep it minimal
- One class per file is not required (unlike Java)

## 4. Error Handling Approach

### API Layer (api.py)

Use `HTTPException` for all API errors:

```python
from fastapi import HTTPException

# 404 - Not Found
if not prompt:
    raise HTTPException(status_code=404, detail="Prompt not found")

# 400 - Bad Request (validation)
if not is_valid_content(content):
    raise HTTPException(status_code=400, detail="Invalid content format")

# 500 - Server Error (unexpected)
try:
    result = risky_operation()
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
```

### Storage Layer (storage.py)

Return `None` for not found, let API layer handle HTTP errors:

```python
# Good
def get_prompt(self, prompt_id: str) -> Prompt | None:
    return self._prompts.get(prompt_id)

# Bad - don't raise HTTP errors in storage
def get_prompt(self, prompt_id: str) -> Prompt:
    if prompt_id not in self._prompts:
        raise HTTPException(status_code=404)
    return self._prompts[prompt_id]
```

### HTTP Status Code Guide

- `200` - Success (GET, PUT)
- `201` - Created (POST)
- `204` - No Content (DELETE)
- `400` - Bad Request (validation failed)
- `404` - Not Found (resource doesn't exist)
- `500` - Server Error (unexpected exception)

## 5. Testing Requirements

### pytest Conventions

```python
# Test file: test_api.py
# Test function naming: test_<what>_<condition>_<expected>

def test_get_prompt_returns_404_when_not_found(client):
    """Test that GET /prompts/{id} returns 404 for non-existent prompt."""
    response = client.get("/prompts/nonexistent-id")
    assert response.status_code == 404
```

### Fixtures (conftest.py)

Use fixtures for reusable test data and setup:

```python
@pytest.fixture(autouse=True)
def clear_storage():
    """Clear storage before each test."""
    storage._prompts.clear()
    storage._collections.clear()
    yield

@pytest.fixture
def sample_prompt():
    """Provide a sample prompt for testing."""
    return {
        "title": "Test Prompt",
        "content": "Hello {{name}}",
        "tags": ["test"]
    }
```

### TestClient Usage

Use FastAPI's TestClient (similar to supertest in Node.js):

```python
from fastapi.testclient import TestClient

def test_create_prompt(client, sample_prompt):
    response = client.post("/prompts", json=sample_prompt)
    assert response.status_code == 201
    assert response.json()["title"] == sample_prompt["title"]
```

### Test Coverage Goals

- All API endpoints must have tests
- Test happy path and error cases
- Use descriptive test names
- One assertion per test when possible

## 6. Python-Specific Guidance

### String Formatting

Prefer f-strings (most readable):

```python
# Good
message = f"Prompt {prompt_id} not found"

# Acceptable
message = "Prompt {} not found".format(prompt_id)

# Avoid
message = "Prompt %s not found" % prompt_id
```

### List Comprehensions

Use when readable, avoid when complex:

```python
# Good - readable
tags = [tag.lower() for tag in prompt.tags]

# Good - with condition
active = [p for p in prompts if p.is_active]

# Bad - too complex, use regular loop
result = [process(x) for x in items if x.valid and x.count > 5 and not x.archived]
```

### Type Hints with Union

Use `|` for union types (Python 3.10+):

```python
# Good (Python 3.10+)
def get_prompt(prompt_id: str) -> Prompt | None:
    pass

# Old style (still works)
from typing import Optional
def get_prompt(prompt_id: str) -> Optional[Prompt]:
    pass
```

### Datetime Handling

Always use UTC for timestamps:

```python
from datetime import datetime

# Good
created_at = datetime.utcnow()

# Bad - timezone-dependent
created_at = datetime.now()
```

### ID Generation

Use UUID4 for IDs (not auto-increment):

```python
import uuid

# Good
prompt_id = str(uuid.uuid4())

# Bad - not unique across distributed systems
prompt_id = len(self._prompts) + 1
```

### Dictionary Operations

Use `.get()` for safe access:

```python
# Good - returns None if not found
prompt = self._prompts.get(prompt_id)

# Bad - raises KeyError if not found
prompt = self._prompts[prompt_id]
```

## 7. Node.js/PHP Equivalents

Quick reference for the developer:

| Python | Node.js | PHP |
|--------|---------|-----|
| `def function():` | `function() {}` | `function() {}` |
| `@decorator` | `@decorator` (TS) | `#[Attribute]` |
| `Type hints` | TypeScript types | Type declarations |
| `**kwargs` | `...spread` | `...$args` |
| `Pydantic` | Zod/Joi | DTOs/Validation |
| `FastAPI` | Express.js | Laravel routes |
| `pip/venv` | npm/node_modules | composer/vendor |
| `pytest` | Jest/Mocha | PHPUnit |
| `None` | `null` | `null` |
| `True/False` | `true/false` | `true/false` |
| `snake_case` | `camelCase` | `camelCase` |

## 8. Common Pitfalls to Avoid

### Don't Modify Function Arguments

```python
# Bad - modifies input
def add_tag(prompt: Prompt, tag: str):
    prompt.tags.append(tag)
    return prompt

# Good - returns new object
def add_tag(prompt: Prompt, tag: str) -> Prompt:
    return prompt.copy(update={"tags": prompt.tags + [tag]})
```

### Don't Use Mutable Default Arguments

```python
# Bad - list is shared across calls
def create_prompt(tags=[]):
    pass

# Good
def create_prompt(tags: List[str] | None = None):
    if tags is None:
        tags = []
```

### Don't Forget to Update Timestamps

```python
# Update operations should update updated_at
def update_prompt(self, prompt_id: str, updates: dict):
    prompt = self._prompts[prompt_id]
    for key, value in updates.items():
        setattr(prompt, key, value)
    prompt.updated_at = datetime.utcnow()  # Don't forget!
```

### Don't Mix Validation Layers

- Pydantic validates at API boundary
- Storage layer assumes valid data
- Don't duplicate validation logic

## 9. Documentation Standards

### Docstrings

Use for public functions (Google style):

```python
def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or content.
    
    Args:
        prompts: List of prompts to search
        query: Search query string
        
    Returns:
        List of prompts matching the query
    """
    query_lower = query.lower()
    return [p for p in prompts if query_lower in p.title.lower() 
            or query_lower in p.content.lower()]
```

### Inline Comments

Use sparingly for complex logic:

```python
# Extract variables from template (e.g., {{name}} -> ["name"])
variables = re.findall(r'\{\{(\w+)\}\}', content)
```

## 10. Project-Specific Rules

### Template Variables

Use `{{variable}}` syntax (double curly braces):

```python
content = "Hello {{name}}, welcome to {{place}}"
# Extract: ["name", "place"]
```

### Sorting

Default sort order is descending (newest first):

```python
prompts = sorted(prompts, key=lambda p: p.created_at, reverse=True)
```

### Collection Relationships

- Prompts can belong to one collection
- Collections can have many prompts
- Deleting a collection should handle orphaned prompts

### Known Technical Debt

The codebase intentionally has bugs for learning purposes:
- Some endpoints return wrong status codes
- Timestamp updates may be missing
- Sorting may be backwards
- Orphaned relationships exist

When fixing bugs, explain what was wrong and why the fix is correct.

---

## Summary

Write Python code that is:
- **Typed**: Always use type hints
- **Validated**: Use Pydantic models
- **Tested**: Write pytest tests
- **Clean**: Follow Python conventions
- **Documented**: Add docstrings for public APIs
- **Explainable**: Remember the developer is learning Python

When in doubt, prefer explicit over implicit, and readability over cleverness.
