from pathlib import Path

PROJECT_MARKERS = {
    "pyproject.toml",
    "setup.py",
    "package.json",
    "Cargo.toml",
    "go.mod",
    ".git",
}


def detect_project_root(file_path, search_root):
    path = Path(file_path).resolve()
    search_root = Path(search_root).resolve()

    if not path.is_relative_to(search_root):
        return None

    for folder in path.parents:
        if any(
            (folder / marker).exists()
            for marker in PROJECT_MARKERS
        ):
            return folder

        if folder == search_root:
            break

    return None