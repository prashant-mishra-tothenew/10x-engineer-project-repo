"""Utility functions for PromptLab"""

from typing import Annotated, Callable, ClassVar, List

from app.models import Prompt

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


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    args = [prompts, descending]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(x_sort_prompts_by_date__mutmut_orig, x_sort_prompts_by_date__mutmut_mutants, args, kwargs, None)


def x_sort_prompts_by_date__mutmut_orig(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
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


def x_sort_prompts_by_date__mutmut_1(prompts: List[Prompt], descending: bool = False) -> List[Prompt]:
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


def x_sort_prompts_by_date__mutmut_2(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
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
    return sorted(None, key=lambda p: p.created_at, reverse=descending)


def x_sort_prompts_by_date__mutmut_3(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
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
    return sorted(prompts, key=None, reverse=descending)


def x_sort_prompts_by_date__mutmut_4(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
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
    return sorted(prompts, key=lambda p: p.created_at, reverse=None)


def x_sort_prompts_by_date__mutmut_5(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
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
    return sorted(key=lambda p: p.created_at, reverse=descending)


def x_sort_prompts_by_date__mutmut_6(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
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
    return sorted(prompts, reverse=descending)


def x_sort_prompts_by_date__mutmut_7(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
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
    return sorted(
        prompts,
        key=lambda p: p.created_at,
    )


def x_sort_prompts_by_date__mutmut_8(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
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
    return sorted(prompts, key=lambda p: None, reverse=descending)


x_sort_prompts_by_date__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_sort_prompts_by_date__mutmut_1": x_sort_prompts_by_date__mutmut_1,
    "x_sort_prompts_by_date__mutmut_2": x_sort_prompts_by_date__mutmut_2,
    "x_sort_prompts_by_date__mutmut_3": x_sort_prompts_by_date__mutmut_3,
    "x_sort_prompts_by_date__mutmut_4": x_sort_prompts_by_date__mutmut_4,
    "x_sort_prompts_by_date__mutmut_5": x_sort_prompts_by_date__mutmut_5,
    "x_sort_prompts_by_date__mutmut_6": x_sort_prompts_by_date__mutmut_6,
    "x_sort_prompts_by_date__mutmut_7": x_sort_prompts_by_date__mutmut_7,
    "x_sort_prompts_by_date__mutmut_8": x_sort_prompts_by_date__mutmut_8,
}
x_sort_prompts_by_date__mutmut_orig.__name__ = "x_sort_prompts_by_date"


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    args = [prompts, collection_id]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_filter_prompts_by_collection__mutmut_orig, x_filter_prompts_by_collection__mutmut_mutants, args, kwargs, None
    )


def x_filter_prompts_by_collection__mutmut_orig(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
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


def x_filter_prompts_by_collection__mutmut_1(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
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
    return [p for p in prompts if p.collection_id != collection_id]


x_filter_prompts_by_collection__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_filter_prompts_by_collection__mutmut_1": x_filter_prompts_by_collection__mutmut_1
}
x_filter_prompts_by_collection__mutmut_orig.__name__ = "x_filter_prompts_by_collection"


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    args = [prompts, query]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(x_search_prompts__mutmut_orig, x_search_prompts__mutmut_mutants, args, kwargs, None)


def x_search_prompts__mutmut_orig(prompts: List[Prompt], query: str) -> List[Prompt]:
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
        p
        for p in prompts
        if query_lower in p.title.lower()
        or (p.description and query_lower in p.description.lower())
        or query_lower in (p.content.lower() if p.content else "")
    ]


def x_search_prompts__mutmut_1(prompts: List[Prompt], query: str) -> List[Prompt]:
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
    query_lower = None
    return [
        p
        for p in prompts
        if query_lower in p.title.lower()
        or (p.description and query_lower in p.description.lower())
        or query_lower in (p.content.lower() if p.content else "")
    ]


def x_search_prompts__mutmut_2(prompts: List[Prompt], query: str) -> List[Prompt]:
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
    query_lower = query.upper()
    return [
        p
        for p in prompts
        if query_lower in p.title.lower()
        or (p.description and query_lower in p.description.lower())
        or query_lower in (p.content.lower() if p.content else "")
    ]


def x_search_prompts__mutmut_3(prompts: List[Prompt], query: str) -> List[Prompt]:
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
        p
        for p in prompts
        if query_lower in p.title.lower()
        or (p.description and query_lower in p.description.lower())
        and query_lower in (p.content.lower() if p.content else "")
    ]


def x_search_prompts__mutmut_4(prompts: List[Prompt], query: str) -> List[Prompt]:
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
        p
        for p in prompts
        if query_lower in p.title.lower()
        and (p.description and query_lower in p.description.lower())
        or query_lower in (p.content.lower() if p.content else "")
    ]


def x_search_prompts__mutmut_5(prompts: List[Prompt], query: str) -> List[Prompt]:
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
        p
        for p in prompts
        if query_lower not in p.title.lower()
        or (p.description and query_lower in p.description.lower())
        or query_lower in (p.content.lower() if p.content else "")
    ]


def x_search_prompts__mutmut_6(prompts: List[Prompt], query: str) -> List[Prompt]:
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
        p
        for p in prompts
        if query_lower in p.title.upper()
        or (p.description and query_lower in p.description.lower())
        or query_lower in (p.content.lower() if p.content else "")
    ]


def x_search_prompts__mutmut_7(prompts: List[Prompt], query: str) -> List[Prompt]:
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
        p
        for p in prompts
        if query_lower in p.title.lower()
        or (p.description or query_lower in p.description.lower())
        or query_lower in (p.content.lower() if p.content else "")
    ]


def x_search_prompts__mutmut_8(prompts: List[Prompt], query: str) -> List[Prompt]:
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
        p
        for p in prompts
        if query_lower in p.title.lower()
        or (p.description and query_lower not in p.description.lower())
        or query_lower in (p.content.lower() if p.content else "")
    ]


