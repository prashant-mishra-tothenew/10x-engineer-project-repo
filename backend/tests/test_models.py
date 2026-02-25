"""Model tests for PromptLab

These tests verify that Pydantic models work correctly.
In Python, Pydantic models are similar to:
- Joi/Zod schemas in Node.js (validation)
- DTOs (Data Transfer Objects) in PHP/Laravel
- TypeScript interfaces with runtime validation

Pydantic automatically validates data and provides serialization.
"""

from datetime import datetime

import pytest
from app.models import (
    Collection,
    CollectionCreate,
    CollectionList,
    HealthResponse,
    Prompt,
    PromptCreate,
    PromptList,
    PromptPatch,
    PromptUpdate,
    get_current_time,
)
from pydantic import ValidationError


class TestPromptModel:
    """Tests for the Prompt model.

    The Prompt model is the main data structure for storing prompt templates.
    It includes validation rules and auto-generated fields (id, timestamps).
    """

    def test_prompt_creation_with_valid_data(self):
        """Test that a Prompt can be created with valid data.

        This tests the happy path - all required fields provided.
        Pydantic will auto-generate id and timestamps.
        """
        prompt = Prompt(title="Test Prompt", content="Test content for the prompt", description="A test description")

        assert prompt.title == "Test Prompt"
        assert prompt.content == "Test content for the prompt"
        assert prompt.description == "A test description"
        assert prompt.id is not None  # Auto-generated
        assert prompt.created_at is not None  # Auto-generated
        assert prompt.updated_at is not None  # Auto-generated
        assert prompt.collection_id is None  # Optional field, defaults to None

    def test_prompt_auto_generates_id(self):
        """Test that Prompt automatically generates a unique ID.

        The id field uses uuid4() as a default factory.
        Similar to auto-increment IDs in databases, but using UUIDs.
        """
        prompt1 = Prompt(title="Prompt 1", content="Content 1")
        prompt2 = Prompt(title="Prompt 2", content="Content 2")

        assert prompt1.id != prompt2.id
        assert len(prompt1.id) > 0
        assert isinstance(prompt1.id, str)

    def test_prompt_auto_generates_timestamps(self):
        """Test that Prompt automatically generates created_at and updated_at.

        Both timestamps should be set to the current time when created.
        Uses get_current_time() which returns UTC datetime object.
        """
        prompt = Prompt(title="Test", content="Content")

        assert prompt.created_at is not None
        assert prompt.updated_at is not None
        assert isinstance(prompt.created_at, datetime)
        assert isinstance(prompt.updated_at, datetime)

    def test_prompt_with_collection_id(self):
        """Test that Prompt can be created with a collection_id.

        collection_id is optional and can be set to link a prompt to a collection.
        """
        prompt = Prompt(title="Test", content="Content", collection_id="collection-123")

        assert prompt.collection_id == "collection-123"

    def test_prompt_validates_title_not_empty(self):
        """Test that Prompt rejects empty title.

        Pydantic's min_length=1 validation ensures title is not empty.
        When validation fails, Pydantic raises ValidationError.
        """
        with pytest.raises(ValidationError) as exc_info:
            Prompt(title="", content="Content")

        # Check that the error is about the title field
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)

    def test_prompt_validates_content_not_empty(self):
        """Test that Prompt rejects empty content.

        Similar to title validation, content must have at least 1 character.
        """
        with pytest.raises(ValidationError) as exc_info:
            Prompt(title="Title", content="")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("content",) for error in errors)

    def test_prompt_validates_title_max_length(self):
        """Test that Prompt rejects title exceeding 200 characters.

        The max_length=200 constraint is enforced by Pydantic.
        """
        with pytest.raises(ValidationError) as exc_info:
            Prompt(title="x" * 201, content="Content")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)

    def test_prompt_validates_description_max_length(self):
        """Test that Prompt rejects description exceeding 500 characters.

        Description is optional but has a max_length=500 constraint.
        """
        with pytest.raises(ValidationError) as exc_info:
            Prompt(title="Title", content="Content", description="x" * 501)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("description",) for error in errors)

    def test_prompt_serialization_to_dict(self):
        """Test that Prompt can be serialized to a dictionary.

        Pydantic's model_dump() converts the model to a dict.
        Similar to JSON.stringify() in Node.js or toArray() in Laravel.
        """
        prompt = Prompt(title="Test", content="Content", description="Description")

        data = prompt.model_dump()

        assert isinstance(data, dict)
        assert data["title"] == "Test"
        assert data["content"] == "Content"
        assert data["description"] == "Description"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert "collection_id" in data


