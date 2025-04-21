import pytest
from fastapi.testclient import TestClient
from main import app
# ya que db_connection se importa en get.py, no es necesario volver a importar utils aquí.
# pero si lo haces, lo usamos solo para tener la clase FakeConnection.
import src.utils as utils

client = TestClient(app)

fake_data = [
    {
        "business_partner_id": "01078462",
        "connection_ean_code": "87160008222122",
        "grid_company_code": "8716948000003",
        "oda_code": "8712423026766",
        "meter_number": "000000000000051018",
        "smart_collectable": "1",
        "brand": "ES",
        "sjv1": 614.00000000,
        "sjv2": 629.00000000,
        "installation": "0800196933",
        "division": "01",
        "move_out_date": "2024-10-01 00:00:00",
        "row_create_datetime": "2024-08-09 07:38:07",
        "move_in_date": "2023-10-02 00:00:00"
    },
    {
        "business_partner_id": "01005462",
        "connection_ean_code": "87160039905315",
        "grid_company_code": "8716948000003",
        "oda_code": "8712423026766",
        "meter_number": "000000000041391017",
        "smart_collectable": "1",
        "brand": "ES",
        "sjv1": 717.00000000,
        "sjv2": None,
        "installation": "0800196938",
        "division": "02",
        "move_out_date": "2024-10-01 00:00:00",
        "row_create_datetime": "2024-08-09 07:38:07",
        "move_in_date": "2023-10-02 00:00:00"
    }
]


class FakeCursor:
    def __init__(self, fake_data):
        self.fake_data = fake_data

    def execute(self, query, values):
        pass

    def fetchall(self):
        return self.fake_data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class FakeConnection:
    def __init__(self, fake_data):
        self.fake_data = fake_data

    def cursor(self, row_factory=None):
        return FakeCursor(self.fake_data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def test_get_meter_data_success(mocker):
    """
    Verifica que, con un filtro válido, el endpoint devuelva status 200 y los datos esperados.
    """
    fake_conn = FakeConnection(fake_data)
    # Parchéa la función db_connection en el módulo donde se usa (src/meter_data/get.py)
    mocker.patch("src.meter_data.get.db_connection", return_value=fake_conn)

    response = client.get("/meter_data/", params={"connection_ean_code": "87160008222122"})

    assert response.status_code == 200
    assert response.json() == {
        "status_code": 200,
        "message": {
            "meter_data": fake_data
        }
    }


def test_get_meter_data_no_filters():
    """
    Verifica que sin filtros se devuelva un error 400.
    """
    response = client.get("/meter_data/")
    assert response.status_code == 400
    assert response.json() == {
        "status_code": 400,
        "message": "At least one filter must be provided"
    }


def test_get_meter_data_not_found(mocker):
    """
    Comprueba que, al enviar un filtro sin coincidencias, se devuelva un error 404.
    """
    fake_conn = FakeConnection([])
    mocker.patch("src.meter_data.get.db_connection", return_value=fake_conn)

    response = client.get("/meter_data/", params={"connection_ean_code": "no_existe"})
    assert response.status_code == 404
    assert response.json() == {
        "status_code": 404,
        "message": "Not found error"
    }