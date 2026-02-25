"""Tests for tagging system

These tests verify the tagging functionality works correctly.
Tags allow users to categorize and organize prompts flexibly.
"""

from datetime import datetime

import pytest
from app.models import Tag, TagCreate
from pydantic import ValidationError


class TestTagModel:
    """Tests for Tag model validation and creation.

    Similar to testing Joi/Zod schemas in Node.js or DTOs in PHP.
    """

    def test_tag_creation_with_valid_name(self):
        """Test that a Tag can be created with a valid name."""
        tag = Tag(name="python")

        assert tag.name == "python"
        assert tag.tag_id is not None
        assert tag.created_at is not None
        assert isinstance(tag.created_at, datetime)

    def test_tag_auto_generates_id(self):
        """Test that Tag automatically generates a unique ID."""
        tag1 = Tag(name="python")
        tag2 = Tag(name="javascript")

        assert tag1.tag_id != tag2.tag_id
        assert len(tag1.tag_id) > 0

    def test_tag_validates_name_not_empty(self):
        """Test that Tag rejects empty name."""
        with pytest.raises(ValidationError) as exc_info:
            Tag(name="")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("name",) for error in errors)

    def test_tag_validates_name_max_length(self):
        """Test that Tag rejects name exceeding 50 characters."""
        with pytest.raises(ValidationError) as exc_info:
            Tag(name="x" * 51)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("name",) for error in errors)

    def test_tag_name_is_case_sensitive(self):
        """Test that tag names preserve case."""
        tag = Tag(name="Python")
        assert tag.name == "Python"


class TestTagCreateModel:
    """Tests for TagCreate model."""

    def test_tag_create_with_valid_name(self):
        """Test that TagCreate works with valid name."""
        data = TagCreate(name="python")
        assert data.name == "python"

    def test_tag_create_validates_required_fields(self):
        """Test that TagCreate requires name field."""
        with pytest.raises(ValidationError):
            TagCreate()


class TestTagStorage:
    """Tests for tag storage operations.

    These tests verify CRUD operations on tags in the storage layer.
    Similar to testing a repository class in Node.js or a model in Laravel.
    """

    def test_create_tag_stores_in_storage(self):
        """Test that creating a tag stores it in storage."""
        from app.models import Tag
        from app.storage import Storage

        storage = Storage()
        tag = Tag(name="python")

        result = storage.create_tag(tag)

        assert result.tag_id == tag.tag_id
        assert result.name == "python"

    def test_get_tag_by_id_returns_tag(self):
        """Test that getting a tag by ID returns the correct tag."""
        from app.models import Tag
        from app.storage import Storage

        storage = Storage()
        tag = Tag(name="python")
        storage.create_tag(tag)

        result = storage.get_tag(tag.tag_id)

        assert result is not None
        assert result.tag_id == tag.tag_id
        assert result.name == "python"

    def test_get_tag_by_nonexistent_id_returns_none(self):
        """Test that getting a non-existent tag returns None."""
        from app.storage import Storage

        storage = Storage()
        result = storage.get_tag("nonexistent-id")

        assert result is None

    def test_get_tag_by_name_returns_tag(self):
        """Test that getting a tag by name returns the correct tag."""
        from app.models import Tag
        from app.storage import Storage

        storage = Storage()
        tag = Tag(name="python")
        storage.create_tag(tag)

        result = storage.get_tag_by_name("python")

        assert result is not None
        assert result.name == "python"

    def test_get_tag_by_name_is_case_sensitive(self):
        """Test that tag name lookup is case-sensitive."""
        from app.models import Tag
        from app.storage import Storage

        storage = Storage()
        tag = Tag(name="Python")
        storage.create_tag(tag)

        result_exact = storage.get_tag_by_name("Python")
        result_lower = storage.get_tag_by_name("python")

        assert result_exact is not None
        assert result_lower is None

    def test_get_all_tags_returns_all_tags(self):
        """Test that getting all tags returns complete list."""
        from app.models import Tag
        from app.storage import Storage

        storage = Storage()
        tag1 = Tag(name="python")
        tag2 = Tag(name="javascript")
        tag3 = Tag(name="ai")

        storage.create_tag(tag1)
        storage.create_tag(tag2)
        storage.create_tag(tag3)

        result = storage.get_all_tags()

        assert len(result) == 3
        tag_names = {t.name for t in result}
        assert "python" in tag_names
        assert "javascript" in tag_names
        assert "ai" in tag_names

    def test_get_all_tags_returns_empty_list_when_no_tags(self):
        """Test that getting all tags returns empty list initially."""
        from app.storage import Storage

        storage = Storage()
        result = storage.get_all_tags()

        assert result == []


