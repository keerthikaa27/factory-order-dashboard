import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime

from app.db.deps import get_db
from app.models.order import Order
from app.core.config import settings
from app.core.deps import get_current_admin




router = APIRouter(
    prefix="/ingest",
    tags=["ingestion"],
)

BASE_DATA_PATH = settings.DATA_FOLDER  # e.g. "data"


def upsert_order(db: Session, data: dict) -> Order:
    """
    Insert or update an Order row based on a natural key.
    This makes daily re-uploads idempotent.
    """

    natural_filter = {
        "source_type": data.get("source_type"),
        "so_number": data.get("so_number"),
        "order_no": data.get("order_no"),
        "po_serial": data.get("po_serial"),
        "part_number": data.get("part_number"),
        "delivery_date": data.get("delivery_date"),
    }

    query = db.query(Order).filter_by(**natural_filter)
    existing = query.first()

    if existing:
        # update existing fields (but don’t override id)
        for key, value in data.items():
            if key == "id":
                continue
            setattr(existing, key, value)
        existing.last_updated_at = datetime.utcnow()
        db.add(existing)
        return existing

    new_obj = Order(**data)
    db.add(new_obj)
    return new_obj


def detect_financial_year(date_value: datetime | None) -> str | None:
    """
    Given a date, return financial year like '2024-2025'.
    Assuming FY starts in April (month 4).
    """
    if not date_value:
        return None
    year = date_value.year
    if date_value.month >= 4:
        return f"{year}-{year + 1}"
    else:
        return f"{year - 1}-{year}"


def parse_date_safe(value):
    """
    Try to parse a date from various formats.
    Return datetime.date or None if failed.
    """
    if pd.isna(value) or value is None or str(value).strip() == "":
        return None

    # If it's already a Timestamp or datetime
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.date()

    text = str(value).strip()
    # Try common formats
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%y", "%d/%m/%y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    # Last try: pandas to_datetime
    try:
        return pd.to_datetime(text).date()
    except Exception:
        return None


def process_outstanding_row(db: Session, row) -> None:
    """
    Map one 'Sales Order Outstanding' row into Order and upsert.
    """
    def get(col_name):
        return row.get(col_name, None)

    so_date = parse_date_safe(get("S/O Date"))
    order_date = parse_date_safe(get("Order Date"))
    delivery_date = parse_date_safe(get("Delivery Date"))
    commitment_date = parse_date_safe(get("Commitment Dt"))
    packslip_date = parse_date_safe(get("Pack Slip Dt"))

    fy = detect_financial_year(order_date or so_date or delivery_date)

    data = {
        "source_type": "OUTSTANDING",
        "status": "PENDING",

        "so_number": str(get("S/O No")) if not pd.isna(get("S/O No")) else None,
        "so_date": so_date,
        "order_no": str(get("Order No")) if not pd.isna(get("Order No")) else None,
        "order_date": order_date,
        "po_serial": str(get("PO Srl")) if not pd.isna(get("PO Srl")) else None,

        "customer_name": get("Buyer Name"),
        "customer_code": str(get("Cust Code")) if not pd.isna(get("Cust Code")) else None,

        "style_no": str(get("Style No")) if not pd.isna(get("Style No")) else None,
        "item_code": str(get("Item Code")) if not pd.isna(get("Item Code")) else None,
        "drawing_no": str(get("Drg.No")) if not pd.isna(get("Drg.No")) else None,
        "size": str(get("Size")) if not pd.isna(get("Size")) else None,

        # For now, we treat Item Code as the main part number
        "part_number": str(get("Item Code")) if not pd.isna(get("Item Code")) else None,

        "order_qty": int(get("Order Qty")) if not pd.isna(get("Order Qty")) else None,
        "pack_qty": int(get("Pack Qty")) if not pd.isna(get("Pack Qty")) else None,
        "sale_qty": int(get("Sale Qty")) if not pd.isna(get("Sale Qty")) else None,
        "cancel_qty": int(get("Cncl.Qty")) if not pd.isna(get("Cncl.Qty")) else None,
        "os_order_qty": int(get("O/S Ord.Qty")) if not pd.isna(get("O/S Ord.Qty")) else None,

        "unit": str(get("Unit")) if not pd.isna(get("Unit")) else None,

        "rate": float(get("Rate")) if not pd.isna(get("Rate")) else None,
        "gross_value": float(get("Gross Value")) if not pd.isna(get("Gross Value")) else None,
        "currency": str(get("Currency")) if not pd.isna(get("Currency")) else None,
        "currency_value": float(get("Currency Value")) if not pd.isna(get("Currency Value")) else None,

        "delivery_date": delivery_date,
        "commitment_date": commitment_date,

        "packslip_no": str(get("Pack Slip No")) if not pd.isna(get("Pack Slip No")) else None,
        "packslip_date": packslip_date,

        "department": str(get("Department")) if not pd.isna(get("Department")) else None,
        "department_remark": str(get("Dept.Remark")) if not pd.isna(get("Dept.Remark")) else None,

        "payment_term": str(get("Payment Term")) if not pd.isna(get("Payment Term")) else None,
        "so_comment": str(get("S.O Comment")) if not pd.isna(get("S.O Comment")) else None,
        "so_special_remark": str(get("SO SPL.Remark")) if not pd.isna(get("SO SPL.Remark")) else None,
        "die_indent": str(get("DIE Indend")) if not pd.isna(get("DIE Indend")) else None,

        "item_description": str(get("Item Description")) if not pd.isna(get("Item Description")) else None,

        "financial_year": fy,
    }

    upsert_order(db, data)


