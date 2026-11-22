# product-catalog Specification

## Purpose
商品マスタの登録・一覧取得・詳細取得・更新を行うREST APIの振る舞いを定義し、安全な商品情報の正本管理を実現する。

## Requirements

### Requirement: 商品登録・取得・更新

システムは商品情報の登録、持ち帰り可否フィルタ付き一覧取得、詳細取得、更新を提供しなければならない（SHALL / MUST）。

#### Scenario: 商品登録と取得・更新

- **WHEN** クライアントが妥当な商品情報で `POST /products` を呼び出したとき
- **THEN** 採番された `id` を含む商品情報を HTTP 201 で返す（SHALL）
- **WHEN** `GET /products` や `PUT /products/{id}` を呼び出したとき
- **THEN** フィルタ結果や更新結果を返し、未存在IDは HTTP 404、不正値は HTTP 422 とする（MUST）

### Requirement: サブモジュール参照のコミット指定管理

本リポジトリは `.gitmodules` に `branch` 設定を持たせず `reference/system-integration` を確定コミット SHA（gitlink）指定で管理しなければならず（MUST）、`reference/system-integration/` 配下を読み取り専用として直接変更してはならない（SHALL）。

#### Scenario: サブモジュール参照の更新とマージ

- **WHEN** `system-integration` の確定コミット SHA（`<commit-sha>`）を `reference/system-integration` にチェックアウトし、`system-integration` PR の Merge commit マージ後に本リポジトリの PR を `main` にマージするとき
- **THEN** `.gitmodules` の書き換えやマージ後の `main` 戻し作業なしで、正しい仕様・画像参照を維持したままマージが完了する（SHALL）
