from pydantic import BaseModel, Field
from model.team import Team
from model.score import Score

class Match(BaseModel):
    id: int
    home_team: Team = Field(None, alias = 'homeTeam')
    away_team: Team = Field(None, alias = 'awayTeam')
    score: Score
