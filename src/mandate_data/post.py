
from src.models import Response, MandateData
from ..utils import db_connection

from fastapi import APIRouter

post_mandate_data_router = APIRouter()


@post_mandate_data_router.post("/mandate_data/", response_model=Response)
async def post_mandate_data(mandate_data : MandateData):
    conn = db_connection()
    cursor = conn.cursor()

    mandate_data_dict = mandate_data.model_dump()
    if not mandate_data_dict:
        return Response(status_code=404, message="Not found error")

    values_tuple = tuple(mandate_data_dict.values())

    cursor.execute("""
        INSERT INTO mandate_data (
        mandate_id, business_partner_id, brand, mandate_status, collection_frequency, 
        row_update_datetime, row_create_datetime, changed_by, collection_type, metering_consent
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, values_tuple)

    conn.commit()
    cursor.close()
    conn.close()

    if mandate_data:
        return Response(status_code=201, message={"mandate_data": mandate_data.model_dump()})
    else:
        return Response(status_code=400, message="Not valid input data error")
