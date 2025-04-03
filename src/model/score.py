from pydantic import BaseModel
from model.full_time import FullTime

class Score(BaseModel):
    winner: str
    fullTime: FullTime
