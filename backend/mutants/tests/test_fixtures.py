"""Test to verify enhanced fixtures work correctly"""

import pytest
from fastapi.testclient import TestClient


class TestEnhancedFixtures:
    """Verify all enhanced fixtures are working properly."""

    def test_prompt_with_special_chars_fixture(self, prompt_with_special_chars):
        """Verify special characters fixture provides correct data."""
        assert "title" in prompt_with_special_chars
        assert "content" in prompt_with_special_chars
        assert "!@#$%^&*()" in prompt_with_special_chars["title"]

    def test_prompt_with_unicode_fixture(self, prompt_with_unicode):
        """Verify Unicode fixture provides correct data."""
        assert "title" in prompt_with_unicode
        assert "你好世界" in prompt_with_unicode["title"]
        assert "🚀" in prompt_with_unicode["content"]

    def test_prompt_with_template_vars_fixture(self, prompt_with_template_vars):
        """Verify template variables fixture provides correct data."""
        assert "{{name}}" in prompt_with_template_vars["content"]
        assert "{{order_id}}" in prompt_with_template_vars["content"]

    def test_max_length_prompt_fixture(self, max_length_prompt):
        """Verify max length fixture has correct lengths."""
        assert len(max_length_prompt["title"]) == 200
        assert len(max_length_prompt["description"]) == 500

    def test_min_length_prompt_fixture(self, min_length_prompt):
        """Verify min length fixture has correct lengths."""
        assert len(min_length_prompt["title"]) == 1
        assert len(min_length_prompt["content"]) == 1

    def test_created_prompt_fixture(self, created_prompt):
        """Verify created_prompt fixture creates a prompt."""
        assert "id" in created_prompt
        assert "created_at" in created_prompt
        assert "updated_at" in created_prompt

    def test_created_collection_fixture(self, created_collection):
        """Verify created_collection fixture creates a collection."""
        assert "id" in created_collection
        assert "created_at" in created_collection

    def test_multiple_prompts_fixture(self, multiple_prompts):
        """Verify multiple_prompts fixture creates 3 prompts."""
        assert len(multiple_prompts) == 3
        assert all("id" in p for p in multiple_prompts)
        # Verify they have different timestamps
        timestamps = [p["created_at"] for p in multiple_prompts]
        assert len(set(timestamps)) == 3  # All unique
