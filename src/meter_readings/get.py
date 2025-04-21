from psycopg.rows import dict_row

from src.models import Response
from ..utils import db_connection

from fastapi import APIRouter
import logging

get_meter_readings_router = APIRouter()

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger("get-meter-data")

@get_meter_readings_router.get("/meter_readings/{meter_readings_id}")
async def get_meter_readings_by_id(meter_readings_id : str) -> Response:
    with db_connection() as conn:
        with conn.cursor(row_factory = dict_row) as cursor:
            cursor.execute("SELECT * FROM meter_readings WHERE meter_readings_id = %s", (meter_readings_id,))
            data = cursor.fetchall()

            if not data:
                logger.warning("No data found")
                return Response(status_code=404, message="Not found error")
            logger.info("Data successfully retrieved")
            return Response(status_code=200, message={"meter_readings": data})

@get_meter_readings_router.get("/meter_readings/{connection_ean_code}")
async def get_meter_readings_by_conn_ean_code(connection_ean_code : str) -> Response:
    with db_connection() as conn:
        with conn.cursor(row_factory = dict_row) as cursor:
            cursor.execute('SELECT * FROM meter_readings WHERE connection_ean_code = %s', (connection_ean_code,))
            data = cursor.fetchall()

            if not data:
                logger.warning("No data found")
                return Response(status_code=404, message="Not found error")
            logger.info("Data successfully retrieved")
            return Response(status_code=200, message={"meter_readings": data})

@get_meter_readings_router.get("/meter_readings/{meter_number}")
async def get_meter_readings_by_meter_number(meter_number : str) -> Response:
    with db_connection() as conn:
        with conn.cursor(row_factory = dict_row) as cursor:
            cursor.execute('SELECT * FROM meter_readings WHERE meter_number = %s', (meter_number,))
            data = cursor.fetchall()

            if not data:
                logger.warning("No data found for ")
                return Response(status_code=404, message="Not found error")
            logger.info("Data successfully retrieved")
            return Response(status_code=200, message={"meter_readings": data})

@get_meter_readings_router.get("/meter_readings/")
async def get_meter_readings_by_params(connection_ean_code: str, meter_number: str) -> Response:
    with db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            query = """
                SELECT * FROM meter_readings 
                WHERE connection_ean_code = %s AND meter_number = %s
            """
            cursor.execute(query, (connection_ean_code, meter_number))
            data = cursor.fetchall()

            if not data:
                logger.warning("No data found for connection_ean_code: %s and meter_number: %s", connection_ean_code, meter_number)
                return Response(status_code=404, message="Not found error")

            logger.info("Data successfully retrieved for connection_ean_code: %s and meter_number: %s", connection_ean_code, meter_number)
            return Response(status_code=200, message={"meter_readings": data})