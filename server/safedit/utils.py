import socket
from pathlib import Path
from typing import Optional, Tuple, Union


def safe_read_text_file(file_path: Union[str, Path]) -> Tuple[Optional[str], bool]:
    """
    Safely read a text file with multiple encoding fallbacks.

    Args:
        file_path: Path to the file to read

    Returns:
        Tuple of (content, success):
        - content: File content as string, or None if failed
        - success: True if file was read successfully, False otherwise
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    try:
        with open(file_path, "rb") as f:
            sample = f.read(8000)
            if b"\0" in sample:
                print(
                    f"[WARNING] File {file_path} appears to be binary and cannot be edited as text"
                )
                return None, False

        # Try multiple encodings to handle Windows/cross-platform files
        encodings_to_try = ["utf-8", "utf-8-sig", "cp1252", "latin1", "ascii"]

        for encoding in encodings_to_try:
            try:
                if isinstance(file_path, Path):
                    content = file_path.read_text(encoding=encoding)
                else:
                    with open(file_path, "r", encoding=encoding) as f:
                        content = f.read()
                return content, True
            except UnicodeDecodeError:
                continue
        else:
            with open(file_path, "rb") as f:
                raw_content = f.read()
                content = raw_content.decode("utf-8", errors="replace")
                print(
                    f"[WARNING] File {file_path} contains invalid characters, some may display incorrectly"
                )
                return content, True

    except Exception as e:
        print(f"[ERROR] Could not read file {file_path}: {e}")
        return None, False


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP
