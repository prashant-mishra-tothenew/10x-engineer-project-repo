"""Test fixtures for PromptLab"""

import pytest
from fastapi.testclient import TestClient
from app.api import app
from app import api as api_module
from app.storage import Storage


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
        "description": "A prompt for AI code review"
    }


@pytest.fixture
def sample_collection_data():
    """Sample collection data for testing."""
    return {
        "name": "Development",
        "description": "Prompts for development tasks"
    }
