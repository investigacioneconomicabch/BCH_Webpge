import urllib.request, json
import pandas as pd
import plotly.express as px
import polars as pl
import os
import subprocess

from IPython.display import Markdown
from tabulate import tabulate

clave_asignada = "ff34cff7b0024ea39eb565fccb9f03b6" #Favor ingresar la clave proporcionada.

file_path = os.path.dirname(__file__)
# file_path = os.getcwd()
exec(open(file_path + "/functions/bch_api.py").read())

# Obtener los grupos
# dfmeta = get_groups_vscode()
dfmeta = get_groups()
print(dfmeta.head())

# Guardar grupos en un archivo
# res_grupo = save_groups_vscode()
res_grupo = save_groups()
print(res_grupo)

# Obtener listado de las variables
# df_all = save_variables_vscode()
df_all = save_variables()
print(df_all)

# Obtener dataframe y gráfico de una variable
Id = 204
df = get_df(Id)
get_plot(Id)
df.columns
df.write_csv(
    file_path + "/api/data.csv",
    separator=";")
print(df)

# Obtener dataframe y gráfico de varias variables
# Id = [1,2,3]
# Id = [6282,204,1]
# Id = [608,609,610]
Id = [204,205,206]


df = get_df(Id[0])
for i in range(1,len(Id)):
    df = df.join(
        get_df(Id[i]), 
        left_on=['Fecha'], 
        right_on=['Fecha'], 
        how='left')
df.write_csv(
    file_path + "/api/data.csv",
    separator=";")
print(df)