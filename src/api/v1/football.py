from fastapi import APIRouter

from model.team import Team
from model.match import Match
from model.statistic import Statistic
from service.football_api_client import FootballAPIClient
import random

router = APIRouter()
client = FootballAPIClient()

@router.get('/team')
async def get_team() -> Team:
    return client.get_team(2061)

@router.get('/matches')
async def get_matches() -> list[Match]:
    return [set_statistic(match) for match in client.get_matches().matches ]

def set_statistic(match: Match):
    match.statistic.shots_on_goal = random.randint(1, 20)
    match.statistic.finishes = random.randint(1, 20)
    match.statistic.corners = random.randint(1, 20)
    match.statistic.goals = random.randint(1, 20)
    return match
