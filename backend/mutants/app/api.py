"""FastAPI routes for PromptLab"""

from typing import Optional

from app import __version__
from app.helpers import create_prompt_copy, nullify_collection_for_prompts

# Use file storage by default for development
# Tests will override this with in-memory storage
from app.json_file_storage import JSONFileStorage
from app.models import (
    Collection,
    CollectionCreate,
    CollectionList,
    HealthResponse,
    Prompt,
    PromptCreate,
    PromptList,
    PromptPatch,
    PromptTagUpdate,
    PromptUpdate,
    Tag,
    TagCreate,
    TagList,
    get_current_time,
)
from app.utils import filter_by_tags, filter_prompts_by_collection, search_prompts, sort_prompts_by_date
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

storage = JSONFileStorage()
print("📁 Using JSONFileStorage (data persists)")


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__,
    docs_url="/docs",  # Swagger UI (default)
    redoc_url=None,  # Disable default ReDoc, we'll add custom one
    openapi_url="/openapi.json",  # OpenAPI spec (default)
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from typing import Annotated, Callable, ClassVar

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


# Custom ReDoc endpoint with explicit CDN version
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """Custom ReDoc documentation page."""
    return HTMLResponse(
        """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PromptLab API - ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        <redoc spec-url="/openapi.json"></redoc>
        <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
    </body>
    </html>
    """
    )


# ============== Health Check ==============


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check the health status of the API.

    Returns:
        HealthResponse: A response object containing the status and version of the API.
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============


