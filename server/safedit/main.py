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

DEFAULT_PORT = 8001


def start_server(path: str, port: int | None = None):
    """Start the FastAPI + Socket.IO server with file watching."""
    file_path = Path(path).resolve()

    if not file_path.exists():
        print(f"File does not exist. Creating new file: {file_path}")
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text("", encoding="utf-8")
        except Exception as e:
            print(f"[ERROR] Could not create file {file_path}: {e}")
            return

    state.file_path = str(file_path)
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
