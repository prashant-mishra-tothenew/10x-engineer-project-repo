# Tagging System Feature Specification

## Overview

The Tagging System feature introduces the ability to associate tags with prompts. Tags allow users to categorize and organize prompts flexibly, facilitating better searchability and management. By enabling tagging, users can more easily filter and discover prompts relevant to specific themes or topics.

## Data Model Diagram

```mermaid
classDiagram
    class Prompt {
        +str id
        +str title
        +str content
        +Optional~str~ description
        +Optional~str~ collection_id
        +List~str~ tags
        +datetime created_at
        +datetime updated_at
    }
    
    class Tag {
        +str tag_id
        +str name
        +datetime created_at
    }
    
    class Collection {
        +str id
        +str name
        +Optional~str~ description
        +datetime created_at
    }
    
    class PromptTag {
        <<Association Table>>
        +str prompt_id FK
        +str tag_id FK
        +datetime tagged_at
    }
    
    Prompt "1" --o "*" PromptTag : has
    Tag "1" --o "*" PromptTag : used in
    PromptTag "*" --o "1" Prompt : belongs to
    PromptTag "*" --o "1" Tag : references
    
    Prompt "*" --> "0..1" Collection : belongs to
    
    note for Prompt "Updated to include tags array\nMany-to-many relationship with Tag"
    note for Tag "New model for tagging system\nReusable across prompts"
    note for PromptTag "Junction table for many-to-many\nTracks when tag was added"
```

### Relationship Details

- **Prompt ↔ Tag**: Many-to-many relationship
  - One prompt can have multiple tags
  - One tag can be used by multiple prompts
  - Implemented via `PromptTag` association table
  
- **Prompt → Collection**: Many-to-one relationship (existing)
  - One prompt belongs to zero or one collection
  - One collection can contain multiple prompts

## User Stories

### User Story 1: Add Tags to Prompts

**As a user, I want to tag my prompts with relevant keywords so that I can categorize them for easy retrieval and organization.**

**Acceptance Criteria:**
- Users can assign multiple tags to a prompt at the time of creation or update.
- Tags are displayed alongside prompts to provide immediate context.

### User Story 2: Search by Tags

**As a user, I want to search for prompts by tags so that I can quickly find prompts related to specific themes.**

**Acceptance Criteria:**
- Users can input tags in a search bar to fetch prompts containing those tags.
- Search results display prompts ranked by relevance to the queried tags.

## Data Model Changes

To support tagging functionality, we propose the following data model changes:

1. **New Model: `Tag`**
   - **Attributes:**
     - `tag_id`: Unique identifier for the tag.
     - `name`: The textual name of the tag.

2. **Update to Existing `Prompt` Model**
   - Add a many-to-many relationship with the `Tag` model to link multiple tags to a single prompt.

## API Flow Diagrams

### Create Tag Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Storage
    
    Client->>API: POST /tags {"name": "python"}
    API->>API: Validate tag name
    
    alt Tag Already Exists
        API->>Storage: Check if tag exists
        Storage-->>API: Tag found
        API-->>Client: 200 OK (existing tag)
    else New Tag
        API->>Storage: Create new tag
        Storage->>Storage: Generate tag_id
        Storage->>Storage: Set created_at
        Storage-->>API: Tag created
        API-->>Client: 201 Created + Tag
    end
```

### Add Tags to Prompt Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Storage
    
    Client->>API: PUT /prompts/{id}/tags {"tags": ["python", "ai"]}
    API->>Storage: Get prompt by ID
    
    alt Prompt Not Found
        Storage-->>API: None
        API-->>Client: 404 Not Found
    else Prompt Found
        API->>Storage: Validate/Create tags
        Storage->>Storage: Get or create each tag
        API->>Storage: Update prompt tags
        Storage->>Storage: Clear existing associations
        Storage->>Storage: Create new associations
        Storage->>Storage: Update prompt.updated_at
        Storage-->>API: Updated prompt with tags
        API-->>Client: 200 OK + Prompt
    end
```

