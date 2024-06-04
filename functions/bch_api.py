import urllib.request, json
import pandas as pd
import plotly.express as px
import polars as pl
import os

from IPython.display import Markdown
from tabulate import tabulate

# clave_asignada = "ff34cff7b0024ea39eb565fccb9f03b6" #Favor ingresar la clave proporcionada.

# Las funciones que ejecutan los procesos están guardadas
# en el archivo "/functions/bch_api.py";
# si se ejecuta este código en otra ruta, debe sustituirse el path:
# file_path + "/functions/bch_api.py"

#####---------------------------------------------------------------------------------------#####
# A partir de código elaborado por Gabriela López:
# https://colab.research.google.com/drive/1R3zpo3L27ypjD7v_FO7GeFPQ_2GeEFKd?usp=sharing
def get_info(url, hdr):
    header = hdr
    req = urllib.request.Request(url, headers=header)
    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    jsondata = response.read()
    bytes_data = jsondata
    data_str = bytes_data.decode('utf-8')
    data = json.loads(data_str)
    df = pd.read_json(json.dumps(data))
    idslist = df['Id'].unique()
    return df

def get_df(id):
    hdr ={'Cache-Control': 'no-cache',
          'clave': clave_asignada,}
    url_0 = "https://bchapi-am.azure-api.net/api/v1/indicadores?formato=Json"
    url = f'https://bchapi-am.azure-api.net/api/v1/indicadores/{id}/cifras'
    all_variables = get_info(url_0, hdr)
    data = get_info(url, hdr)
    df = pd.DataFrame(
        data = data['Valor'].values, 
        index = pd.DatetimeIndex(data['Fecha']))
    df.columns = [all_variables["Descripcion"][id-1]]
    df = pl.from_pandas(df,include_index=True
        ).with_columns(
            pl.col("Fecha").cast(pl.Date))
    df = df.sort("Fecha")
    df = df.unique(maintain_order=True)
    return df

def get_df_interno(id):
    hdr ={'Cache-Control': 'no-cache',
          'clave': clave_asignada,}
    url_0 = "https://servicios.bch.hn/swagger/api/v1/indicadores?formato=Json"
    url = f'https://servicios.bch.hn/swagger/api/v1/indicadores/{id}/cifras'
    all_variables = get_info(url_0, hdr)
    data = get_info(url, hdr)
    df = pd.DataFrame(
        data = data['Valor'].values, 
        index = pd.DatetimeIndex(data['Fecha']))
    df.columns = [all_variables["Descripcion"][id-1]]
    df = pl.from_pandas(df,include_index=True
        ).with_columns(
            pl.col("Fecha").cast(pl.Date))
    df = df.sort("Fecha")
    df = df.unique(maintain_order=True)
    return df

def get_plot(id):
    hdr ={'Cache-Control': 'no-cache',
          'clave': clave_asignada,}
    url_0 = "https://bchapi-am.azure-api.net/api/v1/indicadores?formato=Json"
    url = f'https://bchapi-am.azure-api.net/api/v1/indicadores/{id}/cifras'
    all_variables = get_info(url_0, hdr)
    data = get_info(url, hdr)
    df = pd.DataFrame(
        data = data['Valor'].values, 
        index = pd.DatetimeIndex(data['Fecha']))
    fig = px.line(
        df, 
        # title = all_variables['Descripcion'].unique()[0],
        title = all_variables["Descripcion"][id-1]
        )
    fig.update_layout(
        autosize=False,
        width=800,
        height=500,
        template = 'plotly_white',
        showlegend=False)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    fig.show()

def get_plot_interno(id):
    hdr ={'Cache-Control': 'no-cache',
          'clave': clave_asignada,}
    url_0 = "https://servicios.bch.hn/swagger/api/v1/indicadores?formato=Json"
    url = f'https://servicios.bch.hn/swagger/api/v1/indicadores/{id}/cifras'
    all_variables = get_info(url_0, hdr)
    data = get_info(url, hdr)
    df = pd.DataFrame(
        data = data['Valor'].values, 
        index = pd.DatetimeIndex(data['Fecha']))
    fig = px.line(
        df, 
        # title = all_variables['Descripcion'].unique()[0],
        title = all_variables["Descripcion"][id-1]
        )
    fig.update_layout(
        autosize=False,
        width=800,
        height=500,
        template = 'plotly_white',
        showlegend=False)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    fig.show()

