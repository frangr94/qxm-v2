import pandas as pd
import streamlit as st
import numpy as np
import pymysql
import plotly.graph_objects as go
import json
import plotly.express as px

st.write('''## Registro Nacional de Trabajadores''')

from sqlquery import mysql_connection
from sqlquery import mysql_query_df


cursor = mysql_connection()


def load_selections():
    try:
        with open("selections.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_selections(selections):
    with open("selections.json", "w") as file:
        json.dump(selections, file)

st.title("Checklist")

# Lista de campos existentes y campos que necesitas pedir
all_fields = ["Nombre", "Apellido", "Fecha de Nacimiento", "Género", "Número de Identificación", "Correo", "Teléfono", "Provincia", "Código Postal", "Oficio", "Facturación", "Seguro Médico", "Seguro Laboral", "Cuenta Bancaria" ]

st.subheader("Selecciona los Campos")
selections = load_selections()

for campo in all_fields:
    selected = st.checkbox(campo, key=f"checked_{campo}", value=selections.get(campo, False))
    selections[campo] = selected

st.subheader("Campos Existentes")
for campo in all_fields:
    if selections.get(campo, False):
        ubicacion_key = f"ubicacion_{campo}"
        ubicacion = st.text_input(f"Ubicación de {campo}", key=ubicacion_key, value=selections.get(ubicacion_key, ""))
        selections[ubicacion_key] = ubicacion

save_selections(selections)

# Recopila campos seleccionados y no seleccionados
checked_fields = [campo for campo, selected in selections.items() if selected and not campo.startswith("ubicacion_")]
unchecked_fields = [campo for campo, selected in selections.items() if not selected and not campo.startswith("ubicacion_")]

st.subheader("Campos Necesarios")
st.table(unchecked_fields)

# Gráfico de porcentaje con Plotly
fig = px.pie(names=["Campos Existentes", "Campos Necesarios"], values=[len(checked_fields), len(unchecked_fields)], title="Porcentaje de Campos")
st.plotly_chart(fig)


# se le pasa el nombre de una tabla contenida en una base de datos a la cual se esta conectado
# devuelve un dataframe
def extraer_datos(tabla:str, columnas: list):
    # Generar la parte de la consulta SQL para seleccionar las columnas específicas
    columnas_sql = ', '.join(columnas)

    # Construir la consulta SQL completa
    consulta_sql = "SELECT {} FROM {}".format(columnas_sql, tabla)

    # Ejecutar la consulta SQL
    cursor.execute(consulta_sql)

    # Extraer y dar formato a las filas
    rows = cursor.fetchall()

    # Tomar headers de cada columna
    headers = [column[0] for column in cursor.description]

    # Crear DataFrame
    df = pd.DataFrame(rows, columns=headers)

    return df

# Lista de columnas que deseas seleccionar
columnas_seleccionadas = ["firstname", "lastname", "birthday", "sex", "email", "phone"]

# Tabla de la cual deseas extraer los datos
tabla_seleccionada = "users"

# Llamar a la función para obtener los datos con las columnas seleccionadas
profesionals_data = extraer_datos(tabla_seleccionada, columnas_seleccionadas)







if st.checkbox('Mostrar df'):
    st.dataframe(profesionals_data)

if st.checkbox('Vista de datos'):
    if st.button('Mostrar primeros datos'):
        st.write(profesionals_data.head())
    if st.button('Mostrar últimos datos'):
        st.write(profesionals_data.tail())

dim= st.radio('Dimensión:', ('Filas', 'Columnas'))

if dim== 'Filas':
    st.write('Cantidad de filas:', profesionals_data.shape [0])
else:
    st.write('Cantidad de columnas:', profesionals_data.shape[1])