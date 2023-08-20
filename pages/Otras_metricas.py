import pandas as pd
import streamlit as st
import numpy as np
import pymysql
import plotly.graph_objects as go
import plotly.express as px

from sqlquery import mysql_connection
from sqlquery import mysql_query_df




# configuracion de página
st.set_page_config(page_title='Home',
                    page_icon=':bar_chart:',
                    layout='wide',
                    initial_sidebar_state='collapsed'
                    )

a,b,c=st.columns(3)
with b:
    st.image('src/qxm_logo.png', use_column_width='always')


st.write('''## Graficos varios Seba''')

# conexion a mysql
cursor = mysql_connection()

# VARIACION GLOBAL PROMEDIO DE LOS BUDGETS

# Extraigo tablas projects, categories y projects_budgets y le cambio el nombre a columnas id de las primeras dos tablas para el merge

projects=mysql_query_df('projects',cursor)
projects.rename(columns={'id': 'project_id'}, inplace=True)
categories=mysql_query_df('categories',cursor)
categories.rename(columns={'id': 'category_id'}, inplace=True)
project_budgets=mysql_query_df('project_budgets',cursor)

#Hago el merge

df = project_budgets.merge(projects, on='project_id', how='inner')
df2 = df.merge(categories, on='category_id', how='inner')
df2 = df2[["project_id","price","title"]]

# Calcula el promedio de price para cada project_id
df2['average_price'] = df2.groupby('project_id')['price'].transform('mean')

# Redondea la columna 'average_price' a dos decimales
df2['average_price'] = df2['average_price'].round(2)

# Agrego columna con variación relativa de cada cotización"

df2["variacion_relativa"] = abs(df2["price"]-df2["average_price"])/df2["average_price"]

# Agrego una columna donde calcula la variación relativa promedio de cada project

df2["var_rel_prom"] = ((df2.groupby('project_id')['variacion_relativa'].transform('mean'))*100).round(2)

# agrupo por project

df3 = df2.groupby(["project_id", "title"])["var_rel_prom"].mean().reset_index()

# agrupo para tener cada project con su variación relativa

grouped_df = df3.groupby("title")["var_rel_prom"].mean().reset_index()


    # dar un formato al gráfico
    
fig = px.bar(grouped_df, x="var_rel_prom", y="title", orientation='h', title="Media Global de las variaciones en Budgets")

fig.update_xaxes(title_text="Variación relativa (%)")
fig.update_yaxes(title_text="Categoría")

        # plotear
st.plotly_chart(fig)

st.write('''#### Con estas métricas intento calcular cuanto varían en promedio los budgets para cada categoría. Para eso saqué una variación relativa de los budgets de cada proyecto, luego los agrupé por categoría y saqué un promedio de esas variaciones. ''')

# PORCENTAJE DE PROJECTS CON Y SIN CONTRACTS

projects_view=mysql_query_df('projects_view',cursor)


# Obtén las categorías únicas del DataFrame projects_view
categories = projects_view["category_title"].unique()

# Agrega un checkbox para desactivar el filtro
reset_filter = st.sidebar.checkbox("Desactivar filtro")

if reset_filter:
    # Si el checkbox está marcado, no se aplica ningún filtro
    filtered_data = projects_view
else:
    # Si el checkbox no está marcado, muestra el selectbox y filtra los datos
    selected_category = st.sidebar.selectbox("Seleccione una categoría", categories)
    filtered_data = projects_view[projects_view["category_title"] == selected_category]


# Contar la cantidad de proyectos con y sin contrato
count_has_contract = filtered_data[filtered_data["has_contract"] == "Si"]["project_id"].count()
count_no_contract = filtered_data[filtered_data["has_contract"] == "No"]["project_id"].count()

# Crear un DataFrame para el gráfico
data = {
    "Contrato": ["Con contrato", "Sin contrato"],
    "Cantidad": [count_has_contract, count_no_contract]
}
df_pie = pd.DataFrame(data)

left, right = st.columns(2)

