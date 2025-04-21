from psycopg.rows import dict_row

from src.models import Response
from ..utils import db_connection

from fastapi import APIRouter

delete_meter_readings_router = APIRouter()

@delete_meter_readings_router.delete("/meter_readings/{meter_readings_id}")
async def delete_meter_readings_by_id(meter_readings_id : str) -> Response:
    conn = db_connection()
    cursor = conn.cursor(row_factory = dict_row)

    cursor.execute("SELECT * FROM meter_readings WHERE meter_readings_id = %s", (meter_readings_id,))
    data = cursor.fetchone()
    if not data:
        return Response(status_code=404, message="Not found error")

    cursor.execute("DELETE FROM meter_readings WHERE meter_readings_id = %s", (meter_readings_id,))
# mejor hacer un delete con filtros y usando indices investigarlo en lugar de incluir una id aunque ambas estan bien
    conn.commit()
    cursor.close()
    conn.close()

    return Response(status_code=200, message={"deleted_data": data})