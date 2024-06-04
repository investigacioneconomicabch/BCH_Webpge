# Nota: este código se deriva de códigos elaborados por Gabriela López
wd = "C:/Directorio_Trabajo/GitHub/BCH_Webpage-main/data/"

## Librerías
import ast 
import datetime
import json 
import numpy as np
import os 
import pandas as pd
import re
import requests

from bs4 import BeautifulSoup
from pandas.api.types import infer_dtype
from pathlib import Path
from urllib.parse import unquote

##### Rutas de archivos dinámicos
alpha_num = dict(
    sector_abv = {
        'estadisticas-cambiarias': "EC-",
        'sistema-de-pagos': "ESP-",
        'tipo-de-cambio': "EC-",
        'operaciones-de-mercado-abierto': "EOM-",
        'precios': "EP-",
        'sector-monetario': "EMF-",
        'sector-real':"ESR-",
        'sector-externo':"ESE-",
        'sector-fiscal':"EMF-",
        'resultados-de-encuestas': "ENC-"
        },
    series_abv = {
        'TCPP Negociaciones Diarias': "TCSUB-00",
        'TCPP-Mercado Interbancario de Divisas': "MID-00",
        'Tipo de Cambio de Referencia': "TCR",
        'Ingreso y Egreso de Divisas AC': "DIV-00",
        'Remesas Familiares por Departamento':"REMD-00",
        'Remesas Familiares por País':"REMP-00",
        'Balanza Cambiaria':"BALCAM-00",
        'Tasas IO': "TIR-00",
        'Cotización Principales Monedas': "MON-00",
        'BCH-TR': "BCHTR-00",
        'CCECH': "CCECH-01",
        'ACH PRONTO': "ACH-01",
        'Precio Diario del Dólar-EUA': "TCN-01",
        'Índice del Tipo de Cambio Efectivo Real':"ITCER-00",
        'Información Subasta Diaria': "OMA-01-SD",
        'Información Subasta Estructural': "OMA-01-SE",
        'Información Subasta bonos BCH': "OMA-01-SBBCH",
        'Operaciones de Reporto': "OMA-01-REP",
        'Facilidades permanentes': "OMA-01-FP",
        'Información MED': "OMA-01-MED",
        'Bonos de Sefin': "OMA-01-BSEFIN",
        'Tasa Variable Bonos Sefin': "OMA-01-TSEFIN",
        'Tasa Variable Bonos ENEE': "OMA-01-TENEE",
        'Operaciones de Mercado Secundario': "OMA-01-OMS",
        'Índice de Precios al Consumidor':"IPC-01",
        'Índice de Precios al Consumidor por rubros': "IPC-RUB-00",
        'Índice de Precios al Consumidor por región':"IPC-REG-00",
        'Índice de Inflación Subyacente': "IPC-SUBY-00",
        'Tasa de Política Monetaria': "TPM-01",
        'Tasa Anuales de Interés sobre Operaciones Nuevas': "TI-TION-00",
        'Tasas sobre Operaciones Nuevas Actividad Económica': "TI-TONAE-00",
        'Tasas Saldos Sistema Financiero': "TI-TSSF-00",
        'Tasas Saldos Sistema Financiero por AE': "TI-TSSFAE-00",
        'RIN y ARO':"RIN-01",
        'Emisión y Base Monetaria': "EBM-01",
        'Agregados Monetarios': "AMCC-01",
        'Agregados Monetarios como Porcentaje del PIB': "AMCC-00",
        'Captación de los Bancos Comerciales': "AMCC-02",
        'Captación de las Otras Sociedades': "AMCC-02",
        'Crédito al Sector Privado': "AMCC-03",
        'Préstamos de las Otras Sociedades': "AMCC-04",
        'Préstamos de BC Porcentaje PIB':"AMCC-05",
        'Activos y Pasivos Externos Sistema Financiero': "PFS-02",
        'Activos y Pasivos Externos Banco Comerciales': "PFS-01",
        'Activos y Pasivos Ext Sociedades de Depósitos': "PFS-02",
        'Índice Mensual de Actividad Económica': "IMAE-01",
        'PIB y VAB': "PIBA-04",
        'VAB por Actividad Económica': "PIBA-01",
        'PIB Gasto': "PIBA-02",
        'PIB Ingreso': "PIBA-03",
        'PIB e Ingreso Nacional Per-Cápita': "PIBA-INPC-00",
        'VAB Agropecuario': "PIBA-VABAGRO-00",
        'VAB Industria': "PIBA-VABIND-00",
        'VAB Productos Alimenticios': "PIBA-VABALIM-00",
        'Balanza de Pagos': "BP-01",
        'Cuenta Corriente': "BP-01",
        'Exportaciones de Importaciones de Bienes totales': "BP-01-XMBTOT",
        'Balanza de Bienes por Categoría':"BP-01-BIENES_CAT",
        'Exportaciones FOB de Principales Productos de Mercnacías Generales': "CEB-01",
        'Importaciones de Combustibles por Tipo de Combustible': "CEB-02",
        'Exportaciones e Importaciones de Bienes para Transformación': "CEB-03-MBT",
        'Exportaciones FOB de Bienes para Tranformación': "CEB-03-XBT",
        'Importaciones CIF de Bienes Para Transformación por categoria':"CEB-03-MBTCAT",
        'Balanza de Servicios': "BP-01-BSERV",
        'Ingresos y Egresos de Servicios por Categoria': "IES-01",
        'Remesas Familiares Corrientes': "BP-REM-00",
        'Flujo Neto de Inversión Extranjera hacia Honduras por Actividad Económica': "IED-01-AE",
        'Flujo Neto de Inversión Extranjera hacia Honduras por Región Geográfica':"IED-01-REG",
        'Flujo Neto de Inversión Extrajera Directa hacia Honduras por Componente': "IED-01-COMP",
        'PII Categoría': "PII-01-PIICAT",
        'PII Componente': "PII-01-COMP",
        'PII Activos-Componentes': "PII-01-ACT",
        'PII Pasivos-Componentes': "PII-01-PAS",
        'Deuda Externa pública': "DXTPUB",
        'Deuda Externa Total por Sector': "DE-03-TOT",
        'Deuda Externa Total por Tipo de Deudor':"DE-01-TOT",
        'Deuda Externa Pública por Tipo de Deudor': "DE-01",
        'Deuda Externa Total por Tipo de Acreedor': "DE-02",
        'Financiamiento Externo e Interno AC y SPNF': "PII-01-FNXTNT12",
        'Financiamiento Externo AC y SPNF': "DE-00-FNXT12",
        'Financiamiento Interno AC por Sector':"DE-00-FNINT1",
        'Financiamiento Interno SPNF por Sector': "DE-00-FNINT2",
        'Financiamiento Interno AC y SPNF por Inst': "DE-00-FNINT12",
        'Posición Financiera de la AC y SPNF': "PII-01-POSFIN12",
        'Deuda Interna AC por Transacción': "PII-00-DNT1TS",
        'Deuda Interna del SP por Instrumento': "PII-00-DNTINST",
        'Deuda Interna del Resto del SPNF por Tenedor': "PII-00-DNT2TD",
        'Servicio de Deuda Interna AC':"PII-00-SERDUINT",
        'Expectativas de Inflación': "EP-00-EXPECIF"
        }
)

