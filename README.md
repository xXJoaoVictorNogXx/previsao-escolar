# EducaPrev - Sistema Inteligente de Previsão de Desempenho Escolar 🎓🧠

## 1. Entendimento do Problema e Valor do Projeto
[cite_start]Atualmente, a gestão educacional pública enfrenta um desafio crítico: altos índices de baixo desempenho e evasão escolar[cite: 9]. [cite_start]Embora exista uma grande quantidade de dados armazenados (notas, frequência, contexto social), a atuação da gestão pública costuma ser reativa, identificando os problemas apenas após o fracasso escolar[cite: 10, 11].

O **EducaPrev** foi desenvolvido para transformar dados brutos em inteligência preditiva. [cite_start]O sistema é capaz de aprender com dados históricos e prever quais alunos estão em risco[cite: 13, 42]. [cite_start]Isso gera um **alto valor para a gestão pública**, pois permite a transição de uma postura reativa para uma postura proativa, viabilizando ações antecipadas como acompanhamento pedagógico e intervenções sociais antes que o aluno evada[cite: 13, 27].

## 2. A Solução Proposta e IA Utilizada
Desenvolvemos uma aplicação full-stack composta por uma interface intuitiva para gestores e uma API inteligente. [cite_start]O "cérebro" do sistema utiliza **Redes Neurais Artificiais** para identificar padrões ocultos e gerar previsões[cite: 18]. 

[cite_start]Especificamente, utilizamos uma arquitetura **MLP (Multilayer Perceptron)**, ideal para lidar com dados estruturados[cite: 71]. [cite_start]A base de dados utilizada para o treinamento foi a *Student Alcohol Consumption* (Kaggle), cujas variáveis comportamentais, familiares e acadêmicas mostraram forte correlação com o desempenho final do aluno[cite: 36, 37, 38]. 

### Etapas do Desenvolvimento do Modelo:
* **Tratamento de Dados:** Seleção de atributos relevantes (Faltas, Tempo de Estudo, Histórico de Reprovações e Notas G1/G2). Utilização do `StandardScaler` para padronização.
* [cite_start]**Treinamento:** Modelo classificador MLP treinado com *backpropagation*[cite: 45]. Definimos o critério de risco para alunos com nota final (G3) inferior a 10.
* [cite_start]**Resultados e Métricas:** O modelo demonstrou alta capacidade de generalização e confiança na identificação de padrões de risco, evitando *overfitting*[cite: 62].

## 3. Tecnologias Utilizadas 🛠️

**Front-end (Interface do Gestor):**
* Next.js (App Router)
* React & TypeScript
* Tailwind CSS (Estilização ágil e responsiva)

**Back-end (API de IA):**
* Python 3
* FastAPI & Uvicorn (Alta performance para servir o modelo)
* Scikit-Learn (Treinamento da Rede Neural MLP)
* Pandas & NumPy (Manipulação e estruturação dos dados)
* Joblib (Serialização do modelo)

## 4. Como Rodar o Projeto Localmente 🚀

Este projeto é dividido em duas partes: a API (Python) e o Dashboard (Next.js). Siga os passos abaixo:

### Pré-requisitos
* Node.js instalado (v18+)
* Python 3 instalado

### Passo A: Rodando a API (Inteligência Artificial)
1. Clone o repositório e acesse a pasta da API:
   ```bash
   cd api-educaprev
Instale as dependências:

Bash
pip install fastapi uvicorn scikit-learn pandas pydantic joblib
(Opcional) Para retreinar o modelo com os dados do Kaggle:

Bash
python treinar_modelo.py
Inicie o servidor da API:

Bash
uvicorn main:app --reload
A API estará rodando em http://localhost:8000. Acesse http://localhost:8000/docs para ver a documentação do Swagger.

Passo B: Rodando o Front-end (Dashboard)
Abra um novo terminal e acesse a pasta do front-end:

Bash
cd previsao-escolar
Instale as dependências do Next.js:

Bash
npm install
Inicie o servidor de desenvolvimento:

Bash
npm run dev
O sistema estará disponível em http://localhost:3000.

5. Divisão do Trabalho em Equipe 👥

Código:
[João Victor Ferreira Cantanhede Nogueira]: 

Montagem do slide:
[Rafael Yori]
[Pedro Henrique Carvalho de Oliveira]

Montagem do README:
[Leonardo Gustavo Machado Campos]
[Ryan Lucas Rocha Nunes]


6. Limitações e Trabalhos Futuros
O sistema atual se baseia em uma base de dados externa com viés cultural específico (escolas em Portugal). Como melhoria futura, sugere-se o retreinamento do modelo (fine-tuning) com os dados demográficos reais e específicos da prefeitura local para aumentar a precisão da interferência sociodemográfica no aprendizado do algoritmo
