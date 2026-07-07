from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.routers import auth, circuits, events, health, lap_records, maintenance, users, vehicles

app = FastAPI(
    title="Trajectoire API",
    description="API de la plateforme Trajectoire — Module Trackdays",
    version="0.1.0",
)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    detail = str(exc.orig) if exc.orig else "Database constraint violation"
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": detail},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(vehicles.router)
app.include_router(circuits.router)
app.include_router(events.router)
app.include_router(maintenance.router)
app.include_router(lap_records.router)
