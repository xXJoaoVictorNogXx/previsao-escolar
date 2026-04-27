from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="EducaPrev API", description="API de previsão de risco escolar")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    modelo = joblib.load('modelo_mlp.pkl')
    scaler = joblib.load('scaler.pkl')
except:
    print("Atenção: Rode o script treinar_modelo.py primeiro!")

class AlunoData(BaseModel):
    studytime: int
    failures: int
    absences: int
    G1: float
    G2: float

@app.post("/api/prever")
async def prever_risco(dados: AlunoData):
    entrada = np.array([[
        dados.studytime, 
        dados.failures, 
        dados.absences, 
        dados.G1, 
        dados.G2
    ]])
    
    entrada_scaled = scaler.transform(entrada)
    
    previsao = modelo.predict(entrada_scaled)[0]
    
    probabilidades = modelo.predict_proba(entrada_scaled)[0]
    probabilidade_risco = round(probabilidades[1] * 100, 2)
    
    if previsao == 1:
        status = "Alto Risco de Evasão/Reprovação"
    else:
        status = "Baixo Risco (Desempenho Adequado)"
        
    return {
        "status": status,
        "probabilidade": probabilidade_risco,
        "dados_analisados": dados.dict()
    }

@app.get("/")
def home():
    return {"mensagem": "API EducaPrev Online. Use a rota POST /api/prever"}