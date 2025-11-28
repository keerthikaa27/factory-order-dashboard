from datetime import date, datetime
from pydantic import BaseModel


class OrderSummary(BaseModel):
    id: int
    source_type: str      # OUTSTANDING / DELIVERY
    status: str | None    # PENDING / DISPATCHED

    so_number: str | None = None
    order_no: str | None = None

    customer_name: str | None = None
    customer_code: str | None = None

    part_number: str | None = None

    order_date: date | None = None
    delivery_date: date | None = None
    financial_year: str | None = None

    department: str | None = None
    item_description: str | None = None

    quantity: int | None = None
    order_qty: int | None = None
    os_order_qty: int | None = None   # open qty from outstanding

    last_updated_at: datetime | None = None

    class Config:
        orm_mode = True