class TestTagAPI:
    """Tests for tag API endpoints.

    These tests verify the REST API for tags works correctly.
    Similar to testing Express.js routes or Laravel controllers.
    """

    def test_create_tag_returns_201(self, client):
        """Test that creating a tag returns 201 Created status."""
        tag_data = {"name": "python"}

        response = client.post("/tags", json=tag_data)

        assert response.status_code == 201

    def test_create_tag_returns_tag_with_id(self, client):
        """Test that creating a tag returns the tag with generated ID."""
        tag_data = {"name": "python"}

        response = client.post("/tags", json=tag_data)
        data = response.json()

        assert "tag_id" in data
        assert data["name"] == "python"
        assert "created_at" in data

    def test_create_duplicate_tag_returns_existing_tag(self, client):
        """Test that creating a duplicate tag returns the existing tag.

        Tags are unique by name. If a tag with the same name exists,
        return the existing tag instead of creating a duplicate.
        """
        tag_data = {"name": "python"}

        # Create first time
        response1 = client.post("/tags", json=tag_data)
        data1 = response1.json()

        # Create again with same name
        response2 = client.post("/tags", json=tag_data)
        data2 = response2.json()

        # Should return the same tag
        assert response2.status_code == 200
        assert data2["tag_id"] == data1["tag_id"]
        assert data2["name"] == "python"

    def test_create_tag_with_empty_name_returns_422(self, client):
        """Test that creating a tag with empty name returns 422."""
        tag_data = {"name": ""}

        response = client.post("/tags", json=tag_data)

        assert response.status_code == 422

    def test_get_all_tags_returns_empty_list_initially(self, client):
        """Test that getting all tags returns empty list initially."""
        response = client.get("/tags")

        assert response.status_code == 200
        data = response.json()
        assert data["tags"] == []
        assert data["total"] == 0

    def test_get_all_tags_returns_all_created_tags(self, client):
        """Test that getting all tags returns all created tags."""
        # Create multiple tags
        client.post("/tags", json={"name": "python"})
        client.post("/tags", json={"name": "javascript"})
        client.post("/tags", json={"name": "ai"})

        response = client.get("/tags")
        data = response.json()

        assert response.status_code == 200
        assert data["total"] == 3
        tag_names = {t["name"] for t in data["tags"]}
        assert "python" in tag_names
        assert "javascript" in tag_names
        assert "ai" in tag_names

    def test_get_tag_by_id_returns_200(self, client):
        """Test that getting a tag by ID returns 200."""
        # Create a tag first
        create_response = client.post("/tags", json={"name": "python"})
        tag_id = create_response.json()["tag_id"]

        response = client.get(f"/tags/{tag_id}")

        assert response.status_code == 200

    def test_get_tag_by_id_returns_correct_tag(self, client):
        """Test that getting a tag by ID returns the correct tag."""
        # Create a tag first
        create_response = client.post("/tags", json={"name": "python"})
        tag_id = create_response.json()["tag_id"]

        response = client.get(f"/tags/{tag_id}")
        data = response.json()

        assert data["tag_id"] == tag_id
        assert data["name"] == "python"

    def test_get_tag_by_nonexistent_id_returns_404(self, client):
        """Test that getting a non-existent tag returns 404."""
        response = client.get("/tags/nonexistent-id")

        assert response.status_code == 404


