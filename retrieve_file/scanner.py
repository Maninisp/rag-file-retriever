import os
from pathlib import Path

from .database import save_file

IGNORED_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".idea",
}

MAX_FILE_SIZE_MB = 10  # Set to None to disable

def extract_content(path):
    allowed_extensions = {'.txt', '.md', '.py', '.json', '.csv'}

    if path.suffix.lower() not in allowed_extensions:
        return None

    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeError, OSError) as e:
        print(f"Could not read {path}: {e}")
        return None


def scan_folder(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(
            f"Folder does not exist: {folder}"
        )

    if not folder.is_dir():
        raise NotADirectoryError(
            f"Expected a directory: {folder}"
        )

    file_count = 0

    for current_dir, dirs, files in os.walk(folder):
        # Skip generated directories and Python virtual environments
        dirs[:] = [
            d for d in dirs
            if d not in IGNORED_DIRS
            and not (Path(current_dir) / d / "pyvenv.cfg").is_file()
        ]

        for filename in files:
            path = Path(current_dir) / filename
            file_size = path.stat().st_size

            if MAX_FILE_SIZE_MB is not None:
                if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
                    print(f"Skipped (too large): {path.name}")
                    continue

            file_count += 1

            save_file(
                name=path.name,
                path=str(path.resolve()),
                extension=path.suffix,
                size=file_size,
                content=extract_content(path)
            )

            print(f"Indexed: {path.name}")

    if file_count == 0:
        raise ValueError("The selected folder contains no files.")

