"""Helper functions for API operations.

This module contains reusable helper functions to reduce code duplication
and improve maintainability across the API layer.
"""

from typing import Annotated, Callable, ClassVar

from app.models import Prompt, get_current_time

MutantDict = Annotated[dict[str, Callable], "Mutant"]  # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):  # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os  # type: ignore

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]  # type: ignore
    if mutant_under_test == "fail":  # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException  # type: ignore

        raise MutmutProgrammaticFailException("Failed programmatically")  # type: ignore
    elif mutant_under_test == "stats":  # type: ignore
        from mutmut.__main__ import record_trampoline_hit  # type: ignore

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)  # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"  # type: ignore
    if not mutant_under_test.startswith(prefix):  # type: ignore
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    mutant_name = mutant_under_test.rpartition(".")[-1]  # type: ignore
    if self_arg is not None:  # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)  # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)  # type: ignore
    return result  # type: ignore


def create_prompt_copy(
    existing: Prompt,
    title: str = None,
    content: str = None,
    description: str = None,
    collection_id=None,  # Can be None or a string
    tags: list = None,
    update_timestamp: bool = True,
) -> Prompt:
    args = [existing, title, content, description, collection_id, tags, update_timestamp]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(x_create_prompt_copy__mutmut_orig, x_create_prompt_copy__mutmut_mutants, args, kwargs, None)


