# -- FUNCIONES PARA CONEXION Y CONSULTA --

# se dan parámetros para conectarse a una base de datos usando con_data.txt
# devuelve un "cursor"
import pymysql
def mysql_connection():
    # crear lista donde se guardan las credenciales !!
    cred=[]

    # abrir con_data.txt y leer linea a linea
    with open ('con_data.txt') as f:
        for line in f:
            # ingresar credenciales a lista
            cred.append(line.strip())
    # conectarse a bbdd con pymysql
    conexion = pymysql.connect(host=cred[0],
                            database = cred[1],
                            user= cred[2],
                            password=cred[3])
    # crear objeto cursor (permite realizar queries MYSQL a la base de datos)
    cursor = conexion.cursor()

    return cursor

# se le da un nombre de tabla y un objeto cursor y retorna un dataframe
import pandas as pd
def mysql_query_df(tabla:str,cursor):

    # dependencias

    # seleccionar todos los datos de la tabla
    cursor.execute("SELECT * FROM {}".format(tabla))

    # extraer y dar formato de filas
    rows = cursor.fetchall()

    # tomar headers de cada columna
    headers = [column[0] for column in cursor.description]

    # crear dataframe
    df = pd.DataFrame(rows, columns=headers)

    return df