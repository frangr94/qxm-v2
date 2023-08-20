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
# logo qxm centrado
a,b,c=st.columns(3)
with b:
    st.image('src/qxm_logo.png', use_column_width='always')

# conexion a mysql
# extraccion de tablas
cursor = mysql_connection()

daily_analytics = mysql_query_df('daily_analytics',cursor)


# --- FILTROS ---
st.sidebar.header('Filtros')
daily_analytics['year'] = pd.DatetimeIndex(daily_analytics['date']).year
# sidebar años
año = st.sidebar.select_slider('Años',
                                options=daily_analytics['year'].unique(),
                                value=max(daily_analytics['year'].unique())
                                )
# query del filtro
daily_analytics=daily_analytics.query(
    'year == @año'
)

# -- ZONA KPI --

# total de trabajadores: medida
n_registered_workers = daily_analytics['register_professionals'].sum()

# total de clientes de seguros: medida
n_budgets=daily_analytics['budgets'].sum()

left, right = st.columns(2)
with left:
    st.markdown(f"<h5 style='text-align: center; color: black;'>Total de trabajadores registrados: </h5> ", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: center; color: black;'>{n_registered_workers}</h5>", unsafe_allow_html=True)

with right:
    st.markdown(f"<h5 style='text-align: center; color: black;'>Total presupuestos realizados: </h5> ", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: center; color: black;'>{n_budgets}</h5>", unsafe_allow_html=True)

# -- ZONA GRAFICOS --
with left:

    # budgets (cotizaciones realizadas)
    fig = px.bar(data_frame=daily_analytics,
                x='date',
                y='budgets',
                orientation='v',
                title='Cotizaciones diarias',
                labels={
                    'date':'Fecha',
                    'budgets':'Cotizaciones',
                },
                height=600,
                width=600,
                )
    
    # plotear
    st.plotly_chart(fig)

with right:
    # register profesionals
    fig = px.bar(data_frame=daily_analytics,
                x='date',
                y='register_professionals',
                orientation='v',
                title='Trabajadores resgistrados por día',
                labels={
                    'date':'Fecha',
                    'register_professionals':'Profesionales registrados',
                },
                height=600,
                width=600)

    # plotear
    st.plotly_chart(fig)

with left:
    # register profesionals
    fig = px.bar(data_frame=daily_analytics,
                x='date',
                y='questions',
                orientation='v',
                title='Preguntas por día',
                labels={
                    'date':'Fecha',
                    'questions':'Preguntas',
                },
                height=600,
                width=600)
    # plotear
    st.plotly_chart(fig)

with right:
    # register profesionals
    fig = px.bar(data_frame=daily_analytics,
                x='date',
                y='answers',
                orientation='v',
                title='Respuestas por día',
                labels={
                    'date':'Fecha',
                    'answers':'Respuestas',
                },
                height=600,
                width=600)
    # plotear
    st.plotly_chart(fig)

# cantidad de loggins
# cantidad de preguntas contestadas 