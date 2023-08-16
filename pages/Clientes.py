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




# conexion a mysql
# extraccion de tablas
cursor = mysql_connection()

presupuestos_contratados=mysql_query_df('presupuestos_contratados',cursor)
#st.write(presupuestos_contratados)

mapeo = {0: "No", 1: "Si"}

presupuestos_contratados['bill'] = presupuestos_contratados['bill'].replace(mapeo)
presupuestos_contratados['insurance'] = presupuestos_contratados['insurance'].replace(mapeo)

st.write('''## Estadísticas sobre servicios contratados''')

# --- FILTROS ---
st.sidebar.header('Filtros')


# filtro factura

opciones_factura = presupuestos_contratados['bill'].unique()
factura_predeterminada = opciones_factura[0] if len(opciones_factura) > 0 else None

bill = st.sidebar.radio('Emite factura',
                           options=opciones_factura,
                           index=0,
                           help="Selecciona una opción de factura"
                          )




# filtro seguro contratado

opciones_seguro = presupuestos_contratados['insurance'].unique()
seguro_predeterminado = opciones_seguro[0] if len(opciones_seguro) > 0 else None

insurance = st.sidebar.radio('Contrata seguro',
                           options=opciones_seguro,
                           index=0,
                           help="Selecciona una opción de seguro"
                          )


presupuestos_contratados_filtro=presupuestos_contratados.query(
    'bill == @bill & insurance == @insurance'
)


contracts_per_category = presupuestos_contratados_filtro.groupby('title')['id'].count().sort_values(ascending=False).head(10).reset_index()
#st.write(contracts_per_category)


profesionals_data=mysql_query_df('profesionals_data',cursor)
#st.write(profesionals_data)
df = profesionals_data

# Agrupar por 'category_title' y 'bill' y contar
grouped_data = df.groupby(["category_title", "bill"]).size().reset_index(name="count")
#st.write(grouped_data)

# dividir la página en dos columnas
left, right = st.columns(2)
with left:    
    # dar un formato al gráfico
    

    layout = go.Layout(
        title='Cantidad de Servicios Contratados',
        xaxis=dict(title='n_trabajos'),
        yaxis=dict(title='categoría'),
        width=800,
        height=600
    )
    fig = go.Figure(data=go.Bar(
            y=contracts_per_category["title"],
            x=contracts_per_category["id"],
            orientation='h'
            ),layout=layout)
        
        # plotear
    st.plotly_chart(fig)

    


    df = presupuestos_contratados


# preparo df para graficar
df = presupuestos_contratados
df.head()
df2 = df[["price","title"]]
df2.loc[6, 'price'] = 25000


# Agrupar por la columna 'title' y calcular el precio promedio
average_prices = df2.groupby('title')['price'].mean().reset_index()

# Renombrar la columna 'price' para reflejar que contiene el precio promedio
average_prices.rename(columns={'price': 'average_price'}, inplace=True)

# Agrupar por la columna 'title' y calcular el precio promedio
total_prices = df2.groupby('title')['price'].sum().reset_index()

# Renombrar la columna 'price' para reflejar que contiene el precio promedio
total_prices.rename(columns={'price': 'total'}, inplace=True)
    
# Crear gráfico con Plotly
with right:    
    # dar un formato al gráfico
    

    
    fig = go.Figure(data=go.Bar(
        x=average_prices["title"],
        y=average_prices["average_price"],
        marker=dict(color='rgba(58, 71, 80, 0.6)',
        line=dict(color='rgba(58, 71, 80, 1.0)', width=1)),
        name='Valores',
        ))
    
    fig.update_layout(
        title="Precio Promedio por categoría",
        xaxis_title="categoría",
        yaxis_title="",
        height=600,
        width=600
        )

        
        # plotear
    st.plotly_chart(fig)

with left:
# Crear gráfico con Plotly
    fig = go.Figure(data=go.Bar(
        x=total_prices["title"],
        y=total_prices["total"],
        marker=dict(color='rgba(58, 71, 80, 0.6)',
        line=dict(color='rgba(58, 71, 80, 1.0)', width=1)),
        name='Valores'
        
        ))

# Agregar título al gráfico
    fig.update_layout(
        title="Total contratado por categoría",
        xaxis_title="Categoría",
        yaxis_title="",
        height=600,
        width=600)
    
    
        
        # plotear
    st.plotly_chart(fig)


projects_view=mysql_query_df('projects_view',cursor)
    # Filtro por categoría
selected_category = st.sidebar.selectbox("Seleccione una categoría", projects_view["category_title"].unique())

    

    # Filtrar los datos por categoría seleccionada
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

with right:
    # Crear el gráfico de torta
    fig = px.pie(df_pie, values="Cantidad", names="Contrato", title=f"Porcentaje de proyectos con/sin contrato {selected_category}",width=600,height=600)
    st.plotly_chart(fig)