from pathlib import Path

# from .database import create_database, save_file, BASE_DIR
from .database import save_file

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

    for path in folder.rglob('*'):
        if path.is_file():
            file_count += 1

            save_file(
                name= path.name,
                # path= str(path),                  #'path': 'test_data\\index.db'
                path= str(path.resolve()),        # gets the absolute path
                extension= path.suffix,
                size= path.stat().st_size,
                content= extract_content(path)
            )
            print(f"Indexed: {path.name}")

    if file_count == 0:
        raise ValueError("The selected folder contains no files.")

# if __name__ == "__main__":
#     create_database()
#     scan_folder(BASE_DIR/"test_data")
