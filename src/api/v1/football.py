from fastapi import APIRouter

from model.team import Team
from model.match import Match
from service.football_api_client import FootballAPIClient
from service.football_predict_client import FootballPredictClient
from fastapi.responses import JSONResponse

router = APIRouter()
client = FootballAPIClient()
clientPredict = FootballPredictClient()

@router.get('/team')
async def get_team() -> Team:
    return client.get_team(2061)

@router.get('/matches')
async def get_matches() -> list[Match]:
    return client.get_matches().matches


@router.get('/treinar')
async def get_treinar() -> list[Match]:
    return clientPredict.model()


@router.post("/consultar_time")
async def consultar_time(data: dict):

    finalizacoes = data.get("finalizacoes")
    passebola = data.get("passebola")
    escanteios = data.get("escanteios")

    predict = clientPredict.predict([finalizacoes, passebola, escanteios])

    return JSONResponse(content={"time": predict})