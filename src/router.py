
from fastapi import APIRouter

from src.mandate_data import (get_mandate_data_router, post_mandate_data_router,
                           put_mandate_data_router, delete_mandate_data_router)

from src.meter_readings import (get_meter_readings_router, post_meter_readings_router,
                             put_meter_readings_router, delete_meter_readings_router)

from src.meter_data import (get_meter_data_router, post_meter_data_router,
                             put_meter_data_router, delete_meter_data_router)

api_router = APIRouter()

api_router.include_router(get_mandate_data_router)
api_router.include_router(post_mandate_data_router)
api_router.include_router(put_mandate_data_router)
api_router.include_router(delete_mandate_data_router)

api_router.include_router(get_meter_readings_router)
api_router.include_router(post_meter_readings_router)
api_router.include_router(put_meter_readings_router)
api_router.include_router(delete_meter_readings_router)

api_router.include_router(get_meter_data_router)
api_router.include_router(post_meter_data_router)
api_router.include_router(put_meter_data_router)
api_router.include_router(delete_meter_data_router)
