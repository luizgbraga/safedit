import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .crdt import CRDTManager
from .state import state


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize CRDT manager and store event loop on startup."""
    state.main_event_loop = asyncio.get_running_loop()

    file_path = Path(state.file_path) if state.file_path else None
    state.crdt_manager = CRDTManager(file_path)

    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/file")
    async def get_file():
        return {"content": state.crdt_manager.get_content()}

    return app
