from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database import engine, Base
from src.users.router import router as user_router

# IMPORTANT: Import order matters for cross-references
# Import schemas to trigger Pydantic model rebuilding for forward references
# This resolves "TicketResponseSchema" string reference in UserResponseSchema
import src.schemas

# Import all models together to resolve SQLAlchemy relationships  
# This allows User.tickets relationship to find the Ticket class
import src.models


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Ticketing System", lifespan=lifespan)

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=True)
