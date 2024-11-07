from pathlib import Path

# App directory
APP_DIR = Path(__file__).resolve().parent.parent

# Upload directory for data files
UPLOAD_DIR = APP_DIR / "static" / "uploads"

# Ensure upload directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".csv"} 