print("🚨 INICIANDO O SCRIPT DE ACURÁCIA...") # Coloque isso no topo!
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split

print("Carregando o modelo salvo...")

# 1. Carrega os dados reais para podermos testar
df = pd.read_csv('student-mat.csv', sep=',') # Lembre-se de mudar para ';' se o seu for com ponto e vírgula
df['situacao_risco'] = (df['G3'] < 10).astype(int)

X = df[['studytime', 'failures', 'absences', 'G1', 'G2']]
y = df['situacao_risco']

# 2. Recria exatamente a mesma "prova" que usamos no treinamento (o segredo é o random_state=42)
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Carrega o cérebro (modelo) e o nivelador (scaler) já treinados
modelo = joblib.load('modelo_mlp.pkl')
scaler = joblib.load('scaler.pkl')

# 4. Nivela os dados de teste e calcula a acurácia
X_test_scaled = scaler.transform(X_test)
acuracia = modelo.score(X_test_scaled, y_test)

print("-" * 30)
print(f"📊 Acurácia do modelo salvo: {acuracia * 100:.2f}%")
print("-" * 30)