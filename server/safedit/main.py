import threading
import webbrowser
from pathlib import Path

import socketio
import uvicorn

from .app import create_app
from .socket_handlers import notify_file_change, sio
from .state import state
from .watcher import start_file_watcher

DEFAULT_PORT = 5001


def start_server(path: str, tabs: int, port: int | None = None):
    """Start the FastAPI + Socket.IO server with file watching."""
    state.file_path = str(Path(path).resolve())
    port = port or DEFAULT_PORT

    watcher_thread = threading.Thread(
        target=start_file_watcher,
        args=(state.file_path, notify_file_change),
        daemon=True,
    )
    watcher_thread.start()

    for _ in range(tabs):
        webbrowser.open(f"http://localhost:{port}")

    app = create_app()
    sio_app = socketio.ASGIApp(sio, other_asgi_app=app)
    uvicorn.run(sio_app, host="127.0.0.1", port=port, reload=False)
