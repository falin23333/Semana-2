from time import sleep
from curl_cffi import requests
from datetime import datetime
import pandas as pd
import asyncio
from time import time, sleep

sleep_time = 0.1

def intro():
    print("""
          
┏┓      ┓  ┓•             ┏┓•            ┳┓•    •┓   • ┓   
┃┃┏┓┏┓┏┓┃┏┓┃┓┏┏┳┓┏┓┏  ┓┏  ┗┓┓┏╋┏┓┏┳┓┏┓┏  ┃┃┓┏╋┏┓┓┣┓┓┏┓┏┫┏┓┏
┣┛┗┻┛ ┗┻┗┗ ┗┗┛┛┗┗┗┛┛  ┗┫  ┗┛┗┛┗┗ ┛┗┗┗┻┛  ┻┛┗┛┗┛ ┗┗┛┗┻┗┗┻┗┛┛
                       ┛                                   

          Actividad 2  Rafael Cañada Abolafia 

Se piden realizar las siguientes tareas:

1. Modificar el programa para ejecutando todas las funciones paralelas sean ejecutadas en una corutina.
        a) asyncio.create_task(): 
        b) asyncio.to_thread(): 
Realizar una versión de los algoritmos 2 utilizando requests y aoihttp
          
2. Medir los tiempos de ejecución de todos los algoritmos
        a) Tipología de problema
        b) Librerías utilizadas y su efecto en el tiempo de ejecución
""")
    
def descargar_informacion(simbolo):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/" + simbolo
    params = {
        "formatted": "true",
        "interval": "1d",
        "includeAdjustedClose": "false",
        "period1": "1201824000",
        "period2": "1735603200",
        "symbol": simbolo,
    }
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, params=params, impersonate="chrome")

    if response.status_code == 200:
        response_json = response.json()
        timestamps = response_json["chart"]["result"][0]["timestamp"]
        formatted_timestamps = list(map(lambda x: datetime.utcfromtimestamp(x), timestamps))
        high = response_json["chart"]["result"][0]["indicators"]["quote"][0]["high"]
        volume = response_json["chart"]["result"][0]["indicators"]["quote"][0]["volume"]
        open = response_json["chart"]["result"][0]["indicators"]["quote"][0]["open"]
        close = response_json["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        low = response_json["chart"]["result"][0]["indicators"]["quote"][0]["low"] # Print the JSON response
    else:
        raise Exception("Se ha producido un error en la descarga del simbolo " + str(simbolo))
    dataframe_actual = pd.DataFrame(
        {
            "max": high,
            "min": low,
            "apertura": open,
            "clausura": close,
            "vol": volume,
            "day": formatted_timestamps
        }
    )

    # Add time features
    dataframe_actual["year"] = dataframe_actual["day"].dt.year
    dataframe_actual["week"] = dataframe_actual["day"].dt.isocalendar().week
    dataframe_actual["month"] = dataframe_actual["day"].dt.month
    dataframe_actual["symbol"] = simbolo

    return dataframe_actual
async def descargar_informacion2(simbolo):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/" + simbolo
    params = {
        "formatted": "true",
        "interval": "1d",
        "includeAdjustedClose": "false",
        "period1": "1201824000",
        "period2": "1735603200",
        "symbol": simbolo,
    }
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers, params=params, impersonate="chrome")

    if response.status_code == 200:
        response_json = response.json()
        timestamps = response_json["chart"]["result"][0]["timestamp"]
        formatted_timestamps = list(map(lambda x: datetime.utcfromtimestamp(x), timestamps))
        high = response_json["chart"]["result"][0]["indicators"]["quote"][0]["high"]
        volume = response_json["chart"]["result"][0]["indicators"]["quote"][0]["volume"]
        open = response_json["chart"]["result"][0]["indicators"]["quote"][0]["open"]
        close = response_json["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        low = response_json["chart"]["result"][0]["indicators"]["quote"][0]["low"] # Print the JSON response
    else:
        raise Exception("Se ha producido un error en la descarga del simbolo " + str(simbolo))
    dataframe_actual = pd.DataFrame(
        {
            "max": high,
            "min": low,
            "apertura": open,
            "clausura": close,
            "vol": volume,
            "day": formatted_timestamps
        }
    )

    # Add time features
    dataframe_actual["year"] = dataframe_actual["day"].dt.year
    dataframe_actual["week"] = dataframe_actual["day"].dt.isocalendar().week
    dataframe_actual["month"] = dataframe_actual["day"].dt.month
    dataframe_actual["symbol"] = simbolo

    return dataframe_actual
# el contenido de ambas funciones es la misma, salvo que una es async


def agregar(dataframe, filters):
    aggregated_df = dataframe.groupby(filters).agg({
        "max": "max",
        "min": "min",
        "apertura": "first",
        "clausura": "last",
        "vol": "sum"
    }).reset_index()
    return aggregated_df





async def main():
    
    simbolos = ["AMZN", "GOOG", "F", "AAPL", "OSCR", "NVO", "V", "PFE", "MSFT", "META"]
    
       

    ###################### OPCION A - Creando hilos y luego lanzar todos en bucles anidados, similar al threading
    async def opcion_A():
    
        tareas = []
        resultados_await = []
        for sim in simbolos:
            tareas.append(asyncio.create_task(descargar_informacion2(sim)))    # Ojo , la funcion descargar_informacion SÍ debe ser asyncrona

        for tarea in tareas:
            resultados_await.append(await tarea)
        
        merged_df = pd.concat(resultados_await, ignore_index=True)
        return merged_df
    ###############################################################################################################
    #################### Opcion B - Creando los hilos y lanzandolos todos a la vez con gather #####
    async def opcion_B():
        tareas = []  # Lista donde guardaremos las tareas
        
        for sim in simbolos:
            
            tarea = asyncio.to_thread(descargar_informacion, sim)   # Ojo , la funcion descargar_informacion no debe ser asyncrona
            
            tareas.append(tarea)
        dataframes = await asyncio.gather(*tareas)
        merged_df = pd.concat(dataframes, ignore_index=True)
        return merged_df
    ###############################################################################################
    
    
    
    intro()

    inicio = time()
    merged_df = await opcion_A()
    print(f"Tiempo apartado A to_thread() : {time() - inicio}")
    
    
    inicio = time()
    merged_df2 = await opcion_B()
    print(f"Tiempo apartado B create_task() : {time() - inicio}")

    
if __name__ == "__main__":
    asyncio.run(main())
    