## Funciones
def soup_requests(path):
    response = requests.get(path)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    return soup

def request_filter_save(url=None):
    url = url or data_url
    soup = soup_requests(url)
    data_link_tree = soup.find_all(string=re.compile(filter_terms))
    pattern = re.compile(pattern_string)
    paths = re.findall(pattern, str(data_link_tree))
    return paths

def extract_xlsx_links(url):
    soup = soup_requests(url)
    data_link_tree = soup.find_all(lambda tag: tag.name == 'a' and tag.get('href') and tag.findChild() and tag.findChild().get_text())
    pattern = re.compile(rf'(?:href=")(.*?xlsx)')
    xlsx_links = re.findall(pattern, str(data_link_tree))
    xlsx_link = [main_url + i for i in xlsx_links]
    return xlsx_link

def scrape_and_create_dataframe():
    sectors = request_filter_save()
    data = []
    for sector in sectors:
        # print(sector)
        sector_data_url = main_url + child_url + sector
        paths = request_filter_save(sector_data_url)
        for path in paths:
            xlsx_links = extract_xlsx_links(main_url + child_url + path)
            # print(xlsx_links)
            data.append({
                'Sector': sector,
                'Path': path,
                'XLSXLinks': xlsx_links
            })
    # Create a DataFrame from the scraped data
    df = pd.DataFrame(data)
    # Add columns to the DataFrame using codes loaded from codes.json
    df["Sector_abv"] = [codes['sector_abv'][i] for i in df["Sector"]]
    seriesClean = []
    i = 0
    # print("THIS IS THE LENGTH OF XLSXLINKS", len(df["XLSXLinks"]))
    for links in df["XLSXLinks"]:
        seriesName = " "
        for url in links:
            try:
                filename = re.search(r'\/([^/]+)\.xlsx$', url).group(1)
                seriesName = unquote(filename)
            except:
                print("SKIPPED Cleaning 1", url)
        seriesClean += [seriesName]
        # print(i, seriesName)
        i = i + 1
    df["Nombre"] = seriesClean
    seriescode = []
    for i in df["Nombre"]:
        try:
            code = codes['series_abv'][i]
        except:
            code = ""
            # print("SKIPPED Cleaning 2", url)
        seriescode += [code]
        # print(seriescode)
    df["Nombre_abv"] = seriescode
    df["Code"] = df["Sector_abv"] + df["Nombre_abv"]
    return df

## Lista de archivos por rutas
main_url = "https://www.bch.hn"
child_url = "/estadisticas-y-publicaciones-economicas/reportes-dinamicos/"
data_url = main_url + child_url
filter_terms = re.escape(child_url)
pattern_string = rf'{filter_terms}(.*?)(?:\s|&quot)'
codes = alpha_num
df = scrape_and_create_dataframe()
df.to_csv(wd + 'archivos.csv', index=False)