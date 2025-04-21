from psycopg.rows import dict_row
from psycopg.types.json import Json

from src.models import Response, MeterReadings
from ..utils import db_connection

from fastapi import APIRouter

put_meter_readings_router = APIRouter()


@put_meter_readings_router.put("/meter_readings/{meter_readings_id}")
async def update_meter_readings_by_id(meter_readings_id : str, meter_readings : MeterReadings) -> Response:
    conn = db_connection()
    cursor = conn.cursor(row_factory = dict_row)

    cursor.execute("SELECT * FROM meter_readings WHERE meter_readings_id = %s", (meter_readings_id,))
    data = cursor.fetchone()
    if not data:
        return Response(status_code=404, message="Not found error")

    meter_readings_dict = meter_readings.model_dump()
    if meter_readings_dict.get("reading_electricity") is not None:
        meter_readings_dict["reading_electricity"] = Json(meter_readings_dict["reading_electricity"])
    if meter_readings_dict.get("reading_gas") is not None:
        meter_readings_dict["reading_gas"] = Json(meter_readings_dict["reading_gas"])
    if meter_readings_dict.get("rejection") is not None:
        meter_readings_dict["rejection"] = Json(meter_readings_dict["rejection"])

    values_tuple = tuple(meter_readings_dict.values())

    cursor.execute("""UPDATE meter_readings SET 
                    meter_number = %s,
                    account_id = %s,
                    connection_ean_code = %s,
                    energy_type = %s,
                    validation_status = %s,
                    reading_date = %s,
                    reading_electricity = %s,
                    reading_gas = %s,
                    rejection = %s,
                    brand = %s
                    WHERE meter_readings_id = %s""", values_tuple)

    conn.commit()
    cursor.close()
    conn.close()

    return Response(status_code=201, message={"updated_data": meter_readings_dict})