"""商品管理サービスの Pydantic データモデル定義."""

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """商品情報の共通フィールド定義."""

    name: str
    category: str
    price: int = Field(..., ge=0)
    photo_url: str | None = None
    allergens: list[str] = Field(default_factory=list)
    calories: int = Field(default=0, ge=0)
    prep_time_minutes: int = Field(default=10, ge=0)
    options: list[str] = Field(default_factory=list)
    takeout_available: bool = True


class ProductCreate(ProductBase):
    """商品登録リクエストモデル."""


class ProductUpdate(ProductBase):
    """商品更新リクエストモデル."""


class Product(ProductBase):
    """商品レスポンス・永続化モデル."""

    id: str
