from calendar import week
from cmath import pi
import json
import requests
import os
import sys
import csv
from datetime import datetime, date
import unicodedata
import pandas as pd
import logging

#import csv_test as manage_csv

headers = {'Content-Type':'application/json',
        'sec-ch-ua':'".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'Accept':'application/json, text/plain, */*',
        'sec-ch-ua-mobile':'?0',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'sec-ch-ua-platform':'"Linux"'}

def get_json_page(url, headers):
    return requests.request("GET",url,headers=headers).json()


def strip_accents(texto):
   return ''.join(c for c in unicodedata.normalize('NFD', texto)
                  if unicodedata.category(c) != 'Mn')


def get_productos():
    logging.info(f"## START {get_productos.__name__}")
    url = 'https://d3e6htiiul5ek9.cloudfront.net/prod/productos?string=yerba&array_sucursales=2003-1-7670,10-3-785,24-2-157,24-2-59,10-3-768,9-2-444,10-3-720,24-2-83,10-3-648,24-2-314,10-3-770,24-2-74,10-3-765,24-2-300,24-2-266,9-1-440,10-3-769,9-2-435,24-2-79,2011-1-143,10-3-610,2009-1-78,10-3-772,10-3-793,2011-1-126,24-2-131,10-3-607,9-2-441,24-2-58,10-3-790&offset=0&limit=50&sort=-cant_sucursales_disponible' \

    response = get_json_page(url, headers)

    if response["productos"]:

        cant_productos = response["total"]
        cant_pages = cant_productos // 30

        df_productos = pd.DataFrame.from_records(response["productos"])

        for i in range(cant_pages): #itera para obtener todos los resultados
            #if i%10 == 0:
            logging.info(f"=> Pagina {i}/{cant_pages}") 

            # offset+=30
            url = f"https://d3e6htiiul5ek9.cloudfront.net/prod/productos?string=yerba&array_sucursales=2003-1-7670,10-3-785,24-2-157,24-2-59,10-3-768,9-2-444,10-3-720,24-2-83,10-3-648,24-2-314,10-3-770,24-2-74,10-3-765,24-2-300,24-2-266,9-1-440,10-3-769,9-2-435,24-2-79,2011-1-143,10-3-610,2009-1-78,10-3-772,10-3-793,2011-1-126,24-2-131,10-3-607,9-2-441,24-2-58,10-3-790&offset={i}&limit=30&sort=-cant_sucursales_disponible"
            response = requests.request("GET",url,headers=headers).json()

            df_productos_new_row = (pd.DataFrame.from_records(response["productos"]))
            df_productos = pd.concat([df_productos, df_productos_new_row]) #va sumando al dataframe


    df_productos.to_csv(f"../data/yerba.csv", index=False)
    logging.info(f"## END {get_productos.__name__}")


def get_producto_data(product_id):
    logging.info(f"## START {get_producto_data.__name__} - {product_id}")

    # sucursales_id = get_id_sucursales()
    # ciudad_sucursales_id = ','.join(sucursales_id['buenos_aires'])
    # print(ciudad_sucursales_id)

    # url = f"https://d3e6htiiul5ek9.cloudfront.net/prod/producto?limit=30&id_producto={product_id}&array_sucursales=2003-1-7670,10-3-785,24-2-157,24-2-59,10-3-768,9-2-444,10-3-720,24-2-83,10-3-648,24-2-314,10-3-770,24-2-74,10-3-765,24-2-300,24-2-266,9-1-440,10-3-769,9-2-435,24-2-79,2011-1-143,10-3-610,2009-1-78,10-3-772,10-3-793,2011-1-126,24-2-131,10-3-607,9-2-441,24-2-58,10-3-790"
    url = f"https://d3e6htiiul5ek9.cloudfront.net/prod/producto?limit=30&id_producto={product_id}&array_sucursales=2003-1-7670,10-3-785"

    # url = f"https://d3e6htiiul5ek9.cloudfront.net/prod/producto?limit=30&id_producto={product_id}&array_sucursales={ciudad_sucursales_id}"

    response = get_json_page(url, headers)

    try:
        if response['producto'] and response['total'] != 0:
            # df_producto = pd.DataFrame.from_records(response["producto"], index=[0])

            # if not os.path.isfile('../data/producto_yerba.csv'):
            #     df_producto.to_csv(f"../data/producto_yerba.csv", index=False)
            # else: 
            #     df_producto.to_csv(f"../data/producto_yerba.csv", mode='a', index=False, header=False)
            
            ########

            print(response)
            # print(response['sucursales'])

            aaa
            # cant_suc_con_producto = response['sucursalesConProducto']

            # total_pagina = response['totalPagina']
            # print('---')
            # for i in range(total_pagina):
            #     print(i)
            #     print(f"{i}/{total_pagina}")
            #     df_id = pd.DataFrame({'id': product_id})
            #     df_sucursales =  pd.DataFrame.from_records(response["sucursales"], index=[0])
            #     df_sucursales = pd.concat([df_id, df_sucursales], axis=1)

            
            #     if not os.path.isfile('../data/producto_yerba.csv'):
            #         df_sucursales.to_csv(f"../data/sucursales.csv", index=False)
            #     else: 

            #         df_sucursales.to_csv(f"../data/sucursales.csv", mode='a', index=False, header=False)
                
    except:
        logging.info(f"## Producto no encontrado")


    logging.info(f"## END {get_producto_data.__name__} - {product_id}")

        



def get_sucursales_para_ciudad(ciudad,latitud,longitud):

    """A partir de la url base, la latitud y la longitud, devuelve todas las sucursales de una ciudad"""
    logging.info(f"## START {get_sucursales_para_ciudad.__name__}")
    logging.info(f"=> Obteniendo sucursales de {ciudad}")

    offset = 0
    url = f"https://d3e6htiiul5ek9.cloudfront.net/prod/sucursales?lat={latitud}&lng={longitud}&limit=30&offset={offset}"

    response = get_json_page(url, headers)

    if response["sucursales"]:

        cant_pages = response["total"] // 30 #cantidad de paginas que dan resultados en la api
        #cant_pages = response["totalPagina"]
        
        df_sucursales = pd.DataFrame.from_records(response["sucursales"])

        for i in range(cant_pages): #itera para obtener todos los resultados
            if i%10 == 0:
                logging.info(f"=> Pagina {i}/{cant_pages}")
            offset+=30
            url = f"https://d3e6htiiul5ek9.cloudfront.net/prod/sucursales?lat={latitud}&lng={longitud}&limit=30&offset={offset}"
            response = requests.request("GET",url,headers=headers).json()

            df_sucursales_new_row = (pd.DataFrame.from_records(response["sucursales"]))
            df_sucursales = pd.concat([df_sucursales, df_sucursales_new_row]) #va sumando al dataframe


    ciudad = ciudad.lower().replace(" ", "_")
    df_sucursales.to_csv(f"../data/sucursales/{ciudad}_sucursales.csv", index=False)
    logging.info(f"## END {get_sucursales_para_ciudad.__name__}")

    return df_sucursales

def get_id_sucursales():

    path_ciudades = '../data/ciudades.csv'
    ciudades = []
    with open(path_ciudades, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            ciudades.append(row[0].lower().replace(" ","_"))

    sucursales_ids = {} # {ciudad: [sucursales_id]}
    for ciudad in ciudades:
        path_sucursales = f"../data/sucursales/{ciudad}_sucursales.csv"
        try:
            with open(path_sucursales, 'r') as file:
                csvreader = csv.reader(file)
                next(csvreader) # para saltear el encabezado
                for row in csvreader:
                    # sucursales_ids.append(row[6])
                    if ciudad not in sucursales_ids.keys():

                        sucursales_ids[ciudad] = [row[6]]
                    else:
                        sucursales_ids[ciudad].append(row[6])


        except:
            logging.info(f"## No existe path {path_sucursales}")
    
    return sucursales_ids


def leer_ciudades(path):
    """ Recibe el path de ciudades para leer el archivo y le pasa la ciudad, latitud y longitud a get_sucursales_para_ciudad"""
    
    df_ciudades = pd.read_csv(path)
    
    for ind in df_ciudades.index:
        get_sucursales_para_ciudad(df_ciudades[0][ind], df_ciudades[1][ind], df_ciudades[2][ind])


def leer_producto_id(path):
    with open(path, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            get_producto_data(row[1])
            

if __name__ == '__main__':
    
    #TODO: hacerlo en /config
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s -- : %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p',
                        filename=f"../logs/{date.today()}_scraper.log",
                        filemode='a')

    #TODO: tener un config/constants
    path_ciudades = '../data/ciudades.csv'
    path_yerba = '../data/yerba.csv'

    # testing
    # leer_ciudades(path)
    # con las ciudades obtengo la sucursal de cada ciudad y con el id de cada sucursal obtengo los prod
    # print(get_productos()) 

    print(leer_producto_id(path_yerba))
    #get_sucursales_para_ciudad("Buenos Aires",-34.61315,-58.37723)

    # print(get_id_sucursales())