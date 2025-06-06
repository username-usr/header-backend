from pydantic import BaseModel
from typing import List, Dict

class GenerateTableRequest(BaseModel):
    prompt: str
    model: str = "mistralai/devstral-small:free"

class CellMapRequest(BaseModel):
    prompt: str
    model: str = "mistralai/devstral-small:free"

class TransformTableRequest(BaseModel):
    prompt: str
    table: List[Dict]
    model: str = "mistralai/devstral-small:free"
