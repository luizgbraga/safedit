# safedit

An experimental Python package and playground for building a local, collaborative text editor that merges changes from multiple frontends serving simutaneosly and your OS editor (via file watching) without losing edits or corrupting the file, via LSEQ and CRDT techniques. Used Vue.js + FastAPI.
```
pip install -e .
safedit [path]
```
