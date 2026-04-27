import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib


try:
    df = pd.read_csv('student-mat.csv', sep=',')
    print("✅ Arquivo carregado com sucesso!")
    
    print("\n🔍 Colunas que o Pandas encontrou:")
    print(df.columns.tolist())
    print("-" * 30)
    
except FileNotFoundError:
    print("❌ Erro: O arquivo não foi encontrado.")
    exit()

df['situacao_risco'] = (df['G3'] < 10).astype(int)


X = df[['studytime', 'failures', 'absences', 'G1', 'G2']]
y = df['situacao_risco']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. Treinar a Rede Neural MLP
# Aumentei um pouco as camadas para lidar com os dados reais
modelo = MLPClassifier(
    hidden_layer_sizes=(16, 8), 
    max_iter=2000,              
    activation='relu',          
    solver='adam',              
    random_state=42
)

print("🧠 Treinando a rede neural... aguarde.")
modelo.fit(X_train_scaled, y_train)

joblib.dump(modelo, 'modelo_mlp.pkl')
joblib.dump(scaler, 'scaler.pkl')

acuracia = modelo.score(X_test_scaled, y_test)
print(f"✅ Modelo treinado! Acurácia nos dados de teste: {acuracia * 100:.2f}%")
print("📂 Arquivos 'modelo_mlp.pkl' e 'scaler.pkl' gerados.")