#####---------------------------------------------------------------------------------------#####
# Proceso para obtener información de los grupos
def get_groups():
    file_path = os.path.dirname(__file__)
    exec(open(file_path + "/functions/bch_api.py").read())

    url = "https://bchapi-am.azure-api.net/api/v1/indicadores?formato=Json"
    hdr ={'Cache-Control': 'no-cache',
        'clave': clave_asignada,}
    dfmeta = get_info(url, hdr)
    return dfmeta

def get_groups_interno():
    file_path = os.path.dirname(__file__)
    exec(open(file_path + "/functions/bch_api.py").read())

    url = "https://servicios.bch.hn/swagger/api/v1/indicadores?formato=Json"
    hdr ={'Cache-Control': 'no-cache',
        'clave': clave_asignada,}
    dfmeta = get_info(url, hdr)
    return dfmeta

def get_groups_vscode():
    file_path =  os.getcwd()
    exec(open(file_path + "/functions/bch_api.py").read())

    url = "https://bchapi-am.azure-api.net/api/v1/indicadores?formato=Json"
    hdr ={'Cache-Control': 'no-cache',
        'clave': clave_asignada,}
    dfmeta = get_info(url, hdr)
    return dfmeta

#####---------------------------------------------------------------------------------------#####
# Proceso para obtener información de las variables
# y guardarlas en archivo
# Agregar niveles de Descripción y Grupo
def save_variables():
    file_path = os.path.dirname(__file__)
    dfmeta = get_groups()
    df_all = dfmeta
    df_all[['Niv_Descr_1','Niv_Descr_2','Niv_Descr_3','Niv_Descr_4','Niv_Descr_5','Niv_Descr_6','Niv_Descr_7','Niv_Descr_8']] = df_all['Descripcion'].str.split(
        '-',expand=True)
    df_all["Niv_Descr"] = df_all.notnull().sum(axis=1) - 6
    df_all[
        ['Niv_Gr_1','Niv_Gr_2','Niv_Gr_3','Niv_Gr_4','Niv_Gr_5']]  = df_all['Grupo'].str.split('-',expand=True)
    df_all["Niv_Gr"] = df_all.notnull().sum(axis=1) - 2
    df_all = pl.DataFrame(df_all)
    df_all.write_csv(
            file_path + "/api/variables.csv",
            separator=";")
    return df_all

def save_variables_vscode():
    file_path = os.getcwd()
    # dfmeta = get_groups()
    dfmeta = get_groups_vscode()
    df_all = dfmeta
    df_all[['Niv_Descr_1','Niv_Descr_2','Niv_Descr_3','Niv_Descr_4','Niv_Descr_5','Niv_Descr_6','Niv_Descr_7','Niv_Descr_8']] = df_all['Descripcion'].str.split(
        '-',expand=True)
    df_all["Niv_Descr"] = df_all.notnull().sum(axis=1) - 6
    df_all[
        ['Niv_Gr_1','Niv_Gr_2','Niv_Gr_3','Niv_Gr_4','Niv_Gr_5']]  = df_all['Grupo'].str.split('-',expand=True)
    df_all["Niv_Gr"] = df_all.notnull().sum(axis=1) - 2
    df_all = pl.DataFrame(df_all)
    df_all.write_csv(
            file_path + "/api/variables.csv",
            separator=";")
    return df_all

def save_groups():
    file_path = os.path.dirname(__file__)
    dfmeta = get_groups()
    df_all = dfmeta
    df_all[['Niv_Descr_1','Niv_Descr_2','Niv_Descr_3','Niv_Descr_4','Niv_Descr_5','Niv_Descr_6','Niv_Descr_7','Niv_Descr_8']] = df_all['Descripcion'].str.split(
        '-',expand=True)
    df_all["Niv_Descr"] = df_all.notnull().sum(axis=1) - 6
    df_all[
        ['Niv_Gr_1','Niv_Gr_2','Niv_Gr_3','Niv_Gr_4','Niv_Gr_5']]  = df_all['Grupo'].str.split('-',expand=True)
    df_all["Niv_Gr"] = df_all.notnull().sum(axis=1) - 2
    df_all = pl.DataFrame(df_all)
    df_all.write_csv(
            file_path + "/api/variables.csv",
            separator=";")

    # Resumen por Grupo
    variable = "Grupo"
    res_grupo = df_all.group_by(variable
        ).agg(
        pl.col("Id").len().alias("N_Variables"),
        ).sort("N_Variables",descending=True)
    print(str(res_grupo["N_Variables"].sum()) + " variables")
    print(str(len(res_grupo)) + " grupos")
    res_grupo = pd.DataFrame(res_grupo)
    res_grupo.columns = ["Grupo","N_Variables"]
    res_grupo[
        ['Niv_Gr_1','Niv_Gr_2','Niv_Gr_3','Niv_Gr_4','Niv_Gr_5']]  = res_grupo['Grupo'].str.split('-',expand=True)
    res_grupo["Niv_Gr"] = res_grupo.notnull().sum(axis=1) - 2
    res_grupo = res_grupo.sort_values(
        ["Niv_Gr","N_Variables"], 
        ascending=[False,False])
    res_grupo = pl.DataFrame(res_grupo)
    res_grupo.write_csv(
        file_path + "/api/grupos.csv",
        separator=";")
    return res_grupo

