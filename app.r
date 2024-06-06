#### Librerías ####
library(bslib)
library(dplyr)
library(DT)
library(ggExtra)
library(ggplot2)
library(ggpubr)
library(httr)
library(jsonlite)
library(plotly)
library(shiny)
library(shinydashboard)
library(shinyWidgets)
library(tidyverse)

clave <- "ff34cff7b0024ea39eb565fccb9f03b6" #Favor ingresar la clave proporcionada.

#### Funciones ####
get_indicators <- function() {
  res <- GET(
    "https://bchapi-am.azure-api.net/api/v1/indicadores/?formato=Json",
    add_headers(Clave=clave))
  data <- fromJSON(rawToChar(res$content))
  data <- data.frame(data)
  return(data)
}

get_data_indicator <- function(id) {
  url <- paste0("https://bchapi-am.azure-api.net/api/v1/indicadores/",as.character(id),"/cifras")
  res <- GET(
    url,
    add_headers(Clave=clave))
  data <- fromJSON(rawToChar(res$content))
  data$Fecha <- as.Date(data$Fecha)
  data <- data.frame(data)
  return(data)
}

get_data_indicators <- function(ids) {
  data <- data.frame()
  for (i in 1:length(ids)) { 
    data <- rbind(data,get_data_indicator(ids[i]))
  }
  data$Fecha <- as.Date(data$Fecha)
  data <- data.frame(data)
  return(data)
}

get_groups <- function() {
  res <- GET(
    "https://bchapi-am.azure-api.net/api/v1/indicadores/?formato=Json",
    add_headers(Clave=clave))
  data <- fromJSON(rawToChar(res$content))
  data <- data.frame(data)
  return(data)
}

#### Boxes ####
body <- dashboardBody(
  fluidRow(
#### Grupos ####
    box(
      title = "Seleccione Nivel 1 Grupo",
      width = 3,
      solidHeader = T,
      status = "warning",
      uiOutput("filter_1")),
    box(
      title = "Seleccione Nivel 2 Grupo",
      width = 3,
      solidHeader = T,
      status = "warning",
      uiOutput("filter_2")),
    box(
      title = "Seleccione Nivel 3-5 Grupo",
      width = 4,
      solidHeader = T,
      status = "warning",
      uiOutput("filter_3_5")),
    # box(
    #   title = "Seleccione Nivel 3 Grupo",
    #   width = 2,
    #   solidHeader = T,
    #   status = "warning",
    #   uiOutput("filter_3")),
    # box(
    #   title = "Seleccione Nivel 4 Grupo",
    #   width = 2,
    #   solidHeader = T,
    #   status = "warning",
    #   uiOutput("filter_4")),
    # box(
    #   title = "Seleccione Nivel 5 Grupo",
    #   width = 2,
    #   solidHeader = T,
    #   status = "warning",
    #   uiOutput("filter_5")),
    # # box(
    #   title = "Tabla de Grupos",
    #   width = 4,
    #   solidHeader = T,
    #   status = "warning",
    #   DTOutput('grupos')),
#### Indicadores ####
    box(
      title = "Tabla de Indicadores",
      width = 4,
      solidHeader = T,
      status = "warning",
      DTOutput('indicadores')),
  box(
    title = "Seleccione Id",
    width = 1,
    solidHeader = T,
    status = "primary",
    uiOutput('ids_select')),
  box(
    title = "Gráfico",
    width = 5,
    solidHeader = T,
    status = "success",
    plotlyOutput("fig")),
  box(
      title = "No elegir intervalos: 6642:6687, 7392:7446",
      # 6642 hasta 6687
      # 7392 hasta 7446
      width = 4,
      solidHeader = T,
      status = "primary",
      DTOutput('table')),
  box(
    title = "Descargar Selección",
    width = 2,
    solidHeader = T,
    status = "success",
    downloadButton("download_serie")),

#### ####
))

ui <- dashboardPage(
#### ui ####
  dashboardHeader(title = "Elegir uno por nivel"),
  dashboardSidebar(disable=T), 
  body)
#### ####

