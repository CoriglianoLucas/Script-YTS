import math
import requests
import pandas as pd

movie_title=[]
movie_id=[]
movie_year=[]
movie_genre=[]
movie_synopsis=[]
movie_url=[]
movie_raiting=[]
movie_lenguage=[]
movie_likes=[]
movie_quality=[]
movie_type=[]
movie_size=[]
quality_aux=""
type_aux =""
size_aux=""
e = "  "

url = "https://yts.mx/api/v2/list_movies.json"
response = requests.get(url)
if response.status_code==200:
    datas = response.json()["data"]
    movie_count = datas["movie_count"]
    total_page = math.ceil(movie_count / 20) #20 es la cantidad de peliculas por pagina que usa la API


for i in range(1,total_page+1): # Extraigo los datos mas importantes que se ecunuentran con el endopint movie list
    response = requests.get(url,params={"page":i})
    print(i)
    if response.status_code==200:
        datas = response.json()["data"]
        movies = datas["movies"]
        for m in movies:
            movie_id.append(m["id"])
            movie_title.append(m["title"]) 
            movie_year.append(m["year"])
            try:
                movie_genre.append(m["genres"])
            except KeyError:
                    movie_genre.append("")
            movie_synopsis.append(m["synopsis"])
            movie_url.append(m["url"])
            movie_raiting.append(m["rating"])
            movie_lenguage.append(m["language"])
            try:
                torrents = m["torrents"]
                for t in torrents:
                    quality_aux += e + t["quality"]
                    type_aux += e + t["type"]
                    size_aux += e + t["size"]
                movie_quality.append(quality_aux)
                movie_type.append(type_aux)
                movie_size.append(size_aux)          
            except KeyError:
                movie_quality.append("")
                movie_type.append("")
                movie_size.append("")
            quality_aux=""
            type_aux =""
            size_aux=""
                

e=1
url_id="https://yts.mx/api/v2/movie_details.json"
for id in movie_id: # Recorro todas las ID para extraer la cantidad de likes, que se encuentran con el endpoint movie details
    print(e)
    response = requests.get(url_id,params={"movie_id":id})
    if response.status_code==200:
        datas2 = response.json()["data"]
        movies2 = datas2["movie"]
        movie_likes.append(movies2["like_count"])
        e+=1


final_list = pd.DataFrame({
                            "TITLE":movie_title, # 1er enunciado
                            "SYNOPSIS":movie_synopsis, # 1er enunciado
                            "GENRE":movie_genre, # 1er enunciado
                            "YEAR":movie_year, # 1er enunciado
                            "RAITING":movie_raiting, # plus
                            "LENGUEAGE":movie_lenguage, # plus
                            "LIKES":movie_likes, # plus
                            "QUALITY":movie_quality, #plus
                            "SIZE":movie_size, # plus
                            "TYPE":movie_type, # plus 
                            "LINK":movie_url # 1er enunciado
                         })

final_list.to_csv(r"C:\Users\corig\OneDrive\Documentos\Challege\Pythonlista_peliculas.csv", index=None, header=True, encoding='utf-8-sig')