"""Tests for utility functions in app/utils.py

These tests verify the helper functions used for sorting, filtering,
searching, and validating prompts.
"""

from datetime import datetime, timedelta

import pytest
from app.models import Prompt
from app.utils import (
    extract_variables,
    filter_prompts_by_collection,
    search_prompts,
    sort_prompts_by_date,
    validate_prompt_content,
)


class TestSortPromptsByDate:
    """Tests for sort_prompts_by_date function."""

    def test_sort_descending_returns_newest_first(self):
        """Test that sorting with descending=True returns newest prompts first.

        Validates: Requirements 13.1
        """
        # Create prompts with different timestamps
        now = datetime.utcnow()
        prompt1 = Prompt(
            title="Old Prompt", content="Content 1", created_at=now - timedelta(days=2), updated_at=now - timedelta(days=2)
        )
        prompt2 = Prompt(
            title="Recent Prompt", content="Content 2", created_at=now - timedelta(days=1), updated_at=now - timedelta(days=1)
        )
        prompt3 = Prompt(title="Newest Prompt", content="Content 3", created_at=now, updated_at=now)

        prompts = [prompt1, prompt2, prompt3]
        sorted_prompts = sort_prompts_by_date(prompts, descending=True)

        # Newest should be first
        assert sorted_prompts[0].title == "Newest Prompt"
        assert sorted_prompts[1].title == "Recent Prompt"
        assert sorted_prompts[2].title == "Old Prompt"

    def test_sort_ascending_returns_oldest_first(self):
        """Test that sorting with descending=False returns oldest prompts first.

        Validates: Requirements 13.2
        """
        now = datetime.utcnow()
        prompt1 = Prompt(
            title="Old Prompt", content="Content 1", created_at=now - timedelta(days=2), updated_at=now - timedelta(days=2)
        )
        prompt2 = Prompt(
            title="Recent Prompt", content="Content 2", created_at=now - timedelta(days=1), updated_at=now - timedelta(days=1)
        )
        prompt3 = Prompt(title="Newest Prompt", content="Content 3", created_at=now, updated_at=now)

        prompts = [prompt3, prompt1, prompt2]  # Mixed order
        sorted_prompts = sort_prompts_by_date(prompts, descending=False)

        # Oldest should be first
        assert sorted_prompts[0].title == "Old Prompt"
        assert sorted_prompts[1].title == "Recent Prompt"
        assert sorted_prompts[2].title == "Newest Prompt"


class TestFilterPromptsByCollection:
    """Tests for filter_prompts_by_collection function."""

    def test_filter_returns_only_matching_prompts(self):
        """Test that filtering returns only prompts with matching collection_id.

        Validates: Requirements 13.3
        """
        prompt1 = Prompt(title="Prompt 1", content="Content 1", collection_id="collection-123")
        prompt2 = Prompt(title="Prompt 2", content="Content 2", collection_id="collection-456")
        prompt3 = Prompt(title="Prompt 3", content="Content 3", collection_id="collection-123")

        prompts = [prompt1, prompt2, prompt3]
        filtered = filter_prompts_by_collection(prompts, "collection-123")

        assert len(filtered) == 2
        assert filtered[0].title == "Prompt 1"
        assert filtered[1].title == "Prompt 3"

    def test_filter_returns_empty_list_when_no_matches(self):
        """Test that filtering returns empty list when no prompts match."""
        prompt1 = Prompt(title="Prompt 1", content="Content 1", collection_id="collection-123")

        prompts = [prompt1]
        filtered = filter_prompts_by_collection(prompts, "nonexistent-collection")

        assert filtered == []


class TestSearchPrompts:
    """Tests for search_prompts function."""

    def test_search_finds_prompts_by_title(self):
        """Test that search finds prompts matching query in title.

        Validates: Requirements 13.4
        """
        prompt1 = Prompt(title="Code Review", content="Content 1")
        prompt2 = Prompt(title="Bug Fix", content="Content 2")
        prompt3 = Prompt(title="Code Refactor", content="Content 3")

        prompts = [prompt1, prompt2, prompt3]
        results = search_prompts(prompts, "Code")

        assert len(results) == 2
        assert results[0].title == "Code Review"
        assert results[1].title == "Code Refactor"

    def test_search_finds_prompts_by_content(self):
        """Test that search finds prompts matching query in content."""
        prompt1 = Prompt(title="Prompt 1", content="Review the code")
        prompt2 = Prompt(title="Prompt 2", content="Write documentation")
        prompt3 = Prompt(title="Prompt 3", content="Review the design")

        prompts = [prompt1, prompt2, prompt3]
        results = search_prompts(prompts, "Review")

        assert len(results) == 2

    def test_search_finds_prompts_by_description(self):
        """Test that search finds prompts matching query in description."""
        prompt1 = Prompt(title="Prompt 1", content="Content 1", description="For code review tasks")
        prompt2 = Prompt(title="Prompt 2", content="Content 2", description="For documentation tasks")

        prompts = [prompt1, prompt2]
        results = search_prompts(prompts, "code")

        assert len(results) == 1
        assert results[0].title == "Prompt 1"

    def test_search_is_case_insensitive(self):
        """Test that search is case-insensitive."""
        prompt1 = Prompt(title="Code Review", content="REVIEW CODE")

        prompts = [prompt1]

        # All these should find the prompt
        assert len(search_prompts(prompts, "code")) == 1
        assert len(search_prompts(prompts, "CODE")) == 1
        assert len(search_prompts(prompts, "CoDe")) == 1
        assert len(search_prompts(prompts, "review")) == 1


class TestValidatePromptContent:
    """Tests for validate_prompt_content function."""

    def test_valid_content_returns_true(self):
        """Test that valid content (10+ chars, non-whitespace) returns True.

        Validates: Requirements 13.5
        """
        assert validate_prompt_content("This is valid content") is True
        assert validate_prompt_content("1234567890") is True
        assert validate_prompt_content("   Valid with spaces   ") is True

    def test_empty_content_returns_false(self):
        """Test that empty or whitespace-only content returns False.

        Validates: Requirements 13.6
        """
        assert validate_prompt_content("") is False
        assert validate_prompt_content("   ") is False
        assert validate_prompt_content("\n\t  ") is False

    def test_short_content_returns_false(self):
        """Test that content shorter than 10 characters returns False."""
        assert validate_prompt_content("short") is False
        assert validate_prompt_content("123456789") is False  # 9 chars


class TestExtractVariables:
    """Tests for extract_variables function."""

    def test_extract_single_variable(self):
        """Test extracting a single template variable.

        Validates: Requirements 13.7
        """
        content = "Hello, {{name}}!"
        variables = extract_variables(content)

        assert variables == ["name"]

    def test_extract_multiple_variables(self):
        """Test extracting multiple template variables."""
        content = "Order {{order_id}} for {{customer}} costs {{total}}"
        variables = extract_variables(content)

        assert len(variables) == 3
        assert "order_id" in variables
        assert "customer" in variables
        assert "total" in variables

    def test_extract_no_variables(self):
        """Test that content without variables returns empty list."""
        content = "This has no variables"
        variables = extract_variables(content)

        assert variables == []

    def test_extract_ignores_invalid_syntax(self):
        """Test that invalid variable syntax is ignored."""
        content = "Valid {{var}} but not {single} or {{ spaced }}"
        variables = extract_variables(content)

        # Only valid {{var}} format should be extracted
        assert variables == ["var"]