server <- function(input, output, session) {

#### Grupos ####
  gr <- get_groups() %>% 
    filter(! Grupo %in% "EOM-OMA-01")
  gr <- gr %>% 
    count(Grupo,Periodicidad, sort = TRUE) %>% 
      mutate(Gr3_5 = Grupo) %>%
    separate(
      Grupo, 
      into = c("Gr1","Gr2","Gr3","Gr4","Gr5"), 
      remove = FALSE)
  # gr$Niv_Gr <- rowSums(!is.na(gr[c(2:6)]))
  gr <- gr %>% 
    # mutate(Gr3 = replace_na(Gr3, "")) %>%
    # mutate(Gr4 = replace_na(Gr4, "")) %>%
    # mutate(Gr5 = replace_na(Gr5, "")) %>%
    mutate(
      Gr1 = recode(
        Gr1,
        'EOM' = 'Estadísticas de Operaciones Monetarias',
        'ESR' = 'Estadísticas del Sector Real',
        'ESE' = 'Estadísticas del Sector Externo',
        'EMF' = 'Estadísiticas Monetarias y Financieras (Sector Fiscal)',
        'EM' = 'Estadísticas Monetarias (TPM y RIN)',
        'ESP' = 'Estadísticas de Sistema de Pagos',
        'EC' = 'Estadísticas de Tipo de Cambio',
        'EP' = 'Estadísticas de Precios'),
      Gr2 = recode(
        Gr2,
        'OMA' = 'Operaciones de Mercado Abierto',
        'COU' = 'Cuadro de Oferta y Utilización',
        'CCI' = 'Clasificación Cruzada Industria',
        'VAB' = 'Valor Agregado Bruto',
        'PIBA' = 'PIB Anual',
        'PIBT' = 'PIB Trimestral',
        'ODA' = 'Oferta y Demanda Agregada',
        'IMAE' = 'Índice Mensual de la Actividad Económica',
        'DE' = 'Deuda Externa',
        'CEB' = 'Comercio Exterior de Bienes',
        'BP' = 'Balanza de Pagos',
        'IES' = 'Ingresos y Egresos de Servicios',
        'PII' = 'Posición de Inversión Internacional',
        'IED' = 'Inversión Extranjera Directa',
        'AMCC' = 'Agregados Monetarios, Crédito y Captación',
        'TI' = 'Tasas de Interés',
        'PFS' = 'Panorama de las Sociedades Financieras',
        'EBM' = 'Emisión y Base Monetaria',
        'RIN' = 'Reservas Internacionales Netas',
        'TPM' = 'Tasa de Política Monetaria',
        'ACH' = 'Operaciones de Crédito Compensadas en Ceproban y Liquidadas en BCH',
        'CCECH' = 'Cheques Compensados en Ceproban y Liquidados en BCH',
        'TCR' = 'Tipo de Cambio de Referencia',
        'TCN' = 'Tipo de Cambio Nominal',
        'IPC' = 'Índice de Precios al Consumidor'),
      # Gr3 = recode(
      #   Gr3,
      #   'PROD' = 'Enfoque de la Producción',
      #   'GAST' = 'Enfoque del Gasto',
      #   'TDC' = 'Valores Ajustados'),
      # Gr4 = recode(
      #   Gr4,
      #   'DES' = 'Serie Desestacionalizada',
      #   'OG' = 'Serie Original',
      #   'Valores' = ''),
      # Gr5 = recode(
      #   Gr5,
      #   'CONST' = 'Valores Constantes',
      #   'CORR' = 'Valores Corrientes'),
      Grupo = recode(
        Grupo,
        'EC-TCN-01' = '--',
        'EC-TCR' = '--',
        'EM-RIN-01' = '--',
        'EM-TPM-01' = '--',
        'EMF-AMCC-01' = 'Agregados Monetarios, Crédito y Captación--',
        'EMF-AMCC-02' = 'Captación: Bancos Comerciales y Otras Sociedades de Depósito (Variación y Saldo)--',
        'EMF-AMCC-03' = 'Crédito de los Bancos Comerciales--',
        'EMF-AMCC-04' = 'Crédito Otras Sociedades de Depósito--',
        'EMF-AMCC-05' = 'Saldo de Préstamos (Millones de Lempiras)--',
        'EMF-AMCC-06' = 'Préstamos Nuevos (Flujos acumulados en millones de lempiras)--',
        'EMF-EBM-01' = '--',
        'EMF-PFS-01' = 'Bancos Comerciales, Activos y Pasivos Externos--',
        'EMF-PFS-02' = 'Activos y Pasivos Externos--',
        'EMF-TI-01' = 'Activa y Pasiva, por Moneda--',
        'EMF-TI-02' = 'Por Actividad--',
        'EMF-TI-03' = 'Anuales--',
        'EOM-OMA-01' = 'Tasas de Rendimiento Diario de Valores Gubernamentales--',
        'EOM-OMA-02' = 'Créditos (Niv_Descr_4 = 1-3) e Inversiones (Niv_Descr_4 = 4-6): Monto, Número de Solicitudes y Tasa--',
        'EOM-OMA-03' = 'Monto, Número de Operaciones y Tasa--',
        'EOM-OMA-04' = 'Monto, Número de Operaciones y Tasa (Dólares - Lempiras)--',
        'EP-IPC-01' = '--',
        'ESE-BP-01' = '--',
        'ESE-CEB-01' = 'Productos--',
        'ESE-CEB-02' = 'Combustibles--',
        'ESE-CEB-03' = 'Importaciones AE, BT y Secciones--',
        'ESE-CEB-04' = 'Exportaciones AE y BT--',
        'ESE-DE-01' = 'Deudor--',
        'ESE-DE-02' = 'Acreedor--',
        'ESE-DE-03' = 'Por Institución--',
        'ESE-DE-04' = 'Pagos que vencen en un año o menos--',
        'ESE-IED-01' = '--',
        'ESE-IES-01' = '--',
        'ESE-PII-01' = '--',
        'ESP-ACH-01' = '--',
        'ESP-CCECH-01' = '--',
        'ESR-CCI-01' = '--',
        'ESR-COU-01' = '--',
        'ESR-IMAE-01___' = '--',
        'ESR-ODA-01' = '--',
        'ESR-PIBA-01' = 'Valores Corrientes y Constantes, por Actividad Económica--',
        'ESR-PIBA-02' = 'Precios y Variación, por Componente del Gasto--',
        'ESR-PIBA-03' = 'Precios y Variación, por Componente del Ingreso--',
        'ESR-PIBA-04' = 'Dólares y Lempiras--',
        'ESR-PIBT-GAST-DES-CONST' = 'Enfoque del Gasto-Serie Desestacionalizada-Valores Constantes',
        'ESR-PIBT-GAST-DES-CORR' = 'Enfoque del Gasto-Serie Desestacionalizada-Valores Corrientes',
        'ESR-PIBT-GAST-OG-CONST' = 'Enfoque del Gasto-Serie Original-Valores Constantes',
        'ESR-PIBT-GAST-OG-CORR' = 'Enfoque del Gasto-Serie Original-Valores Corrientes',
        'ESR-PIBT-PROD-DES-CONST' = 'Enfoque de la Producción-Serie Desestacionalizada-Valores Constantes',
        'ESR-PIBT-PROD-DES-CORR' = 'Enfoque de la Producción-Serie Desestacionalizada-Valores Corrientes',
        'ESR-PIBT-PROD-OG-CONST' = 'Enfoque de la Producción-Serie Original-Valores Constantes',
        'ESR-PIBT-PROD-OG-CORR' = 'Enfoque de la Producción-Serie Original-Valores Corrientes',
        'ESR-PIBT-TDC-Valores' = 'Valores Ajustados--',
        'ESR-VAB-01' = 'Valor y Variación, Corrientes y Constantes, por NAEH--',
        'ESR-VAB-02' = 'Precio y Variación, Corrientes y Constantes, por NAEH--')
      ) %>%
    arrange(Gr1,Gr2,desc(n))

#### Selector de Grupos ####
  ## Selector de Nivel 1 Grupos  
  categories_1 <- as.factor(c('Gr1'))

  output$filter_1 <- renderUI({
    pickerInput(
      "filter_1",
      choices = unique(gr$Gr1),
      options = list('actions-box'=T), 
      multiple= T,
      selected = unique(gr$Gr1))
  })

## Selector de Nivel 2 Grupos  
  categories_2 <- c("Gr2")

  output$filter_2 <- renderUI({
    pickerInput(
      "filter_2",
      choices = unique(
        gr %>%
          filter(Gr1 %in% input$filter_1) %>%
          select(Gr2)),
      options = list('actions-box'=T), 
      multiple= T,
      selected = unique(
        gr %>%
          filter(Gr1 %in% input$filter_1) %>%
          select(Gr2)))
  })

## Selector de Nivel 3 Grupos  
  categories_3_5 <- c("Grupo")
  
  output$filter_3_5 <- renderUI({
    pickerInput(
      "filter_3_5",
      choices = unique(
        gr %>%
          filter(Gr1 %in% input$filter_1) %>%
          filter(Gr2 %in% input$filter_2) %>%
          select(Grupo)),
      options = list('actions-box'=T), 
      multiple= T,
      selected = unique(
        gr %>%
          filter(Gr1 %in% input$filter_1) %>%
          filter(Gr2 %in% input$filter_2) %>%
          select(Grupo)))
  })
  
## Selector de Nivel 3 Grupos  
  # categories_3 <- c("Gr3")
  # 
  # output$filter_3 <- renderUI({
  #   pickerInput(
  #     "filter_3",
  #     choices = unique(
  #       gr %>%
  #         filter(Gr1 %in% input$filter_1) %>%
  #         filter(Gr2 %in% input$filter_2) %>%
  #         select(Gr3)),
  #     options = list('actions-box'=T), 
  #     multiple= T,
  #     selected = unique(
  #       gr %>%
  #         filter(Gr1 %in% input$filter_1) %>%
  #         filter(Gr2 %in% input$filter_2) %>%
  #         select(Gr3)))
  # })

## Selector de Nivel 4 Grupos  
  # categories_4 <- c("Gr4")
  # 
  # output$filter_4 <- renderUI({
  #   pickerInput(
  #     "filter_4",
  #     choices = unique(
  #       gr %>%
  #         filter(Gr1 %in% input$filter_1) %>%
  #         filter(Gr2 %in% input$filter_2) %>%
  #         filter(Gr3 %in% input$filter_3) %>%
  #         select(Gr4)),
  #     options = list('actions-box'=T), 
  #     multiple= T,
  #     selected = unique(
  #       gr %>%
  #         filter(Gr1 %in% input$filter_1) %>%
  #         filter(Gr2 %in% input$filter_2) %>%
  #         filter(Gr3 %in% input$filter_3) %>%
  #         select(Gr4)))
  # })
  
## Selector de Nivel 5 Grupos  
  # categories_5 <- c("Gr5")
  # 
  # output$filter_5 <- renderUI({
  #   pickerInput(
  #     "filter_5",
  #     choices = unique(
  #       gr %>%
  #         filter(Gr1 %in% input$filter_1) %>%
  #         filter(Gr2 %in% input$filter_2) %>%
  #         filter(Gr3 %in% input$filter_3) %>%
  #         filter(Gr4 %in% input$filter_4) %>%
  #         select(Gr5)),
  #     options = list('actions-box'=T), 
  #     multiple= T,
  #     selected = unique(
  #       gr %>%
  #         filter(Gr1 %in% input$filter_1) %>%
  #         filter(Gr2 %in% input$filter_2) %>%
  #         filter(Gr3 %in% input$filter_3) %>%
  #         filter(Gr4 %in% input$filter_4) %>%
  #         select(Gr5)))
  # })
  
## Tabla de grupos filtrados  
  # filtered_gr <- 
  #   reactive ({
  #     gr %>%
  #       filter(
  #         Gr1 %in% input$filter_1) %>%
  #       filter(
  #         Gr2 %in% input$filter_2) %>%
  #       filter(
  #         Gr3 %in% input$filter_3) %>%
  #       filter(
  #         Gr4 %in% input$filter_4) %>%
  #       filter(
  #         Gr5 %in% input$filter_5) %>%
  #       select(-c("Gr3","Gr4","Gr5","Niv_Gr"))
  #   })
  # 
  # output$grupos <- renderDataTable(
  #   filtered_gr(),
  #   options = list(
  #     pageLength = 5,
  #     autoWidth = F),)

#### Indicadores ####
  ind <- get_indicators() %>% select(-c(CorrelativoGrupo))
  ind$Id <- as.character(ind$Id)
  ind <- ind %>% 
    #count(Grupo,Periodicidad, sort = TRUE) %>% 
    separate(
      Grupo, 
      into = c("Gr1","Gr2","Gr3","Gr4","Gr5"), 
      remove = FALSE) %>%
    mutate(
      Gr1 = recode(
        Gr1,
        'EOM' = 'Estadísticas de Operaciones Monetarias',
        'ESR' = 'Estadísticas del Sector Real',
        'ESE' = 'Estadísticas del Sector Externo',
        'EMF' = 'Estadísiticas Monetarias y Financieras (Sector Fiscal)',
        'EM' = 'Estadísticas Monetarias (TPM y RIN)',
        'ESP' = 'Estadísticas de Sistema de Pagos',
        'EC' = 'Estadísticas de Tipo de Cambio',
        'EP' = 'Estadísticas de Precios'),
      Gr2 = recode(
        Gr2,
        'OMA' = 'Operaciones de Mercado Abierto',
        'COU' = 'Cuadro de Oferta y Utilización',
        'CCI' = 'Clasificación Cruzada Industria',
        'VAB' = 'Valor Agregado Bruto',
        'PIBA' = 'PIB Anual',
        'PIBT' = 'PIB Trimestral',
        'ODA' = 'Oferta y Demanda Agregada',
        'IMAE' = 'Índice Mensual de la Actividad Económica',
        'DE' = 'Deuda Externa',
        'CEB' = 'Comercio Exterior de Bienes',
        'BP' = 'Balanza de Pagos',
        'IES' = 'Ingresos y Egresos de Servicios',
        'PII' = 'Posición de Inversión Internacional',
        'IED' = 'Inversión Extranjera Directa',
        'AMCC' = 'Agregados Monetarios, Crédito y Captación',
        'TI' = 'Tasas de Interés',
        'PFS' = 'Panorama de las Sociedades Financieras',
        'EBM' = 'Emisión y Base Monetaria',
        'RIN' = 'Reservas Internacionales Netas',
        'TPM' = 'Tasa de Política Monetaria',
        'ACH' = 'Operaciones de Crédito Compensadas en Ceproban y Liquidadas en BCH',
        'CCECH' = 'Cheques Compensados en Ceproban y Liquidados en BCH',
        'TCR' = 'Tipo de Cambio de Referencia',
        'TCN' = 'Tipo de Cambio Nominal',
        'IPC' = 'Índice de Precios al Consumidor'),
      # Gr3 = recode(
      #   Gr3,
      #   'PROD' = 'Enfoque de la Producción',
      #   'GAST' = 'Enfoque del Gasto',
      #   'TDC' = 'Valores Ajustados'),
      # Gr4 = recode(
      #   Gr4,
      #   'DES' = 'Serie Desestacionalizada',
      #   'OG' = 'Serie Original',
      #   'Valores' = ''),
      # Gr5 = recode(
      #   Gr5,
      #   'CONST' = 'Valores Constantes',
      #   'CORR' = 'Valores Corrientes'))
      Grupo = recode(
        Grupo,
        'EC-TCN-01' = '--',
        'EC-TCR' = '--',
        'EM-RIN-01' = '--',
        'EM-TPM-01' = '--',
        'EMF-AMCC-01' = 'Agregados Monetarios, Crédito y Captación--',
        'EMF-AMCC-02' = 'Captación: Bancos Comerciales y Otras Sociedades de Depósito (Variación y Saldo)--',
        'EMF-AMCC-03' = 'Crédito de los Bancos Comerciales--',
        'EMF-AMCC-04' = 'Crédito Otras Sociedades de Depósito--',
        'EMF-AMCC-05' = 'Saldo de Préstamos (Millones de Lempiras)--',
        'EMF-AMCC-06' = 'Préstamos Nuevos (Flujos acumulados en millones de lempiras)--',
        'EMF-EBM-01' = '--',
        'EMF-PFS-01' = 'Bancos Comerciales, Activos y Pasivos Externos--',
        'EMF-PFS-02' = 'Activos y Pasivos Externos--',
        'EMF-TI-01' = 'Activa y Pasiva, por Moneda--',
        'EMF-TI-02' = 'Por Actividad--',
        'EMF-TI-03' = 'Anuales--',
        'EOM-OMA-01' = 'Tasas de Rendimiento Diario de Valores Gubernamentales--',
        'EOM-OMA-02' = 'Créditos (Niv_Descr_4 = 1-3) e Inversiones (Niv_Descr_4 = 4-6): Monto, Número de Solicitudes y Tasa--',
        'EOM-OMA-03' = 'Monto, Número de Operaciones y Tasa--',
        'EOM-OMA-04' = 'Monto, Número de Operaciones y Tasa (Dólares - Lempiras)--',
        'EP-IPC-01' = '--',
        'ESE-BP-01' = '--',
        'ESE-CEB-01' = 'Productos--',
        'ESE-CEB-02' = 'Combustibles--',
        'ESE-CEB-03' = 'Importaciones AE, BT y Secciones--',
        'ESE-CEB-04' = 'Exportaciones AE y BT--',
        'ESE-DE-01' = 'Deudor--',
        'ESE-DE-02' = 'Acreedor--',
        'ESE-DE-03' = 'Por Institución--',
        'ESE-DE-04' = 'Pagos que vencen en un año o menos--',
        'ESE-IED-01' = '--',
        'ESE-IES-01' = '--',
        'ESE-PII-01' = '--',
        'ESP-ACH-01' = '--',
        'ESP-CCECH-01' = '--',
        'ESR-CCI-01' = '--',
        'ESR-COU-01' = '--',
        'ESR-IMAE-01___' = '--',
        'ESR-ODA-01' = '--',
        'ESR-PIBA-01' = 'Valores Corrientes y Constantes, por Actividad Económica--',
        'ESR-PIBA-02' = 'Precios y Variación, por Componente del Gasto--',
        'ESR-PIBA-03' = 'Precios y Variación, por Componente del Ingreso--',
        'ESR-PIBA-04' = 'Dólares y Lempiras--',
        'ESR-PIBT-GAST-DES-CONST' = 'Enfoque del Gasto-Serie Desestacionalizada-Valores Constantes',
        'ESR-PIBT-GAST-DES-CORR' = 'Enfoque del Gasto-Serie Desestacionalizada-Valores Corrientes',
        'ESR-PIBT-GAST-OG-CONST' = 'Enfoque del Gasto-Serie Original-Valores Constantes',
        'ESR-PIBT-GAST-OG-CORR' = 'Enfoque del Gasto-Serie Original-Valores Corrientes',
        'ESR-PIBT-PROD-DES-CONST' = 'Enfoque de la Producción-Serie Desestacionalizada-Valores Constantes',
        'ESR-PIBT-PROD-DES-CORR' = 'Enfoque de la Producción-Serie Desestacionalizada-Valores Corrientes',
        'ESR-PIBT-PROD-OG-CONST' = 'Enfoque de la Producción-Serie Original-Valores Constantes',
        'ESR-PIBT-PROD-OG-CORR' = 'Enfoque de la Producción-Serie Original-Valores Corrientes',
        'ESR-PIBT-TDC-Valores' = 'Valores Ajustados--',
        'ESR-VAB-01' = 'Valor y Variación, Corrientes y Constantes, por NAEH--',
        'ESR-VAB-02' = 'Precio y Variación, Corrientes y Constantes, por NAEH--'))
  # ind$Niv_Gr <- rowSums(!is.na(ind[c(6:10)]))
  # ind <- ind %>% 
  #   mutate(Gr3 = replace_na(Gr3, "")) %>%
  #   mutate(Gr4 = replace_na(Gr4, "")) %>%
  #   mutate(Gr5 = replace_na(Gr5, "")) %>%
    # arrange(desc(Niv_Gr))
 
## Tabla de indicadores filtrados  
  filtered_ind <- 
    reactive ({
      ind %>%
        filter(
          Gr1 %in% input$filter_1) %>%
        filter(
          Gr2 %in% input$filter_2) %>%
        filter(
          Grupo %in% input$filter_3_5) %>%
        # filter(
        #   Gr3 %in% input$filter_3) %>%
        # filter(
        #   Gr4 %in% input$filter_4) %>%
        # filter(
        #   Gr5 %in% input$filter_5) %>% 
        filter(Id %in% (1:6641) | Id %in% (6688:7391) | Id %in% (7447:11519)) %>% 
        select(-c("Grupo","Gr1","Gr2","Gr3","Gr4","Gr5"))
    })
  
  output$indicadores <- renderDataTable(
    filtered_ind(),
    options = list(
      pageLength = 5,
      autoWidth = F),)

  output$ids_select <- renderUI({
    pickerInput(
      "ids_select",
      choices = filtered_ind()$Id,
      options = list('actions-box'=T), 
      multiple= T,
      selected = filtered_ind()$Id)
  })

  
#### Tabla de Valores #### 
  # Nota: no elegir valores en rangos:
  # 6642 hasta 6687
  # 7392 hasta 7446
  filtered_data <- 
    reactive ({
      get_data_indicators(input$ids_select) %>% select(-c("Id"))
    })
  
  output$table <- renderDataTable(
    filtered_data(),
    options = list(
      pageLength = 5,
      autoWidth = F),)

  #### Gráfico ####
    output$fig <- renderPlotly({
      fig <- req(filtered_data()) %>% 
        plot_ly(
          x = ~Nombre, 
          y = ~Suma)
      fig <- fig %>% add_lines(
        x = ~Fecha, 
        y = ~Valor,
        color = ~Nombre)#add_pie(hole = 0.6)
      fig <- fig %>% layout(
        #title = "Representatividad",  
        showlegend = T,
        xaxis = list(title = ''),
        yaxis = list(title = ''),
        legend = list(
          orientation = "h",
          xanchor = "center",
          title=list(text=''),
          x = 0.5),
        title = "",
        xaxis = list(dtick = ""))
      })
  
  #### Gráfico ####
  output$download_serie <- downloadHandler(
    filename = "Series_API.csv",
    content = function(file) {
      write.csv(
        filtered_data(), 
        file, 
        row.names = F)
    }
  )
  
#  in_react_frame <- reactiveVal(df)
#  filtered_frame <-  reactive({
#    frame <- req(in_react_frame())
#    indexes <- req(input$table_rows_all)
#    frame[indexes,]
#  })
#  summarised_frame <- reactive({req(filtered_frame())})
#  output$table <- renderDT(
#    in_react_frame(),
#    options = list(
#      pageLength = 3,
#      autoWidth = F),
#    filter = list(
#      position = 'top',
#      clear = F,
#      plain = T
#    ))
  
#### Gráfico ####
#  output$fig <- renderPlotly({
#    fig <- req(summarised_frame()) %>% plot_ly(x = ~Nombre, y = ~Suma)
#    fig <- fig %>% add_lines(
#      x = ~Fecha, 
#      y = ~Valor,
#      color = ~Nombre)#add_pie(hole = 0.6)
#    fig <- fig %>% layout(
#      #title = "Representatividad",  
#      showlegend = T,
#      xaxis = list(title = ''),
#      yaxis = list(title = ''),
#      legend = list(
#        orientation = "h",
#        xanchor = "center",
#        title=list(text=''),
#        x = 0.5),
#      title = "",
#      xaxis = list(dtick = ""))
#    })

}

shinyApp(ui, server)


#### Ejemplo con menú desplegable dentro del gráfico
# p <- df %>%
#   plot_ly(
#     type = 'scatter', 
#     mode = 'lines',
#     x = ~Fecha, 
#     y = ~Valor,
#     # text = ~Species,
#     # hoverinfo = 'text',
#     mode = 'markers', 
#     transforms = list(
#       list(
#         type = 'filter',
#         mode = 'lines',
#         target = ~Nombre,
#         operation = 'in',
#         value = unique(df$Nombre)[1]
#       )
#     )) %>%
#   layout(
#     updatemenus = list(
#       list(
#         type = 'dropdown',
#         active = 0,
#         buttons = list(
#           list(method = "restyle",
#                args = list("transforms[0].value", unique(df$Nombre)[1]),
#                label = unique(df$Nombre)[1]),
#           list(method = "restyle",
#                args = list("transforms[0].value", unique(df$Nombre)[2]),
#                label = unique(df$Nombre)[2]),
#           list(method = "restyle",
#                args = list("transforms[0].value", unique(df$Nombre)[3]),
#                label = unique(df$Nombre)[3])
#         )
#       )
#     )
#   )
# p

