from datetime import datetime

from pydantic import BaseModel


class MeterData(BaseModel):
    business_partner_id : str
    connection_ean_code : str
    grid_company_code : str
    oda_code : str
    meter_number : str
    smart_collectable : str
    brand : str
    sjv1 : float
    sjv2: float
    installation : str
    division : str
    move_out_date : datetime
    row_create_datetime : datetime
    move_in_date : datetime
