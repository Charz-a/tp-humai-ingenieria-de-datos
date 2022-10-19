from calendar import week
import json
import requests
import os
import csv
from datetime import datetime
import unicodedata
import pandas as pd

#import csv_test as manage_csv

path = './ciudades.csv'

def get_json_page():

    """Request para obtener los productos. Todavia no esta terminada"""

    url = 'https://d3e6htiiul5ek9.cloudfront.net/prod/productos?string=yerba&array_sucursales=10-2-109,24-1-202,2005-1-76,2004-1-15,15-1-5441,3-1-66,9-1-640,9-1-36,12-1-149,13-1-136,9-2-62,10-2-144,15-1-5511,2008-1-191,15-1-5410,15-1-5475,15-1-5366,3-1-65,3-1-1344,15-1-1034,19-1-00525,15-1-5396,9-1-638,44-1-8,9-1-636,9-2-42,9-1-633,44-1-7,15-1-1020,15-1-5435&offset=0&limit=50&sort=-cant_sucursales_disponible'

    headers = {'Content-Type':'application/json',
           'sec-ch-ua':'".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
           'Accept':'application/json, text/plain, */*',
           'sec-ch-ua-mobile':'?0',
           'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
           'sec-ch-ua-platform':'"Linux"'}

    response = requests.request("GET",url,headers=headers)

    return response.json()


def strip_accents(texto):
    
   return ''.join(c for c in unicodedata.normalize('NFD', texto)
                  if unicodedata.category(c) != 'Mn')


def get_sucursales_para_ciudad(ciudad,latitud,longitud):

    """A partir de la url base, la latitud y la longitud, devuelve todas las sucursales de una ciudad"""

    try:
        os.mkdir(ciudad)
    except:
        pass

    offset = 0
    url = "https://d3e6htiiul5ek9.cloudfront.net/prod/sucursales?lat={}&lng={}&limit=30&offset={}".format(latitud,longitud,offset)

    headers = {'Content-Type':'application/json',
           'sec-ch-ua':'".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
           'Accept':'application/json, text/plain, */*',
           'sec-ch-ua-mobile':'?0',
           'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
           'sec-ch-ua-platform':'"Linux"'}

    response = requests.request("GET",url,headers=headers).json()

    
    if response["sucursales"]:
        cant_pages = response["total"] // 30 #cantidad de paginas que dan resultados en la api

        df_sucursales = pd.DataFrame.from_records(response["sucursales"])

        for i in range(cant_pages): #itera para obtener todos los resultados
            offset+=30
            url = "https://d3e6htiiul5ek9.cloudfront.net/prod/sucursales?lat={}&lng={}&limit=30&offset={}".format(latitud,longitud,offset)
            response = requests.request("GET",url,headers=headers).json()
            df_sucursales.append(pd.DataFrame.from_records(response["sucursales"])) #va sumando al dataframe

    df_sucursales.to_csv("./{}/sucursales.csv".format(ciudad))

    return df_sucursales


def leer_ciudades(path):

    """No esta probado, tendría que agarrar el csv de ciudades y para cada ciudad sacar sus sucursales"""
    with open(path, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            get_sucursales_para_ciudad(row[1],row[2],row[3])

#TEST

print(get_sucursales_para_ciudad("Buenos Aires",-34.61315,-58.37723))
