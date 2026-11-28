from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DB_PATH = DATA_DIR / "index.db"
INDEX_PATH = DATA_DIR / "files.index"
IDS_PATH = DATA_DIR / "file_ids.npy"