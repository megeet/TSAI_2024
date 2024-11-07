from pydantic import BaseModel
from typing import List, Dict, Any

class DataResponse(BaseModel):
    filename: str
    headers: List[str]
    data: List[Dict[str, Any]] 