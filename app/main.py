from fastapi import FastAPI
from .routers import postgres  # Assuming routers are in app/routers/

app = FastAPI(title="Agenda Multibase API")

# Include routers
app.include_router(postgres.router, prefix="/api", tags=["PostgreSQL"])

# Startup event to verify connections (optional)
@app.on_event("startup")
async def startup_event():
    # You can add connection checks here if needed
    pass