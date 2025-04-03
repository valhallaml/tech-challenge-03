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


class FootballPredictClient:
    
    def model(self):

        #pegar todas as infos do banco
        data = []

        df = pd.DataFrame(data)

        # Definindo features e target
        X = df[['finalizacoes', 'posse_bola', 'escanteios', 'gols_marcados', 'vitoria']]
        y = df['campeao']

        # Normalizando os dados
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Dividindo em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)

        # Criando o modelo de regressão logística
        model = LogisticRegression(max_iter=500)
        model.fit(X_train, y_train)

        # ** Salvando o modelo treinado e o scaler **
        joblib.dump(model, 'modelo_campeao.pkl')
        joblib.dump(scaler, 'scaler.pkl')

        print("Modelo e scaler salvos com sucesso!")

    def predict(data: dict) -> str:
        
        # Carregar o modelo e o scaler
        model = joblib.load('modelo_campeao.pkl')
        scaler = joblib.load('scaler.pkl')

        # Criar novos dados para previsão
        new_data = pd.DataFrame(data)

        # Normalizar os novos dados
        new_data_scaled = scaler.transform(new_data)

        # Fazer a previsão
        prediction = model.predict(new_data_scaled)
        
        return "Campeão" if prediction[0] == 1 else "Não Campeão"