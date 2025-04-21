from psycopg.rows import dict_row

from ..models import Response
from ..utils import db_connection

from fastapi import APIRouter

delete_meter_data_router = APIRouter()

@delete_meter_data_router.delete("/meter_data/{meter_data_id}")
async def delete_meter_data_by_id(meter_data_id : str) -> Response:
    conn = db_connection()
    cursor = conn.cursor(row_factory = dict_row)

    cursor.execute("SELECT * FROM meter_data WHERE meter_data_id = %s", (meter_data_id,))
    data = cursor.fetchone()
    if not data:
        return Response(status_code=404, message="Not found error")

    cursor.execute("DELETE FROM meter_data WHERE meter_data_id = %s", (meter_data_id,))
# mejor hacer un delete con filtros y usando indices investigarlo en lugar de incluir una id aunque ambas estan bien
    conn.commit()
    cursor.close()
    conn.close()

    return Response(status_code=200, message={"deleted_data": data})