from pydantic import BaseModel


class SupplierCreate(BaseModel):
    title: str
    address: str
    email: str | None = None
    phone: str | None = None


class SupplierEdit(SupplierCreate):
    title: str | None = None
    address: str | None = None


class SupplierPart(BaseModel):
    title: str
    price: float
    sale_price: float
    code: str
    supplier_id: int | None = None


class Supplier(SupplierCreate):
    id: int
    parts: list[SupplierPart]
