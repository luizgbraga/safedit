# safedit

A Python library and CLI for demonstrating multi-client collaborative editing of a file, with a Vue.js/Monaco frontend and custom CRDT logic.

## Quickstart

### 1. Install Python dependencies

```sh
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install the safedit package (editable mode for development)

```sh
pip install -e .
```

### 3. Install frontend dependencies

```sh
cd ../client
npm install
```

### 4. Run safedit

```sh
cd ../server
safedit /path/to/your/file.txt 3
```

This will start the backend and open 3 browser tabs (ports 5001, 5002, 5003) for collaborative editing.

### 5. Start the frontend (for development)

In each client tab, you can run:

```sh
npm run dev -- --port=5001
npm run dev -- --port=5002
npm run dev -- --port=5003
```

Or let the CLI open the tabs for you.

---

- The backend uses FastAPI, Typer, Watchdog, and custom CRDT logic (no external CRDT libs).
- The frontend uses Vue 3, Vite, Monaco Editor, and Socket.IO.

## TODO
- Implement CRDT (LSEQ, etc.) logic in Python
- Implement WebSocket sync endpoints
- Implement frontend sync logic
- Add tests and more features
