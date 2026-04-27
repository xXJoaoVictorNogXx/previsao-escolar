from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

# Inicializa a API
app = FastAPI(title="EducaPrev API", description="API de previsão de risco escolar")

# Configuração de CORS (Permite que o seu Next.js converse com esta API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, coloque a URL do seu front-end
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega o modelo e o scaler que treinamos no Passo 2
try:
    modelo = joblib.load('modelo_mlp.pkl')
    scaler = joblib.load('scaler.pkl')
except:
    print("Atenção: Rode o script treinar_modelo.py primeiro!")

# Define o formato dos dados que o Front-end vai enviar
class AlunoData(BaseModel):
    studytime: int
    failures: int
    absences: int
    G1: float
    G2: float

@app.post("/api/prever")
async def prever_risco(dados: AlunoData):
    # Transforma os dados que chegaram do JSON em um formato que a IA entende
    entrada = np.array([[
        dados.studytime, 
        dados.failures, 
        dados.absences, 
        dados.G1, 
        dados.G2
    ]])
    
    # Padroniza a entrada
    entrada_scaled = scaler.transform(entrada)
    
    # Faz a previsão (0 = Baixo Risco, 1 = Alto Risco/Evasão)
    previsao = modelo.predict(entrada_scaled)[0]
    
    # Pega a probabilidade (certeza) da IA (ex: 85% de chance)
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