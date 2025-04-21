import pytest
from fastapi.testclient import TestClient
from main import app
import src.utils as utils

client = TestClient(app)


# Fixture para configurar la base de datos de prueba.
# Inserta un registro de prueba en la tabla meter_data y luego lo elimina.
@pytest.fixture(scope="module")
def test_db_setup():
    # Conecta a la base de datos utilizando la función real
    conn = utils.db_connection()
    cursor = conn.cursor()

    # Inserta un registro de prueba y devuelve su ID (asumiendo que la tabla tiene una columna autoincremental "meter_data_id")
    insert_sql = """
        INSERT INTO meter_data (
            business_partner_id,
            connection_ean_code,
            grid_company_code,
            oda_code,
            meter_number,
            smart_collectable,
            brand,
            sjv1,
            sjv2,
            installation,
            division,
            move_out_date,
            row_create_datetime,
            move_in_date
        ) VALUES (
            '01078462',
            '87160008222122',
            '8716948000003',
            '8712423026766',
            '000000000000051018',
            '1',
            'ES',
            614,
            629,
            '0800196933',
            '01',
            '2024-10-01 00:00:00',
            '2024-08-09 07:38:07',
            '2023-10-02 00:00:00'
        )
        RETURNING meter_data_id;
    """
    cursor.execute(insert_sql)
    record_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    # La fixture retorna el ID del registro insertado
    yield record_id

    # Luego de la prueba, eliminamos el registro insertado para limpiar la base de datos.
    conn = utils.db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM meter_data WHERE meter_data_id = %s", (record_id,))
    conn.commit()
    cursor.close()
    conn.close()


def test_get_meter_data_integration(test_db_setup):
    """
    Este test de integración verifica que el endpoint get_meter_data devuelva el registro insertado.
    """
    # Hacemos una petición GET con el filtro que coincide con el registro insertado.
    response = client.get("/meter_data/", params={"connection_ean_code": "87160008222122"})

    # Comprobamos que el endpoint responda con un status 200.
    assert response.status_code == 200

    data = response.json()

    # Verificamos que el response tenga el mismo código y contenga la clave "meter_data" en el mensaje.
    assert data["status_code"] == 200
    assert "meter_data" in data["message"]

    # Comprobamos que al menos uno de los registros retornados tenga la connection_ean_code esperada.
    records = data["message"]["meter_data"]
    # Por ejemplo, buscamos el registro insertado:
    matching_records = [r for r in records if r.get("connection_ean_code") == "87160008222122"]
    assert matching_records, "No se encontró el registro esperado en la respuesta"
