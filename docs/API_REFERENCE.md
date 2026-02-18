# API Documentation for PromptLab

This document provides an overview of the API endpoints available in the PromptLab application.

## General Information

- **Base URL**: `http://localhost:8000`
- **Authentication**: None (for now)

## Endpoints

### Health Check

#### Check API Health

- **HTTP Method**: GET
- **Path**: `/health`
- **Description**: Checks the health status of the API.
- **Parameters**: None
- **Response**:
  ```json
  {
    "status": "healthy",
    "version": "1.0.0"
  }
  ```

### Prompts

#### List Prompts

- **HTTP Method**: GET
- **Path**: `/prompts`
- **Description**: Retrieves a list of all prompts with optional filtering and sorting.
- **Parameters**:
  - `collection_id` (query parameter): Optional collection ID to filter prompts.
  - `search` (query parameter): Optional search term to filter prompts by title or content.
- **Response**:
  ```json
  {
    "prompts": [
      {
        "id": "string",
        "title": "Prompt Title",
        "content": "Prompt Content",
        "description": "Optional description",
        "collection_id": "string",
        "created_at": "2023-10-12T10:00:00Z",
        "updated_at": "2023-10-12T10:00:00Z"
      }
    ],
    "total": 1
  }
  ```

#### Get Prompt by ID

- **HTTP Method**: GET
- **Path**: `/prompts/{prompt_id}`
- **Description**: Retrieves a specific prompt by its ID.
- **Parameters**:
  - `prompt_id` (path parameter): The ID of the prompt to retrieve.
- **Response**:
  ```json
  {
    "id": "string",
    "title": "Prompt Title",
    "content": "Prompt Content",
    "description": "Optional description",
    "collection_id": "string",
    "created_at": "2023-10-12T10:00:00Z",
    "updated_at": "2023-10-12T10:00:00Z"
  }
  ```
- **Error Responses**:
  - **404 Not Found**: Prompt not found.
  ```json
  {
    "detail": "Prompt not found"
  }
  ```

#### Create Prompt

- **HTTP Method**: POST
- **Path**: `/prompts`
- **Description**: Creates a new prompt.
- **Parameters**: None
- **Request**:
  ```json
  {
    "title": "New Prompt Title",
    "content": "New prompt content",
    "description": "Optional description",
    "collection_id": "string"
  }
  ```
- **Response**:
  ```json
  {
    "id": "string",
    "title": "New Prompt Title",
    "content": "New prompt content",
    "description": "Optional description",
    "collection_id": "string",
    "created_at": "2023-10-12T10:00:00Z",
    "updated_at": "2023-10-12T10:00:00Z"
  }
  ```
- **Error Responses**:
  - **400 Bad Request**: Collection not found.
  ```json
  {
    "detail": "Collection not found"
  }
  ```

#### Update Prompt

- **HTTP Method**: PUT
- **Path**: `/prompts/{prompt_id}`
- **Description**: Updates an existing prompt by its ID.
- **Parameters**:
  - `prompt_id` (path parameter): The ID of the prompt to update.
- **Request**:
  ```json
  {
    "title": "Updated Prompt Title",
    "content": "Updated prompt content",
    "description": "Updated description",
    "collection_id": "string"
  }
  ```
- **Response**:
  ```json
  {
    "id": "string",
    "title": "Updated Prompt Title",
    "content": "Updated prompt content",
    "description": "Updated description",
    "collection_id": "string",
    "created_at": "2023-10-12T10:00:00Z",
    "updated_at": "2023-10-12T10:00:00Z"
  }
  ```
- **Error Responses**:
  - **404 Not Found**: Prompt not found.
  - **400 Bad Request**: Collection not found.

#### Patch Prompt

- **HTTP Method**: PATCH
- **Path**: `/prompts/{prompt_id}`
- **Description**: Partially updates a prompt by its ID.
- **Parameters**:
  - `prompt_id` (path parameter): The ID of the prompt to update.
- **Request**:
  ```json
  {
    "title": "Optional new title",
    "content": "Optional new content"
  }
  ```
- **Response**:
  ```json
  {
    "id": "string",
    "title": "Updated Prompt Title",
    "content": "Updated prompt content",
    "description": "Updated description",
    "collection_id": "string",
    "created_at": "2023-10-12T10:00:00Z",
    "updated_at": "2023-10-12T10:00:00Z"
  }
  ```
- **Error Responses**:
  - **404 Not Found**: Prompt not found.
  - **400 Bad Request**: Collection not found.

#### Delete Prompt

- **HTTP Method**: DELETE
- **Path**: `/prompts/{prompt_id}`
- **Description**: Deletes a specific prompt by its ID.
- **Parameters**:
  - `prompt_id` (path parameter): The ID of the prompt to delete.
- **Response**: None
- **Error Responses**:
  - **404 Not Found**: Prompt not found.

### Collections

#### List Collections

- **HTTP Method**: GET
- **Path**: `/collections`
- **Description**: Retrieves a list of all collections.
- **Parameters**: None
- **Response**:
  ```json
  {
    "collections": [
      {
        "id": "string",
        "name": "Collection Name",
        "description": "Collection description",
        "created_at": "2023-10-12T10:00:00Z"
      }
    ],
    "total": 1
  }
  ```

#### Get Collection by ID

- **HTTP Method**: GET
- **Path**: `/collections/{collection_id}`
- **Description**: Retrieves a specific collection by its ID.
- **Parameters**:
  - `collection_id` (path parameter): The ID of the collection to retrieve.
- **Response**:
  ```json
  {
    "id": "string",
    "name": "Collection Name",
    "description": "Collection description",
    "created_at": "2023-10-12T10:00:00Z"
  }
  ```
- **Error Responses**:
  - **404 Not Found**: Collection not found.

#### Create Collection

- **HTTP Method**: POST
- **Path**: `/collections`
- **Description**: Creates a new collection.
- **Parameters**: None
- **Request**:
  ```json
  {
    "name": "New Collection Name",
    "description": "New collection description"
  }
  ```
- **Response**:
  ```json
  {
    "id": "string",
    "name": "New Collection Name",
    "description": "New collection description",
    "created_at": "2023-10-12T10:00:00Z"
  }