def x_search_prompts__mutmut_9(prompts: List[Prompt], query: str) -> List[Prompt]:
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
        p
        for p in prompts
        if query_lower in p.title.lower()
        or (p.description and query_lower in p.description.upper())
        or query_lower in (p.content.lower() if p.content else "")
    ]


def x_search_prompts__mutmut_10(prompts: List[Prompt], query: str) -> List[Prompt]:
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
        p
        for p in prompts
        if query_lower in p.title.lower()
        or (p.description and query_lower in p.description.lower())
        or query_lower not in (p.content.lower() if p.content else "")
    ]


def x_search_prompts__mutmut_11(prompts: List[Prompt], query: str) -> List[Prompt]:
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
        p
        for p in prompts
        if query_lower in p.title.lower()
        or (p.description and query_lower in p.description.lower())
        or query_lower in (p.content.upper() if p.content else "")
    ]


def x_search_prompts__mutmut_12(prompts: List[Prompt], query: str) -> List[Prompt]:
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
        p
        for p in prompts
        if query_lower in p.title.lower()
        or (p.description and query_lower in p.description.lower())
        or query_lower in (p.content.lower() if p.content else "XXXX")
    ]


x_search_prompts__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_search_prompts__mutmut_1": x_search_prompts__mutmut_1,
    "x_search_prompts__mutmut_2": x_search_prompts__mutmut_2,
    "x_search_prompts__mutmut_3": x_search_prompts__mutmut_3,
    "x_search_prompts__mutmut_4": x_search_prompts__mutmut_4,
    "x_search_prompts__mutmut_5": x_search_prompts__mutmut_5,
    "x_search_prompts__mutmut_6": x_search_prompts__mutmut_6,
    "x_search_prompts__mutmut_7": x_search_prompts__mutmut_7,
    "x_search_prompts__mutmut_8": x_search_prompts__mutmut_8,
    "x_search_prompts__mutmut_9": x_search_prompts__mutmut_9,
    "x_search_prompts__mutmut_10": x_search_prompts__mutmut_10,
    "x_search_prompts__mutmut_11": x_search_prompts__mutmut_11,
    "x_search_prompts__mutmut_12": x_search_prompts__mutmut_12,
}
x_search_prompts__mutmut_orig.__name__ = "x_search_prompts"


