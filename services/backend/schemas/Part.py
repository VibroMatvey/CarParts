from pydantic import BaseModel


class PartCreate(BaseModel):
    title: str
    price: float
    code: str
    supplier_id: int


class PartEdit(BaseModel):
    title: str | None = None
    price: float | None = None
    code: str | None = None
    supplier_id: str | None = None


class PartSupplier(BaseModel):
    id: int
    title: str
    address: str
    email: str | None = None
    phone: str | None = None


class Part(PartCreate):
    id: int
    supplier: PartSupplier
