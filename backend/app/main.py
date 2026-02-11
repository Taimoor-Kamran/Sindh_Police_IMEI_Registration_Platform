from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_db_and_tables
from app.routes import auth, user, mobile, transfer, admin, device_check, transfer_otp, snatch_report, reports

app = FastAPI(
    title="Sindh Police IMEI Registration System",
    description="Mobile Snatching Prevention Platform powered by Sindh Police",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(mobile.router)
app.include_router(transfer.router)
app.include_router(admin.router)
app.include_router(device_check.router)
app.include_router(transfer_otp.router)
app.include_router(snatch_report.router)
app.include_router(reports.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Sindh Police IMEI Registration System API", "version": "2.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}
