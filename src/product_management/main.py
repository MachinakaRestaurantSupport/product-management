"""商品管理サービスの FastAPI アプリケーション定義."""

from fastapi import FastAPI, HTTPException, status

from product_management.models import Product, ProductCreate, ProductUpdate
from product_management.store import ProductStore
from product_management.ui import create_ui_router


def create_app() -> FastAPI:
    """FastAPI アプリケーションインスタンスを生成する."""
    application = FastAPI(title="Product Management Service", version="0.1.0")
    store = ProductStore()
    application.include_router(create_ui_router(store))

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "product-management"}

    @application.post(
        "/products",
        response_model=Product,
        status_code=status.HTTP_201_CREATED,
    )
    def create_product(payload: ProductCreate) -> Product:
        return store.create(payload)

    @application.get("/products", response_model=list[Product])
    def list_products(takeout_available: bool | None = None) -> list[Product]:
        return store.list_products(takeout_available=takeout_available)

    @application.get("/products/{product_id}", response_model=Product)
    def get_product(product_id: int) -> Product:
        product = store.get(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        return product

    @application.put("/products/{product_id}", response_model=Product)
    def update_product(product_id: int, payload: ProductUpdate) -> Product:
        updated = store.update(product_id, payload)
        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        return updated

    return application


app = create_app()
