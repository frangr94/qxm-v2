import pandas as pd
import streamlit as st
import numpy as np

# Acá se pueden proveer opciones de configuración para la página
st.set_page_config(page_title='Home',
                    page_icon=':bar_chart:',
                    layout='wide',
                    initial_sidebar_state='collapsed'
                    )


# Carga el archivo CSS personalizado
st.markdown('<link href="styles.css" rel="stylesheet">', unsafe_allow_html=True)

# Encabezado con logo y título
col1, col2 = st.columns([2, 8])
with col1:
    st.image('src/qxm_logo.png', width=200)
with col2:
    st.markdown(
        '<div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center; height: 100%;">'
        '<h1 style="font-style: italic; color: #1F77B4; margin-top: 50px; margin-left: 135px; text-align: left;">Departamento de Data</h1>'
        '</div>',
        unsafe_allow_html=True
    )
# Introducción
st.write('''
## Proyecto de Data Analytics para QXM

¡Bienvenidos al Departamento de Data de QXM! En este proyecto, estamos trabajando en el análisis y visualización de datos para brindar información valiosa y ayudar a tomar decisiones informadas. Nuestro objetivo es optimizar la toma de decisiones y generar insights relevantes para mejorar la inclusión laboral de los trabajadores de oficios.

### Objetivos
- Creación de un ***algoritmo transparente*** y aplicable para los trabajadores de QXM.
- Establecimiento de un Departamento de Data para analizar y procesar los datos acumulados.
- Generación de proyecciones para impulsar el crecimiento de QXM y proporcionar información valiosa a organismos públicos y privados.
- Creación de un ***Registro Nacional de Trabajadores de Oficios*** para facilitar la planificación y el análisis del sector.
''')
st.write('''
### Métricas y Análisis
''')

# Menús desplegables para cada sección
with st.expander("***Clientes***"):
    st.write("- Distribución por rubro.")
    st.write("- Distribución por condiciones: Emite factura o no, está bancarizado o no, posee seguro contratado o no.")
    st.write("- Métricas de actividad: Cotizaciones realizadas, cantidad de logins, cantidad de preguntas contestadas.")

with st.expander("***Métricas de Actividad***"):
    st.write("- Cotizaciones realizadas.")
    st.write("- Cantidad de profesionales registrados.")
    st.write("- Cantidad de preguntas y respuestas.")

with st.expander("***Proyectos***"):
    st.write("- Total de proyectos por año.")
    st.write("- Total de contratos por año.")
    st.write("- Total de pagos realizados por año.")

with st.expander("***Trabajadores***"):
    st.write("- Total de trabajadores registrados.")
    st.write("- Total de clientes de seguros.")
    st.write("- Trabajadores por categoría.")
    st.write("- Trabajadores bancarizados y asegurados.")

st.write('''
### Tableros de Métricas
Nuestro equipo ha desarrollado una serie de tableros interactivos para visualizar y analizar los datos en tiempo real. Estos tableros incluyen métricas sobre trabajadores, clientes, proyectos y actividad diaria.

Estamos emocionados de presentar los avances y resultados de nuestro trabajo. ¡Explora los tableros y descubre información valiosa para el crecimiento y desarrollo de QXM!
''')
st.write('''
''')
st.write('''
''')
st.write('''
***¡Gracias por su visita!***
''')


