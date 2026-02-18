# Prompt Versioning Feature Specification

## Overview

The Prompt Versioning feature aims to allow users to track changes in their prompts over time. This will include the ability to view previous versions of a prompt, compare changes, and possibly revert to an older version. The feature is intended to enhance usability by providing authors the flexibility to maintain and refine their prompt content history.

## Data Model Diagram

```mermaid
classDiagram
    class Prompt {
        +str id
        +str title
        +str content
        +Optional~str~ description
        +Optional~str~ collection_id
        +int current_version
        +datetime created_at
        +datetime updated_at
    }
    
    class PromptVersion {
        +str version_id
        +str prompt_id FK
        +int version_number
        +str title
        +str content
        +Optional~str~ description
        +str change_summary
        +datetime created_at
        +str created_by
    }
    
    class Collection {
        +str id
        +str name
        +Optional~str~ description
        +datetime created_at
    }
    
    Prompt "1" --o "*" PromptVersion : has versions
    PromptVersion "*" --> "1" Prompt : belongs to
    Prompt "*" --> "0..1" Collection : belongs to
    
    note for Prompt "current_version tracks\nactive version number"
    note for PromptVersion "Immutable history record\nNever deleted or modified"
```

### Version Tracking Strategy

```mermaid
graph LR
    A[Prompt Created] -->|v1| B[PromptVersion 1]
    A -->|current_version=1| A
    
    C[Prompt Updated] -->|v2| D[PromptVersion 2]
    C -->|current_version=2| C
    
    E[Prompt Updated] -->|v3| F[PromptVersion 3]
    E -->|current_version=3| E
    
    G[Revert to v2] -->|copy v2 data| H[Prompt Updated]
    H -->|v4 snapshot of v2| I[PromptVersion 4]
    H -->|current_version=4| H
    
    style B fill:#e1f5ff
    style D fill:#e1f5ff
    style F fill:#e1f5ff
    style I fill:#ffe1e1
    
    note1[All versions preserved]
    note2[Revert creates new version]
```

## User Stories

### User Story 1: View Prompt Versions

As a user, I want to be able to see all versions of a prompt so that I can track its history and changes.

**Acceptance Criteria**:
- Users can access a list of all past versions of a specific prompt.
- Each version displays key details such as version number, date modified, and changes made.

### User Story 2: Revert to Previous Version

As a user, I want to revert to a previous version of a prompt so that I can undo changes if necessary.

**Acceptance Criteria**:
- Users can select a previous prompt version and set it as the current version.
- The system confirms the successful restoration of the selected version.

## API Flow Diagrams

### Get All Versions Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Storage
    
    Client->>API: GET /prompts/{prompt_id}/versions
    API->>Storage: get_prompt(prompt_id)
    
    alt Prompt Not Found
        Storage-->>API: None
        API-->>Client: 404 Not Found
    else Prompt Found
        API->>Storage: get_prompt_versions(prompt_id)
        Storage->>Storage: Query versions by prompt_id
        Storage->>Storage: Sort by version_number DESC
        Storage-->>API: List of PromptVersion
        API-->>Client: 200 OK + VersionList
    end
```

### Revert to Previous Version Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Storage
    
    Client->>API: POST /prompts/{prompt_id}/versions/{version_id}/revert
    API->>Storage: get_prompt(prompt_id)
    
    alt Prompt Not Found
        Storage-->>API: None
        API-->>Client: 404 Not Found
    else Prompt Exists
        API->>Storage: get_version(version_id)
        
        alt Version Not Found
            Storage-->>API: None
            API-->>Client: 404 Version Not Found
        else Version Exists
            API->>API: Check if version belongs to prompt
            
            alt Version Mismatch
                API-->>Client: 400 Bad Request
            else Valid Revert
                API->>Storage: Create new version from current state
                Storage->>Storage: Save current as new version
                API->>Storage: Update prompt with version data
                Storage->>Storage: Copy title, content, description
                Storage->>Storage: Increment current_version
                Storage->>Storage: Update updated_at timestamp
                Storage-->>API: Updated prompt
                API-->>Client: 200 OK + Prompt
            end
        end
    end
```

### Create Version on Update Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Storage
    
    Client->>API: PUT /prompts/{prompt_id}
    API->>Storage: get_prompt(prompt_id)
    
    alt Prompt Not Found
        Storage-->>API: None
        API-->>Client: 404 Not Found
    else Prompt Found
        API->>Storage: create_version_snapshot(prompt)
        Note over Storage: Save current state<br/>before updating
        Storage->>Storage: Create PromptVersion
        Storage->>Storage: version_number = current_version
        Storage->>Storage: Copy current data
        Storage-->>API: Version created
        
        API->>Storage: update_prompt(prompt_id, new_data)
        Storage->>Storage: Update prompt fields
        Storage->>Storage: Increment current_version
        Storage->>Storage: Update updated_at
        Storage-->>API: Updated prompt
        
        API-->>Client: 200 OK + Prompt
    end
