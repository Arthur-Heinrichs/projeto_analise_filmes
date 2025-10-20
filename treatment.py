import pandas as pd
import numpy as np
import ast



#This codes treats the data we receive from tmdb, removing $, "," and other symbols. (clean_df)
#It also creates other csv files with open fields like genres -> instead of one line for ['adventure', 'action'], it creates two. It makes it easier to work with data later.




df = pd.read_csv("tmdb_movies.csv")


def clean_df(value, datatype):

    #null if data comes with n/a or #n/d from excel by any reason
    if pd.isna(value) or value in ("N/A", "#N/D"):
        return np.nan
    try:
        if datatype == float:
            clean = str(value).replace("$","").replace("R$","").replace(",","")
            return float(clean) 


        if datatype == int:


            #tirando milhares e vírgulas do excel


            clean = str(value).replace(",", "").replace(".","")


            return int(clean)
    except:
        return np.nan

for n in df.columns:

    if df[n].dtype == "int64":   


        df[n] = df[n].apply(clean_df, args=(int,)) 
        (f"{df[n].name} int")

    elif df[n].dtype == "float64":  

        df[n] = df[n].apply(clean_df, args=(float,))
        print(f"{df[n].name} float")

    else:
       print(f"{df[n].name} not float neither int")


df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

df["revenue_per_budget"] = np.where(df["budget"] == 0, np.nan, np.divide(df["revenue"], df["budget"]))


df['yearmonthday'] = df['release_date'].dt.strftime('%Y%m%d').astype(int)

df['yearmonth'] = df['release_date'].dt.strftime('%Y%m').astype(int)

df['year'] = df['release_date'].dt.strftime('%Y').astype(int)

df.to_csv("clean_data.csv") 

print("all data has been cleaned")


df_opened_by_genres = df[["id", "title", "revenue", "budget", "revenue_per_budget", "genres", "production_companies", "yearmonthday", "yearmonth", "year"]].copy()


df_opened_by_production_companies = df[["id","title", "revenue", "budget", "revenue_per_budget","genres", "production_companies", "yearmonthday", "yearmonth", "year"]].copy()

df_opened_countries = df.copy()




df_opened_by_genres["genres"] = df_opened_by_genres["genres"].str.split(", ")


df_opened_by_production_companies["production_companies"] = df_opened_by_production_companies["production_companies"].str.split(", ")


df_opened_by_genres=df_opened_by_genres.explode("genres")


df_opened_by_production_companies=df_opened_by_production_companies.explode("production_companies")


df_opened_countries['origin_country'] = df_opened_countries['origin_country'].apply(ast.literal_eval)
df_opened_countries = df_opened_countries.explode('origin_country')



df_opened_by_genres.to_csv("clean_data_genres.csv")


df_opened_by_production_companies.to_csv("clean_data_companies.csv")

df_opened_countries.to_csv("clean_data_countries.csv")



