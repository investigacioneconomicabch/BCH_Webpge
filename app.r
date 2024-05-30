# Librerías
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
library(tidyverse)

clave <- "ff34cff7b0024ea39eb565fccb9f03b6" #Favor ingresar la clave proporcionada.

# Funciones
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

# ids <- c(1,2,3,4,5) # Total de indicadores: 11519
# df <- get_data_indicators(ids)
# df$Id <- as.character(df$Id)
# df$IndicadorId <- as.character(df$IndicadorId)
# df <- df %>% select(-Id) %>% rename(Id = IndicadorId)
# knitr::kable(tail(df))

body <- dashboardBody(
  fluidRow(
    box(
      title = "Tabla de Indicadores",
      width = 5,
      solidHeader = T,
      status = "warning",
      DTOutput('table_1') ),
    box(
      title = "Grupos",
      width = 5,
      solidHeader = T,
      status = "warning",
      textInput("Id", "Seleccione grupo"),
      textOutput("Seleccion")),
    box(
      title = "Tabla de Valores",
      width = 5,
      solidHeader = T,
      status = "primary",
      DTOutput('table') ),
    box(
      title = "Gráfico",
      width = 5,
      solidHeader = T,
      status = "success",
      plotlyOutput("fig"))
    )
  )

ui <- dashboardPage(
  dashboardHeader(title = "Selección de Datos"),
  dashboardSidebar(disable=T), 
  body)

ind <- get_indicators()
ind$Id <- as.character(ind$Id)
Grupos <- ind %>% distinct(Grupo)

#ui <- fluidPage(
#  headerPanel("Lista de IDs"),
#  sidebarPanel(
#    selectizeInput(
#      inputId = "selectId",
#      label = "Ingrese Valores",
#      choices = ind$Grupo,
#      selected = NULL,
#      multiple = T,
#      width = "100%",
#      options = list(
#        'plugins' = list('remove_button'),
#        'create' = F,
#        'persist' = T
#      )
#    )
#  ),
#  mainPanel(textOutput("caption"))
#)


server <- function(input, output, session) {

## Tabla de Inputs  
  headerPanel("Lista de IDs")
    sidebarPanel(
      selectizeInput(
        inputId = "selectId",
        label = "Ingrese Valores",
        choices = Grupos,
        selected = NULL,
        multiple = T,
        width = "100%",
        options = list(
          'plugins' = list('remove_button'),
          'create' = F,
          'persist' = T
        )
      ))
  #in_react_text <- reactiveVal(Grupos)
  #output$Seleccion <- renderMenu(Grupos[1])

  
#  headerPanel("Lista de IDs"),
#  sidebarPanel(
#    selectizeInput(
#      inputId = "selectId",
#      label = "Ingrese Valores",
#      choices = ind$Grupo,
#      selected = NULL,
#      multiple = T,
#      width = "100%",
#      options = list(
#        'plugins' = list('remove_button'),
#        'create' = F,
#        'persist' = T
#      )
#    )
#  ),
#  mainPanel(textOutput("caption"))

## Tabla de Indicadores  
  ind <- get_indicators()
  ind$Id <- as.character(ind$Id)

  in_react_frame_1 <- reactiveVal(ind)
  filtered_frame_1 <-  reactive({
    frame <- req(in_react_frame_1())
    indexes <- req(input$table_rows_all)
    frame[indexes,]
  })
  summarised_frame_1 <- reactive({req(filtered_frame_1())})
  output$table_1 <- renderDT(
    in_react_frame_1(),
    options = list(
      pageLength = 3,
      autoWidth = F),
    filter = list(
      position = 'top',
      clear = F,
      plain = T
    ))
  
## Tabla de Valores  
  #ids <- req(summarised_frame())
  # 6642 hasta 6687
  # 7392 hasta 7446
  ids <- c(1,2,3,4,5) # Total de indicadores: 11519
  df <- get_data_indicators(ids)
  df$Id <- as.character(df$Id)
  df$IndicadorId <- as.character(df$IndicadorId)
  #df <- df %>% select(-c(Id,Nombre,Descripcion)) %>% rename(Id = IndicadorId)
  df <- df %>% select(-c(Id,Descripcion)) %>% rename(Id = IndicadorId)
  
  in_react_frame <- reactiveVal(df)
  filtered_frame <-  reactive({
    frame <- req(in_react_frame())
    indexes <- req(input$table_rows_all)
    frame[indexes,]
  })
  #summarised_frame <- reactive({req(filtered_frame()) %>% group_by(Nombre) %>% summarize(Suma = sum(Valor))})
  summarised_frame <- reactive({req(filtered_frame())})
  output$table <- renderDT(
    in_react_frame(),
    options = list(
      pageLength = 3,
      autoWidth = F),
    filter = list(
      position = 'top',
      clear = F,
      plain = T
    ))
  
  output$fig <- renderPlotly({
    fig <- req(summarised_frame()) %>% plot_ly(x = ~Nombre, y = ~Suma)
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
      xaxis = list(dtick = "")
    )
  })
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

