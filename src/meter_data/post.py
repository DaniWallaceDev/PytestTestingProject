
from src.models import Response, MeterData
from ..utils import db_connection

from fastapi import APIRouter

post_meter_data_router = APIRouter()


@post_meter_data_router.post("/meter_data/", response_model=Response)
async def post_meter_data(meter_data : MeterData):
    conn = db_connection()
    cursor = conn.cursor()

    meter_data_dict = meter_data.model_dump()
    if not meter_data_dict:
        return Response(status_code=404, message="Not found error")

    values_tuple = tuple(meter_data_dict.values())

    cursor.execute("""
        INSERT INTO meter_data (
        business_partner_id, connection_ean_code, grid_company_code, oda_code, meter_number, 
        smart_collectable, brand, sjv1, sjv2, installation, division, move_out_date,
        row_create_datetime, move_in_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, values_tuple)

    conn.commit()
    cursor.close()
    conn.close()

    if meter_data:
        return Response(status_code=201, message={"meter_data": meter_data.model_dump()})
    else:
        return Response(status_code=400, message="Not valid input data error")
