# Design: 商品管理（product-management）初期MVP設計

## USDM トレーサビリティ

本設計は `reference/system-integration/usdm/product_management/sheet01/ProductManagement_R01/` の要求に基づく。

| USDM 要求ID | 要求概要 | 設計要素 / エンドポイント |
| --- | --- | --- |
| `ProductManagement_R01` | 商品マスタ管理（分類・写真・価格・アレルギー・カロリー・提供時間・オプション・持ち帰り可否） | `Product`, `ProductCreate`, `ProductUpdate` モデル、`ProductStore` |
| `ProductManagement_R01.DM01-01` | `POST /products` で商品情報を登録できる（価格・カロリー0以上、不正値はHTTP 422） | `POST /products` (HTTP 201)、Pydantic `ge=0` バリデーション |
| `ProductManagement_R01.DM01-02` | `GET /products`（持ち帰り可否フィルタ対応）および `GET /products/{product_id}` で一覧・詳細を取得できる | `GET /products?takeout_available=...`, `GET /products/{product_id}` (404対応) |
| `ProductManagement_R01.DM01-03` | `PUT /products/{product_id}` で商品情報を更新でき、存在しないIDには HTTP 404 を返す | `PUT /products/{product_id}` (404対応) |

## アーキテクチャ

- **フレームワーク**: FastAPI + Pydantic v2
- **データストア**: 初期MVPではインメモリストア `ProductStore`（`dict[int, Product]` + 連番ID採番）を採用する。
- **モジュール構成**:
  - `src/product_management/__init__.py`: パッケージ公開シンボル
  - `src/product_management/models.py`: Pydantic スキーマ（`ProductCreate`, `ProductUpdate`, `Product`）
  - `src/product_management/store.py`: インメモリ CRUD ストア（`ProductStore`）
  - `src/product_management/main.py`: FastAPI アプリケーションファクトリ `create_app()` および `app`、各エンドポイント定義
  - `tests/test_products.py`: FastAPI `TestClient` による単体試験

## API エンドポイント仕様

- `GET /health`: `{"status": "ok", "service": "product-management"}`
- `POST /products` (201): `ProductCreate` を受け取り `id` を付与した `Product` を返却
- `GET /products`: `?takeout_available=bool|None` でフィルタし `list[Product]` を返却
- `GET /products/{product_id}`: 該当 `Product` を返却（未存在時は 404）
- `PUT /products/{product_id}`: `ProductUpdate` で更新し `Product` を返却（未存在時は 404）
