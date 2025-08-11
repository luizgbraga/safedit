from asyncio import AbstractEventLoop

from .crdt import CRDTManager


class AppState:
    crdt_manager: CRDTManager = None
    main_event_loop: AbstractEventLoop = None
    file_path: str = None


state = AppState()
