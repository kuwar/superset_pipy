import os


# ----------------------------------------------------------------
# setting configurations for Superset
# ----------------------------------------------------------------

SECRET_KEY=os.getenv("SECRET_KEY", "j2PsZEfNl1ztcp+OGpVAqj8rCKVvVk8b9IYiwCCowXE89xXVC/llEFxV")
JWT_SECRET = os.getenv("JWT_SECRET", "HSCwYSIQLv+S2EJ7sOXxUvW+A7E4SpbUiRs82EkKsuf/fYzRdCgCDfN0")

# You should also set these related JWT configurations
JWT_COOKIE_SECURE = True
JWT_COOKIE_CSRF_PROTECT = True
JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24  # 1 day in seconds

# Superset Metadata database URI
# Set SQLite database to current directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'superset.db')

# For async queries specifically
GLOBAL_ASYNC_QUERIES_JWT_SECRET = os.getenv("GLOBAL_ASYNC_QUERIES_JWT_SECRET", "5D6Tw4aV5yhrXBMjLb29Y7HA7Rc6awRrgx0XKnpI8lTU4udLm0p9Jrry")

# -----------------------------------------------------------------

# ----------------------------------------------------------------
# Enabling file upload
# ----------------------------------------------------------------

ENABLE_JAVASCRIPT_CONTROLS = True
# Define allowed file extensions (expanded list)
ALLOWED_EXTENSIONS = {
    "csv",    # CSV files
    "tsv",    # Tab-separated values
    "xlsx",   # Modern Excel format
    "xls",    # Legacy Excel format
    "parquet", # Apache Parquet (columnar)
    "json",   # JSON files
    "geojson", # GeoJSON format
    "zip",    # Compressed files
    "gzip",   # Gzipped files
    "feather" # Feather format
}

# Maximum file size (in bytes) - 100MB example
FAB_API_MAX_SIZE = 100 * 1024 * 1024

# Feature flags to enable various Superset capabilities
FEATURE_FLAGS = {
    # Core file upload features
    "ENABLE_JAVASCRIPT_CONTROLS": True,
    
    # SQL Lab features
    "SQLLAB_BACKEND_PERSISTENCE": True,
    
    # Dashboard features
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True, 
    "DASHBOARD_NATIVE_FILTERS_SET": True,
    "VERSIONED_EXPORT": True,
    
    # Other useful features
    "ENABLE_TEMPLATE_PROCESSING": True,
    "GLOBAL_ASYNC_QUERIES": False,
    "ENABLE_REACT_CRUD_VIEWS": True,
    "ALLOW_FULL_CSV_EXPORT": True, 
    "ALLOW_ADHOC_SUBQUERY": True,
    
    # Experimental features (if needed)
    "EMBEDDED_SUPERSET": True,
    "ALERT_REPORTS": True
}

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.chmod(UPLOAD_FOLDER, 0o777)

# Set temporary file directory (for handling uploads)
UPLOAD_TEMP_DIRECTORY = f"{UPLOAD_FOLDER}/tmp"
os.makedirs(UPLOAD_TEMP_DIRECTORY, exist_ok=True)
os.chmod(UPLOAD_TEMP_DIRECTORY, 0o777)

# For handling various file encodings
CSV_ALLOWED_ENCODINGS = ["utf-8", "latin-1", "windows-1252"]

# Limit file upload to specific roles (optional)
UPLOAD_ROLES = ["Admin", "Alpha"]

# Set secure content security policy
CONTENT_SECURITY_POLICY = {
    "default-src": "'self'",
    "img-src": "'self' data:",
    "style-src": "'self' 'unsafe-inline'",
    "script-src": "'self' 'unsafe-inline' 'unsafe-eval'",
    "connect-src": "'self'",
}

# Validate CSV before importing
VALIDATE_TABLES = True

# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Enabling various database engines
# ----------------------------------------------------------------
# Increase timeout for database connections
SQLLAB_TIMEOUT = 60

# Enable verbose query logging
QUERY_LOGGER_VERBOSITY = 1

# Disable results backend to troubleshoot connection issues
RESULTS_BACKEND_USE_MSGPACK = False

PREFERRED_DATABASES = [
    "PostgreSQL",
    "MySQL",
    "SQLite",
    "DuckDB",
    # other databases...
]


# ----------------------------------------------------------------