def process_delivery_row(db: Session, row) -> None:
    """
    Map one 'Delivery Report' row into Order and upsert.
    """
    def get(col_name):
        return row.get(col_name, None)

    so_date = parse_date_safe(get("S.O Date"))
    order_date = parse_date_safe(get("Order Dt."))
    delivery_date = parse_date_safe(get("Delv Date"))
    invoice_date = parse_date_safe(get("Date"))
    docket_date = parse_date_safe(get("Docket Dt"))
    packslip_date = parse_date_safe(get("Pack Slip Dt"))

    fy = detect_financial_year(order_date or so_date or delivery_date or invoice_date)

    packslip_no = None
    if not pd.isna(get("Packslip No & Date")):
        text = str(get("Packslip No & Date"))
        packslip_no = text  # you can later split by space or '/' if format is consistent

    data = {
        "source_type": "DELIVERY",
        "status": "DISPATCHED",

        "so_number": str(get("S.O No")) if not pd.isna(get("S.O No")) else None,
        "so_date": so_date,
        "order_no": str(get("Order No")) if not pd.isna(get("Order No")) else None,
        "order_date": order_date,
        "po_serial": str(get("P Srl")) if not pd.isna(get("P Srl")) else None,

        "customer_name": get("Party Name"),
        "customer_code": str(get("Cust Code")) if not pd.isna(get("Cust Code")) else None,

        "met_code": str(get("Met Code")) if not pd.isna(get("Met Code")) else None,
        "product_code": str(get("Produce Code")) if not pd.isna(get("Produce Code")) else None,
        "drawing_no": str(get("Drg.No")) if not pd.isna(get("Drg.No")) else None,
        "size": str(get("Size")) if not pd.isna(get("Size")) else None,

        # For delivery, we treat Produce Code as main part number
        "part_number": str(get("Produce Code")) if not pd.isna(get("Produce Code")) else None,

        "quantity": int(get("Quantity")) if not pd.isna(get("Quantity")) else None,
        "unit": str(get("Unit")) if not pd.isna(get("Unit")) else None,
        "net_kg": float(get("Net (Kg)")) if not pd.isna(get("Net (Kg)")) else None,
        "part_full": str(get("Part/Full")) if not pd.isna(get("Part/Full")) else None,

        "rate": float(get("Rate")) if not pd.isna(get("Rate")) else None,
        "amount": float(get("Amount")) if not pd.isna(get("Amount")) else None,
        "freight_amount": float(get("Frt.Amount")) if not pd.isna(get("Frt.Amount")) else None,

        "packslip_no": packslip_no,
        "packslip_date": packslip_date,

        "invoice_no": str(get("Invoice No")) if not pd.isna(get("Invoice No")) else None,
        "invoice_date": invoice_date,

        "transporter": str(get("Transporter")) if not pd.isna(get("Transporter")) else None,
        "docket_no": str(get("Docket No")) if not pd.isna(get("Docket No")) else None,
        "docket_date": docket_date,

        "freight_mode": str(get("Frt.Mode")) if not pd.isna(get("Frt.Mode")) else None,
        "from_station": str(get("From Station")) if not pd.isna(get("From Station")) else None,
        "to_station": str(get("To Station")) if not pd.isna(get("To Station")) else None,
        "package_details": str(get("Package Details")) if not pd.isna(get("Package Details")) else None,
        "gross_weight": float(get("Gross Wt")) if not pd.isna(get("Gross Wt")) else None,
        "charge_weight": float(get("Charge Wt.")) if not pd.isna(get("Charge Wt.")) else None,
        "insurance_mode": str(get("Insurance Mode")) if not pd.isna(get("Insurance Mode")) else None,

        "delivery_date": delivery_date,
        "department": str(get("Department")) if not pd.isna(get("Department")) else None,
        "state_code": str(get("State Code")) if not pd.isna(get("State Code")) else None,

        "sub_head": str(get("Sub Head")) if not pd.isna(get("Sub Head")) else None,
        "item_description": str(get("Description")) if not pd.isna(get("Description")) else None,

        "financial_year": fy,
    }

    upsert_order(db, data)


