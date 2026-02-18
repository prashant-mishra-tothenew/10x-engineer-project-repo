"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate, PromptPatch,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__

# Use file storage by default for development
# Tests will override this with in-memory storage
from app.json_file_storage import JSONFileStorage
storage = JSONFileStorage()
print("📁 Using JSONFileStorage (data persists)")


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__,
    docs_url="/docs",      # Swagger UI (default)
    redoc_url=None,        # Disable default ReDoc, we'll add custom one
    openapi_url="/openapi.json"  # OpenAPI spec (default)
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom ReDoc endpoint with explicit CDN version
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """Custom ReDoc documentation page."""
    return HTMLResponse("""
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
    """)


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
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """List all prompts with optional filtering and sorting.
    
    Args:
        collection_id (Optional[str]): ID of the collection to filter prompts by.
        search (Optional[str]): Search term for filtering prompts by title or content.

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
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
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
        updated_at=get_current_time()
    )
    
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
    for prompt in prompts_in_collection:
        # Update each prompt to remove collection reference
        updated_prompt = Prompt(
            id=prompt.id,
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            collection_id=None,  # Remove collection reference
            created_at=prompt.created_at,
            updated_at=prompt.updated_at
        )
        storage.update_prompt(prompt.id, updated_prompt)
    
    # Now delete the collection
    storage.delete_collection(collection_id)
    return None