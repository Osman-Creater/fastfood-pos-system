from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"
DB_DIR = ROOT / "db"
MIGRATIONS_DIR = DB_DIR / "migrations"

def ensure_structure() -> dict[str, str]:
    dirs = [BACKEND_DIR, FRONTEND_DIR, DB_DIR, MIGRATIONS_DIR]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    return {
        "backend": str(BACKEND_DIR),
        "frontend": str(FRONTEND_DIR),
        "db": str(DB_DIR),
        "migrations": str(MIGRATIONS_DIR),
    }
