# PromptLab API

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

## Project Overview and Purpose

PromptLab is a comprehensive AI-driven platform designed to facilitate the creation and management of prompts. The application consists of a backend built with FastAPI and a placeholder for a frontend with plans for future implementation. The goal is to streamline prompt engineering processes, enabling developers and writers to efficiently manage prompt collections and their contents.

### Backend

- **Framework**: Built using FastAPI, ensuring fast performance and scalability.
- **Storage**: Currently utilizes in-memory and JSON file storage, with potential extensions to other databases.

### Frontend

- **Current Status**: Planned development. The directory is prepared for future implementation.
- **Technologies**: Suggestions include React.js or Vue.js for seamless integration with FastAPI backend.

## Features List

- **Prompt Management**: Full CRUD operations for prompts.
- **Collection Organization**: Group prompts into collections.
- **Interactive API Documentation**: Seamless exploration via Swagger UI.
- **Asynchronous Calls**: FastAPI leverages asynchronous operations for efficient request handling.

## Project Structure

```
project-root/
│
├── backend/
│   ├── app/
│   │   ├── models.py
│   │   ├── api.py
│   │   ├── utils.py
│   │   ├── storage.py
│   │   └── json_file_storage.py
│   ├── tests/
│   ├── requirements.txt
│   └── main.py
│
├── frontend/
│   └── .gitkeep (Placeholder for future code)
│
├── docs/
├── specs/
└── README.md
```

## Prerequisites and Installation

### Prerequisites

- Python 3.11 or newer
- `pip` package manager

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/10x-engineer-project-repo.git
   cd 10x-engineer-project-repo/backend
   ```

2. **Set Up Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Quick Start Guide

1. **Start the API Server**:

   ```bash
   uvicorn app.api:app --reload
   ```

2. **Access API Documentation**:

   Open `http://127.0.0.1:8000/docs` in a browser for the interactive Swagger UI.

## API Endpoint Summary

### Key Endpoints

- **Prompts**
  - **GET /prompts**: Retrieve all prompts.
  - **POST /prompts**: Create a new prompt.
  - **GET /prompts/{prompt_id}**: Retrieve a prompt by ID.
  - **PUT /prompts/{prompt_id}**: Update a specific prompt.
  - **DELETE /prompts/{prompt_id}**: Delete a prompt.

- **Collections**
  - **GET /collections**: Retrieve all collections.
  - **POST /collections**: Create a new collection.
  - **GET /collections/{collection_id}**: Retrieve a collection by ID.
  - **DELETE /collections/{collection_id}**: Delete a collection.

- **Health Check**
  - **GET /health**: Check service health.

### Data Models with Examples

**Prompt Model**:

```json
{
  "id": "uuid-string",
  "title": "Sample Title",
  "content": "Sample content details here.",
  "description": "Optional description.",
  "collection_id": "uuid-collection-id",
  "created_at": "2023-10-12T10:00:00Z",
  "updated_at": "2023-10-12T10:00:00Z"
}
```

**Collection Model**:

```json
{
  "id": "uuid-string",
  "name": "Collection Name",
  "description": "Collection description.",
  "created_at": "2023-10-12T10:00:00Z"
}
```

## Development Setup

- **Testing with Pytest**:

  ```bash
  pytest tests
  ```  

- **Linting**: Maintain code quality using `flake8`.

  ```bash
  flake8 app
  ```

- **Code Formatting**: Ensure consistent code formatting using `black`.

  ```bash
  black app

## Contributing Guidelines

We appreciate your interest in contributing to PromptLab! Here are some guidelines to help you get started:

### How to Contribute

1. **Fork the Repository**: Use the `Fork` button at the top right of the repository page to create a copy of the repository under your GitHub account.

2. **Clone Your Fork**: Clone your forked repository to your local machine.

   ```bash
   git clone https://github.com/your-username/10x-engineer-project-repo.git
   cd 10x-engineer-project-repo/backend
   ```

3. **Set Up Environment**: Follow the installation instructions in the README to set up your development environment.

4. **Create a Branch**: Create a new branch for your feature or fix. Use a descriptive name for your branch.

   ```bash
   git checkout -b feature/YourFeatureName
   ```

5. **Make Changes**: Implement your feature or fix. Ensure that your code follows the project's coding standards and is well-documented.

6. **Write Tests**: Ensure that you write appropriate tests for your changes. Run all tests to confirm they pass with your modifications.

   ```bash
   pytest tests
   ```

7. **Commit Changes**: Commit your changes with a clear and descriptive commit message.

   ```bash
   git commit -m "Add some feature"
   ```

8. **Push to Your Fork**: Push your changes to your GitHub repository.

   ```bash
   git push origin feature/YourFeatureName
   ```

9. **Submit a Pull Request**: Navigate to the original repository on GitHub and create a pull request. Provide a clear description of your changes and why they should be merged. Mention any issues your PR addresses.

10. **Code Review**: Participate in the code review discussions. Be open to feedback and ready to make further changes if required.

### Code of Conduct

Please note that this project is governed by a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Getting Help

If you need help at any point during the contribution process, feel free to reach out by opening an issue or through the project's communication channels.
