"""Top-level package for Smf2db."""
# smf2db/__init__.py

__app_name__ = "smf2db"
__version__ = "0.1.1"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    UPLOAD_ERROR,
    DB_CONNECTION_ERROR,
) = range(8)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    JSON_ERROR: "Invalid JSON format error",
    UPLOAD_ERROR: "uploading error",
    DB_CONNECTION_ERROR: "database connection error",
}

DEFAULT_DB_HOST = 'localhost'
DEFAULT_DB_PORT = 5432
DEFAULT_DB_USER = 'postgres'