def save_groups_vscode():
    file_path = os.getcwd()
    dfmeta = get_groups_vscode()
    df_all = dfmeta
    df_all[['Niv_Descr_1','Niv_Descr_2','Niv_Descr_3','Niv_Descr_4','Niv_Descr_5','Niv_Descr_6','Niv_Descr_7','Niv_Descr_8']] = df_all['Descripcion'].str.split(
        '-',expand=True)
    df_all["Niv_Descr"] = df_all.notnull().sum(axis=1) - 6
    df_all[
        ['Niv_Gr_1','Niv_Gr_2','Niv_Gr_3','Niv_Gr_4','Niv_Gr_5']]  = df_all['Grupo'].str.split('-',expand=True)
    df_all["Niv_Gr"] = df_all.notnull().sum(axis=1) - 2
    df_all = pl.DataFrame(df_all)
    df_all.write_csv(
            file_path + "/api/variables.csv",
            separator=";")

    # Resumen por Grupo
    variable = "Grupo"
    res_grupo = df_all.group_by(variable
        ).agg(
        pl.col("Id").len().alias("N_Variables"),
        ).sort("N_Variables",descending=True)
    print(str(res_grupo["N_Variables"].sum()) + " variables")
    print(str(len(res_grupo)) + " grupos")
    res_grupo = pd.DataFrame(res_grupo)
    res_grupo.columns = ["Grupo","N_Variables"]
    res_grupo[
        ['Niv_Gr_1','Niv_Gr_2','Niv_Gr_3','Niv_Gr_4','Niv_Gr_5']]  = res_grupo['Grupo'].str.split('-',expand=True)
    res_grupo["Niv_Gr"] = res_grupo.notnull().sum(axis=1) - 2
    res_grupo = res_grupo.sort_values(
        ["Niv_Gr","N_Variables"], 
        ascending=[False,False])
    res_grupo = pl.DataFrame(res_grupo)
    res_grupo.write_csv(
        file_path + "/api/grupos.csv",
        separator=";")
    return res_grupo

#####---------------------------------------------------------------------------------------#####
# Funciones para obtener niveles de la API por grupos
def res_nivel_1():
    # df_all = save_groups()
    df_all = save_groups_vscode()
    df = pl.DataFrame(df_all)
    variable_0 = "Niv_Gr_1"
    variable_1 = "Niv_Gr_2"
    variable_2 = "Niv_Gr_3"
    df = df.group_by(variable_0
        ).agg(
            pl.col(variable_0).len().alias("N_Variables"),
            pl.col(variable_1).n_unique().alias("N_Subgrupos")
        ).sort(["N_Variables","N_Subgrupos",],descending=[True,True])
    print(str(df["N_Variables"].sum()) + " variables")
    print(str(df["Niv_Gr_1"].len()) + " grupos")
    print(str(df["N_Subgrupos"].sum()) + " subgrupos")
    return df

def res_nivel_2(nivel_1):
    # df_all = save_groups()
    df_all = save_groups_vscode()
    df = pl.DataFrame(df_all)
    variable_0 = "Niv_Gr_1"
    variable_1 = "Niv_Gr_2"
    variable_2 = "Niv_Gr_3"
    df = df.filter(
            pl.col("Niv_Gr_1") == nivel_1,
        ).group_by(variable_0,variable_1
        ).agg(
            pl.col(variable_0).len().alias("N_Variables"),
            pl.col(variable_2).n_unique().alias("N_Niv_Gr_2")
        ).sort(["N_Variables","N_Niv_Gr_2",],descending=[True,True])
    print(str(df["N_Variables"].sum()) + " variables")
    print(str(df["Niv_Gr_1"].len()) + " grupos")
    print(str(df["N_Niv_Gr_2"].sum()) + " subgrupos")
    return df

