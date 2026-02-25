"""Test fixtures for PromptLab"""

import time

import pytest
from app import api as api_module
from app.api import app
from app.storage import Storage
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def use_memory_storage():
    """Override file storage with in-memory storage for tests.

    This fixture runs automatically before each test and:
    1. Replaces the file storage with in-memory storage
    2. Clears the storage
    3. Restores original storage after test
    """
    # Save original storage
    original_storage = api_module.storage

    # Replace with in-memory storage
    test_storage = Storage()
    api_module.storage = test_storage

    # Clear storage before test
    test_storage.clear()

    yield test_storage

    # Clear storage after test
    test_storage.clear()

    # Restore original storage
    api_module.storage = original_storage


@pytest.fixture
def sample_prompt_data():
    """Sample prompt data for testing."""
    return {
        "title": "Code Review Prompt",
        "content": "Review the following code and provide feedback:\n\n{{code}}",
        "description": "A prompt for AI code review",
    }


@pytest.fixture
def sample_collection_data():
    """Sample collection data for testing."""
    return {"name": "Development", "description": "Prompts for development tasks"}


# ============== Enhanced Fixtures for Edge Cases ==============


@pytest.fixture
def prompt_with_special_chars():
    """Prompt data with special characters for testing edge cases."""
    return {
        "title": "Special !@#$%^&*() Characters",
        "content": "Content with special chars: <html>, {json}, [array], & ampersand",
        "description": "Testing special characters: quotes \"double\" and 'single'",
    }


@pytest.fixture
def prompt_with_unicode():
    """Prompt data with Unicode characters for testing internationalization."""
    return {
        "title": "Unicode Test: 你好世界 🌍 Привет",
        "content": "Content with emoji 🚀 and symbols: ™ © ® € £ ¥",
        "description": "Testing Unicode: café, naïve, Zürich",
    }


@pytest.fixture
def prompt_with_template_vars():
    """Prompt data with template variables for testing variable extraction."""
    return {
        "title": "Template Variables Test",
        "content": "Hello {{name}}, your order {{order_id}} is ready. Total: {{total}}",
        "description": "Prompt with multiple template variables",
    }


@pytest.fixture
def max_length_prompt():
    """Prompt data with maximum allowed field lengths for boundary testing."""
    return {
        "title": "x" * 200,  # Max title length
        "content": "y" * 1000,  # Long content
        "description": "z" * 500,  # Max description length
    }


@pytest.fixture
def min_length_prompt():
    """Prompt data with minimum valid field lengths for boundary testing."""
    return {
        "title": "A",  # Min title length (1 char)
        "content": "B",  # Min content length (1 char)
        "description": "C",  # Min description length (1 char)
    }


@pytest.fixture
def created_prompt(client, sample_prompt_data):
    """Create a prompt and return its data.

    This is a dependent fixture that creates a prompt in the API
    and returns the response data. Useful when tests need an existing prompt.
    """
    response = client.post("/prompts", json=sample_prompt_data)
    return response.json()


@pytest.fixture
def created_collection(client, sample_collection_data):
    """Create a collection and return its data.

    This is a dependent fixture that creates a collection in the API
    and returns the response data. Useful when tests need an existing collection.
    """
    response = client.post("/collections", json=sample_collection_data)
    return response.json()


@pytest.fixture
def multiple_prompts(client):
    """Create multiple prompts with different timestamps for testing sorting/filtering.

    Returns a list of created prompt data in the order they were created.
    """
    prompts = []

    # Create first prompt
    prompt1 = {"title": "First Prompt", "content": "This is the first prompt content"}
    response1 = client.post("/prompts", json=prompt1)
    prompts.append(response1.json())

    # Small delay to ensure different timestamps
    time.sleep(0.1)

    # Create second prompt
    prompt2 = {"title": "Second Prompt", "content": "This is the second prompt content"}
    response2 = client.post("/prompts", json=prompt2)
    prompts.append(response2.json())

    # Small delay
    time.sleep(0.1)

    # Create third prompt
    prompt3 = {"title": "Third Prompt", "content": "This is the third prompt content"}
    response3 = client.post("/prompts", json=prompt3)
    prompts.append(response3.json())

    return prompts


# ============== Helper Functions ==============


def assert_prompt_matches(response_data: dict, expected_data: dict):
    """Verify prompt response matches expected data.

    This helper checks that the response contains all expected fields
    and that the values match what was submitted.

    Args:
        response_data: The JSON response from the API
        expected_data: The data we expect to see
    """
    assert response_data["title"] == expected_data["title"]
    assert response_data["content"] == expected_data["content"]

    # Check optional description field
    if "description" in expected_data:
        assert response_data["description"] == expected_data["description"]

    # Check optional collection_id field
    if "collection_id" in expected_data:
        assert response_data["collection_id"] == expected_data["collection_id"]


def assert_has_required_fields(data: dict, fields: list):
    """Verify response has all required fields.

    Args:
        data: The response data dictionary
        fields: List of field names that must be present
    """
    for field in fields:
        assert field in data, f"Missing required field: {field}"


def create_prompt_with_collection(client, collection_id: str) -> dict:
    """Helper to create a prompt associated with a collection.

    Args:
        client: The TestClient instance
        collection_id: The ID of the collection to associate with

    Returns:
        dict: The created prompt data
    """
    prompt_data = {
        "title": "Prompt in Collection",
        "content": "This prompt belongs to a collection",
        "collection_id": collection_id,
    }
    response = client.post("/prompts", json=prompt_data)
    return response.json()


def wait_for_timestamp_change():
    """Small delay to ensure timestamps differ.

    Needed because datetime resolution might be too fast for tests
    that verify timestamp changes (like update operations).
    """
    time.sleep(0.1)
