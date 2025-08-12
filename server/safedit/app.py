import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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

    static_dir = Path(__file__).parent / "static"

    if static_dir.exists():
        app.mount(
            "/assets", StaticFiles(directory=static_dir / "assets"), name="assets"
        )

    @app.get("/api/file")
    async def get_file():
        return {"content": state.crdt_manager.get_content()}

    @app.get("/", response_class=FileResponse)
    async def serve_frontend():
        """Serve the main frontend HTML file."""
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        return {"message": "Frontend not built yet. Please build the client first."}

    @app.get("/{path:path}")
    async def serve_static_files(path: str):
        """Serve static files and fallback to index.html for SPA routing."""
        file_path = static_dir / path

        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)

        # For SPA routing, serve index.html for non-API routes
        if not path.startswith("api/"):
            index_path = static_dir / "index.html"
            if index_path.exists():
                return FileResponse(index_path)

        return {"message": "File not found"}

    return app
