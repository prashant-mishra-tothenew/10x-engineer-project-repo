"""Pydantic models for PromptLab

This module defines the data models for the PromptLab application,
including prompts and collections. It utilizes Pydantic for data
validation and serialization.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier using UUID4.

    Returns:
        str: A unique string identifier.

    Example:
        >>> generate_id()
        'a8098c1a-f86e-11da-bd1a-00112444be1e'
    """
    return str(uuid4())


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
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


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
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


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
