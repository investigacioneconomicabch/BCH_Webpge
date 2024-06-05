# Procesos para descarga automática de datos de la página del Banco Central de Honduras

Este repositorio contiene archivos que permiten obtener series estadísticas de Honduras publicadas en la página web del [Banco Central de Honduras (BCH)](www.bch.hn).

Para entender el mecanismo de consulta de la API, se pueden utilizar los siguientes archivos:

1. BCH_API_Python.qmd: uso de la API para consulta de más de 15,000 variables contenidas en los archivos dinámicos; en este archivo se explican cómo obtener los componentes de cada grupo;
2. BCH_API_R.qmd: Brinda ejemplos de códigos en R para obtener información de la API, apegándose a los mecanismos de consulta descritos en [su página web](https://bchapi-am.developer.azure-api.net/):
   1. Consulta de catálogo de indicadores;
   2. Consulta cifras por Id de indicador;
   3. Consulta Indicadores por grupo;
   4. Consulta cifras por grupo de indicadores;
   5. Consulta por fecha de registro;
   6. Consulta de información por Id de indicador;
   7. Conteo de cifras para cada indicador; y
   8. Conteo de cifras para un indicador.
  Adicionalmente, brinda una descripción breve de la composición de los grupos, explica el mecanismo para descargar datos de indicadores por rangos (Id), una tabla en la que pueden filtrarse los indicadores   por palabra clave y un código para graficar los indicadores seleccionados.
3. BCH_API_Julia.qmd: Brinda ejemplos de códigos en Julia para obtener información de la API, obteniendo todo lo que puede ejecutarse en el numeral previo.

Los mecanismos adiconales de consulta son los siguientes:

1. BCH_Webpage.qmd: consulta de algunos archivos ubicados en diferentes rutas de la página web del BCH.
2. PaginaWeb_Julia.qmd: consulta a archivos dinámicos de la página web del BCH.

## BCH_API_Python.qmd

Contiene explicación sobre el contenido de datos disponibles en la [API](https://bchapi-am.developer.azure-api.net/) del Banco Central de Honduras (BCH), utilizando **Python**. Esta API fue desarrollada en 2024 y genera consultas a los archivos dinámicos disponibles a la fecha, limitadas al uso de número de serie como clave de consulta.

Puede tenerse acceso al procedimiento básico en [Google Colab](https://drive.google.com/drive/folders/11cLz9mKMT9ozYQKTYae0f-Sh7LdO6aJD?usp=sharing) (ingresando con su cuenta de Gmail).

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

clave_asignada = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" #Favor ingresar la clave proporcionada.

# Las funciones que ejecutan los procesos están guardadas
# en el archivo "/functions/bch_api.py";
# si se ejecuta este código en otra ruta, debe sustituirse el path:
# file_path + "/functions/bch_api.py"
file_path = os.path.dirname(__file__)
exec(open(file_path + "/functions/bch_api.py").read())
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
url = "https://bchapi-am.azure-api.net/api/v1/indicadores?formato=Json"
hdr ={'Cache-Control': 'no-cache',
      'clave': clave_asignada,}
dfmeta = get_groups_vscode()
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

La nomenclatura utilizada permite dividir estos en un máximo de cinco niveles, tomando en cuenta el separador (-). Puede verse el detalle a continuacion, ordenando de acuerdo al número de niveles (número de subgrupos)^[Nota: en caso que el comando `_vscode` genere errores, usar el comando previo sin este agregado.]:

```
# res_grupo = save_groups()
res_grupo = save_groups_vscode()
print(res_grupo)
```

Esta información, una vez que se ejecuta la función previa, se guarda en `/api/grupos.csv`.

La consulta por variable se realiza tomando en cuenta el número asignado en la API (Id). El listado de todas las variables se obtiene mediante una función:

```
# df_all = save_variables()
df_all = save_variables_vscode()
print(df_all)
```

En la última consulta, se contabilizaban 11,519 variables. Una vez que se ejecuta la función previa, la información sobre las variables (incluyendo su "Id") se guarda en `/api/variables.csv`. Cada una de las variables (excepto el rango desde 7392 hasta 7446), pueden consultarse mediante el siguiente código:

```
# df_all = save_variables()
df_all = save_variables_vscode()
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

Todos los códigos previos están listos para ejecutarse desde el archivo `call_api.py`. Las funciones detalladas previamente se relacionan con la ejecución del código desde VSCode, mientras que las guardadas en el archivo `call_api.py` son las correspondientes a ejecutar el código desde Python.

## BCH_Webpage.qmd

Proceso para descargar y procesar datos desde la página web del [Banco Central de Honduras (BCH)](www.bch.hn) usando **Julia** y **R**, teniendo como resultado un solo archivo. Esto permite obtener datos económicos en formato de serie, disponibles de manera individual en diferentes sitios de la página web, utilizando una consulta al archivo de Excel mediante librerías en R y modificando el formato original con procesos en Julia.

Para ejecutar este proceso desde una computadora, una vez descargados todos los archivos que contiene este repositorio, se necesitan tres cosas:
1) Instalar [R](https://cran.r-project.org/bin/windows/base/) y los paquetes `readxl` y `rio`.
2) Instalar [Julia](https://julialang.org/downloads/) y luego instalar las librerías `CSV`, `DataFrames`, `Dates`, `RCall` y `StatsBase`; y
3) Abrir el archivo `BCH_Webpage.qmd`; en este caso, el directorio por default es `wd = @__DIR__`, el mismo en el que se encuentran los archivos descargados

El procedimiento se ejecuta a través de los códigos en `BCH_Webpage.qmd`; si no se tiene instalado Quarto, puede ejecutarse directamente desde Julia, pegando estas líneas en el prompt (cambiando previamente la ruta en donde se encuentran las carpetas `data` y `functions` en la variable `wd`; por ejemplo, `wd = "C:/Users/your_user/Downloads/BCH_Webpage-main"`.^[En las rutas por default, debe cambiarse "\" por "/".]):

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

Las funciones utilizadas se encuentran en la carpeta "functions", archivos `fn_process.jl` y `fn_get_data.jl`.

Los datos actualizados se guardan en la carpeta "data", archivo "database.csv".

Los datos del archivo "database.csv" cargados en Power BI (tablas y gráficos) pueden verse en la página web del [BCH](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos/series-estadisticas-consolidadas).

Conviene mencionar que los datos se generan a través de consulta a archivos específicos, cuya ruta puede modificarse (por ejemplo, si para la carga de datos del IPC se modifica la ruta "https://www.bch.hn/estadisticos/GIE/LIBSeries%20IPC/Serie%20Mensual%20y%20Promedio%20Anual%20del%20%C3%8Dndice%20de%20Precios%20al%20Consumidor.xls), por lo que podrían generarse errores, mismos que pueden corregirse mediante el seguimiento al código en el archivo `fn_get_data.jl`.

## PaginaWeb_Julia.qmd

Permite recopilar en un solo archivo los datos contenidos en los [archivos dinámicos](https://bchapi-am.developer.azure-api.net/) de la página web del Banco Central de Honduras (BCH), utilizando **Python** y **Julia**.

Para obtener el archivo de Excel desde donde se extraen todas las series (`wd * "data/archivos.csv"`), ejecutar el procedimiento del archivo `scrape_bch.py` de la carpeta `functions`; en este archivo, debe cambiarse la ruta, de acuerdo a la carpeta en que se encuentran los datos. Para ejecutar todo el código contenido en este archivo, se utiliza `PyCall.@pyinclude(wd * "functions/scrape_bch.py")`.

```
using Chain,Conda,CSV,DataFrames,Dates
using HTTP,PyCall,XLSX

wd = @__DIR__
wd = wd * "/"
PyCall.@pyinclude(wd * "functions/scrape_bch.py")
```

Las rutas que permiten ejecutar las consultas a la página web se encuentran en `data/archivos.csv`. Su contenido puede verse mediante:

```
archivos = CSV.read(
    wd * "data/archivos.csv",
    DataFrames.DataFrame)
```

Las columnas de este archivo son las siguientes:

* Sector: ruta inicial de los [archivos dinámicos](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos);
* Path: siguiente ruta para los archivos dinámicos; por ejemplo, para las "estadísticas cambiarias", se tienen [varios submenús](https://www.bch.hn/estadisticas-y-publicaciones-economicas/reportes-dinamicos/estadisticas-cambiarias);
* XLSXLinks: Ruta de lectura para los archivos de Excel;
* Sector_abv: Abreviaturas del sector, estandarizado a cuatro caracteres:
1. EC00: estadisticas-cambiarias;
2. SPAG: sistema-de-pagos;
3. TC00: tipo-de-cambio;
4. OMA0: operaciones-de-mercado-abierto;
5. P000: precios;
6. M000: sector-monetario;
7. R000: sector-real;
8. ET00: sector-externo;
9. FIS0: sector-fiscal;
10 ENC0: resultados-de-encuestas

La consolidación de todas las series económicas de estos grupos (con excepción de las operacionse de mercado abierto) se guardan en un solo archivo en `data/Reportes_Dinamicos.csv`:

```
df = join_dataframes()
```

Para cada serie, se tiene la siguiente información:

* Fecha;
* Nombre_Serie; y
* Valor.

Se agrega adicionalmente columnas con la información relacionada con el archivo de origen, detallada en `data/archivos.csv`.

Debido a que el archivo de Operaciones de Mercado Abierto (serie 22) contiene dos fechas: Emisión y Vencimiento, no tiene el mismo formato del resto de las series previas, por lo que se guarda como un archivo separado  en `data/Reportes_Dinamicos_OMA.csv`:

```
df = get_oma()
```

Las columnas de este archivo son:

* Código ISIN;
* Fecha Emisión;
* Fecha Vencimiento;
* Número de Cupón; y
* Tasa.

Se agrega adicionalmente columnas con la información relacionada con el archivo de origen, detallada en `data/archivos.csv`.
