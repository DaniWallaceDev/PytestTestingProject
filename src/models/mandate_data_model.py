from datetime import datetime

from pydantic import BaseModel

class MandateData(BaseModel):
    mandate_id : str
    business_partner_id : str
    brand: str
    mandate_status : str
    collection_frequency: str
    row_update_datetime : datetime
    row_create_datetime: datetime
    changed_by: str
    collection_type: str
    metering_consent: str