"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """Class for in-memory storage management of prompts and collections.

    This class provides operations to create, read, update, and delete prompts
    and collections using in-memory dictionaries.
    """
    def __init__(self):
        """Initialize the Storage with empty prompts and collections dictionaries."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Add a new prompt to storage.

        Args:
            prompt (Prompt): The prompt to add.

        Returns:
            Prompt: The added prompt object.

        Example:
            >>> my_prompt = Prompt(...)
            >>> storage.create_prompt(my_prompt)
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The prompt object if found, else None.

        Example:
            >>> storage.get_prompt('abc123')
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Get a list of all prompts in storage.

        Returns:
            List[Prompt]: A list of all stored prompts.

        Example:
            >>> storage.get_all_prompts()
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt in storage.

        Args:
            prompt_id (str): The ID of the prompt to update.
            prompt (Prompt): The updated prompt object.

        Returns:
            Optional[Prompt]: The updated prompt if successful, else None.

        Example:
            >>> updated_prompt = Prompt(...)
            >>> storage.update_prompt('abc123', updated_prompt)
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Remove a prompt from storage.

        Args:
            prompt_id (str): The ID of the prompt to delete.

        Returns:
            bool: True if the prompt was deleted, False if not found.

        Example:
            >>> storage.delete_prompt('abc123')
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Add a new collection to storage.

        Args:
            collection (Collection): The collection to add.

        Returns:
            Collection: The added collection object.

        Example:
            >>> my_collection = Collection(...)
            >>> storage.create_collection(my_collection)
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection object if found, else None.

        Example:
            >>> storage.get_collection('def456')
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Get a list of all collections in storage.

        Returns:
            List[Collection]: A list of all stored collections.

        Example:
            >>> storage.get_all_collections()
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Remove a collection from storage.

        Args:
            collection_id (str): The ID of the collection to delete.

        Returns:
            bool: True if the collection was deleted, False if not found.

        Example:
            >>> storage.delete_collection('def456')
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Get all prompts that belong to a specific collection.

        Args:
            collection_id (str): The ID of the collection to filter prompts by.

        Returns:
            List[Prompt]: A list of prompts within the given collection.

        Example:
            >>> storage.get_prompts_by_collection('def456')
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Clear all prompts and collections from storage."""
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()