class TestPromptWithTags:
    """Test suite for prompts with tags field.

    Tests that prompts can be created and updated with tags.
    """

    def test_create_prompt_with_tags_returns_201(self, client):
        """Test that creating a prompt with tags returns 201."""
        prompt_data = {"title": "Test Prompt", "content": "Test content", "tags": ["python", "ai"]}

        response = client.post("/prompts", json=prompt_data)

        assert response.status_code == 201

    def test_create_prompt_with_tags_returns_prompt_with_tags(self, client):
        """Test that creating a prompt with tags returns the prompt with tags."""
        prompt_data = {"title": "Test Prompt", "content": "Test content", "tags": ["python", "ai"]}

        response = client.post("/prompts", json=prompt_data)
        data = response.json()

        assert "tags" in data
        assert set(data["tags"]) == {"python", "ai"}

    def test_create_prompt_without_tags_defaults_to_empty_list(self, client):
        """Test that creating a prompt without tags defaults to empty list."""
        prompt_data = {"title": "Test Prompt", "content": "Test content"}

        response = client.post("/prompts", json=prompt_data)
        data = response.json()

        assert "tags" in data
        assert data["tags"] == []

    def test_get_prompt_returns_tags(self, client):
        """Test that getting a prompt returns its tags."""
        # Create prompt with tags
        create_response = client.post(
            "/prompts", json={"title": "Test Prompt", "content": "Test content", "tags": ["python", "ai"]}
        )
        prompt_id = create_response.json()["id"]

        # Get the prompt
        response = client.get(f"/prompts/{prompt_id}")
        data = response.json()

        assert set(data["tags"]) == {"python", "ai"}

    def test_update_prompt_can_modify_tags(self, client):
        """Test that updating a prompt can modify its tags."""
        # Create prompt with tags
        create_response = client.post("/prompts", json={"title": "Test Prompt", "content": "Test content", "tags": ["python"]})
        prompt_id = create_response.json()["id"]

        # Update with new tags
        update_response = client.put(
            f"/prompts/{prompt_id}",
            json={"title": "Updated Prompt", "content": "Updated content", "tags": ["javascript", "web"]},
        )
        data = update_response.json()

        assert set(data["tags"]) == {"javascript", "web"}


class TestTagFiltering:
    """Test suite for filtering prompts by tags.

    Tests the GET /prompts?tags=tag1,tag2 endpoint.
    """

    def test_filter_by_single_tag_returns_matching_prompts(self, client):
        """Test that filtering by a single tag returns only matching prompts."""
        # Create prompts with different tags
        client.post("/prompts", json={"title": "Python Prompt", "content": "Python content", "tags": ["python"]})
        client.post("/prompts", json={"title": "JavaScript Prompt", "content": "JS content", "tags": ["javascript"]})
        client.post("/prompts", json={"title": "AI Prompt", "content": "AI content", "tags": ["ai"]})

        # Filter by python tag
        response = client.get("/prompts?tags=python")
        data = response.json()

        assert response.status_code == 200
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Python Prompt"

    def test_filter_by_multiple_tags_uses_or_logic(self, client):
        """Test that filtering by multiple tags uses OR logic (matches ANY tag)."""
        # Create prompts with different tags
        client.post("/prompts", json={"title": "Python Prompt", "content": "Python content", "tags": ["python"]})
        client.post("/prompts", json={"title": "JavaScript Prompt", "content": "JS content", "tags": ["javascript"]})
        client.post("/prompts", json={"title": "AI Prompt", "content": "AI content", "tags": ["ai"]})

        # Filter by python OR javascript
        response = client.get("/prompts?tags=python,javascript")
        data = response.json()

        assert response.status_code == 200
        assert data["total"] == 2
        titles = {p["title"] for p in data["prompts"]}
        assert "Python Prompt" in titles
        assert "JavaScript Prompt" in titles
        assert "AI Prompt" not in titles

    def test_filter_by_tags_returns_empty_when_no_matches(self, client):
        """Test that filtering returns empty list when no prompts match."""
        # Create prompt with different tag
        client.post("/prompts", json={"title": "Python Prompt", "content": "Python content", "tags": ["python"]})

        # Filter by non-existent tag
        response = client.get("/prompts?tags=rust")
        data = response.json()

        assert response.status_code == 200
        assert data["total"] == 0
        assert data["prompts"] == []

    def test_filter_by_tags_is_case_sensitive(self, client):
        """Test that tag filtering is case-sensitive."""
        # Create prompt with lowercase tag
        client.post("/prompts", json={"title": "Python Prompt", "content": "Python content", "tags": ["python"]})

        # Filter by uppercase tag
        response = client.get("/prompts?tags=PYTHON")
        data = response.json()

        assert response.status_code == 200
        assert data["total"] == 0

    def test_filter_by_tags_with_prompt_having_multiple_tags(self, client):
        """Test filtering when prompts have multiple tags."""
        # Create prompt with multiple tags
        client.post(
            "/prompts",
            json={"title": "Full Stack Prompt", "content": "Full stack content", "tags": ["python", "javascript", "web"]},
        )
        client.post("/prompts", json={"title": "Backend Prompt", "content": "Backend content", "tags": ["python", "api"]})

        # Filter by python tag
        response = client.get("/prompts?tags=python")
        data = response.json()

        assert response.status_code == 200
        assert data["total"] == 2

    def test_filter_without_tags_parameter_returns_all_prompts(self, client):
        """Test that omitting tags parameter returns all prompts."""
        # Create prompts with tags
        client.post("/prompts", json={"title": "Python Prompt", "content": "Python content", "tags": ["python"]})
        client.post("/prompts", json={"title": "JavaScript Prompt", "content": "JS content", "tags": ["javascript"]})

        # Get all prompts without filter
        response = client.get("/prompts")
        data = response.json()

        assert response.status_code == 200
        assert data["total"] == 2


