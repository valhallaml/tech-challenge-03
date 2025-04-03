from pydantic import BaseModel

class Statistic(BaseModel):
    shots_on_goal: int = 0
    finishes: int = 0
    corners: int = 0
    goals: int = 0