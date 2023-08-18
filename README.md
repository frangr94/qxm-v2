# Dashboards QXM

### Instrucciones de uso:

1) Clonar repositorio:

        $ git clone https://github.com/frangr94/qxm-v2.git

2) Instalar dependencias en el entorno virtual deseado:
        
        $ cd qxm-v2
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

6) Opcional: si se desea cambiar colores de acento, fondo, etc se puede acceder al archivo _config.toml_. Por ejemplo:

        $ cd .streamlit/config.toml

        [theme]
        primaryColor="#F63366"
        backgroundColor="#FFFFFF"
        secondaryBackgroundColor="#F0F2F6"
        textColor="#262730"
        font="sans serif"

        # Nota: utiliza hexcolor


