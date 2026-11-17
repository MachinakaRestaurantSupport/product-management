# ruff: noqa: E501
"""HTML UI router for product-management."""

from html import escape

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import HTMLResponse

from product_management.models import Product
from product_management.store import ProductStore

PORTAL_LINKS = [
    ("portal", "ポータル", "/ui/portal"),
    ("product", "商品管理", "/ui/products"),
    ("menu", "メニュー", "/ui/menus"),
    ("guest", "座席・顧客", "/ui/tables"),
    ("order", "注文かんばん", "/ui/orders/kanban"),
    ("accounting", "会計", "/ui/accounting/checkout"),
    ("sales", "売上", "/ui/sales/daily"),
    ("dine_in", "店内QR", "/ui/dine-in/session"),
    ("takeout", "持ち帰り", "/ui/takeout/login"),
]


def _render_shell(
    *,
    title: str,
    subtitle: str,
    active_subtab: str,
    body_html: str,
    detail_href: str = "/ui/products/prod-1",
) -> str:
    nav_html = "".join(
        f'<a class="nav-pill{" active" if key == "product" else ""}" href="{href}">{escape(label)}</a>'
        for key, label, href in PORTAL_LINKS
    )
    subtabs = [
        ("list", "商品一覧", "/ui/products"),
        ("new", "新規商品登録", "/ui/products/new"),
        ("detail", "商品詳細・編集", detail_href),
    ]
    subtab_html = "".join(
        f'<a class="subtab{" active" if key == active_subtab else ""}" href="{href}">{escape(label)}</a>'
        for key, label, href in subtabs
    )
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)} | まちなか飲食店サポート</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --surface: #ffffff;
      --navy: #0f172a;
      --slate: #334155;
      --muted: #64748b;
      --border: #e2e8f0;
      --accent: #ea580c;
      --accent-soft: #fff7ed;
      --ok-bg: #dcfce7;
      --ok-fg: #166534;
      --warn-bg: #fef3c7;
      --warn-fg: #92400e;
      --info-bg: #dbeafe;
      --info-fg: #1e40af;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Noto Sans CJK JP", "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
      background: var(--bg);
      color: var(--navy);
      line-height: 1.5;
    }}
    .topbar {{
      background: var(--navy);
      color: #fff;
      padding: 0 24px;
      height: 54px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      font-size: 15px;
      white-space: nowrap;
    }}
    .brand-badge {{
      background: var(--accent);
      color: #fff;
      padding: 2px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
    }}
    .nav-links {{
      display: flex;
      gap: 4px;
      flex-wrap: nowrap;
      overflow-x: auto;
    }}
    .nav-pill {{
      color: #cbd5e1;
      text-decoration: none;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 10px;
      border-radius: 6px;
      white-space: nowrap;
    }}
    .nav-pill.active {{
      background: var(--accent);
      color: #fff;
    }}
    .subbar {{
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}
    .subbar h1 {{
      margin: 0;
      font-size: 18px;
      font-weight: 700;
    }}
    .subbar .subtitle {{
      margin: 2px 0 0;
      font-size: 12px;
      color: var(--muted);
    }}
    .subtabs {{
      display: flex;
      gap: 8px;
    }}
    .subtab {{
      text-decoration: none;
      color: var(--slate);
      font-size: 13px;
      font-weight: 600;
      padding: 7px 14px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface);
    }}
    .subtab.active {{
      background: var(--accent-soft);
      color: var(--accent);
      border-color: #fdba74;
    }}
    .container {{
      max-width: 1220px;
      margin: 0 auto;
      padding: 20px 24px 28px;
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin-bottom: 18px;
    }}
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 18px;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }}
    .kpi-label {{
      font-size: 12px;
      color: var(--muted);
      font-weight: 600;
    }}
    .kpi-value {{
      font-size: 24px;
      font-weight: 800;
      margin-top: 4px;
      color: var(--navy);
    }}
    .kpi-sub {{
      font-size: 11px;
      color: var(--muted);
      margin-top: 2px;
    }}
    .toolbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 14px;
      gap: 12px;
    }}
    .filter-pills {{
      display: flex;
      gap: 8px;
    }}
    .pill {{
      text-decoration: none;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 999px;
      border: 1px solid var(--border);
      color: var(--slate);
      background: var(--surface);
    }}
    .pill.active {{
      background: var(--navy);
      color: #fff;
      border-color: var(--navy);
    }}
    .btn {{
      display: inline-block;
      text-decoration: none;
      font-size: 13px;
      font-weight: 700;
      padding: 8px 16px;
      border-radius: 8px;
      border: none;
      cursor: pointer;
    }}
    .btn-primary {{
      background: var(--accent);
      color: #fff;
    }}
    .btn-secondary {{
      background: #f1f5f9;
      color: var(--slate);
      border: 1px solid var(--border);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th {{
      text-align: left;
      padding: 10px 12px;
      background: #f8fafc;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      border-bottom: 1px solid var(--border);
    }}
    td {{
      padding: 11px 12px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }}
    .badge {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
    }}
    .badge-ok {{ background: var(--ok-bg); color: var(--ok-fg); }}
    .badge-warn {{ background: var(--warn-bg); color: var(--warn-fg); }}
    .badge-info {{ background: var(--info-bg); color: var(--info-fg); }}
    .badge-tag {{
      background: #f1f5f9;
      color: var(--slate);
      margin-right: 4px;
    }}
    .form-grid {{
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 18px;
    }}
    .field-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}
    .field {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .field.full {{ grid-column: 1 / -1; }}
    label {{
      font-size: 12px;
      font-weight: 700;
      color: var(--slate);
    }}
    input[type="text"], input[type="number"], select {{
      padding: 9px 11px;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-size: 13px;
      font-family: inherit;
      background: #fff;
    }}
    .check-row {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      padding: 6px 0;
    }}
    .preview-box {{
      border: 1px dashed #cbd5e1;
      border-radius: 10px;
      padding: 16px;
      background: #f8fafc;
    }}
    .price {{
      font-weight: 800;
      font-size: 15px;
      color: var(--navy);
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="brand">
      <span>🍽️ まちなか飲食店サポート</span>
      <span class="brand-badge">店長・スタッフ共通ポータル</span>
    </div>
    <nav class="nav-links">{nav_html}</nav>
  </header>
  <section class="subbar">
    <div>
      <h1>{escape(title)}</h1>
      <p class="subtitle">{escape(subtitle)}</p>
    </div>
    <div class="subtabs">{subtab_html}</div>
  </section>
  <main class="container">
    {body_html}
  </main>
</body>
</html>
"""


def _format_product_row(product: Product) -> str:
    allergens_html = "".join(
        f'<span class="badge badge-warn">{escape(a)}</span> ' for a in product.allergens
    ) or '<span style="color:#94a3b8">なし</span>'
    options_html = "".join(
        f'<span class="badge badge-tag">{escape(o)}</span>' for o in product.options
    ) or '<span style="color:#94a3b8">-</span>'
    takeout_badge = (
        '<span class="badge badge-ok">持ち帰り可</span>'
        if product.takeout_available
        else '<span class="badge badge-info">店内専用</span>'
    )
    return (
        f"<tr>"
        f"<td><strong>{escape(str(product.id))}</strong></td>"
        f'<td><a href="/ui/products/{escape(str(product.id))}" style="color:#0f172a;font-weight:700;text-decoration:none">'
        f"{escape(product.name)}</a></td>"
        f'<td><span class="badge badge-tag">{escape(product.category)}</span></td>'
        f'<td class="price">¥{product.price:,}</td>'
        f"<td>{allergens_html}</td>"
        f"<td>{product.calories} kcal</td>"
        f"<td>{product.prep_time_minutes} 分</td>"
        f"<td>{options_html}</td>"
        f"<td>{takeout_badge}</td>"
        f'<td><a class="btn btn-secondary" style="padding:4px 10px;font-size:12px" href="/ui/products/{escape(str(product.id))}">編集</a></td>'
        f"</tr>"
    )


def create_ui_router(store: ProductStore) -> APIRouter:
    """Create FastAPI router providing HTML management screens for product-management."""
    router = APIRouter(tags=["ui"])

    @router.get("/ui/products", response_class=HTMLResponse)
    def product_list_page(takeout_available: bool | None = Query(default=None)) -> str:
        all_products = store.list_products()
        products = store.list_products(takeout_available=takeout_available)
        takeout_count = sum(1 for p in all_products if p.takeout_available)
        avg_price = round(sum(p.price for p in all_products) / len(all_products)) if all_products else 0
        avg_prep = (
            round(sum(p.prep_time_minutes for p in all_products) / len(all_products))
            if all_products
            else 0
        )
        first_id = all_products[0].id if all_products else "prod-1"

        rows_html = "".join(_format_product_row(p) for p in products)
        if not rows_html:
            rows_html = (
                '<tr><td colspan="10" style="text-align:center;color:#64748b;padding:24px">'
                "該当する商品が登録されていません。</td></tr>"
            )

        body = f"""
        <div class="kpi-grid">
          <div class="card">
            <div class="kpi-label">登録商品マスタ数</div>
            <div class="kpi-value">{len(all_products)} 品</div>
            <div class="kpi-sub">メニュー管理・注文ツールの正本</div>
          </div>
          <div class="card">
            <div class="kpi-label">持ち帰り対応商品</div>
            <div class="kpi-value">{takeout_count} 品</div>
            <div class="kpi-sub">店内専用: {len(all_products) - takeout_count} 品</div>
          </div>
          <div class="card">
            <div class="kpi-label">平均販売単価</div>
            <div class="kpi-value">¥{avg_price:,}</div>
            <div class="kpi-sub">税抜/税込マスタ基準価格</div>
          </div>
          <div class="card">
            <div class="kpi-label">平均調理時間</div>
            <div class="kpi-value">{avg_prep} 分</div>
            <div class="kpi-sub">キッチン提供見込み目安</div>
          </div>
        </div>
        <div class="card">
          <div class="toolbar">
            <div class="filter-pills">
              <a class="pill{" active" if takeout_available is None else ""}" href="/ui/products">すべて ({len(all_products)})</a>
              <a class="pill{" active" if takeout_available is True else ""}" href="/ui/products?takeout_available=true">持ち帰り可 ({takeout_count})</a>
              <a class="pill{" active" if takeout_available is False else ""}" href="/ui/products?takeout_available=false">店内専用 ({len(all_products) - takeout_count})</a>
            </div>
            <a class="btn btn-primary" href="/ui/products/new">＋ 新規商品を登録</a>
          </div>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>商品名</th>
                <th>分類</th>
                <th>正本価格</th>
                <th>アレルギー</th>
                <th>カロリー</th>
                <th>提供時間</th>
                <th>オプション</th>
                <th>提供形態</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>
        """
        return _render_shell(
            title="商品管理 › 商品マスタ一覧",
            subtitle="商品の分類・正本価格・アレルギー・カロリー・提供時間・持ち帰り可否を一元管理します",
            active_subtab="list",
            body_html=body,
            detail_href=f"/ui/products/{first_id}",
        )

    @router.get("/ui/products/new", response_class=HTMLResponse)
    def product_new_page() -> str:
        all_products = store.list_products()
        first_id = all_products[0].id if all_products else "prod-1"
        body = """
        <div class="form-grid">
          <div class="card">
            <h2 style="margin:0 0 14px;font-size:16px">新規商品マスタ登録</h2>
            <form id="product-create-form" onsubmit="submitProduct(event)">
              <div class="field-grid">
                <div class="field">
                  <label>商品名（必須）</label>
                  <input type="text" id="p-name" value="特製マルゲリータピザ" required>
                </div>
                <div class="field">
                  <label>商品分類（必須）</label>
                  <select id="p-category">
                    <option value="メイン">メイン</option>
                    <option value="パスタ" selected>パスタ・ピザ</option>
                    <option value="弁当">弁当</option>
                    <option value="ドリンク">ドリンク</option>
                    <option value="デザート">デザート</option>
                  </select>
                </div>
                <div class="field">
                  <label>正本価格（円）</label>
                  <input type="number" id="p-price" value="1380" min="0" required>
                </div>
                <div class="field">
                  <label>標準提供時間（分）</label>
                  <input type="number" id="p-prep" value="14" min="0">
                </div>
                <div class="field">
                  <label>カロリー（kcal）</label>
                  <input type="number" id="p-cal" value="690" min="0">
                </div>
                <div class="field">
                  <label>持ち帰り可否</label>
                  <select id="p-takeout">
                    <option value="true" selected>持ち帰り可（店内・店外両方）</option>
                    <option value="false">店内飲食専用（テイクアウト不可）</option>
                  </select>
                </div>
                <div class="field full">
                  <label>アレルギー物質（カンマ区切り）</label>
                  <input type="text" id="p-allergens" value="小麦, 乳">
                </div>
                <div class="field full">
                  <label>トッピング・注文オプション（カンマ区切り）</label>
                  <input type="text" id="p-options" value="チーズ増量, ハーフサイズ">
                </div>
                <div class="field full">
                  <label>商品写真 URL</label>
                  <input type="text" id="p-photo" value="https://example.com/images/margherita.jpg">
                </div>
              </div>
              <div style="display:flex;gap:10px;margin-top:18px;justify-content:flex-end">
                <a class="btn btn-secondary" href="/ui/products">一覧へ戻る</a>
                <button type="submit" class="btn btn-primary">商品マスタに登録する</button>
              </div>
            </form>
          </div>
          <div class="card">
            <h2 style="margin:0 0 12px;font-size:16px">メニュー表示プレビュー</h2>
            <div class="preview-box">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                <span class="badge badge-tag">パスタ・ピザ</span>
                <span class="badge badge-ok">持ち帰り可</span>
              </div>
              <h3 style="margin:4px 0 6px;font-size:18px">特製マルゲリータピザ</h3>
              <div style="font-size:22px;font-weight:800;color:#ea580c;margin-bottom:10px">¥1,380</div>
              <div style="font-size:12px;color:#475569;margin-bottom:10px">
                カロリー: 690 kcal ／ 提供目安: 14分
              </div>
              <div style="margin-bottom:8px">
                <span style="font-size:11px;color:#64748b;font-weight:700">アレルゲン:</span>
                <span class="badge badge-warn">小麦</span>
                <span class="badge badge-warn">乳</span>
              </div>
              <div>
                <span style="font-size:11px;color:#64748b;font-weight:700">選択オプション:</span>
                <span class="badge badge-tag">チーズ増量</span>
                <span class="badge badge-tag">ハーフサイズ</span>
              </div>
            </div>
            <div style="margin-top:14px;font-size:12px;color:#64748b;background:#f8fafc;padding:12px;border-radius:8px">
              <strong>I-5 連携ガイド:</strong><br>
              ここで登録した商品マスタは、メニュー管理の公開メニュー構成および注文時の持ち帰り可否・正本価格チェックで参照されます。
            </div>
          </div>
        </div>
        <script>
          async function submitProduct(e) {
            e.preventDefault();
            const splitCsv = (s) => s.split(',').map(v => v.trim()).filter(Boolean);
            const res = await fetch('/products', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({
                name: document.getElementById('p-name').value,
                category: document.getElementById('p-category').value,
                price: Number(document.getElementById('p-price').value),
                prep_time_minutes: Number(document.getElementById('p-prep').value),
                calories: Number(document.getElementById('p-cal').value),
                takeout_available: document.getElementById('p-takeout').value === 'true',
                allergens: splitCsv(document.getElementById('p-allergens').value),
                options: splitCsv(document.getElementById('p-options').value),
                photo_url: document.getElementById('p-photo').value || null
              })
            });
            if (res.ok) { window.location.href = '/ui/products'; }
          }
        </script>
        """
        return _render_shell(
            title="商品管理 › 新規商品登録",
            subtitle="店舗で提供するメニュー商品の基本スペックとアレルゲン情報を登録します",
            active_subtab="new",
            body_html=body,
            detail_href=f"/ui/products/{first_id}",
        )

    @router.get("/ui/products/{product_id}", response_class=HTMLResponse)
    def product_detail_page(product_id: str) -> str:
        product = store.get(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        allergens_csv = ", ".join(product.allergens)
        options_csv = ", ".join(product.options)
        takeout_badge = (
            '<span class="badge badge-ok">持ち帰り可</span>'
            if product.takeout_available
            else '<span class="badge badge-info">店内専用</span>'
        )
        allergen_badges = "".join(
            f'<span class="badge badge-warn">{escape(a)}</span> ' for a in product.allergens
        ) or '<span class="badge badge-tag">特定アレルゲン登録なし</span>'

        body = f"""
        <div class="form-grid">
          <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
              <h2 style="margin:0;font-size:16px">商品スペック編集（ID: {escape(product.id)}）</h2>
              {takeout_badge}
            </div>
            <form onsubmit="updateProduct(event, '{escape(product.id)}')">
              <div class="field-grid">
                <div class="field">
                  <label>商品名</label>
                  <input type="text" id="u-name" value="{escape(product.name)}" required>
                </div>
                <div class="field">
                  <label>分類</label>
                  <input type="text" id="u-category" value="{escape(product.category)}" required>
                </div>
                <div class="field">
                  <label>正本価格（円）</label>
                  <input type="number" id="u-price" value="{product.price}" min="0" required>
                </div>
                <div class="field">
                  <label>標準提供時間（分）</label>
                  <input type="number" id="u-prep" value="{product.prep_time_minutes}" min="0">
                </div>
                <div class="field">
                  <label>カロリー（kcal）</label>
                  <input type="number" id="u-cal" value="{product.calories}" min="0">
                </div>
                <div class="field">
                  <label>持ち帰り可否</label>
                  <select id="u-takeout">
                    <option value="true"{" selected" if product.takeout_available else ""}>持ち帰り可</option>
                    <option value="false"{" selected" if not product.takeout_available else ""}>店内専用</option>
                  </select>
                </div>
                <div class="field full">
                  <label>アレルギー物質</label>
                  <input type="text" id="u-allergens" value="{escape(allergens_csv)}">
                </div>
                <div class="field full">
                  <label>注文オプション</label>
                  <input type="text" id="u-options" value="{escape(options_csv)}">
                </div>
              </div>
              <div style="display:flex;gap:10px;margin-top:18px;justify-content:flex-end">
                <a class="btn btn-secondary" href="/ui/products">商品一覧に戻る</a>
                <button type="submit" class="btn btn-primary">変更内容を保存（PUT /products/{escape(product.id)}）</button>
              </div>
            </form>
          </div>
          <div class="card">
            <h2 style="margin:0 0 12px;font-size:16px">登録情報サマリー</h2>
            <div class="preview-box">
              <div style="font-size:12px;color:#64748b">商品コード: {escape(product.id)}</div>
              <h3 style="margin:6px 0;font-size:20px">{escape(product.name)}</h3>
              <div style="font-size:24px;font-weight:800;color:#ea580c;margin-bottom:12px">¥{product.price:,}</div>
              <p style="margin:6px 0;font-size:13px"><strong>分類:</strong> {escape(product.category)}</p>
              <p style="margin:6px 0;font-size:13px"><strong>カロリー:</strong> {product.calories} kcal</p>
              <p style="margin:6px 0;font-size:13px"><strong>調理目安:</strong> {product.prep_time_minutes} 分</p>
              <p style="margin:10px 0 4px;font-size:13px"><strong>表示アレルゲン:</strong></p>
              <div>{allergen_badges}</div>
            </div>
          </div>
        </div>
        """ + """
        <script>
          async function updateProduct(e, id) {
            e.preventDefault();
            const splitCsv = (s) => s.split(',').map(v => v.trim()).filter(Boolean);
            const res = await fetch('/products/' + id, {
              method: 'PUT',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({
                name: document.getElementById('u-name').value,
                category: document.getElementById('u-category').value,
                price: Number(document.getElementById('u-price').value),
                prep_time_minutes: Number(document.getElementById('u-prep').value),
                calories: Number(document.getElementById('u-cal').value),
                takeout_available: document.getElementById('u-takeout').value === 'true',
                allergens: splitCsv(document.getElementById('u-allergens').value),
                options: splitCsv(document.getElementById('u-options').value)
              })
            });
            if (res.ok) { window.location.reload(); }
          }
        </script>
        """
        return _render_shell(
            title=f"商品管理 › 商品詳細（{product.name}）",
            subtitle="登録済み商品の価格・アレルゲン・持ち帰り設定を確認・更新します",
            active_subtab="detail",
            body_html=body,
            detail_href=f"/ui/products/{product.id}",
        )

    return router