with left:
    # Crear el gráfico de torta
    # Definir el título del gráfico
    if reset_filter:
        title = "Porcentaje de proyectos con/sin contrato"
    else:
        title = f"Porcentaje de proyectos con/sin contrato {selected_category}"

    fig = px.pie(df_pie, values="Cantidad", names="Contrato", title=title,width=600,height=600)
    st.plotly_chart(fig)


# PIE CON PORCENTAJE DE PROJECTS CON REBUDGET

# Extraigo tablas projects, categories y projects_budgets y le cambio el nombre a columnas id de las primeras dos tablas para el merge

projects=mysql_query_df('projects',cursor)
projects.rename(columns={'id': 'project_id'}, inplace=True)
categories=mysql_query_df('categories',cursor)
categories.rename(columns={'id': 'category_id'}, inplace=True)
project_rebudgets=mysql_query_df('project_rebudgets',cursor)
project_rebudgets.rename(columns={'price': 'rebudget'}, inplace=True)

#Hago el merge

df = pd.merge(projects, categories, on='category_id', how='left')
df = df[["project_id","title"]]

# Crear una columna "rebudget" con valores por defecto "No"
df["rebudget"] = "No"

# Filtrar los project_ids que están en la tabla projects_rebudgets
rebudget_project_ids = set(project_rebudgets["project_id"].unique())

# Actualizar la columna "rebudget" a "Si" para los project_ids que están en la tabla projects_rebudgets
df.loc[df["project_id"].isin(rebudget_project_ids), "rebudget"] = "Si"


# Agrupar por título y rebudget y contar la cantidad de proyectos en cada grupo
grouped = df.groupby(["title", "rebudget"])["project_id"].count().reset_index()
grouped.columns = ["title", "rebudget", "project_count"]



if reset_filter:
    filtered_data = grouped
else:
    filtered_data = grouped[grouped["title"] == selected_category]

# Calcular la cantidad de proyectos con y sin rebudget
rebudget_counts = filtered_data["rebudget"].value_counts()

# Definir el título del gráfico
if reset_filter:
        title = "Porcentaje de proyectos con/sin rebudget"
else:
        title = f"Porcentaje de proyectos con/sin rebudget {selected_category}"

# Crear el gráfico de pastel

fig = px.pie(rebudget_counts, values=rebudget_counts.values, names=rebudget_counts.index, 
             title=title,width=600,height=600)
with right:             
    # Mostrar el gráfico
    st.plotly_chart(fig)


# CANTIDAD DE DIAS ENTRE PROJECT Y CONTRACT

# Extraigo tablas projects, categories y contracts, modifico nombres de columnas y hago merge para obtener project_id, title y las fechas de creación del project y del contract

projects=mysql_query_df('projects',cursor)
projects.rename(columns={'id': 'project_id'}, inplace=True)
projects.rename(columns={'created_at': 'created_at_project'}, inplace=True)
categories=mysql_query_df('categories',cursor)
categories.rename(columns={'id': 'category_id'}, inplace=True)
categories = categories[["category_id","title"]]
contracts=mysql_query_df('contracts',cursor)
contracts.rename(columns={'created_at': 'created_at_contract'}, inplace=True)
contracts = contracts[["project_id","created_at_contract"]]

#Hago el merge

df = pd.merge(projects, categories, on='category_id', how='left')
df = df[["project_id","title","created_at_project"]]
df2 = pd.merge(contracts, df, on='project_id', how='inner')

#calculo cantidad de días entre project y contract

df2["dias"] = (df2["created_at_contract"] - df2["created_at_project"]).dt.days

# agrupo por categoría de acuerdo al promedio de días entre contract y project
grouped_days = df2.groupby(["title"])["dias"].mean().reset_index()
grouped_days.columns = ["title", "dias"]


fig = px.bar(grouped_days, x="dias", y="title", orientation='h', title="Cantidad de días entre project y contract")

fig.update_xaxes(title_text="días")
fig.update_yaxes(title_text="Categoría")

        
        # plotear
st.plotly_chart(fig)







