import socketio

from .crdt import CRDTOp
from .state import state
from .utils import safe_read_text_file

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
    import difflib

    if not state.file_path:
        print("[ERROR] No file_path set in state for file change notification!")
        return

    try:
        content, success = safe_read_text_file(state.file_path)
        if not success or content is None:
            return

        old_content = state.crdt_manager.get_content()

        if content != old_content:
            matcher = difflib.SequenceMatcher(None, old_content, content)
            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                if tag == "insert":
                    op = CRDTOp(
                        type="insert",
                        pos=i1,
                        site_id=str(state.crdt_manager.site_id),
                        value=content[j1:j2],
                    )
                    state.crdt_manager.apply_operation(op)
                    asyncio.run_coroutine_threadsafe(
                        sio.emit("crdt_op", op.to_dict()), state.main_event_loop
                    )

                elif tag == "delete":
                    op = CRDTOp(
                        type="delete",
                        pos=i1,
                        site_id=str(state.crdt_manager.site_id),
                        length=i2 - i1,
                    )
                    state.crdt_manager.apply_operation(op)
                    asyncio.run_coroutine_threadsafe(
                        sio.emit("crdt_op", op.to_dict()), state.main_event_loop
                    )

                elif tag == "replace":
                    del_op = CRDTOp(
                        type="delete",
                        pos=i1,
                        site_id=str(state.crdt_manager.site_id),
                        length=i2 - i1,
                    )
                    state.crdt_manager.apply_operation(del_op)
                    asyncio.run_coroutine_threadsafe(
                        sio.emit("crdt_op", del_op.to_dict()), state.main_event_loop
                    )
                    ins_op = CRDTOp(
                        type="insert",
                        pos=i1,
                        site_id=str(state.crdt_manager.site_id),
                        value=content[j1:j2],
                    )
                    state.crdt_manager.apply_operation(ins_op)
                    asyncio.run_coroutine_threadsafe(
                        sio.emit("crdt_op", ins_op.to_dict()), state.main_event_loop
                    )

        if state.main_event_loop:
            new_content = state.crdt_manager.get_content()
            asyncio.run_coroutine_threadsafe(
                sio.emit("file_changed", {"content": new_content}),
                state.main_event_loop,
            )
        else:
            print("[ERROR] No main event loop available!")

    except Exception as e:
        print(f"[ERROR] Could not read/write file {state.file_path}: {e}")
