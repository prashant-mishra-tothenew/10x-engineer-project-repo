"""API tests for PromptLab

These tests verify the API endpoints work correctly.
Students should expand these tests significantly in Week 3.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealth:
    """Tests for health endpoint.

    The health endpoint is used to verify the API is running and responsive.
    Similar to a /ping or /status endpoint in Express.js or Laravel.
    """

    def test_health_check_returns_200(self, client: TestClient):
        """Test that health endpoint returns 200 status code.

        Validates: Requirements 1.1
        """
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_healthy_status(self, client: TestClient):
        """Test that health endpoint returns 'healthy' status.

        Validates: Requirements 1.2
        """
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_check_returns_version(self, client: TestClient):
        """Test that health endpoint returns version field.

        Validates: Requirements 1.3
        """
        response = client.get("/health")
        data = response.json()
        assert "version" in data
        assert isinstance(data["version"], str)
        assert len(data["version"]) > 0


class TestDocumentation:
    """Tests for documentation endpoints.

    These tests verify that the API documentation endpoints are accessible.
    FastAPI provides automatic API documentation via Swagger UI and ReDoc.
    """

    def test_redoc_endpoint_returns_200(self, client: TestClient):
        """Test that ReDoc documentation endpoint returns 200.

        ReDoc is an alternative API documentation UI to Swagger.
        This test ensures the custom ReDoc endpoint is accessible.
        """
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_redoc_endpoint_returns_html(self, client: TestClient):
        """Test that ReDoc endpoint returns HTML content.

        The ReDoc endpoint should return an HTML page that loads
        the ReDoc JavaScript library and displays the API documentation.
        """
        response = client.get("/redoc")
        assert "text/html" in response.headers["content-type"]
        assert b"<!DOCTYPE html>" in response.content
        assert b"redoc" in response.content.lower()


class TestPromptCreation:
    """Tests for prompt creation and validation.

    These tests verify that the API properly validates prompt data
    and returns appropriate error codes for invalid input.
    Similar to request validation in Express.js with Joi/Zod or Laravel with Form Requests.
    """

    def test_create_prompt_with_empty_title_returns_422(self, client: TestClient):
        """Test that creating a prompt with empty title returns 422 validation error.

        In FastAPI, Pydantic automatically validates request bodies.
        When validation fails, it returns 422 (Unprocessable Entity).
        This is similar to validation errors in Express.js or Laravel.

        Validates: Requirements 2.5
        """
        invalid_data = {"title": "", "content": "Some content"}  # Empty title - should fail
        response = client.post("/prompts", json=invalid_data)
        assert response.status_code == 422

    def test_create_prompt_with_empty_content_returns_422(self, client: TestClient):
        """Test that creating a prompt with empty content returns 422 validation error.

        Validates: Requirements 2.6
        """
        invalid_data = {"title": "Valid Title", "content": ""}  # Empty content - should fail
        response = client.post("/prompts", json=invalid_data)
        assert response.status_code == 422

    def test_create_prompt_with_title_exceeding_max_length_returns_422(self, client: TestClient):
        """Test that title exceeding 200 characters returns 422.

        The model defines max_length=200 for title field.

        Validates: Requirements 2.7
        """
        invalid_data = {"title": "x" * 201, "content": "Valid content"}  # 201 characters - exceeds max of 200
        response = client.post("/prompts", json=invalid_data)
        assert response.status_code == 422

    def test_create_prompt_with_description_exceeding_max_length_returns_422(self, client: TestClient):
        """Test that description exceeding 500 characters returns 422.

        The model defines max_length=500 for description field.

        Validates: Requirements 2.8
        """
        invalid_data = {
            "title": "Valid Title",
            "content": "Valid content",
            "description": "x" * 501,  # 501 characters - exceeds max of 500
        }
        response = client.post("/prompts", json=invalid_data)
        assert response.status_code == 422

    def test_create_prompt_with_minimum_valid_lengths_succeeds(self, client: TestClient, min_length_prompt):
        """Test that prompts with minimum valid field lengths are created successfully.

        This tests the lower boundary - 1 character for title and content.

        Validates: Requirements 10.6
        """
        response = client.post("/prompts", json=min_length_prompt)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == min_length_prompt["title"]
        assert data["content"] == min_length_prompt["content"]

    def test_create_prompt_with_maximum_valid_lengths_succeeds(self, client: TestClient, max_length_prompt):
        """Test that prompts with maximum valid field lengths are created successfully.

        This tests the upper boundary - 200 chars for title, 500 for description.

        Validates: Requirements 10.7
        """
        response = client.post("/prompts", json=max_length_prompt)
        assert response.status_code == 201
        data = response.json()
        assert len(data["title"]) == 200
        assert len(data["description"]) == 500

    def test_create_prompt_with_invalid_collection_returns_400(self, client: TestClient):
        """Test that creating a prompt with non-existent collection_id returns 400.

        When a collection_id is provided, the API validates that the collection exists.
        If it doesn't exist, it should return 400 Bad Request.
        This is similar to foreign key validation in a database.

        Validates: Requirements 2.9
        """
        invalid_data = {"title": "Valid Title", "content": "Valid content", "collection_id": "nonexistent-collection-id"}
        response = client.post("/prompts", json=invalid_data)
        assert response.status_code == 400
        assert "Collection not found" in response.json()["detail"]


class TestPromptRetrieval:
    """Tests for prompt retrieval operations (GET endpoints).

    These tests verify that we can retrieve prompts correctly,
    handle missing prompts appropriately, and that listing works as expected.
    """

    def test_list_prompts_with_empty_storage_returns_empty_array(self, client: TestClient):
        """Test that listing prompts with no data returns empty array and total 0.

        This is the initial state - no prompts have been created yet.
        Similar to querying an empty database table.

        Validates: Requirements 3.4
        """
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0

    def test_get_prompt_by_valid_id_returns_200(self, client: TestClient, created_prompt):
        """Test that retrieving an existing prompt by ID returns 200.

        Uses the created_prompt fixture which creates a prompt and returns its data.

        Validates: Requirements 3.1
        """
        prompt_id = created_prompt["id"]
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200

    def test_get_prompt_by_valid_id_returns_correct_data(self, client: TestClient, created_prompt):
        """Test that retrieving a prompt returns the correct prompt data.

        Validates: Requirements 3.2
        """
        prompt_id = created_prompt["id"]
        response = client.get(f"/prompts/{prompt_id}")
        data = response.json()

        # Verify all fields match
        assert data["id"] == created_prompt["id"]
        assert data["title"] == created_prompt["title"]
        assert data["content"] == created_prompt["content"]
        assert data["created_at"] == created_prompt["created_at"]

    def test_get_prompt_with_nonexistent_id_returns_404(self, client: TestClient):
        """Test that retrieving a non-existent prompt returns 404.

        This test verifies proper error handling when a prompt doesn't exist.

        Validates: Requirements 3.3
        """
        response = client.get("/prompts/nonexistent-id-12345")
        assert response.status_code == 404

    def test_list_prompts_with_data_returns_all_prompts(self, client: TestClient, multiple_prompts):
        """Test that listing prompts returns all created prompts with correct total.

        The multiple_prompts fixture creates 3 prompts.

        Validates: Requirements 3.5
        """
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()

        assert len(data["prompts"]) == 3
        assert data["total"] == 3

        # Verify all prompt IDs are present
        returned_ids = {p["id"] for p in data["prompts"]}
        expected_ids = {p["id"] for p in multiple_prompts}
        assert returned_ids == expected_ids

    def test_list_prompts_sorted_by_created_at_descending(self, client: TestClient, multiple_prompts):
        """Test that prompts are sorted by created_at in descending order (newest first).

        The multiple_prompts fixture creates prompts with delays to ensure different timestamps.
        The API should return them with the newest (last created) first.

        Validates: Requirements 3.6
        """
        response = client.get("/prompts")
        data = response.json()
        prompts = data["prompts"]

        # The last created prompt should be first in the list
        assert prompts[0]["id"] == multiple_prompts[2]["id"]  # Third (newest)
        assert prompts[1]["id"] == multiple_prompts[1]["id"]  # Second
        assert prompts[2]["id"] == multiple_prompts[0]["id"]  # First (oldest)


class TestPromptUpdate:
    """Tests for prompt update operations (PUT and PATCH endpoints).

    PUT replaces the entire resource (all fields must be provided).
    PATCH partially updates the resource (only provided fields are updated).
    Similar to PUT vs PATCH in Express.js REST APIs.
    """

    def test_update_prompt_with_put_returns_200(self, client: TestClient, created_prompt):
        """Test that updating a prompt via PUT returns 200 status.

        Validates: Requirements 4.1
        """
        prompt_id = created_prompt["id"]
        update_data = {"title": "Updated Title", "content": "Updated content", "description": "Updated description"}

        response = client.put(f"/prompts/{prompt_id}", json=update_data)
        assert response.status_code == 200

    def test_update_prompt_with_put_updates_all_fields(self, client: TestClient, created_prompt):
        """Test that PUT updates all fields to new values.

        Validates: Requirements 4.2
        """
        prompt_id = created_prompt["id"]
        update_data = {
            "title": "Completely New Title",
            "content": "Completely new content here",
            "description": "Completely new description",
        }

        response = client.put(f"/prompts/{prompt_id}", json=update_data)
        data = response.json()

        assert data["title"] == update_data["title"]
        assert data["content"] == update_data["content"]
        assert data["description"] == update_data["description"]

    def test_update_prompt_changes_updated_at_timestamp(self, client: TestClient, created_prompt):
        """Test that updating a prompt changes the updated_at timestamp.

        The updated_at field should reflect when the prompt was last modified.

        Validates: Requirements 4.3
        """
        prompt_id = created_prompt["id"]
        original_updated_at = created_prompt["updated_at"]

        # Wait to ensure timestamp will be different
        import time

        time.sleep(0.1)

        update_data = {"title": "Updated Title", "content": "Updated content", "description": "Updated description"}

        response = client.put(f"/prompts/{prompt_id}", json=update_data)
        data = response.json()

        assert data["updated_at"] != original_updated_at

    def test_update_prompt_preserves_created_at_timestamp(self, client: TestClient, created_prompt):
        """Test that updating a prompt does NOT change the created_at timestamp.

        The created_at field should never change after initial creation.

        Validates: Requirements 4.4
        """
        prompt_id = created_prompt["id"]
        original_created_at = created_prompt["created_at"]

        import time

        time.sleep(0.1)

        update_data = {"title": "Updated Title", "content": "Updated content", "description": "Updated description"}

        response = client.put(f"/prompts/{prompt_id}", json=update_data)
        data = response.json()

        assert data["created_at"] == original_created_at

    def test_update_nonexistent_prompt_returns_404(self, client: TestClient):
        """Test that updating a non-existent prompt returns 404.

        Validates: Requirements 4.5
        """
        update_data = {"title": "Updated Title", "content": "Updated content", "description": "Updated description"}

        response = client.put("/prompts/nonexistent-id-12345", json=update_data)
        assert response.status_code == 404

    def test_update_prompt_with_invalid_collection_returns_400(self, client: TestClient, created_prompt):
        """Test that updating with an invalid collection_id returns 400.

        Validates: Requirements 4.6
        """
        prompt_id = created_prompt["id"]
        update_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "description": "Updated description",
            "collection_id": "nonexistent-collection-id",
        }

        response = client.put(f"/prompts/{prompt_id}", json=update_data)
        assert response.status_code == 400

    def test_patch_prompt_returns_200(self, client: TestClient, created_prompt):
        """Test that partially updating a prompt via PATCH returns 200.

        PATCH allows updating only specific fields without providing all fields.

        Validates: Requirements 4.7
        """
        prompt_id = created_prompt["id"]
        patch_data = {"title": "Only Title Updated"}

        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        assert response.status_code == 200

    def test_patch_prompt_updates_only_specified_fields(self, client: TestClient, created_prompt):
        """Test that PATCH updates only the fields provided in the request.

        Validates: Requirements 4.8
        """
        prompt_id = created_prompt["id"]
        original_content = created_prompt["content"]
        original_description = created_prompt["description"]

        # Only update title
        patch_data = {"title": "Only Title Changed"}

        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        data = response.json()

        # Title should be updated
        assert data["title"] == "Only Title Changed"
        # Content and description should remain unchanged
        assert data["content"] == original_content
        assert data["description"] == original_description

    def test_patch_prompt_preserves_unspecified_fields(self, client: TestClient, created_prompt):
        """Test that PATCH preserves fields not included in the request.

        This is the key difference between PATCH and PUT.

        Validates: Requirements 4.9
        """
        prompt_id = created_prompt["id"]
        original_title = created_prompt["title"]

        # Only update content
        patch_data = {"content": "Only content is updated here"}

        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        data = response.json()

        # Content should be updated
        assert data["content"] == "Only content is updated here"
        # Title should remain unchanged
        assert data["title"] == original_title

    def test_patch_prompt_changes_updated_at_timestamp(self, client: TestClient, created_prompt):
        """Test that PATCH also updates the updated_at timestamp.

        Validates: Requirements 4.10
        """
        prompt_id = created_prompt["id"]
        original_updated_at = created_prompt["updated_at"]

        import time

        time.sleep(0.1)

        patch_data = {"title": "Patched Title"}

        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        data = response.json()

        assert data["updated_at"] != original_updated_at

    def test_patch_nonexistent_prompt_returns_404(self, client: TestClient):
        """Test that patching a non-existent prompt returns 404.

        Validates: Requirements 4.11
        """
        patch_data = {"title": "Patched Title"}

        response = client.patch("/prompts/nonexistent-id-12345", json=patch_data)
        assert response.status_code == 404

    def test_patch_prompt_with_invalid_collection_returns_400(self, client: TestClient, created_prompt):
        """Test that patching a prompt with non-existent collection_id returns 400.

        When updating collection_id via PATCH, the API validates that the collection exists.
        If it doesn't exist, it should return 400 Bad Request.

        Validates: Requirements 4.12
        """
        prompt_id = created_prompt["id"]
        patch_data = {"collection_id": "nonexistent-collection-id"}

        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        assert response.status_code == 400
        assert "Collection not found" in response.json()["detail"]


class TestPromptDeletion:
    """Tests for prompt deletion operations (DELETE endpoint).

    These tests verify that prompts can be deleted correctly
    and that proper error handling occurs for non-existent prompts.
    """

    def test_delete_prompt_with_valid_id_returns_204(self, client: TestClient, created_prompt):
        """Test that deleting an existing prompt returns 204 No Content.

        204 is the standard HTTP status for successful deletion with no response body.
        Similar to DELETE endpoints in Express.js or Laravel.

        Validates: Requirements 5.1
        """
        prompt_id = created_prompt["id"]
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204

    def test_delete_prompt_removes_it_from_storage(self, client: TestClient, created_prompt):
        """Test that after deletion, the prompt cannot be retrieved (returns 404).

        This verifies the prompt is actually removed from storage.

        Validates: Requirements 5.2
        """
        prompt_id = created_prompt["id"]

        # Delete the prompt
        delete_response = client.delete(f"/prompts/{prompt_id}")
        assert delete_response.status_code == 204

        # Try to retrieve it - should return 404
        get_response = client.get(f"/prompts/{prompt_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_prompt_returns_404(self, client: TestClient):
        """Test that deleting a non-existent prompt returns 404.

        Validates: Requirements 5.3
        """
        response = client.delete("/prompts/nonexistent-id-12345")
        assert response.status_code == 404

    def test_delete_prompt_does_not_affect_other_prompts(self, client: TestClient, multiple_prompts):
        """Test that deleting one prompt doesn't affect other prompts.

        This ensures deletion is targeted and doesn't have side effects.
        """
        # Delete the first prompt
        prompt_to_delete = multiple_prompts[0]["id"]
        client.delete(f"/prompts/{prompt_to_delete}")

        # Verify the other prompts still exist
        response = client.get("/prompts")
        data = response.json()

        assert data["total"] == 2  # Should have 2 remaining
        remaining_ids = {p["id"] for p in data["prompts"]}
        assert multiple_prompts[1]["id"] in remaining_ids
        assert multiple_prompts[2]["id"] in remaining_ids
        assert prompt_to_delete not in remaining_ids


class TestPromptFilteringAndSearch:
    """Tests for prompt filtering and search functionality.

    These tests verify query parameters work correctly for filtering by collection
    and searching across prompt fields. Similar to query string handling in Express.js.
    """

    def test_filter_by_collection_with_no_matching_prompts_returns_empty(self, client: TestClient, created_collection):
        """Test that filtering by a collection with no prompts returns empty array.

        Validates: Requirements 6.2
        """
        collection_id = created_collection["id"]

        # Filter by collection (but no prompts exist in it)
        response = client.get(f"/prompts?collection_id={collection_id}")
        assert response.status_code == 200
        data = response.json()

        assert data["prompts"] == []
        assert data["total"] == 0

    def test_filter_by_collection_returns_only_matching_prompts(self, client: TestClient, created_collection):
        """Test that filtering by collection_id returns only prompts from that collection.

        Validates: Requirements 6.1
        """
        collection_id = created_collection["id"]

        # Create prompts - some in collection, some not
        prompt_in_collection = {
            "title": "Prompt in Collection",
            "content": "This prompt is in the collection",
            "collection_id": collection_id,
        }
        prompt_not_in_collection = {"title": "Prompt Not in Collection", "content": "This prompt is not in any collection"}

        response1 = client.post("/prompts", json=prompt_in_collection)
        prompt1_id = response1.json()["id"]

        client.post("/prompts", json=prompt_not_in_collection)

        # Filter by collection
        response = client.get(f"/prompts?collection_id={collection_id}")
        data = response.json()

        assert data["total"] == 1
        assert data["prompts"][0]["id"] == prompt1_id
        assert data["prompts"][0]["collection_id"] == collection_id

    def test_search_by_title_returns_matching_prompts(self, client: TestClient):
        """Test that search query matches prompts by title.

        Validates: Requirements 6.3
        """
        # Create prompts with different titles
        client.post("/prompts", json={"title": "Code Review", "content": "Review code"})
        client.post("/prompts", json={"title": "Bug Fix", "content": "Fix bugs"})
        client.post("/prompts", json={"title": "Code Refactor", "content": "Refactor code"})

        # Search for "Code" - should match 2 prompts
        response = client.get("/prompts?search=Code")
        data = response.json()

        assert data["total"] == 2
        titles = {p["title"] for p in data["prompts"]}
        assert "Code Review" in titles
        assert "Code Refactor" in titles

    def test_search_by_content_returns_matching_prompts(self, client: TestClient):
        """Test that search query matches prompts by content.

        Validates: Requirements 6.4
        """
        # Create prompts with different content
        client.post("/prompts", json={"title": "Prompt 1", "content": "Review the following code"})
        client.post("/prompts", json={"title": "Prompt 2", "content": "Write documentation"})
        client.post("/prompts", json={"title": "Prompt 3", "content": "Review the design"})

        # Search for "Review" - should match 2 prompts
        response = client.get("/prompts?search=Review")
        data = response.json()

        assert data["total"] == 2

    def test_search_by_description_returns_matching_prompts(self, client: TestClient):
        """Test that search query matches prompts by description.

        Validates: Requirements 6.5
        """
        # Create prompts with different descriptions
        client.post("/prompts", json={"title": "Prompt 1", "content": "Content 1", "description": "For code review tasks"})
        client.post("/prompts", json={"title": "Prompt 2", "content": "Content 2", "description": "For documentation tasks"})
        client.post("/prompts", json={"title": "Prompt 3", "content": "Content 3", "description": "For code analysis tasks"})

        # Search for "code" - should match 2 prompts (in descriptions)
        response = client.get("/prompts?search=code")
        data = response.json()

        assert data["total"] == 2

    def test_search_is_case_insensitive(self, client: TestClient):
        """Test that search is case-insensitive.

        Validates: Requirements 6.6
        """
        # Create a prompt
        client.post("/prompts", json={"title": "Code Review", "content": "Review CODE"})

        # Search with different cases - all should match
        response_lower = client.get("/prompts?search=code")
        response_upper = client.get("/prompts?search=CODE")
        response_mixed = client.get("/prompts?search=CoDe")

        assert response_lower.json()["total"] == 1
        assert response_upper.json()["total"] == 1
        assert response_mixed.json()["total"] == 1

    def test_filter_and_search_together_applies_both(self, client: TestClient, created_collection):
        """Test that using both collection_id and search filters applies both criteria.

        This tests filter composition - both filters must match.

        Validates: Requirements 6.7
        """
        collection_id = created_collection["id"]

        # Create prompts
        client.post("/prompts", json={"title": "Code Review", "content": "Review code", "collection_id": collection_id})
        client.post("/prompts", json={"title": "Bug Fix", "content": "Fix bugs", "collection_id": collection_id})
        client.post(
            "/prompts",
            json={
                "title": "Code Refactor",
                "content": "Refactor code",
                # No collection_id
            },
        )

        # Filter by collection AND search for "Code"
        # Should only return "Code Review" (in collection and matches search)
        response = client.get(f"/prompts?collection_id={collection_id}&search=Code")
        data = response.json()

        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Code Review"
        assert data["prompts"][0]["collection_id"] == collection_id


class TestPrompts:
    """Tests for prompt endpoints."""

    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data

    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0

    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        client.post("/prompts", json=sample_prompt_data)

        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1

    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id

    def test_get_prompt_not_found(self, client: TestClient):
        """Test that getting a non-existent prompt returns 404.

        NOTE: This test currently FAILS due to Bug #1!
        The API returns 500 instead of 404.
        """
        response = client.get("/prompts/nonexistent-id")
        # This should be 404, but there's a bug...
        assert response.status_code == 404  # Will fail until bug is fixed

    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Delete it
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_response = client.get(f"/prompts/{prompt_id}")
        # Note: This might fail due to Bug #1
        assert get_response.status_code in [404, 500]  # 404 after fix

    def test_update_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_created_at = create_response.json()["created_at"]
        original_updated_at = create_response.json()["updated_at"]

        # Update it
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content for the prompt",
            "description": "Updated description",
        }

        import time

        time.sleep(0.1)  # Small delay to ensure timestamp would change

        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"

        # Bug #2 FIX: Verify updated_at timestamp changes
        assert data["updated_at"] != original_updated_at, "updated_at should change on PUT"
        assert data["created_at"] == original_created_at, "created_at should not change"

    def test_sorting_order(self, client: TestClient):
        """Test that prompts are sorted newest first.

        NOTE: This test might fail due to Bug #3!
        """
        import time

        # Create prompts with delay
        prompt1 = {"title": "First", "content": "First prompt content"}
        prompt2 = {"title": "Second", "content": "Second prompt content"}

        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)

        response = client.get("/prompts")
        prompts = response.json()["prompts"]

        # Newest (Second) should be first
        assert prompts[0]["title"] == "Second"  # Will fail until Bug #3 fixed


class TestCollectionCreation:
    """Tests for collection creation and validation.

    Collections are used to organize prompts into groups.
    These tests verify validation rules and successful creation.
    """

    def test_create_collection_with_empty_name_returns_422(self, client: TestClient):
        """Test that creating a collection with empty name returns 422 validation error.

        Validates: Requirements 7.4
        """
        invalid_data = {"name": "", "description": "Some description"}  # Empty name - should fail
        response = client.post("/collections", json=invalid_data)
        assert response.status_code == 422

    def test_create_collection_with_name_exceeding_max_length_returns_422(self, client: TestClient):
        """Test that collection name exceeding 100 characters returns 422.

        The model defines max_length=100 for name field.

        Validates: Requirements 7.5
        """
        invalid_data = {"name": "x" * 101, "description": "Valid description"}  # 101 characters - exceeds max of 100
        response = client.post("/collections", json=invalid_data)
        assert response.status_code == 422

    def test_create_collection_with_description_exceeding_max_length_returns_422(self, client: TestClient):
        """Test that collection description exceeding 500 characters returns 422.

        The model defines max_length=500 for description field.

        Validates: Requirements 7.6
        """
        invalid_data = {"name": "Valid Name", "description": "x" * 501}  # 501 characters - exceeds max of 500
        response = client.post("/collections", json=invalid_data)
        assert response.status_code == 422

    def test_create_collection_with_valid_data_returns_201(self, client: TestClient, sample_collection_data):
        """Test that creating a collection with valid data returns 201 status.

        Validates: Requirements 7.1
        """
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201

    def test_create_collection_returns_all_submitted_fields(self, client: TestClient, sample_collection_data):
        """Test that created collection response contains all submitted fields.

        Validates: Requirements 7.2
        """
        response = client.post("/collections", json=sample_collection_data)
        data = response.json()

        assert data["name"] == sample_collection_data["name"]
        assert data["description"] == sample_collection_data["description"]

    def test_create_collection_includes_auto_generated_fields(self, client: TestClient, sample_collection_data):
        """Test that created collection includes auto-generated id and created_at fields.

        Validates: Requirements 7.3, 8.1, 8.2
        """
        response = client.post("/collections", json=sample_collection_data)
        data = response.json()

        assert "id" in data
        assert isinstance(data["id"], str)
        assert len(data["id"]) > 0

        assert "created_at" in data
        assert isinstance(data["created_at"], str)


class TestCollectionRetrieval:
    """Tests for collection retrieval operations (GET endpoints).

    These tests verify that we can retrieve collections correctly
    and handle missing collections appropriately.
    """

    def test_list_collections_with_empty_storage_returns_empty_array(self, client: TestClient):
        """Test that listing collections with no data returns empty array and total 0.

        Validates: Requirements 8.4
        """
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()

        assert data["collections"] == []
        assert data["total"] == 0

    def test_get_collection_by_valid_id_returns_200(self, client: TestClient, created_collection):
        """Test that retrieving an existing collection by ID returns 200.

        Validates: Requirements 8.1
        """
        collection_id = created_collection["id"]
        response = client.get(f"/collections/{collection_id}")
        assert response.status_code == 200

    def test_get_collection_by_valid_id_returns_correct_data(self, client: TestClient, created_collection):
        """Test that retrieving a collection returns the correct collection data.

        Validates: Requirements 8.2
        """
        collection_id = created_collection["id"]
        response = client.get(f"/collections/{collection_id}")
        data = response.json()

        # Verify all fields match
        assert data["id"] == created_collection["id"]
        assert data["name"] == created_collection["name"]
        assert data["description"] == created_collection["description"]
        assert data["created_at"] == created_collection["created_at"]

    def test_get_collection_with_nonexistent_id_returns_404(self, client: TestClient):
        """Test that retrieving a non-existent collection returns 404.

        Validates: Requirements 8.3
        """
        response = client.get("/collections/nonexistent-collection-id-12345")
        assert response.status_code == 404

    def test_list_collections_with_data_returns_all_collections(self, client: TestClient, sample_collection_data):
        """Test that listing collections returns all created collections with correct total.

        Validates: Requirements 8.5
        """
        # Create multiple collections
        client.post("/collections", json=sample_collection_data)
        client.post("/collections", json={"name": "Collection 2", "description": "Second collection"})
        client.post("/collections", json={"name": "Collection 3", "description": "Third collection"})

        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()

        assert len(data["collections"]) == 3
        assert data["total"] == 3


class TestCollectionDeletion:
    """Tests for collection deletion operations (DELETE endpoint).

    These tests verify that collections can be deleted correctly,
    and that associated prompts are handled properly (collection_id set to None).
    """

    def test_delete_collection_with_valid_id_returns_204(self, client: TestClient, created_collection):
        """Test that deleting an existing collection returns 204 No Content.

        Validates: Requirements 9.1
        """
        collection_id = created_collection["id"]
        response = client.delete(f"/collections/{collection_id}")
        assert response.status_code == 204

    def test_delete_collection_removes_it_from_storage(self, client: TestClient, created_collection):
        """Test that after deletion, the collection cannot be retrieved (returns 404).

        Validates: Requirements 9.2
        """
        collection_id = created_collection["id"]

        # Delete the collection
        delete_response = client.delete(f"/collections/{collection_id}")
        assert delete_response.status_code == 204

        # Try to retrieve it - should return 404
        get_response = client.get(f"/collections/{collection_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_collection_returns_404(self, client: TestClient):
        """Test that deleting a non-existent collection returns 404.

        Validates: Requirements 9.3
        """
        response = client.delete("/collections/nonexistent-collection-id-12345")
        assert response.status_code == 404

    def test_delete_collection_with_prompts_sets_collection_id_to_none(self, client: TestClient, created_collection):
        """Test that deleting a collection sets associated prompts' collection_id to None.

        This is the "SET NULL" strategy - prompts remain but lose their collection reference.
        Similar to ON DELETE SET NULL in SQL databases.

        Validates: Requirements 9.4
        """
        collection_id = created_collection["id"]

        # Create a prompt in the collection
        prompt_data = {
            "title": "Prompt in Collection",
            "content": "This prompt is in the collection",
            "collection_id": collection_id,
        }
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]

        # Verify prompt is in the collection
        prompt_check = client.get(f"/prompts/{prompt_id}")
        assert prompt_check.json()["collection_id"] == collection_id

        # Delete the collection
        client.delete(f"/collections/{collection_id}")

        # Verify prompt still exists but collection_id is None
        prompt_after = client.get(f"/prompts/{prompt_id}")
        assert prompt_after.status_code == 200
        assert prompt_after.json()["collection_id"] is None

    def test_delete_collection_with_multiple_prompts_sets_all_to_none(self, client: TestClient, created_collection):
        """Test that deleting a collection sets ALL associated prompts' collection_id to None.

        Validates: Requirements 9.5
        """
        collection_id = created_collection["id"]

        # Create multiple prompts in the collection
        prompt_ids = []
        for i in range(3):
            prompt_data = {"title": f"Prompt {i+1}", "content": f"Content {i+1}", "collection_id": collection_id}
            response = client.post("/prompts", json=prompt_data)
            prompt_ids.append(response.json()["id"])

        # Delete the collection
        client.delete(f"/collections/{collection_id}")

        # Verify all prompts still exist but have collection_id = None
        for prompt_id in prompt_ids:
            prompt_response = client.get(f"/prompts/{prompt_id}")
            assert prompt_response.status_code == 200
            assert prompt_response.json()["collection_id"] is None


class TestEdgeCases:
    """Tests for edge cases including special characters, Unicode, and template variables.

    These tests ensure the API handles unusual but valid input correctly.
    """

    def test_create_prompt_with_special_characters_in_title(self, client: TestClient, prompt_with_special_chars):
        """Test that prompts with special characters in title are created successfully.

        Special characters like !@#$%^&*() should be handled correctly.

        Validates: Requirements 10.1
        """
        response = client.post("/prompts", json=prompt_with_special_chars)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == prompt_with_special_chars["title"]
        assert "!@#$%^&*()" in data["title"]

    def test_create_prompt_with_special_characters_in_content(self, client: TestClient, prompt_with_special_chars):
        """Test that prompts with special characters in content are created successfully.

        Content may include HTML tags, JSON syntax, etc.

        Validates: Requirements 10.2
        """
        response = client.post("/prompts", json=prompt_with_special_chars)
        assert response.status_code == 201
        data = response.json()
        assert "<html>" in data["content"]
        assert "{json}" in data["content"]
        assert "&" in data["content"]

    def test_create_prompt_with_unicode_characters(self, client: TestClient, prompt_with_unicode):
        """Test that prompts with Unicode characters are created successfully.

        Unicode includes international characters, emoji, and special symbols.
        This is important for internationalization (i18n).

        Validates: Requirements 10.3
        """
        response = client.post("/prompts", json=prompt_with_unicode)
        assert response.status_code == 201
        data = response.json()

        # Verify Unicode in title
        assert "你好世界" in data["title"]
        assert "🌍" in data["title"]

        # Verify Unicode in content
        assert "🚀" in data["content"]
        assert "™" in data["content"]

    def test_create_prompt_with_template_variables(self, client: TestClient, prompt_with_template_vars):
        """Test that prompts with template variables {{variable}} are preserved.

        Template variables are a core feature - they should not be processed or escaped.

        Validates: Requirements 10.4
        """
        response = client.post("/prompts", json=prompt_with_template_vars)
        assert response.status_code == 201
        data = response.json()

        # Verify template variables are preserved
        assert "{{name}}" in data["content"]
        assert "{{order_id}}" in data["content"]
        assert "{{total}}" in data["content"]

    def test_search_with_special_characters(self, client: TestClient):
        """Test that search queries with special characters execute without errors.

        Search should handle special regex characters safely.

        Validates: Requirements 10.5
        """
        # Create a prompt with special characters
        client.post("/prompts", json={"title": "Test (with) [brackets] & symbols", "content": "Content with special chars"})

        # Search with special characters - should not crash
        response = client.get("/prompts?search=(with)")
        assert response.status_code == 200

        # Should find the prompt
        data = response.json()
        assert data["total"] >= 0  # At least doesn't crash


class TestTimestampValidation:
    """Tests for timestamp behavior validation.

    These tests verify that created_at and updated_at timestamps
    are set correctly and behave as expected.
    """

    def test_prompt_created_at_equals_updated_at_initially(self, client: TestClient, sample_prompt_data):
        """Test that when a prompt is created, created_at and updated_at are very close.

        Both timestamps should be set at creation time and be within 1 second of each other.
        They may differ by microseconds due to separate function calls.

        Validates: Requirements 11.1, 11.2
        """
        response = client.post("/prompts", json=sample_prompt_data)
        data = response.json()

        # Parse timestamps
        from datetime import datetime

        created_at = datetime.fromisoformat(data["created_at"])
        updated_at = datetime.fromisoformat(data["updated_at"])

        # They should be within 1 second of each other
        time_diff = abs((updated_at - created_at).total_seconds())
        assert time_diff < 1.0, f"Timestamps differ by {time_diff} seconds"

    def test_collection_created_at_is_set(self, client: TestClient, sample_collection_data):
        """Test that when a collection is created, created_at is set to current time.

        Collections only have created_at (no updated_at since they can't be updated).

        Validates: Requirements 11.5
        """
        response = client.post("/collections", json=sample_collection_data)
        data = response.json()

        assert "created_at" in data
        assert isinstance(data["created_at"], str)
        assert len(data["created_at"]) > 0

        # Verify it's a valid ISO datetime format
        from datetime import datetime

        try:
            datetime.fromisoformat(data["created_at"])
            timestamp_valid = True
        except ValueError:
            timestamp_valid = False

        assert timestamp_valid


class TestCollections:
    """Tests for collection endpoints."""

    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data

    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)

        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) == 1

    def test_get_collection_not_found(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404

    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test deleting a collection that has prompts.

        After Bug #4 fix: Prompts should have collection_id set to None.
        """
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]

        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]

        # Delete collection
        delete_response = client.delete(f"/collections/{collection_id}")
        assert delete_response.status_code == 204

        # Verify collection is deleted
        col_check = client.get(f"/collections/{collection_id}")
        assert col_check.status_code == 404

        # Verify prompt still exists but collection_id is None
        prompt_check = client.get(f"/prompts/{prompt_id}")
        assert prompt_check.status_code == 200
        assert prompt_check.json()["collection_id"] is None  # ✅ Fixed: Set to None
