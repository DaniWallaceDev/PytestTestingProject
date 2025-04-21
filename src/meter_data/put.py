from psycopg.rows import dict_row

from src.models import Response, MeterData
from src.utils import db_connection

from fastapi import APIRouter

put_meter_data_router = APIRouter()

# cambiar a with conn

@put_meter_data_router.put("/meter_data/{meter_data_id}")
async def update_meter_data_by_id(meter_data_id : str, meter_data : MeterData) -> Response:
    conn = db_connection()
    cursor = conn.cursor(row_factory = dict_row)

    cursor.execute("SELECT * FROM meter_data WHERE meter_data_id = %s", (meter_data_id,))
    data = cursor.fetchone()
    if not data:
        return Response(status_code=404, message="Not found error")

    meter_data_dict = meter_data.model_dump()
    values_tuple = tuple(meter_data_dict.values()) + (meter_data_id,)
    cursor.execute("""UPDATE meter_data SET 
                    business_partner_id = %s,
                    connection_ean_code = %s,
                    grid_company_code = %s,
                    oda_code = %s,
                    meter_number = %s,
                    smart_collectable = %s,
                    brand = %s,
                    sjv1 = %s,
                    sjv2 = %s,
                    installation = %s
                    division = %s,
                    move_out_date = %s,
                    row_create_datetime = %s,
                    move_in_date = %s
                    WHERE meter_data_id = %s""", values_tuple)

    conn.commit()
    cursor.close()
    conn.close()

    return Response(status_code=201, message={"updated_data": meter_data_dict})