def x_create_prompt_copy__mutmut_orig(
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


def x_create_prompt_copy__mutmut_1(
    existing: Prompt,
    title: str = None,
    content: str = None,
    description: str = None,
    collection_id=None,  # Can be None or a string
    tags: list = None,
    update_timestamp: bool = False,
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


def x_create_prompt_copy__mutmut_2(
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
    _UNSET = None

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


def x_create_prompt_copy__mutmut_3(
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
    new_collection_id = None

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


def x_create_prompt_copy__mutmut_4(
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
    new_collection_id = existing.collection_id if collection_id is not _UNSET else collection_id

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


def x_create_prompt_copy__mutmut_5(
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
        id=None,
        title=title if title is not None else existing.title,
        content=content if content is not None else existing.content,
        description=description if description is not None else existing.description,
        collection_id=new_collection_id,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_6(
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
        title=None,
        content=content if content is not None else existing.content,
        description=description if description is not None else existing.description,
        collection_id=new_collection_id,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_7(
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
        content=None,
        description=description if description is not None else existing.description,
        collection_id=new_collection_id,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_8(
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
        description=None,
        collection_id=new_collection_id,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_9(
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
        collection_id=None,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_10(
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
        tags=None,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_11(
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
        created_at=None,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_12(
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
        updated_at=None,
    )


def x_create_prompt_copy__mutmut_13(
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
        title=title if title is not None else existing.title,
        content=content if content is not None else existing.content,
        description=description if description is not None else existing.description,
        collection_id=new_collection_id,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_14(
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
        content=content if content is not None else existing.content,
        description=description if description is not None else existing.description,
        collection_id=new_collection_id,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_15(
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
        description=description if description is not None else existing.description,
        collection_id=new_collection_id,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_16(
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
        collection_id=new_collection_id,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_17(
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
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_18(
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
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_19(
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
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_20(
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
    )


def x_create_prompt_copy__mutmut_21(
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
        title=title if title is None else existing.title,
        content=content if content is not None else existing.content,
        description=description if description is not None else existing.description,
        collection_id=new_collection_id,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_22(
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
        content=content if content is None else existing.content,
        description=description if description is not None else existing.description,
        collection_id=new_collection_id,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_23(
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
        description=description if description is None else existing.description,
        collection_id=new_collection_id,
        tags=tags if tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


def x_create_prompt_copy__mutmut_24(
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
        tags=tags if tags is None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time() if update_timestamp else existing.updated_at,
    )


x_create_prompt_copy__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_create_prompt_copy__mutmut_1": x_create_prompt_copy__mutmut_1,
    "x_create_prompt_copy__mutmut_2": x_create_prompt_copy__mutmut_2,
    "x_create_prompt_copy__mutmut_3": x_create_prompt_copy__mutmut_3,
    "x_create_prompt_copy__mutmut_4": x_create_prompt_copy__mutmut_4,
    "x_create_prompt_copy__mutmut_5": x_create_prompt_copy__mutmut_5,
    "x_create_prompt_copy__mutmut_6": x_create_prompt_copy__mutmut_6,
    "x_create_prompt_copy__mutmut_7": x_create_prompt_copy__mutmut_7,
    "x_create_prompt_copy__mutmut_8": x_create_prompt_copy__mutmut_8,
    "x_create_prompt_copy__mutmut_9": x_create_prompt_copy__mutmut_9,
    "x_create_prompt_copy__mutmut_10": x_create_prompt_copy__mutmut_10,
    "x_create_prompt_copy__mutmut_11": x_create_prompt_copy__mutmut_11,
    "x_create_prompt_copy__mutmut_12": x_create_prompt_copy__mutmut_12,
    "x_create_prompt_copy__mutmut_13": x_create_prompt_copy__mutmut_13,
    "x_create_prompt_copy__mutmut_14": x_create_prompt_copy__mutmut_14,
    "x_create_prompt_copy__mutmut_15": x_create_prompt_copy__mutmut_15,
    "x_create_prompt_copy__mutmut_16": x_create_prompt_copy__mutmut_16,
    "x_create_prompt_copy__mutmut_17": x_create_prompt_copy__mutmut_17,
    "x_create_prompt_copy__mutmut_18": x_create_prompt_copy__mutmut_18,
    "x_create_prompt_copy__mutmut_19": x_create_prompt_copy__mutmut_19,
    "x_create_prompt_copy__mutmut_20": x_create_prompt_copy__mutmut_20,
    "x_create_prompt_copy__mutmut_21": x_create_prompt_copy__mutmut_21,
    "x_create_prompt_copy__mutmut_22": x_create_prompt_copy__mutmut_22,
    "x_create_prompt_copy__mutmut_23": x_create_prompt_copy__mutmut_23,
    "x_create_prompt_copy__mutmut_24": x_create_prompt_copy__mutmut_24,
}
x_create_prompt_copy__mutmut_orig.__name__ = "x_create_prompt_copy"


def nullify_collection_for_prompts(prompts: list, storage) -> None:
    args = [prompts, storage]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_nullify_collection_for_prompts__mutmut_orig, x_nullify_collection_for_prompts__mutmut_mutants, args, kwargs, None
    )


def x_nullify_collection_for_prompts__mutmut_orig(prompts: list, storage) -> None:
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


def x_nullify_collection_for_prompts__mutmut_1(prompts: list, storage) -> None:
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
        updated_prompt = None
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_2(prompts: list, storage) -> None:
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
            id=None,
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            collection_id=None,  # Explicitly set to None
            tags=prompt.tags,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_3(prompts: list, storage) -> None:
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
            title=None,
            content=prompt.content,
            description=prompt.description,
            collection_id=None,  # Explicitly set to None
            tags=prompt.tags,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_4(prompts: list, storage) -> None:
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
            content=None,
            description=prompt.description,
            collection_id=None,  # Explicitly set to None
            tags=prompt.tags,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_5(prompts: list, storage) -> None:
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
            description=None,
            collection_id=None,  # Explicitly set to None
            tags=prompt.tags,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_6(prompts: list, storage) -> None:
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
            tags=None,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_7(prompts: list, storage) -> None:
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
            created_at=None,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_8(prompts: list, storage) -> None:
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
            updated_at=None,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_9(prompts: list, storage) -> None:
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
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            collection_id=None,  # Explicitly set to None
            tags=prompt.tags,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_10(prompts: list, storage) -> None:
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
            content=prompt.content,
            description=prompt.description,
            collection_id=None,  # Explicitly set to None
            tags=prompt.tags,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_11(prompts: list, storage) -> None:
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
            description=prompt.description,
            collection_id=None,  # Explicitly set to None
            tags=prompt.tags,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_12(prompts: list, storage) -> None:
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
            collection_id=None,  # Explicitly set to None
            tags=prompt.tags,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_13(prompts: list, storage) -> None:
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
            tags=prompt.tags,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_14(prompts: list, storage) -> None:
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
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_15(prompts: list, storage) -> None:
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
            updated_at=prompt.updated_at,  # Don't update timestamp
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_16(prompts: list, storage) -> None:
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
        )
        storage.update_prompt(prompt.id, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_17(prompts: list, storage) -> None:
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
        storage.update_prompt(None, updated_prompt)


def x_nullify_collection_for_prompts__mutmut_18(prompts: list, storage) -> None:
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
        storage.update_prompt(prompt.id, None)


def x_nullify_collection_for_prompts__mutmut_19(prompts: list, storage) -> None:
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
        storage.update_prompt(updated_prompt)


def x_nullify_collection_for_prompts__mutmut_20(prompts: list, storage) -> None:
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
        storage.update_prompt(
            prompt.id,
        )


x_nullify_collection_for_prompts__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_nullify_collection_for_prompts__mutmut_1": x_nullify_collection_for_prompts__mutmut_1,
    "x_nullify_collection_for_prompts__mutmut_2": x_nullify_collection_for_prompts__mutmut_2,
    "x_nullify_collection_for_prompts__mutmut_3": x_nullify_collection_for_prompts__mutmut_3,
    "x_nullify_collection_for_prompts__mutmut_4": x_nullify_collection_for_prompts__mutmut_4,
    "x_nullify_collection_for_prompts__mutmut_5": x_nullify_collection_for_prompts__mutmut_5,
    "x_nullify_collection_for_prompts__mutmut_6": x_nullify_collection_for_prompts__mutmut_6,
    "x_nullify_collection_for_prompts__mutmut_7": x_nullify_collection_for_prompts__mutmut_7,
    "x_nullify_collection_for_prompts__mutmut_8": x_nullify_collection_for_prompts__mutmut_8,
    "x_nullify_collection_for_prompts__mutmut_9": x_nullify_collection_for_prompts__mutmut_9,
    "x_nullify_collection_for_prompts__mutmut_10": x_nullify_collection_for_prompts__mutmut_10,
    "x_nullify_collection_for_prompts__mutmut_11": x_nullify_collection_for_prompts__mutmut_11,
    "x_nullify_collection_for_prompts__mutmut_12": x_nullify_collection_for_prompts__mutmut_12,
    "x_nullify_collection_for_prompts__mutmut_13": x_nullify_collection_for_prompts__mutmut_13,
    "x_nullify_collection_for_prompts__mutmut_14": x_nullify_collection_for_prompts__mutmut_14,
    "x_nullify_collection_for_prompts__mutmut_15": x_nullify_collection_for_prompts__mutmut_15,
    "x_nullify_collection_for_prompts__mutmut_16": x_nullify_collection_for_prompts__mutmut_16,
    "x_nullify_collection_for_prompts__mutmut_17": x_nullify_collection_for_prompts__mutmut_17,
    "x_nullify_collection_for_prompts__mutmut_18": x_nullify_collection_for_prompts__mutmut_18,
    "x_nullify_collection_for_prompts__mutmut_19": x_nullify_collection_for_prompts__mutmut_19,
    "x_nullify_collection_for_prompts__mutmut_20": x_nullify_collection_for_prompts__mutmut_20,
}
x_nullify_collection_for_prompts__mutmut_orig.__name__ = "x_nullify_collection_for_prompts"