### Search by Tags Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Storage
    participant Utils
    
    Client->>API: GET /prompts?tags=python,ai
    API->>API: Parse tags parameter
    API->>Storage: Get all prompts
    Storage-->>API: All prompts
    
    API->>Utils: filter_by_tags(prompts, ["python", "ai"])
    Utils->>Utils: Check each prompt's tags
    Utils->>Utils: Match ANY tag (OR logic)
    Utils-->>API: Filtered prompts
    
    API->>Utils: sort_by_relevance(prompts, tags)
    Note over Utils: Prompts with more matching<br/>tags ranked higher
    Utils-->>API: Sorted prompts
    
    API-->>Client: 200 OK + PromptList
```

## API Endpoint Specifications

### Endpoint 1: POST `/tags`

- **Description**: Create a new tag.
- **Request**:
  ```json
  {
    "name": "TagName"
  }
  ```
- **Response**:
  ```json
  {
    "tag_id": "string",
    "name": "TagName"
  }
  ```

### Endpoint 2: GET `/prompts?tags=tag1,tag2,...`

- **Description**: Retrieve prompts filtered by associated tags.
- **Request Parameters**: 
  - `tags` (query parameter): Comma-separated list of tag names to filter prompts.
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
        "tags": ["Tag1", "Tag2"],
        "created_at": "2023-10-12T10:00:00Z",
        "updated_at": "2023-10-12T10:00:00Z"
      }
    ],
    "total": 1
  }
  ```

### Endpoint 3: PUT `/prompts/{prompt_id}/tags`

- **Description**: Update tags associated with a specific prompt.
- **Request**:
  ```json
  {
    "tags": ["NewTag1", "NewTag2"]
  }
  ```
