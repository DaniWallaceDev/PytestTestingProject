from psycopg.rows import dict_row

from ..models import Response
from ..utils import db_connection

from fastapi import APIRouter

delete_mandate_data_router = APIRouter()

@delete_mandate_data_router.delete("/mandate_data/{mandate_id}")
async def delete_mandate_data_by_id(mandate_id : str) -> Response:
    conn = db_connection()
    cursor = conn.cursor(row_factory = dict_row)

    cursor.execute("SELECT * FROM mandate_data WHERE mandate_id = %s", (mandate_id,))
    data = cursor.fetchone()
    if not data:
        return Response(status_code=404, message="Not found error")

    cursor.execute("DELETE FROM mandate_data WHERE mandate_id = %s", (mandate_id,))
# mejor hacer un delete con filtros y usando indices investigarlo en lugar de incluir una id aunque ambas estan bien
    conn.commit()
    cursor.close()
    conn.close()

    return Response(status_code=200, message={"deleted_data": data})