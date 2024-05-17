# Procesos para descarga automática de datos de la página del Banco Central de Honduras

Este repositorio contiene archivos que permiten obtener series estadísticas de Honduras publicadas en la página web del [Banco Central de Honduras (BCH)](www.bch.hn).

Los mecanismos de consulta son los siguientes:

1. BCH_API_Python.qmd
2. PaginaWeb_Julia.qmd
3. BCH_Webpage.qmd

## BCH_API_Python.qmd

Contiene explicación sobre el contenido de datos disponibles en la [API](https://bchapi-am.developer.azure-api.net/) del Banco Central de Honduras (BCH), utilizando **Python**. Esta API fue desarrollada en 2024 y genera consultas a los archivos dinámicos disponibles a la fecha, limitadas al uso de número de serie como clave de consulta.

En Python, debe instalarse previamente las funciones listadas en el siguiente código:

```
import urllib.request, json
import pandas as pd
import plotly.express as px
import polars as pl
import os
import subprocess

from IPython.display import Markdown
from tabulate import tabulate
```

Una vez que se crea el registro de usuario (usar el botón "Suscribirse" en el [sitio web](https://bchapi-am.developer.azure-api.net/), puede verse el procedimiento de registro e inicio de sesión en [YouTube](https://www.youtube.com/watch?v=8ZBllMSsKw4)), se necesita obtener una clave (ver explicación en [YouTube](https://www.youtube.com/watch?v=mV90s74OCfc)), ejecutando una consulta al catálogo de indicadores. Favor sustituir en el código la clave actual por su clave asignada.

Para conocer los datos disponibles, se debe ejecutar una consulta al catálogo de indicadores, que contiene información sobre las series disponibles:

* Nombre (código)
* Descripción
* Periodicidad
* Grupo
* Correlativo del Grupo

Las funciones utilizadas para ejecutar el proceso se encuentran en el archivo `functions/bch_api.py`.

Como ejemplo de la consulta que contiene todas las variables, se muestran los primeros cinco elementos:

```
clave_asignada = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" #Favor ingresar la clave proporcionada.

# Las funciones que ejecutan los procesos están guardadas
# en el archivo "/functions/bch_api.py";
# si se ejecuta este código en otra ruta, debe sustituirse el path:
# file_path + "/functions/bch_api.py"
file_path = os.path.dirname(__file__)
exec(open(file_path + "/functions/bch_api.py").read())

url = "https://bchapi-am.azure-api.net/api/v1/indicadores?formato=Json"
hdr ={'Cache-Control': 'no-cache',
      'clave': clave_asignada,}
dfmeta = get_info(url, hdr)
dfmeta.head()
```

Las variables están categorizadas en 8 grupos principales y 54 subgrupos (columna "Grupo"). Los 8 grupos mencionados permiten consolidar los archivos de acuerdo con el origen de los datos en la página web del BCH, que en su mayoría pueden consultarse en los [reportes dinámicos](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos).

1. EOM = [Estadísticas de Operaciones Monetarias](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos/operaciones-de-mercado-abierto)
2. ESR = [Estadísticas del Sector Real](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos/sector-real)
3. ESE = [Estadísticas del Sector Externo](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos/sector-externo)
4. EMF = [Estadísiticas Monetarias y Financieras (Sector Fiscal)](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos/sector-fiscal)
5. EM = [Estadísticas Monetarias (TPM y RIN)](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos/sector-monetario)
6. ESP = [Estadísticas de Sistema de Pagos](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos/sistema-de-pagos)
7. EC = [Estadísticas de Tipo de Cambio](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos/tipo-de-cambio)
8. EP = [Estadísticas de Precios](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos/precios)

La nomenclatura utilizada permite dividir estos en un máximo de cinco niveles, tomando en cuenta el separador (-). Puede verse el detalle a continuacion, ordenando de acuerdo al número de niveles (número de subgrupos):

```
res_grupo = save_groups()
print(res_grupo)
```

Esta información, una vez que se ejecuta la función previa, se guarda en `/api/grupos.csv`.

La consulta por variable se realiza tomando en cuenta el número asignado en la API (Id). El listado de todas las variables se obtiene mediante una función:

```
df_all = save_variables()
print(df_all)
```

Una vez que se ejecuta la función previa, la información sobre las variables (incluyendo su "Id") se guarda en `/api/variables.csv`. Cada una de las variables (excepto el rango desde 7392 hasta 7446), pueden consultarse mediante el siguiente código:

```
df_all = save_variables()
Id = 204
df = get_df(Id)
get_plot(Id)
df.columns
df.write_csv(
    file_path + "/api/data.csv",
    separator=";")
print(df)
```

Con este código, se obtiene un DataFrame de la variable, con la fecha y el valor correspondiente, y su respectivo gráfico; asimismo, se guardan los datos en el archivo `api/data.csv`.

Si quiere obtenerse varias variables de manera simultánea, puede ejecutarse el siguiente código (Id es un vector conteniendo los Id's de las variables a consultar):

```
Id = [1,2,3]
# Id = [6282,204,1]
# Id = [608,609,610]

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
```

Todos los códigos previos están listos para ejecutarse desde el archivo `call_api.py`.

## PaginaWebBCH.qmd
Proceso para descargar y procesar datos desde la página web del [Banco Central de Honduras (BCH)](www.bch.hn) usando Julia, teniendo como resultado un solo archivo.

Para ejecutar este proceso desde una computadora, una vez descargados todos los archivos que contiene este repositorio, se necesitan tres cosas:
1) Instalar [R](https://cran.r-project.org/bin/windows/base/) y los paquetes "readxl" y "rio"
2) Instalar [Julia](https://julialang.org/downloads/) y luego instalar las librerías "CSV", "DataFrames", "Dates", "RCall" y "StatsBase"; y
3) Abrir el archivo "BCH_Webpage.qmd"; en este caso, el directorio por default es "wd = @__DIR__", el mismo en el que se encuentran los archivos descargados

El procedimiento se ejecuta a través de los códigos en "BCH_Webpage.qmd"; si no se tiene instalado Quarto, puede ejecutarse directamente desde Julia, pegando estas líneas en el prompt (cambiando previamente la ruta en donde se encuentran las carpetas "data" y "functions" en la variable "wd"; por ejemplo, wd = "C:/Users/your_user/Downloads/BCH_Webpage-main".^[En las rutas por default, debe cambiarse "\" por "/".]):

```
using CSV,DataFrames,Dates,RCall,StatsBase

wd = @__DIR__;
include(wd * "/functions/fn_process.jl");
include(wd * "/functions/fn_get_data.jl");
data = get_data()
CSV.write(
    wd * "/data/database.csv",
    data;
    delim = ";")
````

Las funciones utilizadas se encuentran en la carpeta "functions", archivos "fn_process.jl" y "fn_get_data.jl".

Los datos actualizados se guardan en la carpeta "data", archivo "database.csv".

Los datos del archivo "database.csv" cargados en Power BI (tablas y gráficos) pueden verse en la página web del [BCH](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos/series-estadisticas-consolidadas).
