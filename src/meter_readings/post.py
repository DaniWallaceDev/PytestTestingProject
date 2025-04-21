from psycopg.types.json import Json

from src.models import Response, MeterReadings
from ..utils import db_connection

from fastapi import APIRouter

post_meter_readings_router = APIRouter()

@post_meter_readings_router.post("/meter_readings/", response_model=Response)
async def post_meter_reading(meter_readings : MeterReadings):
    conn = db_connection()
    cursor = conn.cursor()

    meter_readings_dict = meter_readings.model_dump()
    if meter_readings_dict.get("reading_electricity") is not None:
        meter_readings_dict["reading_electricity"] = Json(meter_readings_dict["reading_electricity"])
    if meter_readings_dict.get("reading_gas") is not None:
        meter_readings_dict["reading_gas"] = Json(meter_readings_dict["reading_gas"])
    if meter_readings_dict.get("rejection") is not None:
        meter_readings_dict["rejection"] = Json(meter_readings_dict["rejection"])

    values_tuple = tuple(meter_readings_dict.values())

    cursor.execute("""
        INSERT INTO meter_readings (
        meter_number, account_id, connection_ean_code, energy_type, validation_status, 
        reading_date, reading_electricity, reading_gas, rejection, brand
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, values_tuple)

    conn.commit()
    cursor.close()
    conn.close()

    if meter_readings:
        return Response(status_code=201, message={"meter_readings": meter_readings.model_dump()})
    else:
        return Response(status_code=400, message="Not valid input data error")