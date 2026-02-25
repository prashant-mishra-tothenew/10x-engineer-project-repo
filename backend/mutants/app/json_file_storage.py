import json
import os
from typing import Annotated, Callable, ClassVar, Dict, List, Optional

from app.models import Collection, Prompt

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


class JSONFileStorage:
    def __init__(self, prompt_file="prompts.json", collection_file="collections.json"):
        args = [prompt_file, collection_file]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁ__init____mutmut_orig(self, prompt_file="prompts.json", collection_file="collections.json"):
        self.prompt_file = prompt_file
        self.collection_file = collection_file
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._load_data()

    def xǁJSONFileStorageǁ__init____mutmut_1(self, prompt_file="XXprompts.jsonXX", collection_file="collections.json"):
        self.prompt_file = prompt_file
        self.collection_file = collection_file
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._load_data()

    def xǁJSONFileStorageǁ__init____mutmut_2(self, prompt_file="PROMPTS.JSON", collection_file="collections.json"):
        self.prompt_file = prompt_file
        self.collection_file = collection_file
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._load_data()

    def xǁJSONFileStorageǁ__init____mutmut_3(self, prompt_file="prompts.json", collection_file="XXcollections.jsonXX"):
        self.prompt_file = prompt_file
        self.collection_file = collection_file
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._load_data()

    def xǁJSONFileStorageǁ__init____mutmut_4(self, prompt_file="prompts.json", collection_file="COLLECTIONS.JSON"):
        self.prompt_file = prompt_file
        self.collection_file = collection_file
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._load_data()

    def xǁJSONFileStorageǁ__init____mutmut_5(self, prompt_file="prompts.json", collection_file="collections.json"):
        self.prompt_file = None
        self.collection_file = collection_file
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._load_data()

    def xǁJSONFileStorageǁ__init____mutmut_6(self, prompt_file="prompts.json", collection_file="collections.json"):
        self.prompt_file = prompt_file
        self.collection_file = None
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._load_data()

    def xǁJSONFileStorageǁ__init____mutmut_7(self, prompt_file="prompts.json", collection_file="collections.json"):
        self.prompt_file = prompt_file
        self.collection_file = collection_file
        self._prompts: Dict[str, Prompt] = None
        self._collections: Dict[str, Collection] = {}
        self._load_data()

    def xǁJSONFileStorageǁ__init____mutmut_8(self, prompt_file="prompts.json", collection_file="collections.json"):
        self.prompt_file = prompt_file
        self.collection_file = collection_file
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = None
        self._load_data()

    xǁJSONFileStorageǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁ__init____mutmut_1": xǁJSONFileStorageǁ__init____mutmut_1,
        "xǁJSONFileStorageǁ__init____mutmut_2": xǁJSONFileStorageǁ__init____mutmut_2,
        "xǁJSONFileStorageǁ__init____mutmut_3": xǁJSONFileStorageǁ__init____mutmut_3,
        "xǁJSONFileStorageǁ__init____mutmut_4": xǁJSONFileStorageǁ__init____mutmut_4,
        "xǁJSONFileStorageǁ__init____mutmut_5": xǁJSONFileStorageǁ__init____mutmut_5,
        "xǁJSONFileStorageǁ__init____mutmut_6": xǁJSONFileStorageǁ__init____mutmut_6,
        "xǁJSONFileStorageǁ__init____mutmut_7": xǁJSONFileStorageǁ__init____mutmut_7,
        "xǁJSONFileStorageǁ__init____mutmut_8": xǁJSONFileStorageǁ__init____mutmut_8,
    }
    xǁJSONFileStorageǁ__init____mutmut_orig.__name__ = "xǁJSONFileStorageǁ__init__"

    def _load_data(self):
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁ_load_data__mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁ_load_data__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁ_load_data__mutmut_orig(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_1(self):
        """Load prompts and collections from files."""
        if os.path.exists(None):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_2(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(None, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_3(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, None) as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_4(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open("r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_5(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(
                self.prompt_file,
            ) as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_6(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "XXrXX") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_7(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "R") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_8(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = None
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_9(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(None)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_10(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = None

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_11(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["XXidXX"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_12(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["ID"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_13(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(None):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_14(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(None, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_15(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, None) as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_16(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open("r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_17(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(
                self.collection_file,
            ) as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_18(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "XXrXX") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_19(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "R") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_20(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = None
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_21(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(None)
                for c in collections:
                    self._collections[c["id"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_22(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["id"]] = None

    def xǁJSONFileStorageǁ_load_data__mutmut_23(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["XXidXX"]] = Collection(**c)

    def xǁJSONFileStorageǁ_load_data__mutmut_24(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p["id"]] = Prompt(**p)

        if os.path.exists(self.collection_file):
            with open(self.collection_file, "r") as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c["ID"]] = Collection(**c)

    xǁJSONFileStorageǁ_load_data__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁ_load_data__mutmut_1": xǁJSONFileStorageǁ_load_data__mutmut_1,
        "xǁJSONFileStorageǁ_load_data__mutmut_2": xǁJSONFileStorageǁ_load_data__mutmut_2,
        "xǁJSONFileStorageǁ_load_data__mutmut_3": xǁJSONFileStorageǁ_load_data__mutmut_3,
        "xǁJSONFileStorageǁ_load_data__mutmut_4": xǁJSONFileStorageǁ_load_data__mutmut_4,
        "xǁJSONFileStorageǁ_load_data__mutmut_5": xǁJSONFileStorageǁ_load_data__mutmut_5,
        "xǁJSONFileStorageǁ_load_data__mutmut_6": xǁJSONFileStorageǁ_load_data__mutmut_6,
        "xǁJSONFileStorageǁ_load_data__mutmut_7": xǁJSONFileStorageǁ_load_data__mutmut_7,
        "xǁJSONFileStorageǁ_load_data__mutmut_8": xǁJSONFileStorageǁ_load_data__mutmut_8,
        "xǁJSONFileStorageǁ_load_data__mutmut_9": xǁJSONFileStorageǁ_load_data__mutmut_9,
        "xǁJSONFileStorageǁ_load_data__mutmut_10": xǁJSONFileStorageǁ_load_data__mutmut_10,
        "xǁJSONFileStorageǁ_load_data__mutmut_11": xǁJSONFileStorageǁ_load_data__mutmut_11,
        "xǁJSONFileStorageǁ_load_data__mutmut_12": xǁJSONFileStorageǁ_load_data__mutmut_12,
        "xǁJSONFileStorageǁ_load_data__mutmut_13": xǁJSONFileStorageǁ_load_data__mutmut_13,
        "xǁJSONFileStorageǁ_load_data__mutmut_14": xǁJSONFileStorageǁ_load_data__mutmut_14,
        "xǁJSONFileStorageǁ_load_data__mutmut_15": xǁJSONFileStorageǁ_load_data__mutmut_15,
        "xǁJSONFileStorageǁ_load_data__mutmut_16": xǁJSONFileStorageǁ_load_data__mutmut_16,
        "xǁJSONFileStorageǁ_load_data__mutmut_17": xǁJSONFileStorageǁ_load_data__mutmut_17,
        "xǁJSONFileStorageǁ_load_data__mutmut_18": xǁJSONFileStorageǁ_load_data__mutmut_18,
        "xǁJSONFileStorageǁ_load_data__mutmut_19": xǁJSONFileStorageǁ_load_data__mutmut_19,
        "xǁJSONFileStorageǁ_load_data__mutmut_20": xǁJSONFileStorageǁ_load_data__mutmut_20,
        "xǁJSONFileStorageǁ_load_data__mutmut_21": xǁJSONFileStorageǁ_load_data__mutmut_21,
        "xǁJSONFileStorageǁ_load_data__mutmut_22": xǁJSONFileStorageǁ_load_data__mutmut_22,
        "xǁJSONFileStorageǁ_load_data__mutmut_23": xǁJSONFileStorageǁ_load_data__mutmut_23,
        "xǁJSONFileStorageǁ_load_data__mutmut_24": xǁJSONFileStorageǁ_load_data__mutmut_24,
    }
    xǁJSONFileStorageǁ_load_data__mutmut_orig.__name__ = "xǁJSONFileStorageǁ_load_data"

    def _save_data(self, file_path: str, data: Dict):
        args = [file_path, data]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁ_save_data__mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁ_save_data__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁ_save_data__mutmut_orig(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_1(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = None
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_2(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = None
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_3(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict or item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_4(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "XXcreated_atXX" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_5(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "CREATED_AT" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_6(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" not in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_7(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["XXcreated_atXX"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_8(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["CREATED_AT"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_9(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = None
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_10(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["XXcreated_atXX"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_11(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["CREATED_AT"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_12(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["XXcreated_atXX"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_13(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["CREATED_AT"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_14(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict or item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_15(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "XXupdated_atXX" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_16(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "UPDATED_AT" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_17(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" not in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_18(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["XXupdated_atXX"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_19(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["UPDATED_AT"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_20(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = None
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_21(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["XXupdated_atXX"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_22(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["UPDATED_AT"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_23(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["XXupdated_atXX"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_24(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["UPDATED_AT"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_25(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(None)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_26(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(None, "w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_27(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, None) as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_28(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open("w") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_29(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(
            file_path,
        ) as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_30(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "XXwXX") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_31(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "W") as f:
            json.dump(serialized_data, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_32(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(None, f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_33(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, None, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_34(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=None)

    def xǁJSONFileStorageǁ_save_data__mutmut_35(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(f, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_36(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, indent=4)

    def xǁJSONFileStorageǁ_save_data__mutmut_37(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(
                serialized_data,
                f,
            )

    def xǁJSONFileStorageǁ_save_data__mutmut_38(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if "created_at" in item_dict and item_dict["created_at"]:
                item_dict["created_at"] = item_dict["created_at"].isoformat()
            if "updated_at" in item_dict and item_dict["updated_at"]:
                item_dict["updated_at"] = item_dict["updated_at"].isoformat()
            serialized_data.append(item_dict)

        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=5)

    xǁJSONFileStorageǁ_save_data__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁ_save_data__mutmut_1": xǁJSONFileStorageǁ_save_data__mutmut_1,
        "xǁJSONFileStorageǁ_save_data__mutmut_2": xǁJSONFileStorageǁ_save_data__mutmut_2,
        "xǁJSONFileStorageǁ_save_data__mutmut_3": xǁJSONFileStorageǁ_save_data__mutmut_3,
        "xǁJSONFileStorageǁ_save_data__mutmut_4": xǁJSONFileStorageǁ_save_data__mutmut_4,
        "xǁJSONFileStorageǁ_save_data__mutmut_5": xǁJSONFileStorageǁ_save_data__mutmut_5,
        "xǁJSONFileStorageǁ_save_data__mutmut_6": xǁJSONFileStorageǁ_save_data__mutmut_6,
        "xǁJSONFileStorageǁ_save_data__mutmut_7": xǁJSONFileStorageǁ_save_data__mutmut_7,
        "xǁJSONFileStorageǁ_save_data__mutmut_8": xǁJSONFileStorageǁ_save_data__mutmut_8,
        "xǁJSONFileStorageǁ_save_data__mutmut_9": xǁJSONFileStorageǁ_save_data__mutmut_9,
        "xǁJSONFileStorageǁ_save_data__mutmut_10": xǁJSONFileStorageǁ_save_data__mutmut_10,
        "xǁJSONFileStorageǁ_save_data__mutmut_11": xǁJSONFileStorageǁ_save_data__mutmut_11,
        "xǁJSONFileStorageǁ_save_data__mutmut_12": xǁJSONFileStorageǁ_save_data__mutmut_12,
        "xǁJSONFileStorageǁ_save_data__mutmut_13": xǁJSONFileStorageǁ_save_data__mutmut_13,
        "xǁJSONFileStorageǁ_save_data__mutmut_14": xǁJSONFileStorageǁ_save_data__mutmut_14,
        "xǁJSONFileStorageǁ_save_data__mutmut_15": xǁJSONFileStorageǁ_save_data__mutmut_15,
        "xǁJSONFileStorageǁ_save_data__mutmut_16": xǁJSONFileStorageǁ_save_data__mutmut_16,
        "xǁJSONFileStorageǁ_save_data__mutmut_17": xǁJSONFileStorageǁ_save_data__mutmut_17,
        "xǁJSONFileStorageǁ_save_data__mutmut_18": xǁJSONFileStorageǁ_save_data__mutmut_18,
        "xǁJSONFileStorageǁ_save_data__mutmut_19": xǁJSONFileStorageǁ_save_data__mutmut_19,
        "xǁJSONFileStorageǁ_save_data__mutmut_20": xǁJSONFileStorageǁ_save_data__mutmut_20,
        "xǁJSONFileStorageǁ_save_data__mutmut_21": xǁJSONFileStorageǁ_save_data__mutmut_21,
        "xǁJSONFileStorageǁ_save_data__mutmut_22": xǁJSONFileStorageǁ_save_data__mutmut_22,
        "xǁJSONFileStorageǁ_save_data__mutmut_23": xǁJSONFileStorageǁ_save_data__mutmut_23,
        "xǁJSONFileStorageǁ_save_data__mutmut_24": xǁJSONFileStorageǁ_save_data__mutmut_24,
        "xǁJSONFileStorageǁ_save_data__mutmut_25": xǁJSONFileStorageǁ_save_data__mutmut_25,
        "xǁJSONFileStorageǁ_save_data__mutmut_26": xǁJSONFileStorageǁ_save_data__mutmut_26,
        "xǁJSONFileStorageǁ_save_data__mutmut_27": xǁJSONFileStorageǁ_save_data__mutmut_27,
        "xǁJSONFileStorageǁ_save_data__mutmut_28": xǁJSONFileStorageǁ_save_data__mutmut_28,
        "xǁJSONFileStorageǁ_save_data__mutmut_29": xǁJSONFileStorageǁ_save_data__mutmut_29,
        "xǁJSONFileStorageǁ_save_data__mutmut_30": xǁJSONFileStorageǁ_save_data__mutmut_30,
        "xǁJSONFileStorageǁ_save_data__mutmut_31": xǁJSONFileStorageǁ_save_data__mutmut_31,
        "xǁJSONFileStorageǁ_save_data__mutmut_32": xǁJSONFileStorageǁ_save_data__mutmut_32,
        "xǁJSONFileStorageǁ_save_data__mutmut_33": xǁJSONFileStorageǁ_save_data__mutmut_33,
        "xǁJSONFileStorageǁ_save_data__mutmut_34": xǁJSONFileStorageǁ_save_data__mutmut_34,
        "xǁJSONFileStorageǁ_save_data__mutmut_35": xǁJSONFileStorageǁ_save_data__mutmut_35,
        "xǁJSONFileStorageǁ_save_data__mutmut_36": xǁJSONFileStorageǁ_save_data__mutmut_36,
        "xǁJSONFileStorageǁ_save_data__mutmut_37": xǁJSONFileStorageǁ_save_data__mutmut_37,
        "xǁJSONFileStorageǁ_save_data__mutmut_38": xǁJSONFileStorageǁ_save_data__mutmut_38,
    }
    xǁJSONFileStorageǁ_save_data__mutmut_orig.__name__ = "xǁJSONFileStorageǁ_save_data"

    def create_prompt(self, prompt: Prompt) -> Prompt:
        args = [prompt]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁcreate_prompt__mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁcreate_prompt__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁcreate_prompt__mutmut_orig(self, prompt: Prompt) -> Prompt:
        self._prompts[prompt.id] = prompt
        self._save_data(self.prompt_file, self._prompts)
        return prompt

    def xǁJSONFileStorageǁcreate_prompt__mutmut_1(self, prompt: Prompt) -> Prompt:
        self._prompts[prompt.id] = None
        self._save_data(self.prompt_file, self._prompts)
        return prompt

    def xǁJSONFileStorageǁcreate_prompt__mutmut_2(self, prompt: Prompt) -> Prompt:
        self._prompts[prompt.id] = prompt
        self._save_data(None, self._prompts)
        return prompt

    def xǁJSONFileStorageǁcreate_prompt__mutmut_3(self, prompt: Prompt) -> Prompt:
        self._prompts[prompt.id] = prompt
        self._save_data(self.prompt_file, None)
        return prompt

    def xǁJSONFileStorageǁcreate_prompt__mutmut_4(self, prompt: Prompt) -> Prompt:
        self._prompts[prompt.id] = prompt
        self._save_data(self._prompts)
        return prompt

    def xǁJSONFileStorageǁcreate_prompt__mutmut_5(self, prompt: Prompt) -> Prompt:
        self._prompts[prompt.id] = prompt
        self._save_data(
            self.prompt_file,
        )
        return prompt

    xǁJSONFileStorageǁcreate_prompt__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁcreate_prompt__mutmut_1": xǁJSONFileStorageǁcreate_prompt__mutmut_1,
        "xǁJSONFileStorageǁcreate_prompt__mutmut_2": xǁJSONFileStorageǁcreate_prompt__mutmut_2,
        "xǁJSONFileStorageǁcreate_prompt__mutmut_3": xǁJSONFileStorageǁcreate_prompt__mutmut_3,
        "xǁJSONFileStorageǁcreate_prompt__mutmut_4": xǁJSONFileStorageǁcreate_prompt__mutmut_4,
        "xǁJSONFileStorageǁcreate_prompt__mutmut_5": xǁJSONFileStorageǁcreate_prompt__mutmut_5,
    }
    xǁJSONFileStorageǁcreate_prompt__mutmut_orig.__name__ = "xǁJSONFileStorageǁcreate_prompt"

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        args = [prompt_id]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁget_prompt__mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁget_prompt__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁget_prompt__mutmut_orig(self, prompt_id: str) -> Optional[Prompt]:
        return self._prompts.get(prompt_id)

    def xǁJSONFileStorageǁget_prompt__mutmut_1(self, prompt_id: str) -> Optional[Prompt]:
        return self._prompts.get(None)

    xǁJSONFileStorageǁget_prompt__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁget_prompt__mutmut_1": xǁJSONFileStorageǁget_prompt__mutmut_1
    }
    xǁJSONFileStorageǁget_prompt__mutmut_orig.__name__ = "xǁJSONFileStorageǁget_prompt"

    def get_all_prompts(self) -> List[Prompt]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁget_all_prompts__mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁget_all_prompts__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁget_all_prompts__mutmut_orig(self) -> List[Prompt]:
        return list(self._prompts.values())

    def xǁJSONFileStorageǁget_all_prompts__mutmut_1(self) -> List[Prompt]:
        return list(None)

    xǁJSONFileStorageǁget_all_prompts__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁget_all_prompts__mutmut_1": xǁJSONFileStorageǁget_all_prompts__mutmut_1
    }
    xǁJSONFileStorageǁget_all_prompts__mutmut_orig.__name__ = "xǁJSONFileStorageǁget_all_prompts"

    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        args = [prompt_id, prompt]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁupdate_prompt__mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁupdate_prompt__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁupdate_prompt__mutmut_orig(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        self._save_data(self.prompt_file, self._prompts)
        return prompt

    def xǁJSONFileStorageǁupdate_prompt__mutmut_1(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        if prompt_id in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        self._save_data(self.prompt_file, self._prompts)
        return prompt

    def xǁJSONFileStorageǁupdate_prompt__mutmut_2(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = None
        self._save_data(self.prompt_file, self._prompts)
        return prompt

    def xǁJSONFileStorageǁupdate_prompt__mutmut_3(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        self._save_data(None, self._prompts)
        return prompt

    def xǁJSONFileStorageǁupdate_prompt__mutmut_4(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        self._save_data(self.prompt_file, None)
        return prompt

    def xǁJSONFileStorageǁupdate_prompt__mutmut_5(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        self._save_data(self._prompts)
        return prompt

    def xǁJSONFileStorageǁupdate_prompt__mutmut_6(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        self._save_data(
            self.prompt_file,
        )
        return prompt

    xǁJSONFileStorageǁupdate_prompt__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁupdate_prompt__mutmut_1": xǁJSONFileStorageǁupdate_prompt__mutmut_1,
        "xǁJSONFileStorageǁupdate_prompt__mutmut_2": xǁJSONFileStorageǁupdate_prompt__mutmut_2,
        "xǁJSONFileStorageǁupdate_prompt__mutmut_3": xǁJSONFileStorageǁupdate_prompt__mutmut_3,
        "xǁJSONFileStorageǁupdate_prompt__mutmut_4": xǁJSONFileStorageǁupdate_prompt__mutmut_4,
        "xǁJSONFileStorageǁupdate_prompt__mutmut_5": xǁJSONFileStorageǁupdate_prompt__mutmut_5,
        "xǁJSONFileStorageǁupdate_prompt__mutmut_6": xǁJSONFileStorageǁupdate_prompt__mutmut_6,
    }
    xǁJSONFileStorageǁupdate_prompt__mutmut_orig.__name__ = "xǁJSONFileStorageǁupdate_prompt"

    def delete_prompt(self, prompt_id: str) -> bool:
        args = [prompt_id]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁdelete_prompt__mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁdelete_prompt__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁdelete_prompt__mutmut_orig(self, prompt_id: str) -> bool:
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            self._save_data(self.prompt_file, self._prompts)
            return True
        return False

    def xǁJSONFileStorageǁdelete_prompt__mutmut_1(self, prompt_id: str) -> bool:
        if prompt_id not in self._prompts:
            del self._prompts[prompt_id]
            self._save_data(self.prompt_file, self._prompts)
            return True
        return False

    def xǁJSONFileStorageǁdelete_prompt__mutmut_2(self, prompt_id: str) -> bool:
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            self._save_data(None, self._prompts)
            return True
        return False

    def xǁJSONFileStorageǁdelete_prompt__mutmut_3(self, prompt_id: str) -> bool:
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            self._save_data(self.prompt_file, None)
            return True
        return False

    def xǁJSONFileStorageǁdelete_prompt__mutmut_4(self, prompt_id: str) -> bool:
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            self._save_data(self._prompts)
            return True
        return False

    def xǁJSONFileStorageǁdelete_prompt__mutmut_5(self, prompt_id: str) -> bool:
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            self._save_data(
                self.prompt_file,
            )
            return True
        return False

    def xǁJSONFileStorageǁdelete_prompt__mutmut_6(self, prompt_id: str) -> bool:
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            self._save_data(self.prompt_file, self._prompts)
            return False
        return False

    def xǁJSONFileStorageǁdelete_prompt__mutmut_7(self, prompt_id: str) -> bool:
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            self._save_data(self.prompt_file, self._prompts)
            return True
        return True

    xǁJSONFileStorageǁdelete_prompt__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁdelete_prompt__mutmut_1": xǁJSONFileStorageǁdelete_prompt__mutmut_1,
        "xǁJSONFileStorageǁdelete_prompt__mutmut_2": xǁJSONFileStorageǁdelete_prompt__mutmut_2,
        "xǁJSONFileStorageǁdelete_prompt__mutmut_3": xǁJSONFileStorageǁdelete_prompt__mutmut_3,
        "xǁJSONFileStorageǁdelete_prompt__mutmut_4": xǁJSONFileStorageǁdelete_prompt__mutmut_4,
        "xǁJSONFileStorageǁdelete_prompt__mutmut_5": xǁJSONFileStorageǁdelete_prompt__mutmut_5,
        "xǁJSONFileStorageǁdelete_prompt__mutmut_6": xǁJSONFileStorageǁdelete_prompt__mutmut_6,
        "xǁJSONFileStorageǁdelete_prompt__mutmut_7": xǁJSONFileStorageǁdelete_prompt__mutmut_7,
    }
    xǁJSONFileStorageǁdelete_prompt__mutmut_orig.__name__ = "xǁJSONFileStorageǁdelete_prompt"

    def create_collection(self, collection: Collection) -> Collection:
        args = [collection]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁcreate_collection__mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁcreate_collection__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁcreate_collection__mutmut_orig(self, collection: Collection) -> Collection:
        self._collections[collection.id] = collection
        self._save_data(self.collection_file, self._collections)
        return collection

    def xǁJSONFileStorageǁcreate_collection__mutmut_1(self, collection: Collection) -> Collection:
        self._collections[collection.id] = None
        self._save_data(self.collection_file, self._collections)
        return collection

    def xǁJSONFileStorageǁcreate_collection__mutmut_2(self, collection: Collection) -> Collection:
        self._collections[collection.id] = collection
        self._save_data(None, self._collections)
        return collection

    def xǁJSONFileStorageǁcreate_collection__mutmut_3(self, collection: Collection) -> Collection:
        self._collections[collection.id] = collection
        self._save_data(self.collection_file, None)
        return collection

    def xǁJSONFileStorageǁcreate_collection__mutmut_4(self, collection: Collection) -> Collection:
        self._collections[collection.id] = collection
        self._save_data(self._collections)
        return collection

    def xǁJSONFileStorageǁcreate_collection__mutmut_5(self, collection: Collection) -> Collection:
        self._collections[collection.id] = collection
        self._save_data(
            self.collection_file,
        )
        return collection

    xǁJSONFileStorageǁcreate_collection__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁcreate_collection__mutmut_1": xǁJSONFileStorageǁcreate_collection__mutmut_1,
        "xǁJSONFileStorageǁcreate_collection__mutmut_2": xǁJSONFileStorageǁcreate_collection__mutmut_2,
        "xǁJSONFileStorageǁcreate_collection__mutmut_3": xǁJSONFileStorageǁcreate_collection__mutmut_3,
        "xǁJSONFileStorageǁcreate_collection__mutmut_4": xǁJSONFileStorageǁcreate_collection__mutmut_4,
        "xǁJSONFileStorageǁcreate_collection__mutmut_5": xǁJSONFileStorageǁcreate_collection__mutmut_5,
    }
    xǁJSONFileStorageǁcreate_collection__mutmut_orig.__name__ = "xǁJSONFileStorageǁcreate_collection"

    def get_collection(self, collection_id: str) -> Optional[Collection]:
        args = [collection_id]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁget_collection__mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁget_collection__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁget_collection__mutmut_orig(self, collection_id: str) -> Optional[Collection]:
        return self._collections.get(collection_id)

    def xǁJSONFileStorageǁget_collection__mutmut_1(self, collection_id: str) -> Optional[Collection]:
        return self._collections.get(None)

    xǁJSONFileStorageǁget_collection__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁget_collection__mutmut_1": xǁJSONFileStorageǁget_collection__mutmut_1
    }
    xǁJSONFileStorageǁget_collection__mutmut_orig.__name__ = "xǁJSONFileStorageǁget_collection"

    def get_all_collections(self) -> List[Collection]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁget_all_collections__mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁget_all_collections__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁget_all_collections__mutmut_orig(self) -> List[Collection]:
        return list(self._collections.values())

    def xǁJSONFileStorageǁget_all_collections__mutmut_1(self) -> List[Collection]:
        return list(None)

    xǁJSONFileStorageǁget_all_collections__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁget_all_collections__mutmut_1": xǁJSONFileStorageǁget_all_collections__mutmut_1
    }
    xǁJSONFileStorageǁget_all_collections__mutmut_orig.__name__ = "xǁJSONFileStorageǁget_all_collections"

    def delete_collection(self, collection_id: str) -> bool:
        args = [collection_id]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁdelete_collection__mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁdelete_collection__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁdelete_collection__mutmut_orig(self, collection_id: str) -> bool:
        if collection_id in self._collections:
            del self._collections[collection_id]
            self._save_data(self.collection_file, self._collections)
            return True
        return False

    def xǁJSONFileStorageǁdelete_collection__mutmut_1(self, collection_id: str) -> bool:
        if collection_id not in self._collections:
            del self._collections[collection_id]
            self._save_data(self.collection_file, self._collections)
            return True
        return False

    def xǁJSONFileStorageǁdelete_collection__mutmut_2(self, collection_id: str) -> bool:
        if collection_id in self._collections:
            del self._collections[collection_id]
            self._save_data(None, self._collections)
            return True
        return False

    def xǁJSONFileStorageǁdelete_collection__mutmut_3(self, collection_id: str) -> bool:
        if collection_id in self._collections:
            del self._collections[collection_id]
            self._save_data(self.collection_file, None)
            return True
        return False

    def xǁJSONFileStorageǁdelete_collection__mutmut_4(self, collection_id: str) -> bool:
        if collection_id in self._collections:
            del self._collections[collection_id]
            self._save_data(self._collections)
            return True
        return False

    def xǁJSONFileStorageǁdelete_collection__mutmut_5(self, collection_id: str) -> bool:
        if collection_id in self._collections:
            del self._collections[collection_id]
            self._save_data(
                self.collection_file,
            )
            return True
        return False

    def xǁJSONFileStorageǁdelete_collection__mutmut_6(self, collection_id: str) -> bool:
        if collection_id in self._collections:
            del self._collections[collection_id]
            self._save_data(self.collection_file, self._collections)
            return False
        return False

    def xǁJSONFileStorageǁdelete_collection__mutmut_7(self, collection_id: str) -> bool:
        if collection_id in self._collections:
            del self._collections[collection_id]
            self._save_data(self.collection_file, self._collections)
            return True
        return True

    xǁJSONFileStorageǁdelete_collection__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁdelete_collection__mutmut_1": xǁJSONFileStorageǁdelete_collection__mutmut_1,
        "xǁJSONFileStorageǁdelete_collection__mutmut_2": xǁJSONFileStorageǁdelete_collection__mutmut_2,
        "xǁJSONFileStorageǁdelete_collection__mutmut_3": xǁJSONFileStorageǁdelete_collection__mutmut_3,
        "xǁJSONFileStorageǁdelete_collection__mutmut_4": xǁJSONFileStorageǁdelete_collection__mutmut_4,
        "xǁJSONFileStorageǁdelete_collection__mutmut_5": xǁJSONFileStorageǁdelete_collection__mutmut_5,
        "xǁJSONFileStorageǁdelete_collection__mutmut_6": xǁJSONFileStorageǁdelete_collection__mutmut_6,
        "xǁJSONFileStorageǁdelete_collection__mutmut_7": xǁJSONFileStorageǁdelete_collection__mutmut_7,
    }
    xǁJSONFileStorageǁdelete_collection__mutmut_orig.__name__ = "xǁJSONFileStorageǁdelete_collection"

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        args = [collection_id]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁJSONFileStorageǁget_prompts_by_collection__mutmut_orig"),
            object.__getattribute__(self, "xǁJSONFileStorageǁget_prompts_by_collection__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁJSONFileStorageǁget_prompts_by_collection__mutmut_orig(self, collection_id: str) -> List[Prompt]:
        return [p for p in self._prompts.values() if p.collection_id == collection_id]

    def xǁJSONFileStorageǁget_prompts_by_collection__mutmut_1(self, collection_id: str) -> List[Prompt]:
        return [p for p in self._prompts.values() if p.collection_id != collection_id]

    xǁJSONFileStorageǁget_prompts_by_collection__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁJSONFileStorageǁget_prompts_by_collection__mutmut_1": xǁJSONFileStorageǁget_prompts_by_collection__mutmut_1
    }
    xǁJSONFileStorageǁget_prompts_by_collection__mutmut_orig.__name__ = "xǁJSONFileStorageǁget_prompts_by_collection"
