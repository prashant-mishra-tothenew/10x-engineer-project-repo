"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Annotated, Callable, ClassVar, Dict, List, Optional

from app.models import Collection, Prompt, Tag

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


class Storage:
    """Class for in-memory storage management of prompts, collections, and tags.

    This class provides operations to create, read, update, and delete prompts,
    collections, and tags using in-memory dictionaries.
    """

    def __init__(self):
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStorageǁ__init____mutmut_orig(self):
        """Initialize the Storage with empty dictionaries."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._tags: Dict[str, Tag] = {}  # tag_id -> Tag
        self._tag_names: Dict[str, str] = {}  # name -> tag_id (for quick lookup)

    def xǁStorageǁ__init____mutmut_1(self):
        """Initialize the Storage with empty dictionaries."""
        self._prompts: Dict[str, Prompt] = None
        self._collections: Dict[str, Collection] = {}
        self._tags: Dict[str, Tag] = {}  # tag_id -> Tag
        self._tag_names: Dict[str, str] = {}  # name -> tag_id (for quick lookup)

    def xǁStorageǁ__init____mutmut_2(self):
        """Initialize the Storage with empty dictionaries."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = None
        self._tags: Dict[str, Tag] = {}  # tag_id -> Tag
        self._tag_names: Dict[str, str] = {}  # name -> tag_id (for quick lookup)

    def xǁStorageǁ__init____mutmut_3(self):
        """Initialize the Storage with empty dictionaries."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._tags: Dict[str, Tag] = None  # tag_id -> Tag
        self._tag_names: Dict[str, str] = {}  # name -> tag_id (for quick lookup)

    def xǁStorageǁ__init____mutmut_4(self):
        """Initialize the Storage with empty dictionaries."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._tags: Dict[str, Tag] = {}  # tag_id -> Tag
        self._tag_names: Dict[str, str] = None  # name -> tag_id (for quick lookup)

    xǁStorageǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁ__init____mutmut_1": xǁStorageǁ__init____mutmut_1,
        "xǁStorageǁ__init____mutmut_2": xǁStorageǁ__init____mutmut_2,
        "xǁStorageǁ__init____mutmut_3": xǁStorageǁ__init____mutmut_3,
        "xǁStorageǁ__init____mutmut_4": xǁStorageǁ__init____mutmut_4,
    }
    xǁStorageǁ__init____mutmut_orig.__name__ = "xǁStorageǁ__init__"

    # ============== Prompt Operations ==============

    def create_prompt(self, prompt: Prompt) -> Prompt:
        args = [prompt]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁcreate_prompt__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁcreate_prompt__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    # ============== Prompt Operations ==============

    def xǁStorageǁcreate_prompt__mutmut_orig(self, prompt: Prompt) -> Prompt:
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

    # ============== Prompt Operations ==============

    def xǁStorageǁcreate_prompt__mutmut_1(self, prompt: Prompt) -> Prompt:
        """Add a new prompt to storage.

        Args:
            prompt (Prompt): The prompt to add.

        Returns:
            Prompt: The added prompt object.

        Example:
            >>> my_prompt = Prompt(...)
            >>> storage.create_prompt(my_prompt)
        """
        self._prompts[prompt.id] = None
        return prompt

    xǁStorageǁcreate_prompt__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁcreate_prompt__mutmut_1": xǁStorageǁcreate_prompt__mutmut_1
    }
    xǁStorageǁcreate_prompt__mutmut_orig.__name__ = "xǁStorageǁcreate_prompt"

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        args = [prompt_id]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁget_prompt__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁget_prompt__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStorageǁget_prompt__mutmut_orig(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The prompt object if found, else None.

        Example:
            >>> storage.get_prompt('abc123')
        """
        return self._prompts.get(prompt_id)

    def xǁStorageǁget_prompt__mutmut_1(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The prompt object if found, else None.

        Example:
            >>> storage.get_prompt('abc123')
        """
        return self._prompts.get(None)

    xǁStorageǁget_prompt__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁget_prompt__mutmut_1": xǁStorageǁget_prompt__mutmut_1
    }
    xǁStorageǁget_prompt__mutmut_orig.__name__ = "xǁStorageǁget_prompt"

    def get_all_prompts(self) -> List[Prompt]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁget_all_prompts__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁget_all_prompts__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStorageǁget_all_prompts__mutmut_orig(self) -> List[Prompt]:
        """Get a list of all prompts in storage.

        Returns:
            List[Prompt]: A list of all stored prompts.

        Example:
            >>> storage.get_all_prompts()
        """
        return list(self._prompts.values())

    def xǁStorageǁget_all_prompts__mutmut_1(self) -> List[Prompt]:
        """Get a list of all prompts in storage.

        Returns:
            List[Prompt]: A list of all stored prompts.

        Example:
            >>> storage.get_all_prompts()
        """
        return list(None)

    xǁStorageǁget_all_prompts__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁget_all_prompts__mutmut_1": xǁStorageǁget_all_prompts__mutmut_1
    }
    xǁStorageǁget_all_prompts__mutmut_orig.__name__ = "xǁStorageǁget_all_prompts"

    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        args = [prompt_id, prompt]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁupdate_prompt__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁupdate_prompt__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStorageǁupdate_prompt__mutmut_orig(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
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

    def xǁStorageǁupdate_prompt__mutmut_1(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
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
        if prompt_id in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt

    def xǁStorageǁupdate_prompt__mutmut_2(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
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
        self._prompts[prompt_id] = None
        return prompt

    xǁStorageǁupdate_prompt__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁupdate_prompt__mutmut_1": xǁStorageǁupdate_prompt__mutmut_1,
        "xǁStorageǁupdate_prompt__mutmut_2": xǁStorageǁupdate_prompt__mutmut_2,
    }
    xǁStorageǁupdate_prompt__mutmut_orig.__name__ = "xǁStorageǁupdate_prompt"

    def delete_prompt(self, prompt_id: str) -> bool:
        args = [prompt_id]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁdelete_prompt__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁdelete_prompt__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStorageǁdelete_prompt__mutmut_orig(self, prompt_id: str) -> bool:
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

    def xǁStorageǁdelete_prompt__mutmut_1(self, prompt_id: str) -> bool:
        """Remove a prompt from storage.

        Args:
            prompt_id (str): The ID of the prompt to delete.

        Returns:
            bool: True if the prompt was deleted, False if not found.

        Example:
            >>> storage.delete_prompt('abc123')
        """
        if prompt_id not in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False

    def xǁStorageǁdelete_prompt__mutmut_2(self, prompt_id: str) -> bool:
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
            return False
        return False

    def xǁStorageǁdelete_prompt__mutmut_3(self, prompt_id: str) -> bool:
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
        return True

    xǁStorageǁdelete_prompt__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁdelete_prompt__mutmut_1": xǁStorageǁdelete_prompt__mutmut_1,
        "xǁStorageǁdelete_prompt__mutmut_2": xǁStorageǁdelete_prompt__mutmut_2,
        "xǁStorageǁdelete_prompt__mutmut_3": xǁStorageǁdelete_prompt__mutmut_3,
    }
    xǁStorageǁdelete_prompt__mutmut_orig.__name__ = "xǁStorageǁdelete_prompt"

    # ============== Collection Operations ==============

    def create_collection(self, collection: Collection) -> Collection:
        args = [collection]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁcreate_collection__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁcreate_collection__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    # ============== Collection Operations ==============

    def xǁStorageǁcreate_collection__mutmut_orig(self, collection: Collection) -> Collection:
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

    # ============== Collection Operations ==============

    def xǁStorageǁcreate_collection__mutmut_1(self, collection: Collection) -> Collection:
        """Add a new collection to storage.

        Args:
            collection (Collection): The collection to add.

        Returns:
            Collection: The added collection object.

        Example:
            >>> my_collection = Collection(...)
            >>> storage.create_collection(my_collection)
        """
        self._collections[collection.id] = None
        return collection

    xǁStorageǁcreate_collection__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁcreate_collection__mutmut_1": xǁStorageǁcreate_collection__mutmut_1
    }
    xǁStorageǁcreate_collection__mutmut_orig.__name__ = "xǁStorageǁcreate_collection"

    def get_collection(self, collection_id: str) -> Optional[Collection]:
        args = [collection_id]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁget_collection__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁget_collection__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStorageǁget_collection__mutmut_orig(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection object if found, else None.

        Example:
            >>> storage.get_collection('def456')
        """
        return self._collections.get(collection_id)

    def xǁStorageǁget_collection__mutmut_1(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection object if found, else None.

        Example:
            >>> storage.get_collection('def456')
        """
        return self._collections.get(None)

    xǁStorageǁget_collection__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁget_collection__mutmut_1": xǁStorageǁget_collection__mutmut_1
    }
    xǁStorageǁget_collection__mutmut_orig.__name__ = "xǁStorageǁget_collection"

    def get_all_collections(self) -> List[Collection]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁget_all_collections__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁget_all_collections__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStorageǁget_all_collections__mutmut_orig(self) -> List[Collection]:
        """Get a list of all collections in storage.

        Returns:
            List[Collection]: A list of all stored collections.

        Example:
            >>> storage.get_all_collections()
        """
        return list(self._collections.values())

    def xǁStorageǁget_all_collections__mutmut_1(self) -> List[Collection]:
        """Get a list of all collections in storage.

        Returns:
            List[Collection]: A list of all stored collections.

        Example:
            >>> storage.get_all_collections()
        """
        return list(None)

    xǁStorageǁget_all_collections__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁget_all_collections__mutmut_1": xǁStorageǁget_all_collections__mutmut_1
    }
    xǁStorageǁget_all_collections__mutmut_orig.__name__ = "xǁStorageǁget_all_collections"

    def delete_collection(self, collection_id: str) -> bool:
        args = [collection_id]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁdelete_collection__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁdelete_collection__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStorageǁdelete_collection__mutmut_orig(self, collection_id: str) -> bool:
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

    def xǁStorageǁdelete_collection__mutmut_1(self, collection_id: str) -> bool:
        """Remove a collection from storage.

        Args:
            collection_id (str): The ID of the collection to delete.

        Returns:
            bool: True if the collection was deleted, False if not found.

        Example:
            >>> storage.delete_collection('def456')
        """
        if collection_id not in self._collections:
            del self._collections[collection_id]
            return True
        return False

    def xǁStorageǁdelete_collection__mutmut_2(self, collection_id: str) -> bool:
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
            return False
        return False

    def xǁStorageǁdelete_collection__mutmut_3(self, collection_id: str) -> bool:
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
        return True

    xǁStorageǁdelete_collection__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁdelete_collection__mutmut_1": xǁStorageǁdelete_collection__mutmut_1,
        "xǁStorageǁdelete_collection__mutmut_2": xǁStorageǁdelete_collection__mutmut_2,
        "xǁStorageǁdelete_collection__mutmut_3": xǁStorageǁdelete_collection__mutmut_3,
    }
    xǁStorageǁdelete_collection__mutmut_orig.__name__ = "xǁStorageǁdelete_collection"

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        args = [collection_id]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁget_prompts_by_collection__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁget_prompts_by_collection__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStorageǁget_prompts_by_collection__mutmut_orig(self, collection_id: str) -> List[Prompt]:
        """Get all prompts that belong to a specific collection.

        Args:
            collection_id (str): The ID of the collection to filter prompts by.

        Returns:
            List[Prompt]: A list of prompts within the given collection.

        Example:
            >>> storage.get_prompts_by_collection('def456')
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]

    def xǁStorageǁget_prompts_by_collection__mutmut_1(self, collection_id: str) -> List[Prompt]:
        """Get all prompts that belong to a specific collection.

        Args:
            collection_id (str): The ID of the collection to filter prompts by.

        Returns:
            List[Prompt]: A list of prompts within the given collection.

        Example:
            >>> storage.get_prompts_by_collection('def456')
        """
        return [p for p in self._prompts.values() if p.collection_id != collection_id]

    xǁStorageǁget_prompts_by_collection__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁget_prompts_by_collection__mutmut_1": xǁStorageǁget_prompts_by_collection__mutmut_1
    }
    xǁStorageǁget_prompts_by_collection__mutmut_orig.__name__ = "xǁStorageǁget_prompts_by_collection"

    # ============== Utility ==============

    def clear(self):
        """Clear all prompts, collections, and tags from storage."""
        self._prompts.clear()
        self._collections.clear()
        self._tags.clear()
        self._tag_names.clear()

    # ============== Tag Operations ==============

    def create_tag(self, tag: Tag) -> Tag:
        args = [tag]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁcreate_tag__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁcreate_tag__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    # ============== Tag Operations ==============

    def xǁStorageǁcreate_tag__mutmut_orig(self, tag: Tag) -> Tag:
        """Add a new tag to storage.

        Args:
            tag (Tag): The tag to add.

        Returns:
            Tag: The added tag object.

        Example:
            >>> my_tag = Tag(name="python")
            >>> storage.create_tag(my_tag)
        """
        self._tags[tag.tag_id] = tag
        self._tag_names[tag.name] = tag.tag_id
        return tag

    # ============== Tag Operations ==============

    def xǁStorageǁcreate_tag__mutmut_1(self, tag: Tag) -> Tag:
        """Add a new tag to storage.

        Args:
            tag (Tag): The tag to add.

        Returns:
            Tag: The added tag object.

        Example:
            >>> my_tag = Tag(name="python")
            >>> storage.create_tag(my_tag)
        """
        self._tags[tag.tag_id] = None
        self._tag_names[tag.name] = tag.tag_id
        return tag

    # ============== Tag Operations ==============

    def xǁStorageǁcreate_tag__mutmut_2(self, tag: Tag) -> Tag:
        """Add a new tag to storage.

        Args:
            tag (Tag): The tag to add.

        Returns:
            Tag: The added tag object.

        Example:
            >>> my_tag = Tag(name="python")
            >>> storage.create_tag(my_tag)
        """
        self._tags[tag.tag_id] = tag
        self._tag_names[tag.name] = None
        return tag

    xǁStorageǁcreate_tag__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁcreate_tag__mutmut_1": xǁStorageǁcreate_tag__mutmut_1,
        "xǁStorageǁcreate_tag__mutmut_2": xǁStorageǁcreate_tag__mutmut_2,
    }
    xǁStorageǁcreate_tag__mutmut_orig.__name__ = "xǁStorageǁcreate_tag"

    def get_tag(self, tag_id: str) -> Optional[Tag]:
        args = [tag_id]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁget_tag__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁget_tag__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStorageǁget_tag__mutmut_orig(self, tag_id: str) -> Optional[Tag]:
        """Retrieve a tag by its ID.

        Args:
            tag_id (str): The ID of the tag to retrieve.

        Returns:
            Optional[Tag]: The tag object if found, else None.

        Example:
            >>> storage.get_tag('abc123')
        """
        return self._tags.get(tag_id)

    def xǁStorageǁget_tag__mutmut_1(self, tag_id: str) -> Optional[Tag]:
        """Retrieve a tag by its ID.

        Args:
            tag_id (str): The ID of the tag to retrieve.

        Returns:
            Optional[Tag]: The tag object if found, else None.

        Example:
            >>> storage.get_tag('abc123')
        """
        return self._tags.get(None)

    xǁStorageǁget_tag__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁget_tag__mutmut_1": xǁStorageǁget_tag__mutmut_1
    }
    xǁStorageǁget_tag__mutmut_orig.__name__ = "xǁStorageǁget_tag"

    def get_tag_by_name(self, name: str) -> Optional[Tag]:
        args = [name]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁget_tag_by_name__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁget_tag_by_name__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStorageǁget_tag_by_name__mutmut_orig(self, name: str) -> Optional[Tag]:
        """Retrieve a tag by its name.

        Tag names are case-sensitive. This is useful for checking
        if a tag already exists before creating a new one.

        Args:
            name (str): The name of the tag to retrieve.

        Returns:
            Optional[Tag]: The tag object if found, else None.

        Example:
            >>> storage.get_tag_by_name('python')
        """
        tag_id = self._tag_names.get(name)
        if tag_id:
            return self._tags.get(tag_id)
        return None

    def xǁStorageǁget_tag_by_name__mutmut_1(self, name: str) -> Optional[Tag]:
        """Retrieve a tag by its name.

        Tag names are case-sensitive. This is useful for checking
        if a tag already exists before creating a new one.

        Args:
            name (str): The name of the tag to retrieve.

        Returns:
            Optional[Tag]: The tag object if found, else None.

        Example:
            >>> storage.get_tag_by_name('python')
        """
        tag_id = None
        if tag_id:
            return self._tags.get(tag_id)
        return None

    def xǁStorageǁget_tag_by_name__mutmut_2(self, name: str) -> Optional[Tag]:
        """Retrieve a tag by its name.

        Tag names are case-sensitive. This is useful for checking
        if a tag already exists before creating a new one.

        Args:
            name (str): The name of the tag to retrieve.

        Returns:
            Optional[Tag]: The tag object if found, else None.

        Example:
            >>> storage.get_tag_by_name('python')
        """
        tag_id = self._tag_names.get(None)
        if tag_id:
            return self._tags.get(tag_id)
        return None

    def xǁStorageǁget_tag_by_name__mutmut_3(self, name: str) -> Optional[Tag]:
        """Retrieve a tag by its name.

        Tag names are case-sensitive. This is useful for checking
        if a tag already exists before creating a new one.

        Args:
            name (str): The name of the tag to retrieve.

        Returns:
            Optional[Tag]: The tag object if found, else None.

        Example:
            >>> storage.get_tag_by_name('python')
        """
        tag_id = self._tag_names.get(name)
        if tag_id:
            return self._tags.get(None)
        return None

    xǁStorageǁget_tag_by_name__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁget_tag_by_name__mutmut_1": xǁStorageǁget_tag_by_name__mutmut_1,
        "xǁStorageǁget_tag_by_name__mutmut_2": xǁStorageǁget_tag_by_name__mutmut_2,
        "xǁStorageǁget_tag_by_name__mutmut_3": xǁStorageǁget_tag_by_name__mutmut_3,
    }
    xǁStorageǁget_tag_by_name__mutmut_orig.__name__ = "xǁStorageǁget_tag_by_name"

    def get_all_tags(self) -> List[Tag]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁStorageǁget_all_tags__mutmut_orig"),
            object.__getattribute__(self, "xǁStorageǁget_all_tags__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁStorageǁget_all_tags__mutmut_orig(self) -> List[Tag]:
        """Get a list of all tags in storage.

        Returns:
            List[Tag]: A list of all stored tags.

        Example:
            >>> storage.get_all_tags()
        """
        return list(self._tags.values())

    def xǁStorageǁget_all_tags__mutmut_1(self) -> List[Tag]:
        """Get a list of all tags in storage.

        Returns:
            List[Tag]: A list of all stored tags.

        Example:
            >>> storage.get_all_tags()
        """
        return list(None)

    xǁStorageǁget_all_tags__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁStorageǁget_all_tags__mutmut_1": xǁStorageǁget_all_tags__mutmut_1
    }
    xǁStorageǁget_all_tags__mutmut_orig.__name__ = "xǁStorageǁget_all_tags"


# Global storage instance
storage = Storage()
