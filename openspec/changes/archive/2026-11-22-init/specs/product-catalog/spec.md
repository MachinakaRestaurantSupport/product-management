## Purpose

商品マスタの登録・一覧取得・詳細取得・更新を行うREST APIの振る舞いを定義し、安全な商品情報の正本管理を実現する。

## ADDED Requirements

### Requirement: 商品登録・取得・更新

システムは商品情報の登録、持ち帰り可否フィルタ付き一覧取得、詳細取得、更新を提供しなければならない（SHALL / MUST）。

#### Scenario: 商品登録と取得・更新

- **WHEN** クライアントが妥当な商品情報で `POST /products` を呼び出したとき
- **THEN** 採番された `id` を含む商品情報を HTTP 201 で返す（SHALL）
- **WHEN** `GET /products` や `PUT /products/{id}` を呼び出したとき
- **THEN** フィルタ結果や更新結果を返し、未存在IDは HTTP 404、不正値は HTTP 422 とする（MUST）
