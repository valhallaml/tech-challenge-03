from pydantic import BaseModel, Field
from model.match import Match

class Matches(BaseModel):
    matches: list[Match]
