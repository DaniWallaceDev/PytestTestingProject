from datetime import datetime

from pydantic import BaseModel

class ReadingElectricity(BaseModel):
    supplyLow: float
    supplyHigh: float
    returnLow: float
    returnHigh: float

class ReadingGas(BaseModel):
    gasTotal: float

class Rejection(BaseModel):
    code: str
    reason: str

class MeterReadings(BaseModel):
    meter_number : str
    account_id : str
    connection_ean_code : str
    energy_type : str
    validation_status : str
    reading_date : datetime
    reading_electricity : ReadingElectricity|None
    reading_gas : ReadingGas|None
    rejection : Rejection|None
    brand : str