def validate_prompt_content(content: str) -> bool:
    args = [content]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_validate_prompt_content__mutmut_orig, x_validate_prompt_content__mutmut_mutants, args, kwargs, None
    )


def x_validate_prompt_content__mutmut_orig(content: str) -> bool:
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


def x_validate_prompt_content__mutmut_1(content: str) -> bool:
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
    if not content and not content.strip():
        return False
    return len(content.strip()) >= 10


def x_validate_prompt_content__mutmut_2(content: str) -> bool:
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
    if content or not content.strip():
        return False
    return len(content.strip()) >= 10


def x_validate_prompt_content__mutmut_3(content: str) -> bool:
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
    if not content or content.strip():
        return False
    return len(content.strip()) >= 10


def x_validate_prompt_content__mutmut_4(content: str) -> bool:
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
        return True
    return len(content.strip()) >= 10


def x_validate_prompt_content__mutmut_5(content: str) -> bool:
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
    return len(content.strip()) > 10


def x_validate_prompt_content__mutmut_6(content: str) -> bool:
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
    return len(content.strip()) >= 11


x_validate_prompt_content__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_validate_prompt_content__mutmut_1": x_validate_prompt_content__mutmut_1,
    "x_validate_prompt_content__mutmut_2": x_validate_prompt_content__mutmut_2,
    "x_validate_prompt_content__mutmut_3": x_validate_prompt_content__mutmut_3,
    "x_validate_prompt_content__mutmut_4": x_validate_prompt_content__mutmut_4,
    "x_validate_prompt_content__mutmut_5": x_validate_prompt_content__mutmut_5,
    "x_validate_prompt_content__mutmut_6": x_validate_prompt_content__mutmut_6,
}
x_validate_prompt_content__mutmut_orig.__name__ = "x_validate_prompt_content"


def extract_variables(content: str) -> List[str]:
    args = [content]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(x_extract_variables__mutmut_orig, x_extract_variables__mutmut_mutants, args, kwargs, None)


def x_extract_variables__mutmut_orig(content: str) -> List[str]:
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

    pattern = r"\{\{(\w+)\}\}"
    return re.findall(pattern, content)


def x_extract_variables__mutmut_1(content: str) -> List[str]:
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

    pattern = None
    return re.findall(pattern, content)


def x_extract_variables__mutmut_2(content: str) -> List[str]:
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

    pattern = r"XX\{\{(\w+)\}\}XX"
    return re.findall(pattern, content)


def x_extract_variables__mutmut_3(content: str) -> List[str]:
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

    pattern = r"\{\{(\w+)\}\}"
    return re.findall(None, content)


def x_extract_variables__mutmut_4(content: str) -> List[str]:
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

    pattern = r"\{\{(\w+)\}\}"
    return re.findall(pattern, None)


def x_extract_variables__mutmut_5(content: str) -> List[str]:
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

    pattern = r"\{\{(\w+)\}\}"
    return re.findall(content)


def x_extract_variables__mutmut_6(content: str) -> List[str]:
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

    pattern = r"\{\{(\w+)\}\}"
    return re.findall(
        pattern,
    )


x_extract_variables__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_extract_variables__mutmut_1": x_extract_variables__mutmut_1,
    "x_extract_variables__mutmut_2": x_extract_variables__mutmut_2,
    "x_extract_variables__mutmut_3": x_extract_variables__mutmut_3,
    "x_extract_variables__mutmut_4": x_extract_variables__mutmut_4,
    "x_extract_variables__mutmut_5": x_extract_variables__mutmut_5,
    "x_extract_variables__mutmut_6": x_extract_variables__mutmut_6,
}
x_extract_variables__mutmut_orig.__name__ = "x_extract_variables"


def filter_by_tags(prompts: List[Prompt], tags: List[str]) -> List[Prompt]:
    args = [prompts, tags]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(x_filter_by_tags__mutmut_orig, x_filter_by_tags__mutmut_mutants, args, kwargs, None)