```

## Data Model Changes

To support prompt versioning, we need to modify and extend the existing data models as follows:

1. **New Model: `PromptVersion`**
   - **Attributes**:
     - `version_id`: Unique identifier for version
     - `prompt_id`: Foreign key linking to the parent prompt
     - `title`: Title of the prompt version
     - `content`: Content of the prompt version
     - `description`: Optional description of the prompt version
     - `created_at`: Timestamp of when the version was created

2. **Update to Existing `Prompt` Model**
   - Add a relation to `PromptVersion` to enable tracking of multiple versions linked to a single prompt.

## API Endpoint Specifications

### Endpoint 1: GET `/prompts/{prompt_id}/versions`

- **Description**: Retrieve all versions of a specific prompt.
- **Request Parameters**: 
  - `prompt_id`: ID of the prompt for which to retrieve versions.
- **Response**:
  ```json
  {
    "versions": [
      {
        "version_id": "string",
        "title": "Version Title",
        "content": "Version Content",
        "description": "Optional Description",
        "created_at": "2023-10-12T10:00:00Z"
      },
      ...
    ],
    "total": 5
  }
  ```

### Endpoint 2: POST `/prompts/{prompt_id}/versions/{version_id}/revert`

- **Description**: Revert a specific prompt to a selected version.
- **Request Parameters**: 
  - `prompt_id`: ID of the prompt to revert.
  - `version_id`: ID of the version to revert to.
- **Response**: 
  - **200 OK**: Confirmation of successful reversion.
  - **Error 404**: If the prompt or version is not found.
  - **Error 409**: If the provided version is already the current prompt version.

## Edge Cases to Handle

1. **Concurrent Modifications**: Ensure that the prompt is not updated concurrently while a reversion attempt is occurring.
2. **Version Limits**: Decide on a policy for how many versions to retain (e.g., maximum number of past versions or a time-based retention).
3. **Data Integrity**: Ensure that reverting to a past version correctly updates references and does not disrupt other dependent data relationships.
4. **Reversion Confirmation**: Provide a confirmation step to users before making irreversible reversion changes.

## Implementation Guide

### Database Schema

```mermaid
erDiagram
    PROMPT ||--o{ PROMPT_VERSION : has
    PROMPT }o--|| COLLECTION : belongs_to
    
    PROMPT {
        string id PK
        string title
        string content
        string description
        string collection_id FK
        int current_version
        datetime created_at
        datetime updated_at
    }
    
    PROMPT_VERSION {
        string version_id PK
        string prompt_id FK
        int version_number
        string title
        string content
        string description
        string change_summary
        datetime created_at
    }
    
    COLLECTION {
        string id PK
        string name
        string description
        datetime created_at
    }
```

### Version Lifecycle States

```mermaid
stateDiagram-v2
    [*] --> V1_Created: Prompt Created
    V1_Created --> V1_Active: Version 1 Snapshot
    
    V1_Active --> V2_Created: Prompt Updated
    V2_Created --> V2_Active: Version 2 Snapshot
    V1_Active --> V1_Historical: Version 2 Active
    
    V2_Active --> V3_Created: Prompt Updated
    V3_Created --> V3_Active: Version 3 Snapshot
    V2_Active --> V2_Historical: Version 3 Active
    
    V2_Historical --> V4_Created: Revert to V2
    V4_Created --> V4_Active: Version 4 (Copy of V2)
    V3_Active --> V3_Historical: Version 4 Active
    
    note right of V1_Historical
        All versions preserved
        Never deleted
    end note
    
    note right of V4_Active
        Revert creates new version
        Does not modify history
    end note
```

### Pydantic Model Updates

```mermaid
classDiagram
    class PromptBase {
        +str title
        +str content
        +Optional~str~ description
        +Optional~str~ collection_id
    }
    
    class Prompt {
        +str id
        +int current_version
        +datetime created_at
        +datetime updated_at
    }
    
    class PromptVersionBase {
        +str title
        +str content
        +Optional~str~ description
        +Optional~str~ change_summary
    }
    
    class PromptVersion {
        +str version_id
        +str prompt_id
        +int version_number
        +datetime created_at
    }
    
    class PromptVersionList {
        +List~PromptVersion~ versions
        +int total
    }
    
    class RevertRequest {
        +str version_id
    }
    
    PromptBase <|-- Prompt
    PromptVersionBase <|-- PromptVersion
    PromptVersion --o PromptVersionList
    
    note for Prompt "Add current_version field"
    note for PromptVersion "New model for version history"
    note for RevertRequest "Request body for revert endpoint"
