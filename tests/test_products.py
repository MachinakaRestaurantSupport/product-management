"""商品管理APIの単体試験."""

import pytest
from fastapi.testclient import TestClient

from product_management.main import create_app


@pytest.fixture
def client() -> TestClient:
    """テストごとに独立した FastAPI TestClient を生成する."""
    return TestClient(create_app())


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "product-management"}


def test_create_product_with_defaults_and_full_fields(client: TestClient) -> None:
    minimal_payload = {
        "name": "ブレンドコーヒー",
        "category": "ドリンク",
        "price": 450,
    }
    res_min = client.post("/products", json=minimal_payload)
    assert res_min.status_code == 201
    data_min = res_min.json()
    assert isinstance(data_min["id"], str)
    assert data_min["id"].startswith("prod-")
    assert {k: v for k, v in data_min.items() if k != "id"} == {
        "name": "ブレンドコーヒー",
        "category": "ドリンク",
        "price": 450,
        "photo_url": None,
        "allergens": [],
        "calories": 0,
        "prep_time_minutes": 10,
        "options": [],
        "takeout_available": True,
    }

    full_payload = {
        "name": "特製カツカレー",
        "category": "メイン",
        "price": 1200,
        "photo_url": "https://example.com/katsu-curry.jpg",
        "allergens": ["小麦", "豚肉"],
        "calories": 850,
        "prep_time_minutes": 15,
        "options": ["大盛り", "辛口"],
        "takeout_available": False,
    }
    res_full = client.post("/products", json=full_payload)
    assert res_full.status_code == 201
    data_full = res_full.json()
    assert isinstance(data_full["id"], str)
    assert data_full["id"] != data_min["id"]
    assert data_full["name"] == "特製カツカレー"
    assert data_full["allergens"] == ["小麦", "豚肉"]
    assert data_full["takeout_available"] is False


def test_list_products_and_takeout_filter(client: TestClient) -> None:
    client.post(
        "/products",
        json={"name": "サンドイッチ", "category": "軽食", "price": 600, "takeout_available": True},
    )
    client.post(
        "/products",
        json={
            "name": "鉄板ステーキ",
            "category": "メイン",
            "price": 1800,
            "takeout_available": False,
        },
    )

    res_all = client.get("/products")
    assert res_all.status_code == 200
    assert len(res_all.json()) == 2

    res_takeout = client.get("/products", params={"takeout_available": True})
    assert res_takeout.status_code == 200
    assert [item["name"] for item in res_takeout.json()] == ["サンドイッチ"]

    res_dine_in = client.get("/products", params={"takeout_available": False})
    assert res_dine_in.status_code == 200
    assert [item["name"] for item in res_dine_in.json()] == ["鉄板ステーキ"]


def test_get_product_and_not_found(client: TestClient) -> None:
    created = client.post(
        "/products",
        json={"name": "抹茶ラテ", "category": "ドリンク", "price": 550},
    ).json()

    res_found = client.get(f"/products/{created['id']}")
    assert res_found.status_code == 200
    assert res_found.json()["name"] == "抹茶ラテ"

    res_missing = client.get("/products/999")
    assert res_missing.status_code == 404


def test_update_product_and_not_found(client: TestClient) -> None:
    created = client.post(
        "/products",
        json={"name": "チーズケーキ", "category": "デザート", "price": 500},
    ).json()

    update_payload = {
        "name": "濃厚チーズケーキ",
        "category": "デザート",
        "price": 580,
        "photo_url": "https://example.com/cheesecake.png",
        "allergens": ["乳", "卵", "小麦"],
        "calories": 380,
        "prep_time_minutes": 5,
        "options": ["ホイップ追加"],
        "takeout_available": True,
    }
    res_update = client.put(f"/products/{created['id']}", json=update_payload)
    assert res_update.status_code == 200
    updated = res_update.json()
    assert updated["id"] == created["id"]
    assert updated["name"] == "濃厚チーズケーキ"
    assert updated["price"] == 580
    assert updated["allergens"] == ["乳", "卵", "小麦"]

    res_missing = client.put("/products/999", json=update_payload)
    assert res_missing.status_code == 404


@pytest.mark.parametrize(
    "invalid_payload",
    [
        {"name": "不正価格", "category": "ドリンク", "price": -1},
        {"name": "不正カロリー", "category": "ドリンク", "price": 100, "calories": -10},
        {"name": "不正提供時間", "category": "ドリンク", "price": 100, "prep_time_minutes": -5},
        {"name": "必須項目欠落", "category": "ドリンク"},
    ],
)
def test_create_product_validation_error(client: TestClient, invalid_payload: dict) -> None:
    response = client.post("/products", json=invalid_payload)
    assert response.status_code == 422


def test_update_product_validation_error(client: TestClient) -> None:
    created = client.post(
        "/products",
        json={"name": "コーヒー", "category": "ドリンク", "price": 400},
    ).json()

    response = client.put(
        f"/products/{created['id']}",
        json={"name": "コーヒー", "category": "ドリンク", "price": -100},
    )
    assert response.status_code == 422


def test_product_ui_screens(client: TestClient) -> None:
    created = client.post(
        "/products",
        json={
            "name": "ボロネーゼ",
            "category": "パスタ",
            "price": 1200,
            "allergens": ["小麦"],
            "calories": 780,
        },
    ).json()

    res_list = client.get("/ui/products")
    assert res_list.status_code == 200
    assert "ボロネーゼ" in res_list.text

    res_new = client.get("/ui/products/new")
    assert res_new.status_code == 200
    assert "新規商品マスタ登録" in res_new.text

    res_detail = client.get(f"/ui/products/{created['id']}")
    assert res_detail.status_code == 200
    assert "ボロネーゼ" in res_detail.text

    res_missing = client.get("/ui/products/prod-missing")
    assert res_missing.status_code == 404
