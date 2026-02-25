"""Helper functions for API operations.

This module contains reusable helper functions to reduce code duplication
and improve maintainability across the API layer.
"""

from app.models import Prompt, get_current_time


def create_prompt_copy(
    existing: Prompt,
    title: str = None,
    content: str = None,
    description: str = None,
    collection_id=None,  # Can be None or a string
    tags: list = None,
    update_timestamp: bool = True,
) -> Prompt:
    """Create a copy of a prompt with optional field updates.

    This helper reduces code duplication when creating updated versions
    of prompts. It preserves existing values for any fields not specified.

    Args:
        existing (Prompt): The original prompt to copy from.
        title (str, optional): New title, or None to keep existing.
        content (str, optional): New content, or None to keep existing.
        description (str, optional): New description, or None to keep existing.
        collection_id (str or None, optional): New collection_id. Pass None explicitly to clear it.
        tags (list, optional): New tags list, or None to keep existing.
        update_timestamp (bool): Whether to update the updated_at timestamp.

    Returns:
        Prompt: A new Prompt instance with updated fields.

    Example:
        >>> updated = create_prompt_copy(
        ...     existing=old_prompt,
        ...     title="New Title",
        ...     update_timestamp=True
        ... )
        >>> # To clear collection_id:
        >>> updated = create_prompt_copy(
        ...     existing=old_prompt,
        ...     collection_id=None,
        ...     update_timestamp=False
        ... )
    """
    # Use a sentinel to distinguish between "not provided" and "explicitly None"
    _UNSET = object()

    # Determine which values to use
    new_collection_id = existing.collection_id if collection_id is _UNSET else collection_id

    return Prompt(
        id=existing.id,
        title=title if title is not None else existing.title,
        content=content if content is not None else existing.content,
        description=description if description is not None else existing.description,
        collection_id=new_collection_id,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def nullify_collection_for_prompts(prompts: list, storage) -> None:
    """Remove collection references from a list of prompts.

    This helper function updates all prompts in a list to set their
    collection_id to None. Used when deleting a collection.

    Args:
        prompts (list): List of Prompt objects to update.
        storage: Storage instance to persist updates.

    Returns:
        None

    Example:
        >>> prompts = storage.get_prompts_by_collection(collection_id)
        >>> nullify_collection_for_prompts(prompts, storage)
    """
    from app.models import Prompt

    for prompt in prompts:
        # Explicitly create a new prompt with collection_id set to None
        updated_prompt = Prompt(
            id=prompt.id,
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            collection_id=None,  # Explicitly set to None
            tags=prompt.tags,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)
