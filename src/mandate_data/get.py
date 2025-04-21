from psycopg.rows import dict_row

from ..models import Response
from ..utils import db_connection

from fastapi import APIRouter
import logging


get_mandate_data_router = APIRouter()

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger("get-meter-data")

@get_mandate_data_router.get("/mandate_data/{mandate_id}")
async def get_mandate_data_by_id(mandate_id : str) -> Response:
    with db_connection() as conn:
        with conn.cursor(row_factory = dict_row) as cursor:
            cursor.execute("SELECT * FROM mandate_data WHERE mandate_id = %s", (mandate_id,))
            data = cursor.fetchall()

            if not data:
                logger.warning("No data found")
                return Response(status_code=404, message="Not found error")
            logger.info("Data successfully retrieved")
            return Response(status_code=200, message={"mandate_data": data})

@get_mandate_data_router.get("/mandate_data/{row_update_datetime}")
async def get_mandate_data_by_update_datetime(row_update_datetime : str) -> Response:
    with db_connection() as conn:
        with conn.cursor(row_factory = dict_row) as cursor:
            cursor.execute('SELECT * FROM mandate_data WHERE row_update_datetime = %s', (row_update_datetime,))
            data = cursor.fetchall()

            if not data:
                logger.warning("No data found")
                return Response(status_code=404, message="Not found error")
            logger.info("Data successfully retrieved")
            return Response(status_code=200, message={"mandate_data": data})

@get_mandate_data_router.get("/mandate_data/{business_partner_id}")
async def get_mandate_data_by_business_partner_id(business_partner_id : str) -> Response:
    with db_connection() as conn:
        with conn.cursor(row_factory = dict_row) as cursor:
            cursor.execute('SELECT * FROM mandate_data WHERE business_partner_id = %s', (business_partner_id,))
            data = cursor.fetchall()

            if not data:
                logger.warning("No data found for ")
                return Response(status_code=404, message="Not found error")
            logger.info("Data successfully retrieved")
            return Response(status_code=200, message={"mandate_data": data})

@get_mandate_data_router.get("/mandate_data/")
async def get_mandate_data_by_params(row_update_datetime: str, business_partner_id: str) -> Response:
    with db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            query = """
                SELECT * FROM mandate_data 
                WHERE row_update_datetime = %s AND business_partner_id = %s
            """
            cursor.execute(query, (row_update_datetime, business_partner_id))
            data = cursor.fetchall()

            if not data:
                logger.warning("No data found for row_update_datetime: %s and business_partner_id: %s", row_update_datetime, business_partner_id)
                return Response(status_code=404, message="Not found error")

            logger.info("Data successfully retrieved for row_update_datetime: %s and business_partner_id: %s", row_update_datetime, business_partner_id)
            return Response(status_code=200, message={"mandate_data": data})
