# product-management

飲食店スタッフが商品の分類、写真、価格、アレルギー、カロリー、提供時間、オプション、持ち帰り可否を管理するツールです。  
店長・スタッフ共通ポータル（[ポータル画面イメージ](reference/system-integration/docs/images/portal/01-portal-dashboard.png)）における商品マスタの正本を担い、メニュー管理や注文管理と連携します。

## 画面遷移図

縮小画面キャプチャを用いた `product-management` の画面遷移図です（draw.io 編集用ソース: [transition.drawio](reference/system-integration/docs/images/product_management/transition.drawio)）。

![product-management 画面遷移図](reference/system-integration/docs/images/product_management/transition.svg)

## 代表機能イメージ

### 1. 商品マスタ一覧・提供形態フィルタ (`GET /ui/products`)
登録済み商品のID・商品名・分類・正本価格・アレルギー物質・カロリー・提供時間・注文オプション・持ち帰り可否を一覧で確認し、「すべて」「持ち帰り可」「店内専用」で絞り込みできます。

![商品マスタ一覧](reference/system-integration/docs/images/product_management/01-product-list.png)

### 2. 新規商品登録 (`GET /ui/products/new`)
商品名・分類・価格・調理時間・カロリー・アレルギー・オプション・持ち帰り可否を入力し、右側のメニュー表示プレビューを確認しながら `POST /products` で登録します。

![新規商品登録](reference/system-integration/docs/images/product_management/02-product-register.png)

### 3. 商品詳細・スペック編集 (`GET /ui/products/{product_id}`)
登録済み商品のスペックサマリーを確認し、価格やアレルゲン・持ち帰り可否等を `PUT /products/{product_id}` で更新できます。

![商品詳細・編集](reference/system-integration/docs/images/product_management/03-product-detail.png)

## 提供 API・UI エンドポイント

| 種別 | メソッド & パス | 機能概要 |
|---|---|---|
| API | `GET /health` | ヘルスチェック |
| API | `POST /products` | 商品の新規登録 |
| API | `GET /products` | 商品一覧取得（`takeout_available` フィルタ対応） |
| API | `GET /products/{product_id}` | 商品詳細取得 |
| API | `PUT /products/{product_id}` | 商品情報更新 |
| UI | `GET /ui/products` | 商品マスタ一覧画面 |
| UI | `GET /ui/products/new` | 新規商品登録画面 |
| UI | `GET /ui/products/{product_id}` | 商品詳細・編集画面 |

## テスト・静的解析の実行

```bash
../.venv/bin/python3 -m pytest -v
../.venv/bin/ruff check .
```
