import pandas as pd
import streamlit as st
import numpy as np
import pymysql
import plotly.graph_objects as go
import plotly.express as px

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

# conexion a mysql y extracción de tablas
# con mysql_connection se crea un objeto "cursor" que permite realizar consultas
# con mysql_query se usa ese cursor para pedir una tabla. devuelve un df
from sqlquery import mysql_connection
from sqlquery import mysql_query_df

cursor = mysql_connection()

profesionals_data = mysql_query_df('profesionals_data',cursor)
insurance_clients = mysql_query_df('insurance_clients',cursor)

# --- FILTROS ---

st.sidebar.header('Filtros')

# sidebar bill
bill = st.sidebar.multiselect('Emite factura',
                                    options=profesionals_data['bill'].unique(),
                                    default=profesionals_data['bill'].unique()
                                    )
# query del filtro
profesionals_data=profesionals_data.query(
    'bill == @bill'
)


# -- ZONA KPI --

# total de trabajadores: medida
n_workers = profesionals_data['id'].count()

# total de clientes de seguros: medida
n_insurance_clients = insurance_clients['id'].count()

left, right = st.columns(2)
with left:
    st.markdown(f"<h5 style='text-align: center; color: black;'>Total de trabajadores: </h5> ", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: center; color: black;'>{n_workers}</h5>", unsafe_allow_html=True)

with right:
    st.markdown(f"<h5 style='text-align: center; color: black;'>Total de clientes de seguros: </h5> ", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: center; color: black;'>{n_insurance_clients}</h5>", unsafe_allow_html=True)




# -- TRABAJADORES POR CATEGORÍA GRÁFICO --
# agrupar profesionales por categoría
profesionals_per_category = profesionals_data['id'].groupby(profesionals_data['category_title']).count().sort_values(ascending=False).reset_index()
# recategorizar: si hay menos de 5, etiqueta como "Otra"
profesionals_per_category['recat_title'] = profesionals_per_category['category_title']
profesionals_per_category.loc[profesionals_per_category['id']<=5,'recat_title'] = 'Otra'
#ordenar
profesionals_per_category=profesionals_per_category.sort_values(by='id', ascending=False)

# dar un formato al gráfico
fig = px.bar(data_frame=profesionals_per_category,
             x='recat_title',
             y='id',
             orientation='v',
             title='Trabajadores por categoría',
             labels={
                'recat_title':'Categoría',
                'id':'Cantidad de trabajadores',
                'category_title':'Categoría'
             },
             color='recat_title',
             height=600,
             width=1300)
# plotear
st.plotly_chart(fig)

#columnas
left, right = st.columns(2)

with left:
    # -- BANCARIZADO SI NO --
    bank = profesionals_data['id'].groupby(profesionals_data['bank_account']).count().reset_index()
    fig = px.pie(data_frame=bank,
                names='bank_account',
                values='id',
                title='Trabajadores bancarizados',
                labels={'id':'Cantidad',
                        'bank_account':'Bancarizados'},
                width=600,
                height=400)
    st.plotly_chart(fig)

with right:
# -- POSEE SEGURO SI O NO --
    insurance = profesionals_data['id'].groupby(profesionals_data['insurance']).count().reset_index()
    fig = px.pie(data_frame=insurance,
                names='insurance',
                values='id',
                title='Trabajadores asegurados',
                labels={'id':'Cantidad',
                        'insurance':'Asegurados'},
                        width=600,
                        height=400)
    st.plotly_chart(fig)

 #trabajadores por rubro(X)
 #bancarizado SI O NO(X)
 #posee seguro SI O NO(X)
 # cotizaciones()
 # loggins()
 # preguntas contestadas()    

