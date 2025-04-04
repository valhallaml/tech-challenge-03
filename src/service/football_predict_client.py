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

        #pegar todas as infos do banco
        result: list[MatchEntity] = MatchEntityRepository.find_all(db)

        data = [
            {k: v for k, v in row.__dict__.items() if k != '_sa_instance_state'}
            for row in result
        ]

        df = pd.DataFrame(data)

        # Definindo features e target
        X = df[['shots_on_goal', 'finishes', 'corners', 'goals']]
        y = df[['winner']]

        # Normalizando os dados
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(X)

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
        new_data = pd.DataFrame([data])

        # Normalizar os novos dados
        new_data_scaled = scaler.transform(new_data)

        # Fazer a previsão
        prediction = model.predict(new_data_scaled)
        
        return "Campeão" if prediction[0] == 1 else "Não Campeão"