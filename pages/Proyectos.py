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

projects = mysql_query_df('projects',cursor)
projects['year'] = pd.DatetimeIndex(projects['created_at']).year

project_budgets = mysql_query_df('project_budgets', cursor)
project_budgets['year'] = pd.DatetimeIndex(project_budgets['created_at']).year

categories = mysql_query_df('categories', cursor)
categories.rename(columns={'id':'category_id'},inplace=True)
categories=categories[['category_id','title']]

payments = mysql_query_df('payments', cursor)

projects = projects.join(categories, on='category_id',how="left",rsuffix='c_')

# -- FILTROS --
st.sidebar.header('Filtros')

# años
año = st.sidebar.slider('Años',
                        min_value=min(projects['year']),
                        max_value=max(projects['year']),
                        value=max(projects['year'])
                                )
# query del filtro
projects=projects.query(
    'year <= @año'
)

project_budgets=project_budgets.query(
    'year<=@año'
)

# deshabilitar selectbox
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

st.sidebar.checkbox("Disable selectbox widget", key="disabled")

# categorías
category = st.sidebar.selectbox('Seleccione una categoría',
                                projects['title'].unique(),
                                disabled=st.session_state.disabled)

projects = projects.query(
    'title == @category'
)

# -- ZONA KPI --

# total de proyectos
total_projects = projects['id'].count()
# promedio de cantidad de budget por project
avg_budget_quantity = np.mean(projects['budgets_count'])
# presupuesto promedio
avg_budget = np.mean(project_budgets['price'])


left, center, right = st.columns(3)

with left:
    st.markdown(f"<h5 style='text-align: center; color: black;'>Total de proyectos: </h5> ", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: center; color: black;'>{total_projects}</h5>", unsafe_allow_html=True)


with center:
    st.markdown(f"<h5 style='text-align: center; color: black;'>Promedio de presupuestos por proyecto: </h5> ", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: center; color: black;'>{round(avg_budget_quantity,2)}</h5>", unsafe_allow_html=True)

with right:
    st.markdown(f"<h5 style='text-align: center; color: black;'>Presupuesto promedio: </h5> ", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: center; color: black;'>${int(avg_budget)}</h5>", unsafe_allow_html=True)




left, right = st.columns(2)

with left:
    # total de proyectos
    yearly_projects=projects['id'].groupby(projects['year']).count().reset_index()
    fig = px.bar(data_frame=yearly_projects,
                x='year',
                y='id',
                orientation='v',
                title='Total de proyectos',
                width=600,
                height=600,
                labels={'id':'Total de proyectos',
                        'year':'Año'}
                )
    
    fig.update_xaxes(type='category')

    st.plotly_chart(fig)

import plotly.graph_objects as go

contracts = mysql_query_df('contracts',cursor)
contracts['year']=pd.DatetimeIndex(contracts['created_at']).year

with right:
    # proyectos y contratos por año
    yearly_contracts = contracts['uuid'].groupby(contracts['year']).count().reset_index()
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=yearly_contracts['year'],
                             y=yearly_contracts['uuid'],
                             name='Contratos'
                             ))
    fig.add_trace(go.Scatter(x=yearly_projects['year'],
                             y=yearly_projects['id'],
                             name='Proyectos'))
    fig.update_layout(
        title="Proyectos y contratos por año",
        xaxis_title="Año",
        yaxis_title="Contratos y proyectos por año",
        height=600,
        width=600)
    
    fig.update_xaxes(type='category')

    st.plotly_chart(fig)

payments['year'] = pd.DatetimeIndex(payments['created_at']).year
yearly_payments = payments['uuid'].groupby(payments['year']).count().reset_index()
with left:
    fig = px.bar(data_frame=yearly_payments,
                x='year',
                y='uuid',
                height=600,
                width=600,
                title='Pagos realizados por año',
                labels={'uuid':'Pagos realizados',
                'year':'Año'})
    st.plotly_chart(fig)

with right:
    fig=px.bar(data_frame=payments,
                x='year',
                y='price',
                height=600,
                width=600,
                title='Total en $ de pagos realizados',
                labels={'year':'Año',
                'price':'Total de pagos realizados en $'})
    st.plotly_chart(fig)
