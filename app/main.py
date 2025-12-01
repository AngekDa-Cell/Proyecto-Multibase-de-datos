from fastapi import FastAPI
from .routers import postgres, mongo, redis

app = FastAPI(title="Agenda Multibase API")

# Include routers
app.include_router(postgres.router, prefix="/api", tags=["PostgreSQL"])
app.include_router(mongo.router, prefix="/api", tags=["MongoDB"])
app.include_router(redis.router, prefix="/api", tags=["Redis"])

# Startup event to verify connections (optional)
@app.on_event("startup")
async def startup_event():
    # You can add connection checks here if needed
    pass