```

### Implementation Steps

```mermaid
graph TD
    A[Step 1: Update Models] --> B[Step 2: Update Storage]
    B --> C[Step 3: Add Version Endpoints]
    C --> D[Step 4: Modify Update Logic]
    D --> E[Step 5: Add Utils Functions]
    E --> F[Step 6: Write Tests]
    
    A --> A1[Add PromptVersion model]
    A --> A2[Add current_version to Prompt]
    A --> A3[Add PromptVersionList model]
    
    B --> B1[Add _prompt_versions dict]
    B --> B2[Add create_version_snapshot]
    B --> B3[Add get_prompt_versions]
    B --> B4[Add get_version]
    
    C --> C1[GET /prompts/id/versions]
    C --> C2[GET /prompts/id/versions/version_id]
    C --> C3[POST /prompts/id/versions/version_id/revert]
    
    D --> D1[Modify update_prompt to create version]
    D --> D2[Modify patch_prompt to create version]
    D --> D3[Initialize current_version on create]
    
    E --> E1[compare_versions function]
    E --> E2[calculate_diff function]
    E --> E3[validate_revert function]
    
    F --> F1[Test version creation on update]
    F --> F2[Test get versions list]
    F --> F3[Test revert functionality]
    F --> F4[Test edge cases]
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e1ffe1
    style D fill:#ffe1f5
    style E fill:#f5e1ff
    style F fill:#ffe1e1
```

### Storage Layer Changes

```mermaid
graph TB
    subgraph "Storage Class"
        A[_prompts: Dict]
        B[_collections: Dict]
        C[_prompt_versions: Dict]
    end
    
    subgraph "New Methods"
        D[create_version_snapshot]
        E[get_prompt_versions]
        F[get_version]
        G[revert_to_version]
    end
    
    subgraph "Modified Methods"
        H[create_prompt]
        I[update_prompt]
        J[patch_prompt]
    end
    
    C --> D
    C --> E
    C --> F
    C --> G
    
    A --> H
    A --> I
    A --> J
    
    H -->|Initialize version 1| D
    I -->|Create snapshot before update| D
    J -->|Create snapshot before patch| D
    
    style C fill:#ffe1e1
    style D fill:#e1ffe1
    style E fill:#e1ffe1
    style F fill:#e1ffe1
    style G fill:#e1ffe1
```

### Version Comparison Feature

```mermaid
graph LR
    A[Version A] --> C[Diff Calculator]
    B[Version B] --> C
    
    C --> D[Title Changes]
    C --> E[Content Changes]
    C --> F[Description Changes]
    
    D --> G[Diff Result]
    E --> G
    F --> G
    
    G --> H[Display to User]
    
    style C fill:#e1f5ff
    style G fill:#e1ffe1
```

## Testing Strategy

```mermaid
mindmap
    root((Version Tests))
        Version Creation
            Create on prompt update
            Create on prompt patch
            Version number increments
            Snapshot accuracy
        Version Retrieval
            Get all versions
            Get specific version
            Sort by version number
            Empty version list
        Revert Functionality
            Revert to previous version
            Revert creates new version
            Version number increments
            Cannot revert to non-existent
        Edge Cases
            Concurrent updates
            Revert to current version
            Invalid version ID
            Prompt not found
            Version limit enforcement
        Data Integrity
            All fields copied correctly
            Timestamps preserved
            Relationships maintained
            No data loss
```

## Performance Considerations

```mermaid
graph TB
    A[Version Storage] --> B{Scale}
    
    B -->|Small Scale| C[In-Memory OK]
    B -->|Large Scale| D[Optimization Needed]
    
    C --> C1[Dict lookups: O 1]
    C --> C2[Version list: O n]
    C --> C3[Good for < 100 versions/prompt]
    
    D --> D1[Add version limit per prompt]
    D --> D2[Archive old versions]
    D --> D3[Compress version content]
    D --> D4[Index by prompt_id]
    
    style C fill:#ccffcc
    style D fill:#ffffcc
```

### Version Retention Policy

```mermaid
graph LR
    A[New Version Created] --> B{Check Version Count}
    
    B -->|Under Limit| C[Store Version]
    B -->|At Limit| D[Apply Retention Policy]
    
    D --> E[Keep Recent N Versions]
    D --> F[Archive Older Versions]
    D --> G[Delete Oldest Version]
    
    C --> H[Version Stored]
    E --> H
    F --> I[Archived Storage]
    G --> J[Version Removed]
    
    style C fill:#ccffcc
    style F fill:#ffffcc
    style G fill:#ffcccc
```

## Future Enhancements

- **Version Comparison UI**: Side-by-side diff view showing changes between versions
- **Version Branching**: Create alternate versions without affecting main history
- **Version Tags**: Label important versions (e.g., "production", "tested")
- **Bulk Revert**: Revert multiple prompts to specific date/time
- **Version Comments**: Add notes explaining why changes were made
- **Change Tracking**: Track who made changes (requires authentication)
- **Automatic Versioning**: Configure when to create versions (every save vs manual)
- **Version Export**: Download version history as JSON/CSV

---

**Implementation Priority**: High  
**Estimated Effort**: 12-16 hours  
**Dependencies**: None (extends existing Prompt model)  
**Breaking Changes**: None (additive feature, adds current_version field)

---


This specification captures the essential details needed to implement the prompt versioning feature. It blends both technical requirements and user interaction considerations to ensure smooth development and deployment.