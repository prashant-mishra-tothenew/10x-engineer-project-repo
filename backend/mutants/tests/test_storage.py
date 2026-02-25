"""Storage layer tests for PromptLab

These tests verify the storage layer operations work correctly.
In Python, this is similar to testing a repository class in Node.js or a model in Laravel.
"""

import pytest
from app.models import Collection, Prompt
from app.storage import Storage


class TestStoragePromptOperations:
    """Tests for prompt storage operations.

    These tests verify CRUD operations on prompts in the storage layer.
    Think of this like testing a database repository or DAO in other frameworks.
    """

    def test_delete_nonexistent_prompt_returns_false(self):
        """Test that deleting a non-existent prompt returns False.

        This tests the edge case where we try to delete a prompt
        that doesn't exist in storage. Should return False, not raise an error.
        """
        storage = Storage()
        result = storage.delete_prompt("nonexistent-id")
        assert result is False

    def test_delete_existing_prompt_returns_true(self):
        """Test that deleting an existing prompt returns True.

        This verifies the happy path for deletion.
        """
        storage = Storage()
        # Create a prompt first
        prompt = Prompt(title="Test Prompt", content="Test content", description="Test description")
        storage.create_prompt(prompt)

        # Now delete it
        result = storage.delete_prompt(prompt.id)
        assert result is True

        # Verify it's gone
        assert storage.get_prompt(prompt.id) is None


class TestStorageCollectionOperations:
    """Tests for collection storage operations.

    These tests verify CRUD operations on collections in the storage layer.
    """

    def test_delete_nonexistent_collection_returns_false(self):
        """Test that deleting a non-existent collection returns False.

        This tests the edge case where we try to delete a collection
        that doesn't exist in storage. Should return False, not raise an error.
        """
        storage = Storage()
        result = storage.delete_collection("nonexistent-id")
        assert result is False

    def test_delete_existing_collection_returns_true(self):
        """Test that deleting an existing collection returns True.

        This verifies the happy path for deletion.
        """
        storage = Storage()
        # Create a collection first
        collection = Collection(name="Test Collection", description="Test description")
        storage.create_collection(collection)

        # Now delete it
        result = storage.delete_collection(collection.id)
        assert result is True

        # Verify it's gone
        assert storage.get_collection(collection.id) is None

    def test_get_prompts_by_collection_returns_empty_list_for_nonexistent_collection(self):
        """Test that getting prompts for a non-existent collection returns empty list.

        This verifies that querying prompts by a collection that doesn't exist
        returns an empty list rather than raising an error.
        """
        storage = Storage()
        prompts = storage.get_prompts_by_collection("nonexistent-id")
        assert prompts == []
        assert isinstance(prompts, list)
