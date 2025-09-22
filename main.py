import requests
import pandas as pd
import time
import csv
import json


#Fazer uma função que coleta todas as movie ids dos top 10 filmes

def extrair_tmdb(ano, pag):
    filme_id = []
    for pagina in range(1, pag+1):
        r = requests.get("https://api.themoviedb.org/3/discover/movie",
                          params={
                              "api_key":"SUA API",
                              "language":"en-US",
                              "page":pagina,
                              "primary_release_year":ano,
                              "sort_by":"revenue.desc"},
                           timeout=10
                        )
        r.raise_for_status()
        dados = r.json()
        for item in dados.get("results",[]):
            filme_id.append(item["id"])
        time.sleep(0.25)
    return filme_id[:10]

#Função que retorna a partir dos ids de filme, os detalhes dos filmes

def detalhe_tmdb(filme_id):
    url = f"https://api.themoviedb.org/3/movie/{filme_id}?language=en-US"
    headers = {
                "accept": "application/json",
                "Authorization": "Seu token do tmdb"}
    r = requests.get(url, headers=headers,
                     timeout=10
                    )
    r.raise_for_status()
    return r.json()

#Função que exporta os dados para o excel

def exportar_para_csv(dados_filmes, nome_arquivo='filmes_tmdb.csv'):
    
    campos = [
        'id', 'title', 'overview', 'original_language', 
        'runtime', 'origin_country', 'budget', 'revenue', 'release_date', 
        'genres', 'production_companies'
    ]
    
    try:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.DictWriter(arquivo_csv, fieldnames=campos)
            writer.writeheader()
            for filme in dados_filmes:
                linha = {}
                for campo in ['id', 'title', 'overview', 'original_language', 
                              'runtime', 'origin_country', 'budget', 
                              'revenue', 'release_date'
                             ]:
                    linha[campo] = filme.get(campo, 'N/A')
                linha['genres'] = ', '.join([g['name'] for g in filme.get('genres', [])])
                linha['production_companies'] = ', '.join([g['name'] for g in filme.get('production_companies', [])])
                writer.writerow(linha)    
    except Exception as e:
        print(f"Erro ao exportar para CSV: {e}")

#função que chama o código, define o range de anos e etc

def coletar_filmes(ano_ini=2014, ano_fim=2024, pags_totais=2):
    todos_filmes = []
    for ano in range(ano_ini, ano_fim + 1):
        print(f"Coletando IDs do ano {ano}...")
        tmdb_ids = extrair_tmdb(ano, pag=pags_totais)
        for filme in tmdb_ids:
            detalhes = detalhe_tmdb(filme)
            todos_filmes.append(detalhes)
    exportar_para_csv(todos_filmes)

coletar_filmes()
          








































