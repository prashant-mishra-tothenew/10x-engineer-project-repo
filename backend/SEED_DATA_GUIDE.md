# Seed Data Guide

## Overview

The `seed_data.py` script populates your PromptLab API with sample data for testing and development.

## What It Creates

### 1. Tags (10 tags)
- python
- javascript
- ai
- web
- api
- database
- testing
- devops
- security
- documentation

Each tag has a unique color for visual identification.

### 2. Collections (3 collections)
- Development - For software development tasks
- Writing - For content creation
- AI & Machine Learning - For AI and ML tasks

### 3. Prompts (50 prompts)
- Each prompt is assigned to a random collection
- Each prompt has 1-3 random tags
- Includes realistic titles, descriptions, and content with variables

## How to Use

### Step 1: Start the API Server

```bash
# Terminal 1: Start the backend
cd backend
python main.py

# API will be available at http://localhost:8000
```

### Step 2: Run the Seed Script

```bash
# Terminal 2: Run seed script (make sure you're in the venv)
cd backend
source venv/bin/activate  # Activate virtual environment
python seed_data.py
```

Or run it directly with the venv python:

```bash
cd backend
venv/bin/python seed_data.py
```

### Expected Output

```
🌱 Starting database seeding...

📌 Creating tags...
  ✓ Created tag: python
  ✓ Created tag: javascript
  ✓ Created tag: ai
  ...

✅ Created 10 tags

📁 Creating collections...
  ✓ Created collection: Development
  ✓ Created collection: Writing
  ✓ Created collection: AI & Machine Learning

✅ Created 3 collections

💬 Creating prompts...
  ✓ Created prompt: Code Review Example 1 [tags: python, testing]
  ✓ Created prompt: Bug Finder Example 2 [tags: javascript, api, devops]
  ...

✅ Seeding complete!
   - 10 tags
   - 3 collections
   - 50 prompts
```

## Verify the Data

### Using the API

```bash
# Get all tags
curl http://localhost:8000/tags

# Get all collections
curl http://localhost:8000/collections

# Get all prompts
curl http://localhost:8000/prompts

# Filter prompts by tag
curl http://localhost:8000/prompts?tags=python,ai
```

### Using Interactive Docs

Open http://localhost:8000/docs in your browser to:
- Browse all endpoints
- Test API calls interactively
- See the seeded data

## Clearing Data

Since the storage is in-memory, simply restart the server to clear all data:

```bash
# Stop the server (Ctrl+C)
# Start it again
python main.py

# Data is now empty
```

## Customizing Seed Data

### Add More Tags

Edit the `TAGS` list in `seed_data.py`:

```python
TAGS = [
    {"name": "your-tag", "color": "#hexcolor"},
    # ... more tags
]
```

### Add More Collections

Edit the `collections` list in the `seed_data()` function:

```python
collections = [
    {
        "name": "Your Collection",
        "description": "Description here"
    },
    # ... more collections
]
```

### Change Number of Prompts

Modify the number in the `generate_random_prompts()` call:

```python
# Generate 100 prompts instead of 50
prompts = generate_random_prompts(100, [coll["id"] for coll in created_collections], tag_names)
```

### Customize Prompt Templates

Edit the lists in `generate_random_prompts()`:

```python
titles = [
    "Your Custom Title",
    # ... more titles
]

descriptions = [
    "Your custom description",
    # ... more descriptions
]

contents = [
    "Your custom content with {{variables}}",
    # ... more content templates
]
```

## Troubleshooting

### Error: "Could not connect to API"

**Problem**: The API server is not running.

**Solution**: Start the server first:
```bash
cd backend
python main.py
```

### Error: "Failed to create tag/collection/prompt"

**Problem**: The API might have validation errors or the data format is incorrect.

**Solution**:
1. Check the API logs in Terminal 1
2. Verify the data format matches the Pydantic models
3. Check http://localhost:8000/docs for expected formats

### Tags Not Showing on Prompts

**Problem**: Tags might not be properly associated.

**Solution**:
1. Verify tags were created first (check output)
2. Ensure tag names match exactly (case-sensitive)
3. Check the API response for errors

## Example Use Cases

### Testing Tag Filtering

```bash
# Seed the database
python seed_data.py

# Test filtering by single tag
curl http://localhost:8000/prompts?tags=python

# Test filtering by multiple tags (OR logic)
curl http://localhost:8000/prompts?tags=python,ai
```

### Testing Collection Organization

```bash
# Get all prompts in Development collection
curl http://localhost:8000/prompts?collection_id=<collection-id>
```

### Testing Search with Tags

```bash
# Search prompts and filter by tags
curl "http://localhost:8000/prompts?search=code&tags=python"
```

## Notes

- The script uses `random.choice()` and `random.sample()` so each run creates different data
- Tags are created with the "get-or-create" pattern (won't duplicate if run multiple times)
- Collections and prompts will duplicate if you run the script multiple times without restarting the server
- All data is lost when the server restarts (in-memory storage)

## Next Steps

After seeding:
1. Explore the data at http://localhost:8000/docs
2. Test the tag filtering functionality
3. Try creating new prompts with tags
4. Test the PUT /prompts/{id}/tags endpoint
5. Build the frontend to visualize the tagged prompts
