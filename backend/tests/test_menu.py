import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routes import reset_store

client = TestClient(app)
VALID = {"sku": "KOPI-001", "nama": "Kopi Susu", "kategori": "kopi", "harga": 25000}


@pytest.fixture(autouse=True)
def _clean():
    reset_store()


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_create_returns_201_location_and_server_id():
    r = client.post("/api/menu", json=VALID)
    assert r.status_code == 201
    assert r.json()["id"] == 1
    assert r.headers["location"] == "/api/menu/1"


def test_input_id_is_ignored():
    r = client.post("/api/menu", json={**VALID, "id": 99})
    assert r.json()["id"] == 1


@pytest.mark.parametrize("sku", ["KOPI-01", "KOPI-0001", "kopi-001", "TEH-001", "KOPI001", ""])
def test_invalid_sku_422(sku):
    assert client.post("/api/menu", json={**VALID, "sku": sku}).status_code == 422


@pytest.mark.parametrize("kategori", ["minuman", "Kopi", "", None])
def test_invalid_kategori_422(kategori):
    assert client.post("/api/menu", json={**VALID, "kategori": kategori}).status_code == 422


@pytest.mark.parametrize("kategori", ["kopi", "non-kopi", "makanan"])
def test_valid_kategori(kategori):
    r = client.post("/api/menu", json={**VALID, "kategori": kategori})
    assert r.status_code == 201


def test_missing_fields_and_bad_harga_422():
    assert client.post("/api/menu", json={}).status_code == 422
    assert client.post("/api/menu", json={**VALID, "harga": 0}).status_code == 422


def test_duplicate_sku_409():
    client.post("/api/menu", json=VALID)
    assert client.post("/api/menu", json=VALID).status_code == 409


def test_get_by_id_and_404():
    client.post("/api/menu", json=VALID)
    assert client.get("/api/menu/1").json()["sku"] == "KOPI-001"
    assert client.get("/api/menu/999").status_code == 404


def test_list_skip_limit_search():
    for i in range(1, 6):
        client.post("/api/menu", json={**VALID, "sku": f"KOPI-00{i}", "nama": f"Menu {i}"})
    assert client.get("/api/menu").status_code == 200
    assert len(client.get("/api/menu").json()) == 5
    assert [m["id"] for m in client.get("/api/menu?skip=1&limit=2").json()] == [2, 3]
    assert [m["id"] for m in client.get("/api/menu?search=menu 4").json()] == [4]
    assert [m["id"] for m in client.get("/api/menu?search=kopi-005").json()] == [5]
    assert client.get("/api/menu?limit=0").status_code == 422
    assert client.get("/api/menu?skip=-1").status_code == 422