def res_nivel_3(nivel_1,nivel_2,variable_2):
    # df_all = save_variables()
    df_all = save_variables_vscode()
    df = pl.DataFrame(df_all)
    variable_0 = "Niv_Gr_1"
    variable_1 = "Niv_Gr_2"
    df = df.filter(
            pl.col("Niv_Gr_1") == nivel_1,
            pl.col("Niv_Gr_2") == nivel_2
        ).group_by(
            [variable_0,variable_1,variable_2]
        ).agg(
            # pl.col("Niv_Gr_1").len().alias("N_Niv_Gr_2"),
            pl.col("Niv_Gr_2").len().alias("N_Variables"),
        ).sort("N_Variables",descending=True)
    print(str(len(df)) + " subgrupos")
    # print(str(df["N_Niv_Gr_2"].sum()) + " niveles")
    print(str(df["N_Variables"].sum()) + " variables")
    return df

def res_nivel_4(nivel_1,nivel_2,variable_2,def_variable_2,variable_3):
    # df_all = save_variables()
    df_all = save_variables_vscode()
    df = pl.DataFrame(df_all)
    variable_0 = "Niv_Gr_1"
    variable_1 = "Niv_Gr_2"
    df = df.filter(
            pl.col("Niv_Gr_1") == nivel_1,
            pl.col("Niv_Gr_2") == nivel_2,
            pl.col(variable_2) == def_variable_2,
        ).group_by(
            [variable_0,variable_1,variable_2,variable_3]
        ).agg(
            pl.col(variable_3).len().alias("N_Variables"),
        ).sort("N_Variables",descending=True)
    return df

def res_nivel_5(
    nivel_1,nivel_2,
    variable_2,def_variable_2,
    variable_3,variable_4):
    # df_all = save_variables()
    df_all = save_variables_vscode()
    df = pl.DataFrame(df_all)
    variable_0 = "Niv_Gr_1"
    variable_1 = "Niv_Gr_2"
    df = df.filter(
            pl.col("Niv_Gr_1") == nivel_1,
            pl.col("Niv_Gr_2") == nivel_2,
            pl.col(variable_2) == def_variable_2,
            # pl.col(variable_3) == def_variable_3,
        ).group_by(
            [variable_0,variable_1,variable_2,variable_3,variable_4]
        ).agg(
            pl.col(variable_4).len().alias("N_Variables"),
        ).sort("N_Variables",descending=True)
    return df

def res_nivel_6(
    nivel_1,nivel_2,
    variable_2,def_variable_2,
    variable_3,variable_4,variable_5):
    # df_all = save_variables()
    df_all = save_variables_vscode()
    df = pl.DataFrame(df_all)
    variable_0 = "Niv_Gr_1"
    variable_1 = "Niv_Gr_2"
    df = df.filter(
            pl.col("Niv_Gr_1") == nivel_1,
            pl.col("Niv_Gr_2") == nivel_2,
            pl.col(variable_2) == def_variable_2,
            # pl.col(variable_3) == variable_3,
            # pl.col(variable_3) == def_variable_3,
        ).group_by(
            [variable_0,variable_1,variable_2,variable_3,variable_4,variable_5]
        ).agg(
            pl.col(variable_5).len().alias("N_Variables"),
        ).sort("N_Variables",descending=True)
    return df

def res_nivel_7(
    nivel_1,nivel_2,
    variable_2,def_variable_2,
    variable_3,variable_4,variable_5,variable_6):
    # df_all = save_variables()
    df_all = save_variables_vscode()
    df = pl.DataFrame(df_all)
    variable_0 = "Niv_Gr_1"
    variable_1 = "Niv_Gr_2"
    df = df.filter(
            pl.col("Niv_Gr_1") == nivel_1,
            pl.col("Niv_Gr_2") == nivel_2,
            pl.col(variable_2) == def_variable_2,
            # pl.col(variable_3) == variable_3,
            # pl.col(variable_3) == def_variable_3,
        ).group_by(
            [variable_0,variable_1,variable_2,variable_3,variable_4,variable_5,variable_6]
        ).agg(
            pl.col(variable_5).len().alias("N_Variables"),
        ).sort("N_Variables",descending=True)
    return df

# print("Prueba de ingreso efectivo de funciones")