class TestUpdatePromptTags:
    """Test suite for updating prompt tags via dedicated endpoint.

    Tests the PUT /prompts/{id}/tags endpoint.
    """

    def test_update_prompt_tags_returns_200(self, client):
        """Test that updating prompt tags returns 200."""
        # Create prompt with initial tags
        create_response = client.post("/prompts", json={"title": "Test Prompt", "content": "Test content", "tags": ["python"]})
        prompt_id = create_response.json()["id"]

        # Update tags
        response = client.put(f"/prompts/{prompt_id}/tags", json={"tags": ["javascript", "web"]})

        assert response.status_code == 200

    def test_update_prompt_tags_replaces_existing_tags(self, client):
        """Test that updating tags replaces all existing tags."""
        # Create prompt with initial tags
        create_response = client.post(
            "/prompts", json={"title": "Test Prompt", "content": "Test content", "tags": ["python", "backend"]}
        )
        prompt_id = create_response.json()["id"]

        # Update tags
        response = client.put(f"/prompts/{prompt_id}/tags", json={"tags": ["javascript", "frontend"]})
        data = response.json()

        assert set(data["tags"]) == {"javascript", "frontend"}
        assert "python" not in data["tags"]
        assert "backend" not in data["tags"]

    def test_update_prompt_tags_with_empty_list_removes_all_tags(self, client):
        """Test that updating with empty list removes all tags."""
        # Create prompt with tags
        create_response = client.post(
            "/prompts", json={"title": "Test Prompt", "content": "Test content", "tags": ["python", "ai"]}
        )
        prompt_id = create_response.json()["id"]

        # Remove all tags
        response = client.put(f"/prompts/{prompt_id}/tags", json={"tags": []})
        data = response.json()

        assert data["tags"] == []

    def test_update_prompt_tags_updates_timestamp(self, client):
        """Test that updating tags updates the updated_at timestamp."""
        # Create prompt
        create_response = client.post("/prompts", json={"title": "Test Prompt", "content": "Test content", "tags": ["python"]})
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]

        # Small delay to ensure timestamp difference
        import time

        time.sleep(0.01)

        # Update tags
        response = client.put(f"/prompts/{prompt_id}/tags", json={"tags": ["javascript"]})
        data = response.json()

        assert data["updated_at"] > original_updated_at

    def test_update_tags_for_nonexistent_prompt_returns_404(self, client):
        """Test that updating tags for non-existent prompt returns 404."""
        response = client.put("/prompts/nonexistent-id/tags", json={"tags": ["python"]})

        assert response.status_code == 404

    def test_update_prompt_tags_preserves_other_fields(self, client):
        """Test that updating tags doesn't change other prompt fields."""
        # Create prompt
        create_response = client.post(
            "/prompts",
            json={
                "title": "Original Title",
                "content": "Original content",
                "description": "Original description",
                "tags": ["python"],
            },
        )
        prompt_id = create_response.json()["id"]

        # Update only tags
        response = client.put(f"/prompts/{prompt_id}/tags", json={"tags": ["javascript"]})
        data = response.json()

        assert data["title"] == "Original Title"
        assert data["content"] == "Original content"
        assert data["description"] == "Original description"
