import socketio

from .crdt import CRDTOp
from .state import state

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def crdt_op(sid, op):
    """Handle CRDT operation from frontend."""
    state.crdt_manager.apply_operation(CRDTOp.from_dict(op))
    with open(state.file_path, "w", encoding="utf-8") as f:
        f.write(state.crdt_manager.get_content())

    # Broadcast the op to all other clients (except sender)
    await sio.emit("crdt_op", op, skip_sid=sid)


def notify_file_change():
    """Emit file_changed event with new content when the watcher detects changes."""
    import asyncio

    if not state.file_path:
        print("[ERROR] No file_path set in state for file change notification!")
        return
    try:
        with open(state.file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Could not read file {state.file_path}: {e}")
        content = ""

    if state.main_event_loop:
        asyncio.run_coroutine_threadsafe(
            sio.emit("file_changed", {"content": content}), state.main_event_loop
        )
    else:
        print("[ERROR] No main event loop available for file change notification!")
