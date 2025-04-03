from pydantic import BaseModel

class FullTime(BaseModel):
    home: int
    away: int
