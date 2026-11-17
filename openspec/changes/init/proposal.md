# Proposal: 商品管理（product-management）初期MVP実装

## Why

街なか飲食店支援ツール（MachinakaRestaurantSupportTools）における商品マスタの正本を一元管理するため、商品管理サービスの初期MVPを構築する。メニュー作成や注文管理などの他サービスが参照する正確な商品情報（分類・写真・価格・アレルゲン・カロリー・提供時間・オプション・持ち帰り可否）をAPI経由で登録・参照・更新できるようにする。

## What Changes

- Python プロジェクト基盤（`pyproject.toml`）を追加する。
- FastAPI ベースの REST API（`/health`, `POST /products`, `GET /products`, `GET /products/{product_id}`, `PUT /products/{product_id}`）を実装する。
- Pydantic モデルおよびインメモリストアを実装する。
- 単体試験（`tests/test_products.py`）を追加し、正常系・フィルタ・404・422バリデーションを検証する。

## Impact

- 新規コード: `pyproject.toml`, `src/product_management/`, `tests/test_products.py`
- `reference/system-integration/` 配下は読み取り専用とし変更しない。
