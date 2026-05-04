import streamlit as st
import pandas as pd
import joblib
import os

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))

caminho_modelo = os.path.join(PASTA_ATUAL, 'modelo_mlp.pkl')
caminho_scaler = os.path.join(PASTA_ATUAL, 'scaler.pkl')

modelo = joblib.load(caminho_modelo)
scaler = joblib.load(caminho_scaler)


st.set_page_config(page_title="EducaPrev Dashboard", page_icon="📊", layout="wide")

st.title("📊 EducaPrev - Sistema de Inteligência Pedagógica")
st.markdown("Insira os indicadores do aluno para gerar o **Relatório Preditivo de Desempenho**.")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎒 Perfil Acadêmico")
    studytime = st.selectbox("Tempo de Estudo Semanal", [1, 2, 3, 4], help="1: <2h, 2: 2-5h, 3: 5-10h, 4: >10h")
    failures = st.number_input("Reprovações Anteriores", min_value=0, max_value=10, value=0)

with col2:
    st.subheader("📅 Frequência")
    absences = st.number_input("Número Total de Faltas", min_value=0, max_value=93, value=0)

with col3:
    st.subheader("📝 Notas (0 a 20)")
    g1 = st.slider("1º Período (G1)", min_value=0, max_value=20, value=12)
    g2 = st.slider("2º Período (G2)", min_value=0, max_value=20, value=12)

st.markdown("---")

if st.button("🚀 Gerar Análise Completa do Aluno", use_container_width=True):
    
    dados_aluno = pd.DataFrame({'studytime': [studytime], 'failures': [failures], 'absences': [absences], 'G1': [g1], 'G2': [g2]})
    dados_nivelados = scaler.transform(dados_aluno)
    
    previsao = modelo.predict(dados_nivelados)[0]
    probabilidade_risco = modelo.predict_proba(dados_nivelados)[0][1] * 100 # Pega a chance da classe 1 (Risco)
    
    # SEÇÃO DE RESULTADOS NA TELA
    st.header("📋 Relatório Preditivo")
    
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        if previsao == 1:
            st.error("🚨 **ALTO RISCO DE EVASÃO OU REPROVAÇÃO**")
            st.metric(label="Probabilidade de Insucesso (Rede Neural)", value=f"{probabilidade_risco:.1f}%")
            st.progress(int(probabilidade_risco))
        else:
            st.success("✅ **ALUNO FORA DE RISCO**")
            st.metric(label="Probabilidade de Insucesso", value=f"{probabilidade_risco:.1f}%")
            st.progress(int(probabilidade_risco))
            
    with res_col2:
        st.markdown("**📉 Evolução das Notas (G1 → G2)**")
        grafico_notas = pd.DataFrame({"Notas": [g1, g2]}, index=["1º Período", "2º Período"])
        st.line_chart(grafico_notas, height=150)
        
        if g2 < g1:
            st.warning("⚠️ O desempenho caiu do 1º para o 2º período.")
        elif g2 > g1:
            st.info("📈 O desempenho está melhorando.")
        else:
            st.info("➖ O desempenho está estagnado.")

    st.markdown("---")
    
    st.subheader("💡 Plano de Ação Recomendado")
    
    acoes = []
    if absences > 10:
        acoes.append("- **Atenção Familiar:** Número de faltas elevado. Recomenda-se contato imediato com os responsáveis para investigar os motivos da ausência.")
    if studytime <= 2:
        acoes.append("- **Apoio Pedagógico:** Baixo tempo de estudo reportado. Inserir o aluno em grupos de reforço escolar no contraturno.")
    if failures > 0:
        acoes.append("- **Acompanhamento Psicológico:** Histórico de reprovação anterior detectado. O aluno pode precisar de suporte para lidar com frustração acadêmica.")
    if g2 < 10:
        acoes.append("- **Recuperação Imediata:** Notas atuais abaixo da média exigida. Revisão intensiva das matérias críticas.")
        
    if not acoes and previsao == 0:
        st.write("🌟 Manter o aluno no fluxo normal. Não há intervenções críticas necessárias no momento.")
    else:
        for acao in acoes:
            st.write(acao)