def x_filter_by_tags__mutmut_orig(prompts: List[Prompt], tags: List[str]) -> List[Prompt]:
    """Filter prompts by tags using OR logic (matches ANY tag).

    Returns prompts that have at least one of the specified tags.
    Tag matching is case-sensitive.

    Args:
        prompts (List[Prompt]): The list of prompts to filter.
        tags (List[str]): List of tag names to filter by.

    Returns:
        List[Prompt]: Prompts that have at least one matching tag.

    Example:
        >>> filter_by_tags(prompts, ["python", "javascript"])
        # Returns prompts tagged with python OR javascript
    """
    if not tags:
        return prompts

    tag_set = set(tags)
    return [p for p in prompts if tag_set.intersection(p.tags)]


def x_filter_by_tags__mutmut_1(prompts: List[Prompt], tags: List[str]) -> List[Prompt]:
    """Filter prompts by tags using OR logic (matches ANY tag).

    Returns prompts that have at least one of the specified tags.
    Tag matching is case-sensitive.

    Args:
        prompts (List[Prompt]): The list of prompts to filter.
        tags (List[str]): List of tag names to filter by.

    Returns:
        List[Prompt]: Prompts that have at least one matching tag.

    Example:
        >>> filter_by_tags(prompts, ["python", "javascript"])
        # Returns prompts tagged with python OR javascript
    """
    if tags:
        return prompts

    tag_set = set(tags)
    return [p for p in prompts if tag_set.intersection(p.tags)]


def x_filter_by_tags__mutmut_2(prompts: List[Prompt], tags: List[str]) -> List[Prompt]:
    """Filter prompts by tags using OR logic (matches ANY tag).

    Returns prompts that have at least one of the specified tags.
    Tag matching is case-sensitive.

    Args:
        prompts (List[Prompt]): The list of prompts to filter.
        tags (List[str]): List of tag names to filter by.

    Returns:
        List[Prompt]: Prompts that have at least one matching tag.

    Example:
        >>> filter_by_tags(prompts, ["python", "javascript"])
        # Returns prompts tagged with python OR javascript
    """
    if not tags:
        return prompts

    tag_set = None
    return [p for p in prompts if tag_set.intersection(p.tags)]


def x_filter_by_tags__mutmut_3(prompts: List[Prompt], tags: List[str]) -> List[Prompt]:
    """Filter prompts by tags using OR logic (matches ANY tag).

    Returns prompts that have at least one of the specified tags.
    Tag matching is case-sensitive.

    Args:
        prompts (List[Prompt]): The list of prompts to filter.
        tags (List[str]): List of tag names to filter by.

    Returns:
        List[Prompt]: Prompts that have at least one matching tag.

    Example:
        >>> filter_by_tags(prompts, ["python", "javascript"])
        # Returns prompts tagged with python OR javascript
    """
    if not tags:
        return prompts

    tag_set = set(None)
    return [p for p in prompts if tag_set.intersection(p.tags)]


def x_filter_by_tags__mutmut_4(prompts: List[Prompt], tags: List[str]) -> List[Prompt]:
    """Filter prompts by tags using OR logic (matches ANY tag).

    Returns prompts that have at least one of the specified tags.
    Tag matching is case-sensitive.

    Args:
        prompts (List[Prompt]): The list of prompts to filter.
        tags (List[str]): List of tag names to filter by.

    Returns:
        List[Prompt]: Prompts that have at least one matching tag.

    Example:
        >>> filter_by_tags(prompts, ["python", "javascript"])
        # Returns prompts tagged with python OR javascript
    """
    if not tags:
        return prompts

    tag_set = set(tags)
    return [p for p in prompts if tag_set.intersection(None)]


x_filter_by_tags__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_filter_by_tags__mutmut_1": x_filter_by_tags__mutmut_1,
    "x_filter_by_tags__mutmut_2": x_filter_by_tags__mutmut_2,
    "x_filter_by_tags__mutmut_3": x_filter_by_tags__mutmut_3,
    "x_filter_by_tags__mutmut_4": x_filter_by_tags__mutmut_4,
}
x_filter_by_tags__mutmut_orig.__name__ = "x_filter_by_tags"
