"""商品マスタのインメモリストア実装."""

from product_management.models import Product, ProductCreate, ProductUpdate


class ProductStore:
    """インメモリで商品マスタを管理するストア."""

    def __init__(self) -> None:
        self._items: dict[int, Product] = {}
        self._next_id: int = 1

    def create(self, payload: ProductCreate) -> Product:
        """新規商品を登録し、採番したID付きの商品を返す."""
        product = Product(id=self._next_id, **payload.model_dump())
        self._items[product.id] = product
        self._next_id += 1
        return product

    def list_products(self, takeout_available: bool | None = None) -> list[Product]:
        """商品一覧を返す。takeout_available が指定された場合はフィルタする."""
        products = list(self._items.values())
        if takeout_available is None:
            return products
        return [item for item in products if item.takeout_available is takeout_available]

    def get(self, product_id: int) -> Product | None:
        """指定IDの商品を取得する。存在しない場合は None を返す."""
        return self._items.get(product_id)

    def update(self, product_id: int, payload: ProductUpdate) -> Product | None:
        """指定IDの商品情報を更新する。存在しない場合は None を返す."""
        if product_id not in self._items:
            return None
        updated = Product(id=product_id, **payload.model_dump())
        self._items[product_id] = updated
        return updated
