# Ejecutar en terminal: python -m pip install requests mysql-connector-Python
import requests, mysql.connector

# Setup de conexion a la bbdd
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sasa",
    database="db_lab4tp2"
)

cursor = db.cursor()


for i in range(1, 301):

    try:
        # Conseguimos el json de la url
        data = requests.get(f'https://restcountries.eu/rest/v2/callingcode/{i}').json()[0]

        # Buscamos si ya hay una entrada en la bbdd
        cursor.execute(f"select * from pais where codigoPais = {i}")
        result = cursor.fetchall()

        if not result:

            # Si no la hay, la creamos
            print(f"El codigo {i} no se encuentra en la bbdd, insertando...")
            query = "INSERT INTO pais (" \
                    "codigoPais, nombrePais, capitalPais, region, poblacion, latitud, longitud) " \
                    """VALUES ({},"{}","{}","{}",{},{},{})""".format(i, data["name"], data["capital"], data["region"],
                                                                 data["population"], data["latlng"][0],
                                                                 data["latlng"][1])

            cursor.execute(query)

            db.commit()

        else:

            # Si la hay, la actualizamos
            print(f"El codigo {i} ya se encuentra en la bbdd, actualizando...")
            query = "UPDATE pais SET " \
                    """nombrePais = "{}", capitalPais = "{}", region = "{}", poblacion = {}, """ \
                    "latitud = {}, longitud = {} WHERE codigoPais= {}".format(
                data["name"], data["capital"], data["region"], data["population"],
                data["latlng"][0], data["latlng"][1], i)

            cursor.execute(query)

            db.commit()
    except KeyError:
        print(f"El código {i} no existe en restcountries")
    except Exception as ex:
        print(ex)