class TestPromptCreateModel:
    """Tests for the PromptCreate model.

    PromptCreate is used for API requests to create new prompts.
    It only includes fields that the user can provide (no id, no timestamps).
    """

    def test_prompt_create_with_required_fields_only(self):
        """Test that PromptCreate works with just required fields.

        Only title and content are required. Description and collection_id are optional.
        """
        data = PromptCreate(title="Test", content="Content")

        assert data.title == "Test"
        assert data.content == "Content"
        assert data.description is None
        assert data.collection_id is None

    def test_prompt_create_with_all_fields(self):
        """Test that PromptCreate works with all fields provided."""
        data = PromptCreate(title="Test", content="Content", description="Description", collection_id="collection-123")

        assert data.title == "Test"
        assert data.content == "Content"
        assert data.description == "Description"
        assert data.collection_id == "collection-123"

    def test_prompt_create_validates_required_fields(self):
        """Test that PromptCreate requires title and content.

        Missing required fields should raise ValidationError.
        """
        with pytest.raises(ValidationError):
            PromptCreate(title="Test")  # Missing content

        with pytest.raises(ValidationError):
            PromptCreate(content="Content")  # Missing title


class TestPromptUpdateModel:
    """Tests for the PromptUpdate model.

    PromptUpdate is used for PUT requests (full replacement).
    All fields are required because PUT replaces the entire resource.
    """

    def test_prompt_update_requires_all_fields(self):
        """Test that PromptUpdate requires all fields.

        PUT is a full replacement, so all fields must be provided.
        """
        data = PromptUpdate(
            title="Updated Title", content="Updated Content", description="Updated Description", collection_id="collection-123"
        )

        assert data.title == "Updated Title"
        assert data.content == "Updated Content"
        assert data.description == "Updated Description"
        assert data.collection_id == "collection-123"

    def test_prompt_update_allows_none_for_optional_fields(self):
        """Test that PromptUpdate allows None for optional fields.

        Description and collection_id can be explicitly set to None.
        """
        data = PromptUpdate(title="Title", content="Content", description=None, collection_id=None)

        assert data.description is None
        assert data.collection_id is None


class TestPromptPatchModel:
    """Tests for the PromptPatch model.

    PromptPatch is used for PATCH requests (partial updates).
    All fields are optional - only provided fields will be updated.
    """

    def test_prompt_patch_with_single_field(self):
        """Test that PromptPatch works with just one field.

        PATCH allows updating only specific fields.
        """
        data = PromptPatch(title="New Title")

        assert data.title == "New Title"
        # Other fields should not be set (will be excluded when serializing)

    def test_prompt_patch_with_multiple_fields(self):
        """Test that PromptPatch works with multiple fields."""
        data = PromptPatch(title="New Title", content="New Content")

        assert data.title == "New Title"
        assert data.content == "New Content"

    def test_prompt_patch_excludes_unset_fields(self):
        """Test that PromptPatch only includes fields that were explicitly set.

        This is important for PATCH - we only want to update provided fields.
        model_dump(exclude_unset=True) returns only the fields that were set.
        """
        data = PromptPatch(title="New Title")

        # Only title should be in the dict when exclude_unset=True
        dumped = data.model_dump(exclude_unset=True)
        assert "title" in dumped
        assert "content" not in dumped
        assert "description" not in dumped
        assert "collection_id" not in dumped


