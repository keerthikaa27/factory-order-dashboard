from app.api.v1.auth import router as auth_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.ingestion import router as ingestion_router
from app.api.v1.orders import router as orders_router
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import Base, engine
from app.db.deps import get_db
from app.models.order import Order
from app.api.v1.ingestion import router as ingestion_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Factory Order Management API",
        version="0.1.0",
        description="Backend API for Factory Order Management Dashboard",
    )

    origins = [origin.strip() for origin in settings.CORS_ALLOWED_ORIGINS.split(",")]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup():
        Base.metadata.create_all(bind=engine)

    app.include_router(ingestion_router)
    app.include_router(orders_router)
    app.include_router(analytics_router)
    app.include_router(auth_router)



    @app.get("/")
    async def root():
        return {"message": "Factory Order Management API is running"}

    @app.get("/health")
    async def health_check():
        return {
            "status": "ok",
            "environment": settings.APP_ENV,
            "database_url": settings.DATABASE_URL,
        }

    @app.get("/debug/orders/summary")
    def orders_summary(db: Session = Depends(get_db)):
        total = db.query(func.count(Order.id)).scalar()
        pending = db.query(func.count(Order.id)).filter(Order.status == "PENDING").scalar()
        dispatched = db.query(func.count(Order.id)).filter(Order.status == "DISPATCHED").scalar()

        return {
            "total_orders": total,
            "pending_orders": pending,
            "dispatched_orders": dispatched,
        }

    @app.get("/debug/orders")
    def list_orders(limit: int = 50, db: Session = Depends(get_db)):
        orders = (
            db.query(Order)
            .order_by(Order.id.desc())
            .limit(limit)
            .all()
        )

        result = []
        for o in orders:
            result.append(
                {
                    "id": o.id,
                    "source_type": o.source_type,
                    "status": o.status,
                    "so_number": o.so_number,
                    "customer_name": o.customer_name,
                    "part_number": o.part_number,
                    "order_date": o.order_date,
                    "delivery_date": o.delivery_date,
                    "financial_year": o.financial_year,
                }
            )

        return result

    @app.get("/debug/orders/{order_id}")
    def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
        order = db.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        # Convert SQLAlchemy object to JSON-serializable dict
        return jsonable_encoder(order)



    return app


app = create_app()
