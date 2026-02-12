from typing import Dict, Optional, List
import json
import os

from app.models import Prompt, Collection


class JSONFileStorage:
    def __init__(self, prompt_file='prompts.json', collection_file='collections.json'):
        self.prompt_file = prompt_file
        self.collection_file = collection_file
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._load_data()
    
    def _load_data(self):
        """Load prompts and collections from files."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, 'r') as f:
                prompts = json.load(f)
                for p in prompts:
                    self._prompts[p['id']] = Prompt(**p)
        
        if os.path.exists(self.collection_file):
            with open(self.collection_file, 'r') as f:
                collections = json.load(f)
                for c in collections:
                    self._collections[c['id']] = Collection(**c)
    
    def _save_data(self, file_path: str, data: Dict):
        """Save data back to the associated JSON file."""
        serialized_data = []
        for v in data.values():
            item_dict = v.model_dump()
            # Convert datetime fields to ISO format or handle as needed
            if 'created_at' in item_dict and item_dict['created_at']:
                item_dict['created_at'] = item_dict['created_at'].isoformat()
            if 'updated_at' in item_dict and item_dict['updated_at']:
                item_dict['updated_at'] = item_dict['updated_at'].isoformat()
            serialized_data.append(item_dict)
        
        with open(file_path, 'w') as f:
            json.dump(serialized_data, f, indent=4)
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        self._prompts[prompt.id] = prompt
        self._save_data(self.prompt_file, self._prompts)
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        self._save_data(self.prompt_file, self._prompts)
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            self._save_data(self.prompt_file, self._prompts)
            return True
        return False
    
    def create_collection(self, collection: Collection) -> Collection:
        self._collections[collection.id] = collection
        self._save_data(self.collection_file, self._collections)
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        if collection_id in self._collections:
            del self._collections[collection_id]
            self._save_data(self.collection_file, self._collections)
            return True
        return False

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        return [p for p in self._prompts.values() if p.collection_id == collection_id]