class TestCollectionModel:
    """Tests for the Collection model.

    Collections are used to organize prompts into groups.
    Similar to folders or categories in other systems.
    """

    def test_collection_creation_with_valid_data(self):
        """Test that a Collection can be created with valid data."""
        collection = Collection(name="Test Collection", description="A test collection")

        assert collection.name == "Test Collection"
        assert collection.description == "A test collection"
        assert collection.id is not None  # Auto-generated
        assert collection.created_at is not None  # Auto-generated

    def test_collection_auto_generates_id(self):
        """Test that Collection automatically generates a unique ID."""
        col1 = Collection(name="Collection 1")
        col2 = Collection(name="Collection 2")

        assert col1.id != col2.id
        assert len(col1.id) > 0

    def test_collection_auto_generates_timestamp(self):
        """Test that Collection automatically generates created_at timestamp."""
        collection = Collection(name="Test")

        assert collection.created_at is not None
        assert isinstance(collection.created_at, datetime)

    def test_collection_validates_name_not_empty(self):
        """Test that Collection rejects empty name."""
        with pytest.raises(ValidationError) as exc_info:
            Collection(name="")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("name",) for error in errors)

    def test_collection_validates_name_max_length(self):
        """Test that Collection rejects name exceeding 100 characters."""
        with pytest.raises(ValidationError) as exc_info:
            Collection(name="x" * 101)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("name",) for error in errors)

    def test_collection_validates_description_max_length(self):
        """Test that Collection rejects description exceeding 500 characters."""
        with pytest.raises(ValidationError) as exc_info:
            Collection(name="Test", description="x" * 501)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("description",) for error in errors)

    def test_collection_description_is_optional(self):
        """Test that Collection can be created without description."""
        collection = Collection(name="Test")

        assert collection.name == "Test"
        assert collection.description is None


class TestCollectionCreateModel:
    """Tests for the CollectionCreate model.

    CollectionCreate is used for API requests to create new collections.
    """

    def test_collection_create_with_required_fields_only(self):
        """Test that CollectionCreate works with just the name."""
        data = CollectionCreate(name="Test Collection")

        assert data.name == "Test Collection"
        assert data.description is None

    def test_collection_create_with_all_fields(self):
        """Test that CollectionCreate works with all fields."""
        data = CollectionCreate(name="Test Collection", description="Test Description")

        assert data.name == "Test Collection"
        assert data.description == "Test Description"


class TestResponseModels:
    """Tests for response wrapper models.

    These models wrap API responses with metadata like total counts.
    """

    def test_prompt_list_model(self):
        """Test that PromptList wraps a list of prompts with total count."""
        prompt1 = Prompt(title="Prompt 1", content="Content 1")
        prompt2 = Prompt(title="Prompt 2", content="Content 2")

        prompt_list = PromptList(prompts=[prompt1, prompt2], total=2)

        assert len(prompt_list.prompts) == 2
        assert prompt_list.total == 2
        assert prompt_list.prompts[0].title == "Prompt 1"
        assert prompt_list.prompts[1].title == "Prompt 2"

    def test_prompt_list_with_empty_list(self):
        """Test that PromptList works with empty list."""
        prompt_list = PromptList(prompts=[], total=0)

        assert prompt_list.prompts == []
        assert prompt_list.total == 0

    def test_collection_list_model(self):
        """Test that CollectionList wraps a list of collections with total count."""
        col1 = Collection(name="Collection 1")
        col2 = Collection(name="Collection 2")

        collection_list = CollectionList(collections=[col1, col2], total=2)

        assert len(collection_list.collections) == 2
        assert collection_list.total == 2
        assert collection_list.collections[0].name == "Collection 1"

    def test_health_response_model(self):
        """Test that HealthResponse contains status and version."""
        health = HealthResponse(status="healthy", version="1.0.0")

        assert health.status == "healthy"
        assert health.version == "1.0.0"


class TestUtilityFunctions:
    """Tests for utility functions in models module."""

    def test_get_current_time_returns_datetime(self):
        """Test that get_current_time() returns a datetime object.

        This function is used as the default factory for timestamp fields.
        In Python, datetime objects are similar to Date objects in JavaScript.
        """
        timestamp = get_current_time()

        assert isinstance(timestamp, datetime)
        assert timestamp is not None

    def test_get_current_time_returns_utc_time(self):
        """Test that get_current_time() returns UTC time.

        The timestamp should be timezone-aware or in UTC.
        """
        timestamp = get_current_time()

        # Verify it's a datetime object
        assert isinstance(timestamp, datetime)
        # Should be recent (within last minute)
        now = datetime.utcnow()
        time_diff = abs((now - timestamp).total_seconds())
        assert time_diff < 60  # Within 60 seconds

    def test_get_current_time_returns_different_values(self):
        """Test that get_current_time() returns current time (not cached).

        Each call should return a fresh timestamp.
        """
        import time

        time1 = get_current_time()
        time.sleep(0.01)  # Sleep 10 milliseconds
        time2 = get_current_time()

        # Both should be datetime objects
        assert isinstance(time1, datetime)
        assert isinstance(time2, datetime)
        # time2 should be after time1 (or equal if very fast)
        assert time2 >= time1
