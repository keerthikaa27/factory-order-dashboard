from typing import List, Optional
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.deps import get_db
from app.models.order import Order
from app.schemas.order import OrderSummary

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.get("/search", response_model=List[OrderSummary])
def search_orders(
    po_number: Optional[str] = None,        # PO / Order No
    serial_number: Optional[str] = None,    # PO Srl / P Srl
    part_number: Optional[str] = None,      # Item Code / Produce Code
    customer_name: Optional[str] = None,
    status: Optional[str] = None,           # PENDING / DISPATCHED
    source_type: Optional[str] = None,      # OUTSTANDING / DELIVERY
    financial_year: Optional[str] = None,
    limit: int = 50,
    skip: int = 0,
    db: Session = Depends(get_db),
):
    """
    Main search endpoint.

    - Search by PO number (order_no or so_number)
    - Serial number (po_serial)
    - Part number (unified part_number)
    - Customer name (contains, case-insensitive)
    - Filter by status, source_type, financial_year
    """

    query = db.query(Order)

    if po_number:
        like_value = f"%{po_number}%"
        query = query.filter(
            or_(
                Order.order_no.ilike(like_value),
                Order.so_number.ilike(like_value),
            )
        )

    if serial_number:
        like_value = f"%{serial_number}%"
        query = query.filter(Order.po_serial.ilike(like_value))

    if part_number:
        like_value = f"%{part_number}%"
        query = query.filter(Order.part_number.ilike(like_value))

    if customer_name:
        like_value = f"%{customer_name}%"
        query = query.filter(Order.customer_name.ilike(like_value))

    if status:
        query = query.filter(Order.status == status.upper())

    if source_type:
        query = query.filter(Order.source_type == source_type.upper())

    if financial_year:
        query = query.filter(Order.financial_year == financial_year)

    results = (
        query.order_by(Order.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return results


@router.get("/open", response_model=List[OrderSummary])
def open_orders(
    today_only: bool = False,
    part_number: Optional[str] = None,
    customer_name: Optional[str] = None,
    limit: int = 100,
    skip: int = 0,
    db: Session = Depends(get_db),
):
    """
    Open Orders View:

    - All PENDING orders (status = PENDING)
    - Optional: only today's delivery_date
    - Optional: filter by part_number and/or customer_name
    """
    query = db.query(Order).filter(Order.status == "PENDING")

    if today_only:
        query = query.filter(Order.delivery_date == date.today())

    if part_number:
        like_value = f"%{part_number}%"
        query = query.filter(Order.part_number.ilike(like_value))

    if customer_name:
        like_value = f"%{customer_name}%"
        query = query.filter(Order.customer_name.ilike(like_value))

    results = (
        query.order_by(Order.delivery_date.asc().nulls_last(), Order.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return results