- **Response**:
  ```json
  {
    "id": "string",
    "title": "Prompt Title",
    "content": "Prompt Content",
    "description": "Optional description",
    "collection_id": "string",
    "tags": ["NewTag1", "NewTag2"],
    "created_at": "2023-10-12T10:00:00Z",
    "updated_at": "2023-10-12T10:00:00Z"
  }


## Implementation Guide

### Database Schema Changes

```mermaid
erDiagram
    PROMPT ||--o{ PROMPT_TAG : has
    TAG ||--o{ PROMPT_TAG : used_in
    PROMPT }o--|| COLLECTION : belongs_to
    
    PROMPT {
        string id PK
        string title
        string content
        string description
        string collection_id FK
        datetime created_at
        datetime updated_at
    }
    
    TAG {
        string tag_id PK
        string name UK "Unique"
        datetime created_at
    }
    
    PROMPT_TAG {
        string prompt_id FK
        string tag_id FK
        datetime tagged_at
    }
    
    COLLECTION {
        string id PK
        string name
        string description
        datetime created_at
    }
```

### Pydantic Model Updates

```mermaid
classDiagram
    class TagBase {
        +str name
    }
    
    class TagCreate {
        <<Create>>
    }
    
    class Tag {
        +str tag_id
        +datetime created_at
    }
    
    class PromptBase {
        +str title
        +str content
        +Optional~str~ description
        +Optional~str~ collection_id
        +List~str~ tags
    }
    
    class PromptCreate {
        <<Create>>
    }
    
    class PromptUpdate {
        <<Update>>
    }
    
    class Prompt {
        +str id
        +datetime created_at
        +datetime updated_at
    }
    
    class PromptTagUpdate {
        +List~str~ tags
    }
    
    TagBase <|-- TagCreate
    TagBase <|-- Tag
    PromptBase <|-- PromptCreate
    PromptBase <|-- PromptUpdate
    PromptBase <|-- Prompt
    
    note for PromptBase "Add tags: List[str] = []"
    note for Tag "New model"
    note for PromptTagUpdate "Dedicated model for tag updates"
```

### Implementation Steps

```mermaid
graph TD
    A[Step 1: Update Models] --> B[Step 2: Update Storage]
    B --> C[Step 3: Add Tag Endpoints]
    C --> D[Step 4: Update Prompt Endpoints]
    D --> E[Step 5: Add Utils Functions]
    E --> F[Step 6: Write Tests]
    
    A --> A1[Add Tag model in models.py]
    A --> A2[Add tags field to PromptBase]
    A --> A3[Add PromptTagUpdate model]
    
    B --> B1[Add _tags dict to Storage]
    B --> B2[Add _prompt_tags dict for associations]
    B --> B3[Add CRUD methods for tags]
    
    C --> C1[POST /tags - Create tag]
    C --> C2[GET /tags - List all tags]
    C --> C3[GET /tags/tag_id - Get tag]
    
    D --> D1[Update POST /prompts - Accept tags]
    D --> D2[Update PUT /prompts/id - Accept tags]
    D --> D3[Add PUT /prompts/id/tags - Update tags only]
    D --> D4[Update GET /prompts - Filter by tags]
    
    E --> E1[filter_by_tags function]
    E --> E2[sort_by_tag_relevance function]
    E --> E3[get_popular_tags function]
    
    F --> F1[Test tag CRUD operations]
    F --> F2[Test prompt with tags]
    F --> F3[Test tag filtering]
    F --> F4[Test tag search]
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e1ffe1
    style D fill:#ffe1f5
    style E fill:#f5e1ff
    style F fill:#ffe1e1
```

### Code Structure Changes

```mermaid
graph LR
    subgraph "models.py"
        M1[Tag Models]
        M2[Updated Prompt Models]
    end
    
    subgraph "storage.py"
        S1[Tag Storage]
        S2[PromptTag Associations]
        S3[Updated Prompt Methods]
    end
    
    subgraph "api.py"
        A1[Tag Endpoints]
        A2[Updated Prompt Endpoints]
    end
    
    subgraph "utils.py"
        U1[filter_by_tags]
        U2[sort_by_relevance]
    end
    
    M1 --> S1
    M2 --> S3
    S1 --> A1
    S2 --> A1
    S3 --> A2
    U1 --> A2
    U2 --> A2
    
    style M1 fill:#e1ffe1
    style M2 fill:#e1ffe1
    style S1 fill:#fff4e1
    style S2 fill:#fff4e1
    style S3 fill:#fff4e1
    style A1 fill:#e1f5ff
    style A2 fill:#e1f5ff
    style U1 fill:#f5e1ff
    style U2 fill:#f5e1ff
```

## Testing Strategy

### Test Coverage Requirements

```mermaid
mindmap
    root((Tag System Tests))
        Tag CRUD
            Create tag
            Get tag by ID
            List all tags
            Duplicate tag handling
        Prompt with Tags
            Create prompt with tags
            Update prompt tags
            Remove all tags
            Invalid tag handling
        Tag Filtering
            Filter by single tag
            Filter by multiple tags
            OR logic vs AND logic
            Empty results
        Tag Search
            Search prompts by tag
            Relevance ranking
            Case sensitivity
            Partial matches
        Edge Cases
            Non-existent tags
            Empty tag list
            Special characters in tags
            Very long tag names
```

## Performance Considerations

```mermaid
graph TB
    A[Tag Operations] --> B{Optimization Needed?}
    
    B -->|Small Scale| C[Current In-Memory OK]
    B -->|Large Scale| D[Database Required]
    
    C --> C1[Dict lookups: O 1]
    C --> C2[Tag filtering: O n]
    C --> C3[Good for < 10k prompts]
    
    D --> D1[Add indexes on tag_name]
    D --> D2[Add indexes on prompt_tags]
    D --> D3[Consider full-text search]
    D --> D4[Cache popular tags]
    
    style C fill:#ccffcc
    style D fill:#ffffcc
```

## Future Enhancements

- **Tag Autocomplete**: Suggest existing tags as user types
- **Tag Analytics**: Show most popular tags, tag usage over time
- **Tag Hierarchies**: Parent/child tag relationships (e.g., "python" → "python-3.10")
- **Tag Synonyms**: Map similar tags (e.g., "ML" → "machine-learning")
- **Tag Colors**: Visual categorization with color coding
- **Tag Permissions**: Control who can create/use certain tags

---

**Implementation Priority**: Medium  
**Estimated Effort**: 8-12 hours  
**Dependencies**: None (extends existing Prompt model)  
**Breaking Changes**: None (additive feature)