@router.post("/outstanding-csv")
async def ingest_outstanding_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),
):
    """
    Ingest 'Sales Order Outstanding' CSV uploaded by client.
    """
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file")

    try:
        # Read CSV into DataFrame
        df = pd.read_csv(file.file)

        # Normalize column names: strip spaces
        df.columns = [col.strip() for col in df.columns]

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {e}")

    rows_processed = 0

    for _, row in df.iterrows():
        process_outstanding_row(db, row)
        rows_processed += 1

    db.commit()

    return {"status": "success", "rows_processed": rows_processed}


@router.post("/delivery-csv")
async def ingest_delivery_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),
):
    """
    Ingest 'Delivery Report' CSV uploaded by client.
    """

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file")

    try:
        df = pd.read_csv(file.file)
        df.columns = [col.strip() for col in df.columns]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {e}")

    rows_processed = 0

    for _, row in df.iterrows():
        process_delivery_row(db, row)
        rows_processed += 1

    db.commit()

    return {"status": "success", "rows_processed": rows_processed}


@router.post("/from-folder")
def ingest_from_folder(db: Session = Depends(get_db)):
    admin = Depends(get_current_admin),
    """
    Ingest Outstanding + Delivery data from local folder structure.

    Expects:
      <BASE_DATA_PATH>/outstanding/*.xlsx or *.csv
      <BASE_DATA_PATH>/delivery/*.xlsx or *.csv

    Example:
      data/outstanding/sales_outstanding.xlsx
      data/delivery/delivery_report.xlsx
    """
    outstanding_dir = os.path.join(BASE_DATA_PATH, "outstanding")
    delivery_dir = os.path.join(BASE_DATA_PATH, "delivery")

    processed = {"outstanding": 0, "delivery": 0}

    # Ensure base dirs exist (won't crash if missing; just skip)
    os.makedirs(outstanding_dir, exist_ok=True)
    os.makedirs(delivery_dir, exist_ok=True)

    def read_table(path: str) -> pd.DataFrame:
        if path.lower().endswith(".csv"):
            df_local = pd.read_csv(path)
        else:
            # assume Excel
            df_local = pd.read_excel(path)
        df_local.columns = [col.strip() for col in df_local.columns]
        return df_local

    # Outstanding files
    for file_name in os.listdir(outstanding_dir):
        if not (file_name.lower().endswith(".csv") or file_name.lower().endswith(".xlsx") or file_name.lower().endswith(".xls")):
            continue
        file_path = os.path.join(outstanding_dir, file_name)
        df = read_table(file_path)
        for _, row in df.iterrows():
            process_outstanding_row(db, row)
            processed["outstanding"] += 1

    # Delivery files
    for file_name in os.listdir(delivery_dir):
        if not (file_name.lower().endswith(".csv") or file_name.lower().endswith(".xlsx") or file_name.lower().endswith(".xls")):
            continue
        file_path = os.path.join(delivery_dir, file_name)
        df = read_table(file_path)
        for _, row in df.iterrows():
            process_delivery_row(db, row)
            processed["delivery"] += 1

    db.commit()

    return {"status": "success", "processed": processed, "base_path": BASE_DATA_PATH}
