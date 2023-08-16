# Dashboards QXM

### Instrucciones de uso:

1) Clonar repositorio:

        $ git clone https://github.com/frangr94/qxm-v2.git

2) Instalar dependencias en el entorno virtual deseado:
        
        $ cd qxm-dashboards
        $ pip install -r requirements.txt

3) Abrir editor de MYSQL y ejecutar _vistas_script.sql_ (solo la primera vez)

4) Crear archivo con el nombre "con_data.txt" e introducir los datos de la conexión para pymysql:

        $ touch con_data.txt

5) Abrir con_data.txt y proveer información usando el mismo formato. Guardar:
        
        host
        database
        user
        password

5) Ejecutar Home.py:
        
        $ streamlit run Home.py
