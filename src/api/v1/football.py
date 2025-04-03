from fastapi import APIRouter

from model.team import Team
from model.match import Match
from service.football_api_client import FootballAPIClient

router = APIRouter()
client = FootballAPIClient()

@router.get('/team')
async def get_team() -> Team:
    return client.get_team(2061)

@router.get('/matches')
async def get_matches() -> list[Match]:
    return client.get_matches().matches