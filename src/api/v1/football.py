from fastapi import APIRouter, Depends

from model.team import Team
from model.match import Match
from service.football_api_client import FootballAPIClient
from service.football_predict_client import FootballPredictClient
from fastapi.responses import JSONResponse
from repository.match import MatchEntityRepository
from entity.match import MatchEntity

from core.database import SessionLocal
from core.session import get_session

import random

router = APIRouter()
client = FootballAPIClient()
clientPredict = FootballPredictClient()

@router.get('/team')
async def get_team() -> Team:
    return client.get_team(2061)

@router.get('/matches')
async def get_matches(db = Depends(get_session)) -> bool:
    matches = [to_entity(match) for match in client.get_matches().matches ]
    for match in matches:
        MatchEntityRepository.save(db, match)
    return True

@router.get('/treinar')
async def get_treinar(db = Depends(get_session)):
    return clientPredict.model(db=db)

@router.post("/consultar_time")
async def consultar_time(data: dict):

    shots_on_goal = data.get('shots_on_goal')
    finishes = data.get('finishes')
    corners = data.get('corners')
    goals = data.get('goals')

    data = {
        'shots_on_goal': int(shots_on_goal),
        'finishes': int(finishes),
        'corners': int(corners),
        'goals': int(goals)
    }
    predict = clientPredict.predict(data)

    return predict

def to_entity(match: Match) -> MatchEntity:

    match_entity = MatchEntity()

    match_entity.match_id = match.id
    match_entity.home_team = match.home_team.short_name
    match_entity.away_team = match.away_team.short_name
    match_entity.winner = get_winner(match.score.winner)

    match_entity.shots_on_goal = random.randint(0, 15)
    match_entity.finishes = random.randint(0, 15)
    match_entity.corners = random.randint(0, 20)
    match_entity.goals = random.randint(0, 4)

    return match_entity

def get_winner(winner: str) -> int:
    if winner == 'HOME_TEAM':
        return 1
    return 0