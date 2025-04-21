from psycopg.rows import dict_row

from src.models import Response, MandateData
from src.utils import db_connection

from fastapi import APIRouter

put_mandate_data_router = APIRouter()


@put_mandate_data_router.put("/mandate_data/{mandate_id}")
async def update_mandate_data_by_id(mandate_id : str, mandate_data : MandateData) -> Response:
    conn = db_connection()
    cursor = conn.cursor(row_factory = dict_row)

    cursor.execute("SELECT * FROM mandate_data WHERE mandate_id = %s", (mandate_id,))
    data = cursor.fetchone()
    if not data:
        return Response(status_code=404, message="Not found error")

    mandate_data_dict = mandate_data.model_dump()
    values_tuple = tuple(mandate_data_dict.values()) + (mandate_id,)
    cursor.execute("""UPDATE mandate_data SET 
                    mandate_id = %s,
                    business_partner_id = %s,
                    brand = %s,
                    mandate_status = %s,
                    collection_frequency = %s,
                    row_update_datetime = %s,
                    row_create_datetime = %s,
                    changed_by = %s,
                    collection_type = %s,
                    metering_consent = %s
                    WHERE mandate_id = %s""", values_tuple)

    conn.commit()
    cursor.close()
    conn.close()

    return Response(status_code=201, message={"updated_data": mandate_data_dict})