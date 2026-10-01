from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.admin import router as admin_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.auth import router as auth_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.food_cost import router as food_cost_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.manager import router as manager_router
from app.api.routes.orders import router as orders_router
from app.api.routes.reports import router as reports_router
from app.api.routes.shifts import router as shifts_router

app = FastAPI(
    title="FastFood POS + Bookkeeping API",
    description="Multi-location fast-food POS, inventory, and accounting backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")
app.include_router(inventory_router, prefix="/api/v1")
app.include_router(food_cost_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")
app.include_router(shifts_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(manager_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "fastfood-pos-api"}

@app.get("/")
def root():
    return {"message": "FastFood POS + Bookkeeping API is running"}
