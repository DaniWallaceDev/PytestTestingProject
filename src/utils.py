import psycopg, logging
from psycopg import sql


logging.basicConfig(level = logging.INFO)
logger = logging.getLogger("db")

def db_connection() -> psycopg.connection:
    conn = psycopg.connect(
        "dbname=postgres host=localhost password=1234 user=postgres")

    if conn:
        logger.info("Successful connection")
        return conn
    else:
        logger.error("Connection error")
        return None

def generate_select_query(table_name, filters):
    """
    Genera una consulta SQL SELECT dinámica basada en los filtros deseados.

    Args:
        table_name (str): Nombre de la tabla.
        filters (dict): Diccionario con los nombres de las columnas y sus valores a filtrar.

    Return:
        tuple: Una tupla que contiene la consulta SQL y una lista de valores para los marcadores de posición.
    """
    # Construcción de la query SQL

    query = sql.SQL("SELECT * FROM {table} WHERE ").format(table=sql.Identifier(table_name))
    conditions = []
    values = []

    for column, value in filters.items():
        conditions.append(sql.SQL("{} = %s").format(sql.Identifier(column)))
        values.append(value)

    query += sql.SQL(" AND ").join(conditions)

    return query, values