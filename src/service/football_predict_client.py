import os
import time
import requests
from typing import Dict
import joblib

from model.team import Team
from model.matches import Matches
from core.configs import settings
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from repository.match import MatchEntityRepository
from entity.match import MatchEntity


class FootballPredictClient:
    
    def model(self, db):

        # pegar todas as infos do banco
        result: list[MatchEntity] = MatchEntityRepository.find_all(db)

        data = {
            'shots_on_goal': [m.shots_on_goal for m in result],
            'finishes': [m.finishes for m in result],
            'corners': [m.corners for m in result],
            'goals': [m.goals for m in result],
            'winner': [m.winner for m in result]
        }

        df = pd.DataFrame(data)

        # Definindo features e target
        x = df[['shots_on_goal', 'finishes', 'corners', 'goals']]
        y = df['winner']

        # Normalizando os dados
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)

        # Dividindo em treino e teste
        x_train, _, y_train, _ = train_test_split(x_scaled, y, test_size=0.3, random_state=42, stratify=y)

        # Criando o modelo de regressão logística
        model = LogisticRegression(max_iter=500)
        model.fit(x_train, y_train)

        # ** Salvando o modelo treinado e o scaler **
        joblib.dump(model, 'modelo_campeao.pkl')
        joblib.dump(scaler, 'scaler.pkl')

        print("Modelo e scaler salvos com sucesso!")

    def predict(self, data: dict) -> str:
        
        # Carregar o modelo e o scaler
        model = joblib.load('modelo_campeao.pkl')
        scaler = joblib.load('scaler.pkl')

        # Criar novos dados para previsão
        new_data = pd.DataFrame([list(data.values())])

        # Normalizar os novos dados
        new_data_scaled = scaler.transform(new_data)

        # Fazer a previsão
        prediction = model.predict(new_data_scaled)
        
        return "Campeão" if prediction[0] == 1 else "Não Campeão"