from typing import Any, Dict, List

from pydantic import BaseModel


class KVBatch(BaseModel):
    data: Dict[str, Any]


class KeyBatch(BaseModel):
    keys: List[str]
