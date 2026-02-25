"""Pydantic models for PromptLab

This module defines the data models for the PromptLab application,
including prompts and collections. It utilizes Pydantic for data
validation and serialization.
"""

from datetime import datetime
from typing import Annotated, Callable, ClassVar, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

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


def generate_id() -> str:
    args = []  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(x_generate_id__mutmut_orig, x_generate_id__mutmut_mutants, args, kwargs, None)


def x_generate_id__mutmut_orig() -> str:
    """Generate a unique identifier using UUID4.

    Returns:
        str: A unique string identifier.

    Example:
        >>> generate_id()
        'a8098c1a-f86e-11da-bd1a-00112444be1e'
    """
    return str(uuid4())


def x_generate_id__mutmut_1() -> str:
    """Generate a unique identifier using UUID4.

    Returns:
        str: A unique string identifier.

    Example:
        >>> generate_id()
        'a8098c1a-f86e-11da-bd1a-00112444be1e'
    """
    return str(None)


x_generate_id__mutmut_mutants: ClassVar[MutantDict] = {"x_generate_id__mutmut_1": x_generate_id__mutmut_1}  # type: ignore
x_generate_id__mutmut_orig.__name__ = "x_generate_id"


def get_current_time() -> datetime:
    """Get the current UTC time.

    Returns:
        datetime: The current time in UTC.

    Example:
        >>> get_current_time()
        datetime.datetime(2023, 10, 12, 12, 0, 0)
    """
    return datetime.utcnow()


# ============== Prompt Models ==============


class PromptBase(BaseModel):
    """Base model for prompts, defining common fields.

    Attributes:
        title (str): The title of the prompt.
        content (str): The main content of the prompt.
        description (Optional[str]): A brief description of the prompt.
        collection_id (Optional[str]): The ID of the collection this prompt belongs to.
        tags (List[str]): List of tag names associated with this prompt.
    """

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class PromptCreate(PromptBase):
    """Model for creating new prompts, extending the base prompt model."""

    pass


class PromptUpdate(PromptBase):
    """Model for updating existing prompts, extending the base prompt model."""

    pass


class PromptPatch(BaseModel):
    """Model for partially updating prompts (PATCH).

    All fields are optional to allow partial updates.

    Attributes:
        title (Optional[str]): The optional title of the prompt.
        content (Optional[str]): The optional main content of the prompt.
        description (Optional[str]): An optional description of the prompt.
        collection_id (Optional[str]): An optional collection ID.
        tags (Optional[List[str]]): Optional list of tag names.
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: Optional[List[str]] = None


class Prompt(PromptBase):
    """Comprehensive prompt model including metadata.

    Attributes:
        id (str): Unique identifier for the prompt.
        created_at (datetime): Timestamp of when the prompt was created.
        updated_at (datetime): Timestamp of the last prompt update.
    """

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============


class CollectionBase(BaseModel):
    """Base collection model with common fields.

    Attributes:
        name (str): The name of the collection.
        description (Optional[str]): A brief description of the collection.
    """

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model for creating new collections, based on the base model."""

    pass


class Collection(CollectionBase):
    """Comprehensive collection model including metadata.

    Attributes:
        id (str): Unique identifier for the collection.
        created_at (datetime): Timestamp of when the collection was created.
    """

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============


class PromptList(BaseModel):
    """Model representing a list of prompts.

    Attributes:
        prompts (List[Prompt]): A list of prompt objects.
        total (int): The total number of prompts.
    """

    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Model representing a list of collections.

    Attributes:
        collections (List[Collection]): A list of collection objects.
        total (int): The total number of collections.
    """

    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Model for API health check response.

    Attributes:
        status (str): Status of the API service.
        version (str): Current version of the API.
    """

    status: str
    version: str


# ============== Tag Models ==============


class TagBase(BaseModel):
    """Base model for tags.

    Tags allow users to categorize and organize prompts flexibly.
    Similar to labels in GitHub or tags in WordPress.

    Attributes:
        name (str): The name of the tag (e.g., "python", "ai", "code-review").
    """

    name: str = Field(..., min_length=1, max_length=50)


class TagCreate(TagBase):
    """Model for creating new tags.

    Used in POST /tags endpoint to create a new tag.
    """

    pass


class Tag(TagBase):
    """Complete tag model including metadata.

    Attributes:
        tag_id (str): Unique identifier for the tag.
        created_at (datetime): Timestamp of when the tag was created.
    """

    tag_id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


class TagList(BaseModel):
    """Model representing a list of tags.

    Attributes:
        tags (List[Tag]): A list of tag objects.
        total (int): The total number of tags.
    """

    tags: List[Tag]
    total: int


class PromptTagUpdate(BaseModel):
    """Model for updating only the tags of a prompt.

    Used in PUT /prompts/{id}/tags endpoint to update tags without
    requiring all other prompt fields.

    Attributes:
        tags (List[str]): List of tag names to set for the prompt.
    """

    tags: List[str] = Field(default_factory=list)
