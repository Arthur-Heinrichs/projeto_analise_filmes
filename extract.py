import requests
import pandas as pd
import time
import csv
import json



#This code operates with four functions. 

# One collects the IDs from tmdb - top 50 movies by revenue (extract_tmdb), 
# The second uses the ID to get movie information (details_tmdb), 
# The third will be called later to export all colected data to csv (export_csv)
# the last one calls these two inside a for loop with a range of years (colect_movies).


#Don´t forget to increase the number of pages (colect_movies) if you want to colect more than 50 movies 


#Colects tmdb movie ids

def extract_tmdb(year, pag):


    movie_id = []


    for page in range(1, pag+1):

#To consult movie ids we have to provide a language. en-US does not mean only movies made in the US, but movies that have some sort of translation to this language.
        r = requests.get("https://api.themoviedb.org/3/discover/movie",
                          params={
                              "api_key":"your api key here",
                              "language":"en-US",
                              "page":page,
                              "primary_release_year":year,
                              "sort_by":"revenue.desc"},
                           timeout=10
                        )
        r.raise_for_status()
        data = r.json()
        for item in data.get("results",[]):
            movie_id.append(item["id"])
        time.sleep(0.25)
    return movie_id[:50]


def details_tmdb(movie_id):


    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
                "accept": "application/json",
                #here you have to put your authorization key with the Bearer, not the api key, otherwise it won't work.
                "Authorization": "Bearer <your authorization code here>"}
    r = requests.get(url, 
                     headers=headers,
                     timeout=10
                    )
    r.raise_for_status()
    return r.json()


def export_to_csv(movie_data, file_name='tmdb_movies.csv'):
    #you can choose other fields you would like from tmdb movies in this https://developer.themoviedb.org/reference/movie-details 
    fields = [
        'id', 'title', 'overview', 'original_language', 


        'runtime', 'origin_country', 'budget', 'revenue', 'release_date', 


        'genres', 'production_companies'
    ]
    try:
        with open(file_name, 'w', newline='', encoding='utf-8') as file_csv:
            writer = csv.DictWriter(file_csv, fieldnames=fields)
            writer.writeheader()
            for movie in movie_data:


                line = {}


                for field in ['id', 'title', 'overview', 'original_language', 


                              'runtime', 'origin_country', 'budget', 


                              'revenue', 'release_date'


                             ]:


                    line[field] = movie.get(field, 'N/A')
                line['genres'] = ', '.join([g['name'] for g in movie.get('genres', [])])
                line['production_companies'] = ', '.join([g['name'] for g in movie.get('production_companies', [])])
            
                writer.writerow(line)    


    except Exception as e:


        print(f"failed to export to csv due to: {e}")


def colect_movies(year_ini=2014, year_fim=2024, total_pages=3):


    all_movies = []


    for year in range(year_ini, year_fim + 1):


        print(f"Collecting ids of year {year}...")


        tmdb_ids = extract_tmdb(year, pag=total_pages)


        for movie in tmdb_ids:


            details = details_tmdb(movie)


            all_movies.append(details)


    export_to_csv(all_movies)



colect_movies()


          





























































































































