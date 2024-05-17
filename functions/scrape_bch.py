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
        'estadisticas-cambiarias': "EC00",
        'sistema-de-pagos': "SPAG",
        'tipo-de-cambio': "TC00",
        'operaciones-de-mercado-abierto': "OMA0",
        'precios': "P000",
        'sector-monetario': "M000",
        'sector-real':"R000",
        'sector-externo':"ET00",
        'sector-fiscal':"FIS0",
        'resultados-de-encuestas': "ENC0"
        },
    series_abv = {
        'TCPP Negociaciones Diarias': "ND",
        'TCPP-Mercado Interbancario de Divisas': "MINTBD",
        'Tipo de Cambio de Referencia': "REF",
        'Ingreso y Egreso de Divisas AC': "IGEGD1",
        'Remesas Familiares por Departamento':"RFDEP",
        'Remesas Familiares por País':"RFORG",
        'Balanza Cambiaria':"BALCAM",
        'Tasas IO': "TIO",
        'Cotización Principales Monedas': "CPMON",
        'BCH-TR': "BCHTR",
        'CCECH': "CCECH",
        'ACH PRONTO': "ACHP",
        'Precio Diario del Dólar-EUA': "PDDEUA",
        'Índice del Tipo de Cambio Efectivo Real':"ITCER",
        'Información Subasta Diaria': "INFSBD",
        'Información Subasta Estructural': "INFSET",
        'Información Subasta bonos BCH': "INFSB",
        'Operaciones de Reporto': "OREPO",
        'Facilidades permanentes': "FPERM",
        'Información MED': "INFMED",
        'Bonos de Sefin': "BSEFIN",
        'Tasa Variable Bonos Sefin': "TSEFIN",
        'Tasa Variable Bonos ENEE': "TENEE",
        'Operaciones de Mercado Secundario': "OMSEC",
        'Índice de Precios al Consumidor':"IPC",
        'Índice de Precios al Consumidor por rubros': "IPCR",
        'Índice de Precios al Consumidor por región':"IPCREG",
        'Índice de Inflación Subyacente': "IIFSUB",
        'Tasa de Política Monetaria': "TPM",
        'Tasa Anuales de Interés sobre Operaciones Nuevas': "TINON",
        'Tasas sobre Operaciones Nuevas Actividad Económica': "TONAE",
        'Tasas Saldos Sistema Financiero': "TSLSF",
        'Tasas Saldos Sistema Financiero por AE': "TSLSF1",
        'RIN y ARO':"RINARO",
        'Emisión y Base Monetaria': "EBM",
        'Agregados Monetarios': "AM",
        'Agregados Monetarios como Porcentaje del PIB': "AMPPIB",
        'Captación de los Bancos Comerciales': "CBCOM",
        'Captación de las Otras Sociedades': "COSO",
        'Crédito al Sector Privado': "CRDPRV",
        'Préstamos de las Otras Sociedades': "PTOSO",
        'Préstamos de BC Porcentaje PIB':"PTBCPPIB",
        'Activos y Pasivos Externos Sistema Financiero': "SFIN",
        'Activos y Pasivos Externos Banco Comerciales': "BCOM",
        'Activos y Pasivos Ext Sociedades de Depósitos': "SODEP",
        'Índice Mensual de Actividad Económica': "IMAE",
        'PIB y VAB': "PIBVAB",
        'VAB por Actividad Económica': "VABAE",
        'PIB Gasto': "PIBG",
        'PIB Ingreso': "PIBIG",
        'PIB e Ingreso Nacional Per-Cápita': "PIBIGPC",
        'VAB Agropecuario': "VABAGRO",
        'VAB Industria': "VABIND",
        'VAB Productos Alimenticios': "VABPRDA",
        'Balanza de Pagos': "BALPAG",
        'Cuenta Corriente': "CCOR",
        'Exportaciones de Importaciones de Bienes totales': "EXIMPBT",
        'Balanza de Bienes por Categoría':"BALBCAT",
        'Exportaciones FOB de Principales Productos de Mercnacías Generales': "EXPPMG",
        'Importaciones de Combustibles por Tipo de Combustible': "IMPCOM",
        'Exportaciones e Importaciones de Bienes para Transformación': "BTRF",
        'Exportaciones FOB de Bienes para Tranformación': "EXPBTRF",
        'Importaciones CIF de Bienes Para Transformación por categoria':"IMPBTRF",
        'Balanza de Servicios': "BALSER",
        'Ingresos y Egresos de Servicios por Categoria': "SERCAT",
        'Remesas Familiares Corrientes': "RFCOR",
        'Flujo Neto de Inversión Extranjera hacia Honduras por Actividad Económica': "IVEXJAE",
        'Flujo Neto de Inversión Extranjera hacia Honduras por Región Geográfica':"IVEXJREG",
        'Flujo Neto de Inversión Extrajera Directa hacia Honduras por Componente': "IVDR",
        'PII Categoría': "PIICAT",
        'PII Componente': "PII",
        'PII Activos-Componentes': "PIIA",
        'PII Pasivos-Componentes': "PIIP",
        'Deuda Externa pública': "DXTPUB",
        'Deuda Externa Total por Sector': "DXTST",
        'Deuda Externa Total por Tipo de Deudor':"DXTDEU",
        'Deuda Externa Pública por Tipo de Deudor': "DXTDPUB",
        'Deuda Externa Total por Tipo de Acreedor': "DXTACRE",
        'Financiamiento Externo e Interno AC y SPNF': "FNXTNT12",
        'Financiamiento Externo AC y SPNF': "FNXT12",
        'Financiamiento Interno AC por Sector':"FNINT1",
        'Financiamiento Interno SPNF por Sector': "FNINT2",
        'Financiamiento Interno AC y SPNF por Inst': "FNINT12",
        'Posición Financiera de la AC y SPNF': "POSFIN12",
        'Deuda Interna AC por Transacción': "DNT1TS",
        'Deuda Interna del SP por Instrumento': "DNTINST",
        'Deuda Interna del Resto del SPNF por Tenedor': "DNT2TD",
        'Servicio de Deuda Interna AC':"SERDUINT",
        'Expectativas de Inflación': "EXPECIF"
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