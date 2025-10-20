# 🎬 Análise de Dados de Cinema - Pipeline ETL
<br>
Um projeto de análise de dados sobre o mercado de cinema antes durante e após a pandemia de covid-19, implementando um pipeline ETL completo com Python e visualização interativa.
<br>
Sobre o Projeto
<br>
Este projeto coleta, processa e analisa dados dos top 50 filmes do TMDB por faturamento global de 2014 a 2024 e dados de faturamento total de cinema do box office mojo, transformando dados brutos da API em insights visuais através de um dashboard interativo.
<br>

# 🛠️ Tecnologias Utilizadas

    Python 3 - Linguagem principal

    Pandas - Manipulação e análise de dados

    Plotly - Gráficos interativos e visualizações

    Streamlit - Dashboard e interface web

    Requests - Integração com APIs

    TMDB API / 2025 Worldwide Box Office - Fonte de dados dos filmes

# 📁 Estrutura do Projeto
projeto_analise_filmes/
├── extract.py                  # Coleta dados da API
├── treatment.py                # Limpeza e criação de tabelas auxiliares
├── dash.py                     # Dashboard Streamlit
├── tmdb_movies.csv             # Dados brutos TMDB
├── boxoffice.csv               # Dados brutos Box Office mojo
├── clean_data.csv              # Dados processados
└── moviedata.pdf               # Exemplo de pdf extraído do meu projeto

# 🎮 Como executar
1. Clone o repositório
bash

git clone https://github.com/seu-usuario/projeto_analise_filmes.git
cd projeto_analise_filmes

2. Instale as dependências
Necessário instalar python, streamlit e pyplot (instalando o streamlit, você já recebe a biblioteca pandas)

3. Execute o dashboard
bash

streamlit run app.py

4. Acesse no navegador
text

http://localhost:8501

📈 Funcionalidades do Dashboard

    📊 Gráficos: Quantidade de Filmes lançados, distribuição por país de origem, comparações entre faturamento e orçamento dos filmes e muito mais!
   
    🔍 Análises: feitas com base no insight dos gráficos e algumas pesquisas relacionadas ao mercado de cinema.
