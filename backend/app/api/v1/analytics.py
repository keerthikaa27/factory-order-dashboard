from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.deps import get_db
from app.models.order import Order

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)

def parse_financial_year(fy: str) -> tuple[date, date]:
    """
    Parse '2024-2025' into (2024-04-01, 2025-03-31)
    """
    try:
        start_str, end_str = fy.split("-")
        start_year = int(start_str)
        end_year = int(end_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid financial_year format. Use 'YYYY-YYYY'")

    # FY assumed as 1 April -> 31 March
    start = date(start_year, 4, 1)
    end = date(end_year, 3, 31)
    return start, end



# 1. Financial Year Sales Totals

@router.get("/financial-year")
def financial_year_summary(
    financial_year: str = Query(..., example="2024-2025"),
    db: Session = Depends(get_db),
):
    start, end = parse_financial_year(financial_year)

    q = (
        db.query(
            func.coalesce(func.sum(Order.amount), 0).label("total_sales_amount"),
            func.coalesce(func.sum(Order.quantity), 0).label("total_quantity"),
        )
        .filter(Order.source_type == "DELIVERY")
        .filter(Order.delivery_date >= start)
        .filter(Order.delivery_date <= end)
    )

    row = q.one()
    return {
        "financial_year": financial_year,
        "total_sales_amount": float(row.total_sales_amount or 0),
        "total_quantity": int(row.total_quantity or 0),
    }

# 2. Product-wise Sales Breakdown
@router.get("/product-wise")
def product_wise_sales(
    financial_year: str = Query(..., example="2024-2025"),
    db: Session = Depends(get_db),
):
    start, end = parse_financial_year(financial_year)

    q = (
        db.query(
            Order.part_number.label("part_number"),
            func.coalesce(func.sum(Order.amount), 0).label("total_amount"),
        )
        .filter(Order.source_type == "DELIVERY")
        .filter(Order.delivery_date >= start)
        .filter(Order.delivery_date <= end)
        .group_by(Order.part_number)
        .order_by(func.sum(Order.amount).desc())
    )

    return [
        {
            "part_number": row.part_number,
            "total_amount": float(row.total_amount or 0),
        }
        for row in q.all()
    ]



# 3. Customer-wise Sales Analysis
@router.get("/customer-wise")
def customer_wise_sales(
    financial_year: str = Query(..., example="2024-2025"),
    db: Session = Depends(get_db),
):
    start, end = parse_financial_year(financial_year)

    q = (
        db.query(
            Order.customer_name.label("customer_name"),
            func.coalesce(func.sum(Order.amount), 0).label("total_amount"),
        )
        .filter(Order.source_type == "DELIVERY")
        .filter(Order.delivery_date >= start)
        .filter(Order.delivery_date <= end)
        .group_by(Order.customer_name)
        .order_by(func.sum(Order.amount).desc())
    )

    return [
        {
            "customer_name": row.customer_name,
            "total_amount": float(row.total_amount or 0),
        }
        for row in q.all()
    ]