@app.get("/prompts", response_model=PromptList)
def list_prompts(collection_id: Optional[str] = None, search: Optional[str] = None, tags: Optional[str] = None):
    """List all prompts with optional filtering and sorting.

    Args:
        collection_id (Optional[str]): ID of the collection to filter prompts by.
        search (Optional[str]): Search term for filtering prompts by title or content.
        tags (Optional[str]): Comma-separated list of tags to filter by (OR logic).

    Returns:
        PromptList: List of prompts and their total count.

    Raises:
        HTTPException: Raised with a status code 400 if any filter processing fails.
    """
    prompts = storage.get_all_prompts()

    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)

    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)

    # Filter by tags if specified
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",")]
        prompts = filter_by_tags(prompts, tag_list)

    # Sort by date (newest first)
    prompts = sort_prompts_by_date(prompts, descending=True)

    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a specific prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to retrieve.

    Returns:
        Prompt: The prompt object associated with the provided ID.

    Raises:
        HTTPException: Raised with status code 404 if the prompt is not found.
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.

    Args:
        prompt_data (PromptCreate): Data required to create a new prompt.

    Returns:
        Prompt: The newly created prompt object.

    Raises:
        HTTPException: Raised with status code 400 if the collection is not found.
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Update an existing prompt identified by its ID.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptUpdate): Updated data for the prompt.

    Returns:
        Prompt: The updated prompt with new information.

    Raises:
        HTTPException: Raised with status code 404 if the prompt is not found.
        HTTPException: Raised with status code 400 if the collection is not found.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Update the prompt with new timestamp
    updated_prompt = create_prompt_copy(
        existing=existing,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        tags=prompt_data.tags,
        update_timestamp=True,
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch):
    """Partially update a prompt identified by its ID.

    Only updates the fields that are provided in the request.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptPatch): Fields to update in the prompt.

    Returns:
        Prompt: The updated prompt object with merged data.

    Raises:
        HTTPException: Raised with status code 404 if the prompt is not found.
        HTTPException: Raised with status code 400 if the collection is not found.
    """
    # Get existing prompt
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Get the update data, excluding unset fields
    update_data = prompt_data.model_dump(exclude_unset=True)

    # Validate collection if provided
    if "collection_id" in update_data and update_data["collection_id"] is not None:
        collection = storage.get_collection(update_data["collection_id"])
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Create updated prompt by merging existing with updates
    updated_prompt = Prompt(
        id=existing.id,
        title=update_data.get("title", existing.title),
        content=update_data.get("content", existing.content),
        description=update_data.get("description", existing.description),
        collection_id=update_data.get("collection_id", existing.collection_id),
        created_at=existing.created_at,
        updated_at=get_current_time(),
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.put("/prompts/{prompt_id}/tags", response_model=Prompt)
def update_prompt_tags(prompt_id: str, tag_data: PromptTagUpdate):
    """Update only the tags of a specific prompt.

    This endpoint allows updating just the tags without requiring
    all other prompt fields. It's more convenient than PUT /prompts/{id}
    when you only want to change tags.

    Args:
        prompt_id (str): The ID of the prompt to update.
        tag_data (PromptTagUpdate): New tags for the prompt.

    Returns:
        Prompt: The updated prompt with new tags.

    Raises:
        HTTPException: Raised with status code 404 if the prompt is not found.

    Example:
        >>> PUT /prompts/abc123/tags {"tags": ["python", "ai"]}
        >>> # Returns prompt with updated tags
    """
    # Get existing prompt
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Create updated prompt with new tags
    updated_prompt = create_prompt_copy(existing=existing, tags=tag_data.tags, update_timestamp=True)

    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a specific prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to delete.

    Returns:
        None: Indicates successful deletion.

    Raises:
        HTTPException: Raised with status code 404 if the prompt is not found.
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============


@app.get("/collections", response_model=CollectionList)
def list_collections():
    """List all collections.

    Returns:
        CollectionList: A list of all collections and their total count.
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a specific collection by its ID.

    Args:
        collection_id (str): The ID of the collection to retrieve.

    Returns:
        Collection: The collection object associated with the provided ID.

    Raises:
        HTTPException: Raised with status code 404 if the collection is not found.
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    Args:
        collection_data (CollectionCreate): Data required to create a new collection.

    Returns:
        Collection: The newly created collection object.
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a specific collection by its ID.

    Also handles prompt adjustments to remove collection references.

    Args:
        collection_id (str): The ID of the collection to delete.

    Returns:
        None: Indicates successful deletion.

    Raises:
        HTTPException: Raised with status code 404 if the collection is not found.
    """
    # Check if collection exists
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # Strategy: SET NULL - Set collection_id to None for all prompts in this collection
    prompts_in_collection = storage.get_prompts_by_collection(collection_id)
    nullify_collection_for_prompts(prompts_in_collection, storage)

    # Now delete the collection
    storage.delete_collection(collection_id)
    return None


# ============== Tag Endpoints ==============


@app.post("/tags", response_model=Tag)
def create_tag(tag_data: TagCreate, response: Response):
    """Create a new tag or return existing tag if name already exists.

    Tags are unique by name. If a tag with the same name already exists,
    this endpoint returns the existing tag instead of creating a duplicate.
    This is similar to "get or create" pattern in ORMs.

    Args:
        tag_data (TagCreate): Data required to create a new tag.
        response (Response): FastAPI response object to set status code.

    Returns:
        Tag: The newly created tag object or existing tag.

    Example:
        >>> # First call creates new tag
        >>> POST /tags {"name": "python"}
        >>> # Returns: {"tag_id": "abc123", "name": "python", ...}
        >>>
        >>> # Second call with same name returns existing tag
        >>> POST /tags {"name": "python"}
        >>> # Returns: {"tag_id": "abc123", "name": "python", ...}
    """
    # Check if tag already exists
    existing_tag = storage.get_tag_by_name(tag_data.name)
    if existing_tag:
        # Return existing tag with 200 status
        response.status_code = 200
        return existing_tag

    # Create new tag
    tag = Tag(**tag_data.model_dump())
    response.status_code = 201
    return storage.create_tag(tag)


@app.get("/tags", response_model=TagList)
def list_tags():
    """List all tags.

    Returns all tags in the system. Tags can be used to categorize
    and organize prompts flexibly.

    Returns:
        TagList: A list of all tags and their total count.

    Example:
        >>> GET /tags
        >>> # Returns: {"tags": [...], "total": 5}
    """
    tags = storage.get_all_tags()
    return TagList(tags=tags, total=len(tags))


@app.get("/tags/{tag_id}", response_model=Tag)
def get_tag(tag_id: str):
    """Retrieve a specific tag by its ID.

    Args:
        tag_id (str): The ID of the tag to retrieve.

    Returns:
        Tag: The tag object associated with the provided ID.

    Raises:
        HTTPException: Raised with status code 404 if the tag is not found.

    Example:
        >>> GET /tags/abc123
        >>> # Returns: {"tag_id": "abc123", "name": "python", ...}
    """
    tag = storage.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag
