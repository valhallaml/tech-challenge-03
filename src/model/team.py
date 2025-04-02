from pydantic import BaseModel, Field
from typing import Optional

class Team(BaseModel):
    id: int
    name: str
    short_name: Optional[str] = Field(None, alias='shortName')
