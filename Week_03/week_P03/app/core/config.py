from pathlib import Path

# Base directory of the project (week_P03)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# App directory
APP_DIR = BASE_DIR / "app"

# Upload directory for data files
UPLOAD_DIR = APP_DIR / "static" / "uploads"

# Ensure upload directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".csv"} 