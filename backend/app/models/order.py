from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Float,
)
from sqlalchemy.sql import func

from app.db.session import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    # Source and status
    source_type = Column(String, index=True, nullable=False)  # "OUTSTANDING" or "DELIVERY"
    status = Column(String, index=True, nullable=True)        # "PENDING" or "DISPATCHED"

    # Common identifiers
    so_number = Column(String, index=True, nullable=True)     # S/O No
    so_date = Column(Date, nullable=True)

    order_no = Column(String, index=True, nullable=True)      # Order No
    order_date = Column(Date, nullable=True)

    po_serial = Column(String, index=True, nullable=True)     # PO Srl / P Srl

    # Customer info
    customer_name = Column(String, index=True, nullable=True) # Buyer Name / Party Name
    customer_code = Column(String, index=True, nullable=True) # Cust Code

    # Item / product details
    style_no = Column(String, index=True, nullable=True)      # Style No (Outstanding)
    item_code = Column(String, index=True, nullable=True)     # Item Code (Outstanding)
    met_code = Column(String, index=True, nullable=True)      # Met Code (Delivery)
    product_code = Column(String, index=True, nullable=True)  # Produce Code (Delivery)
    drawing_no = Column(String, index=True, nullable=True)    # Drg.No
    size = Column(String, index=True, nullable=True)          # Size

    # For unified search, we can later fill this with whichever code is main "part number"
    part_number = Column(String, index=True, nullable=True)   # e.g. 707, derived from item_code/product_code/etc.

    # Quantities
    order_qty = Column(Integer, nullable=True)                # Order Qty (Outstanding)
    pack_qty = Column(Integer, nullable=True)                 # Pack Qty (Outstanding)
    sale_qty = Column(Integer, nullable=True)                 # Sale Qty (Outstanding)
    cancel_qty = Column(Integer, nullable=True)               # Cncl.Qty (Outstanding)
    os_order_qty = Column(Integer, nullable=True)             # O/S Ord.Qty (Outstanding)
    quantity = Column(Integer, nullable=True)                 # Quantity (Delivery)

    unit = Column(String, nullable=True)                      # Unit (both)

    net_kg = Column(Float, nullable=True)                     # Net (Kg) (Delivery)
    part_full = Column(String, nullable=True)                 # Part/Full (Delivery)

    # Money
    rate = Column(Float, nullable=True)                       # Rate (both)
    amount = Column(Float, nullable=True)                     # Amount (Delivery)
    gross_value = Column(Float, nullable=True)                # Gross Value (Outstanding)
    currency = Column(String, nullable=True)                  # Currency (Outstanding)
    currency_value = Column(Float, nullable=True)             # Currency Value (Outstanding)
    freight_amount = Column(Float, nullable=True)             # Frt.Amount (Delivery)

    # Dates related to delivery/commitment
    delivery_date = Column(Date, nullable=True)               # Delivery Date / Delv Date
    commitment_date = Column(Date, nullable=True)             # Commitment Dt (Outstanding)

    # Invoicing / documents
    packslip_no = Column(String, index=True, nullable=True)   # Pack Slip No / Packslip No
    packslip_date = Column(Date, nullable=True)               # Pack Slip Dt
    invoice_no = Column(String, index=True, nullable=True)    # Invoice No (Delivery)
    invoice_date = Column(Date, nullable=True)                # Date (invoice date in Delivery)
    docket_no = Column(String, nullable=True)                 # Docket No (Delivery)
    docket_date = Column(Date, nullable=True)                 # Docket Dt (Delivery)

    # Transport / logistics
    transporter = Column(String, nullable=True)               # Transporter
    freight_mode = Column(String, nullable=True)              # Frt.Mode
    from_station = Column(String, nullable=True)              # From Station
    to_station = Column(String, nullable=True)                # To Station
    package_details = Column(String, nullable=True)           # Package Details
    gross_weight = Column(Float, nullable=True)               # Gross Wt
    charge_weight = Column(Float, nullable=True)              # Charge Wt.
    insurance_mode = Column(String, nullable=True)            # Insurance Mode

    # Department / state / misc
    department = Column(String, index=True, nullable=True)    # Department
    department_remark = Column(String, nullable=True)         # Dept.Remark
    state_code = Column(String, nullable=True)                # State Code
    payment_term = Column(String, nullable=True)              # Payment Term
    so_comment = Column(String, nullable=True)                # S.O Comment
    so_special_remark = Column(String, nullable=True)         # SO SPL.Remark
    die_indent = Column(String, nullable=True)                # DIE Indend

    sub_head = Column(String, nullable=True)                  # Sub Head (Delivery)

    # Descriptions
    item_description = Column(String, nullable=True)          # Item Description / Description

    # Calculated / meta
    financial_year = Column(String, index=True, nullable=True) # e.g. "2024-2025"

    last_updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
