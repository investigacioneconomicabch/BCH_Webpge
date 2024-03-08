from selenium import webdriver
from selenium.webdriver.common.by import By

import requests

def login_SICE(username, password):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option( "prefs", { "download.default_directory": "C:/IE/Julia/GitHub/BCH_Webpage-main" })

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://sisee.bch.hn/SICE/Login.aspx")

    username_field = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$UserName')
    password_field = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$Password')
    submit_button  = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$LoginButton')

    username_field.send_keys(username)
    password_field.send_keys(password)
    submit_button.click()

    response = driver.get('https://sisee.bch.hn/SICE/ConsultaSACAjustado.aspx')

    return driver
    
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_SICE_query(driver, serie, year, month, country):
    series_dict = dict(Importaciones = 0, Exportaciones = 1, BalanzaCambiaria = 2)

    driver.get('https://sisee.bch.hn/SICE/ConsultaSACAjustado.aspx')

    select_element = driver.find_element(By.ID,'ContentPlaceHolder1_DDLComercio')
    select = Select(select_element)
    select.select_by_value(str(series_dict[serie]))

    dropdown_arrow = driver.find_element(By.ID, "ContentPlaceHolder1_BtnAnual")
    dropdown_arrow.click()

    wait = WebDriverWait(driver, 10)
    year_month_window = wait.until(EC.visibility_of_element_located((By.ID, "ContentPlaceHolder1_SeleccionardeListaAnual_BtnSeleccionarTodo")))

    dropdown_arrow = driver.find_element(By.ID, "ContentPlaceHolder1_SeleccionardeListaAnual_BtnSeleccionarTodo")
    dropdown_arrow.click()

    if year:
        ChkAnual = driver.find_element(By.ID,'ContentPlaceHolder1_ChkAnual')
        ChkAnual.click()

    if month:
        ChkMes = driver.find_element(By.ID,'ContentPlaceHolder1_ChkMes')
        ChkMes.click()

    if country:
        ChkPais = driver.find_element(By.ID,'ContentPlaceHolder1_ChkPais')
        ChkPais.click()

    download_button = driver.find_element(By.ID,'ContentPlaceHolder1_BtnDescargar')
    download_button.click()
