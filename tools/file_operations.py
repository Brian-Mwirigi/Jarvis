from langchain.tools import tool
from pathlib import Path
import os
import shutil
import subprocess
import platform
from typing import Optional


REPO_ROOT = Path(__file__).resolve().parents[1]


def _safe_resolve(rel_path: str) -> Path:
    """Resolve a path relative to the repository root and prevent traversal outside it."""
    p = (REPO_ROOT / rel_path).resolve()
    try:
        p.relative_to(REPO_ROOT)
    except Exception:
        raise ValueError("Access denied: path outside repository root is not allowed")
    return p


@tool("create_file", return_direct=True)
def create_file(path: str, content: str = "") -> str:
    """Create a file at `path` (relative to project root) and write `content`.

    Example: create_file("notes/todo.txt", "Buy milk")
    """
    try:
        p = _safe_resolve(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            f.write(content)
        return f"Created file: {p.relative_to(REPO_ROOT)}"
    except Exception as e:
        return f"Error creating file: {e}"


@tool("read_file", return_direct=True)
def read_file(path: str, max_chars: Optional[int] = 2000) -> str:
    """Read a file (relative to project root). Returns up to `max_chars` characters.

    Example: read_file("notes/todo.txt")
    """
    try:
        p = _safe_resolve(path)
        if not p.exists():
            return f"File not found: {p.relative_to(REPO_ROOT)}"
        if p.is_dir():
            return f"Path is a directory: {p.relative_to(REPO_ROOT)}"
        text = p.read_text(encoding="utf-8")
        if max_chars and len(text) > max_chars:
            return text[:max_chars] + f"\n\n... (truncated, total {len(text)} chars)"
        return text
    except Exception as e:
        return f"Error reading file: {e}"


@tool("write_file", return_direct=True)
def write_file(path: str, content: str, append: bool = False) -> str:
    """Write to a file. If append=True, append; otherwise overwrite.

    Example: write_file("notes/todo.txt", "More tasks", append=True)
    """
    try:
        p = _safe_resolve(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if append else "w"
        with p.open(mode, encoding="utf-8") as f:
            f.write(content)
        return f"Wrote to file: {p.relative_to(REPO_ROOT)} (append={append})"
    except Exception as e:
        return f"Error writing file: {e}"


@tool("delete_path", return_direct=True)
def delete_path(path: str) -> str:
    """Delete a file or directory (recursively).

    Example: delete_path("notes/old.txt")
    """
    try:
        p = _safe_resolve(path)
        if not p.exists():
            return f"Not found: {p.relative_to(REPO_ROOT)}"
        if p.is_dir():
            shutil.rmtree(p)
            return f"Deleted directory: {p.relative_to(REPO_ROOT)}"
        else:
            p.unlink()
            return f"Deleted file: {p.relative_to(REPO_ROOT)}"
    except Exception as e:
        return f"Error deleting path: {e}"


@tool("list_dir", return_direct=True)
def list_dir(path: str = ".") -> str:
    """List files and directories under `path` relative to repo root.

    Example: list_dir("notes")
    """
    try:
        p = _safe_resolve(path)
        if not p.exists():
            return f"Not found: {p.relative_to(REPO_ROOT)}"
        if p.is_file():
            return f"Path is a file: {p.relative_to(REPO_ROOT)}"
        entries = []
        for child in sorted(p.iterdir()):
            t = "DIR" if child.is_dir() else "FILE"
            size = "-" if child.is_dir() else f"{child.stat().st_size} bytes"
            entries.append(f"{t:4}  {child.name:40} {size}")
        if not entries:
            return f"(empty) {p.relative_to(REPO_ROOT)}"
        header = f"Listing for {p.relative_to(REPO_ROOT)}:\n"
        return header + "\n".join(entries)
    except Exception as e:
        return f"Error listing directory: {e}"


@tool("open_application", return_direct=True)
def open_application(app_name: str) -> str:
    """Attempt to open an application by name. On Windows uses `start`, on macOS `open`, on Linux `xdg-open`.

    Example: open_application("notepad")
    """
    try:
        system = platform.system()
        # If app_name looks like a file path, try to open it
        if os.path.exists(app_name):
            if system == "Windows":
                os.startfile(app_name)
                return f"Opened: {app_name}"
            elif system == "Darwin":
                subprocess.Popen(["open", app_name])
                return f"Opened: {app_name}"
            else:
                subprocess.Popen(["xdg-open", app_name])
                return f"Opened: {app_name}"

        # Try to launch by executable name
        exe = shutil.which(app_name)
        if exe:
            subprocess.Popen([exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"Launched application: {app_name}"

        # Platform-specific fallbacks
        if system == "Windows":
            subprocess.Popen(["start", app_name], shell=True)
            return f"Tried to start (Windows start): {app_name}"
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", app_name])
            return f"Tried to open (macOS): {app_name}"
        else:
            return f"Cannot find or launch application: {app_name}"
    except Exception as e:
        return f"Error launching application: {e}"
