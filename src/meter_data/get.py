from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from psycopg.rows import dict_row
from ..models.response import Response
from ..utils import db_connection, generate_select_query
from fastapi import APIRouter
import logging

get_meter_data_router = APIRouter()
logger = logging.getLogger("get-meter-data")


@get_meter_data_router.get("/meter_data/")
async def get_meter_data(
    connection_ean_code: str = None,
    business_partner_id: str = None,
    meter_data_id: str = None
):
    try:
        filters = {}
        if meter_data_id:
            filters["meter_data_id"] = meter_data_id
        if connection_ean_code:
            filters["connection_ean_code"] = connection_ean_code
        if business_partner_id:
            filters["business_partner_id"] = business_partner_id

        if not filters:
            logger.warning("No filters provided")
            resp = Response(
                status_code=400,
                message="At least one filter must be provided"
            )
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder(resp.model_dump())
            )

        query, values = generate_select_query("meter_data", filters)

        with db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, values)
                data = cursor.fetchall()

                if not data:
                    logger.warning("No data found for filters: %s", filters)
                    resp = Response(
                        status_code=404,
                        message="Not found error"
                    )
                    return JSONResponse(
                        status_code=404,
                        content=jsonable_encoder(resp.model_dump())
                    )

                logger.info("Data successfully retrieved for filters: %s", filters)
                resp = Response(
                    status_code=200,
                    message={"meter_data": data}
                )
                return JSONResponse(
                    status_code=200,
                    content=jsonable_encoder(resp.model_dump())
                )

    except Exception as e:
        logger.error(f"An error occurred in {e}")
        resp = Response(
            status_code=500,
            message="An internal error occurred in get_meter_data function"
        )
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(resp.model_dump())
        )
