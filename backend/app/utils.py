"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt

def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by their creation date.
    
    This function takes a list of `Prompt` objects and sorts them by
their `created_at` attribute.
    
    Args:
        prompts (List[Prompt]): The list of prompts to sort.
        descending (bool, optional): If True, sorts by newest first. If False, sorts by oldest first. Defaults to True.

    Returns:
        List[Prompt]: The list of prompts sorted by date.
    
    Example:
        >>> sort_prompts_by_date(prompts, descending=True)
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)

def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by a specific collection ID.
    
    Iterates over a list of prompts and filters them based on the collection_id provided.
    
    Args:
        prompts (List[Prompt]): The list of prompts to filter.
        collection_id (str): The ID of the collection to filter by.

    Returns:
        List[Prompt]: A list of prompts that belong to the specified collection.

    Example:
        >>> filter_prompts_by_collection(prompts, '1234')
    """
    return [p for p in prompts if p.collection_id == collection_id]

def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search for prompts that match a query string.
    
    Searches through the title, content, and description of each prompt to see if they contain the query string.
    
    Args:
        prompts (List[Prompt]): The list of prompts to search through.
        query (str): The search string.

    Returns:
        List[Prompt]: A list of prompts that contain the query string in their title, content, or description.

    Example:
        >>> search_prompts(prompts, 'review')
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower()) or
           query_lower in (p.content.lower() if p.content else '')
    ]

def validate_prompt_content(content: str) -> bool:
    """Validate the content of a prompt.
    
    Checks if the provided content string is valid by ensuring it is not empty,
    not only whitespace, and is at least 10 characters long.
    
    Args:
        content (str): The prompt content to validate.

    Returns:
        bool: True if the content is valid, False otherwise.

    Example:
        >>> validate_prompt_content('This is a valid prompt content.')
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10

def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    Finds all variables within braces (e.g., {{variable}}) in the content string.
    
    Args:
        content (str): The string content from which variables are extracted.

    Returns:
        List[str]: A list of variable names extracted from the content.

    Example:
        >>> extract_variables('Hello, {{name}}!')
        ['name']
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
