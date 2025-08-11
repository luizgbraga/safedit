import threading
import webbrowser
from pathlib import Path

import socketio
import uvicorn

from .app import create_app
from .socket_handlers import notify_file_change, sio
from .state import state
from .utils import get_local_ip
from .watcher import start_file_watcher

DEFAULT_PORT = 5001


def start_server(path: str, port: int | None = None):
    """Start the FastAPI + Socket.IO server with file watching."""
    state.file_path = str(Path(path).resolve())
    port = port or DEFAULT_PORT

    watcher_thread = threading.Thread(
        target=start_file_watcher,
        args=(state.file_path, notify_file_change),
        daemon=True,
    )
    watcher_thread.start()

    local_ip = get_local_ip()
    url = f"http://{local_ip}:{port}"
    print(
        f"\n\033[97mShare this URL for others to join: \033[35m{url}\033[97m\033[0m\n"
    )
    webbrowser.open(f"http://localhost:{port}")

    app = create_app()
    sio_app = socketio.ASGIApp(sio, other_asgi_app=app)
    uvicorn.run(sio_app, host="0.0.0.0", port=port, reload=False, log_level="warning")
