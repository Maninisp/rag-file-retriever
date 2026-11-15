from pathlib import Path

from database import create_database, save_file

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
    """
    Scans the specified folder and returns a list of file paths.

    Args:
        folder_path (str): The path to the folder to scan.

    Returns:
        list: A list of file paths in the specified folder.
    """
    folder = Path(folder_path)

    for path in folder.rglob('*'):
        if path.is_file():
            save_file(
                name= path.name,
                # path= str(path),                  #'path': 'test_data\\index.db'
                path= str(path.resolve()),        # gets the absolute path
                extension= path.suffix,
                size= path.stat().st_size,
                content= extract_content(path)
            )
            print(f"Indexed: {path.name}")

if __name__ == "__main__":
    create_database()
    scan_folder("test_data")
