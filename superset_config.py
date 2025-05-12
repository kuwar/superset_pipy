import os
from celery.schedules import crontab
from flask_caching.backends.rediscache import RedisCache
# from superset.tasks.types import FixedExecutor


# ----------------------------------------------------------------
# setting configurations for Superset
# ----------------------------------------------------------------

SECRET_KEY=os.getenv("SECRET_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")

# set related JWT configurations
JWT_COOKIE_SECURE = True
JWT_COOKIE_CSRF_PROTECT = True
JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24  # 1 day in seconds

# Superset Metadata database URI
# Set SQLite database to current directory
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'superset.db')
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/superset_metadata'
print("Database URI set to:", SQLALCHEMY_DATABASE_URI)

# For async queries specifically
GLOBAL_ASYNC_QUERIES_JWT_SECRET = os.getenv("GLOBAL_ASYNC_QUERIES_JWT_SECRET")

# Web server timeout (should be lower than your load balancer timeout)
SUPERSET_WEBSERVER_TIMEOUT = 60  # in seconds

# If running behind a proxy/load balancer that uses X-Forwarded headers
# Disable SSL
ENABLE_PROXY_FIX = False

# Optional: Disable flask-compress if not using Gunicorn
# COMPRESS_REGISTER = False

# Specify any other needed configurations
ROW_LIMIT = 5000  # Default row limit for queries

# Enable debug mode for local testing
DEBUG = True


# ************************************************************

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
    "GLOBAL_ASYNC_QUERIES": True,
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

# ************************************************************

# ----------------------------------------------------------------
# Enabling various database engines
# ----------------------------------------------------------------

# Increase timeout for database connections
SQLLAB_TIMEOUT = 60

# Enable verbose query logging
QUERY_LOGGER_VERBOSITY = 1

PREFERRED_DATABASES = [
    "PostgreSQL",
    "MySQL",
    "SQLite",
    "DuckDB",
    # other databases...
]

# ************************************************************


# ----------------------------------------------------------------
# Configure Superset to Use Redis and Celery
# ----------------------------------------------------------------
# 
# enable support for long-running queries that execute beyond the typical web request's timeout (30-60 seconds), 
# you need to configure an asynchronous backend for Superset consisting of Celery workers and a message queue (Redis) 

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_CELERY_DB = os.getenv('REDIS_CELERY_DB')
REDIS_RESULTS_DB = os.getenv('REDIS_RESULTS_DB')
REDIS_CACHE_DB = os.getenv('REDIS_CACHE_DB')  # DB for caching

# Celery Configuration
class CeleryConfig(object):
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = (
        "superset.sql_lab",
        "superset.tasks.scheduler",
        "superset.tasks.cache",  # Added for cache warming
    )
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 10
    task_acks_late = True
    task_annotations = {
        "sql_lab.get_sql_results": {
            "rate_limit": "100/s",
        },
    }
    # only the beat_schedule is relevant to alerts/reports
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=0, hour=0),
        },
    }

CELERY_CONFIG = CeleryConfig

# Results backend - where query results are stored
RESULTS_BACKEND = RedisCache(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    key_prefix='superset_results',
    db=int(REDIS_RESULTS_DB)
)

# Use MessagePack for serialization (improves performance)
# Disable results backend to troubleshoot connection issues
# Set to True when using Redis as results backend
RESULTS_BACKEND_USE_MSGPACK = True

# Cache Configuration for dashboards, filters, etc.
# Use a different Redis DB for caching
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,  # 24 hours
    'CACHE_KEY_PREFIX': 'superset_filter_cache',
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': int(REDIS_PORT),
    'CACHE_REDIS_DB': int(REDIS_CACHE_DB),
}

# Additional cache configurations
FILTER_STATE_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_filter_cache',
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_DB}'
}

EXPLORE_FORM_DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_explore_form',
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_DB}'
}

DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,  # 24 hours
    'CACHE_KEY_PREFIX': 'superset_data',
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': int(REDIS_PORT),
    'CACHE_REDIS_DB': int(REDIS_CACHE_DB), 
}

# macOS specific setting to avoid fork issues
if os.uname().sysname == 'Darwin':
    os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'


# ************************************************************

# ----------------------------------------------------------------
# Alert/Report Configurations
# ----------------------------------------------------------------

# How long to keep alert/report state before pruning
ALERT_REPORTS_WORKING_TIME_OUT_LIMIT = 3600  # 1 hour

# Configure email for sending alerts
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_MAIL_FROM = os.getenv("SMTP_MAIL_FROM")
# EMAIL_REPORTS_SUBJECT_PREFIX = "[Superset] " # optional - overwrites default value in config.py of "[Report] "

# Optionally configure Slack for notifications
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")

# Screenshots will be taken but no messages actually sent as long as ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
ALERT_REPORTS_NOTIFICATION_DRY_RUN = False
ALERT_REPORT_SLACK_V2 = True

WEBDRIVER_TYPE = "chrome"
# For macOS, specify Chrome binary path
WEBDRIVER_BINARY = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WEBDRIVER_OPTION_ARGS = [
    "--headless",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-setuid-sandbox",
    "--disable-extensions",
]

# This is for internal use, you can keep http
WEBDRIVER_BASEURL = "http://localhost:8088" # When running using docker compose use "http://superset_app:8088'
# This is the link sent to the recipient. Change to your domain, e.g. https://superset.mydomain.com
WEBDRIVER_BASEURL_USER_FRIENDLY = "http://localhost:8088"

# ALERT_REPORTS_EXECUTORS = [FixedExecutor("admin")]

# Where to store screenshots for reports
SCREENSHOT_LOCATE_WAIT = 100
SCREENSHOT_LOAD_WAIT = 600


# For creating thumbnails of dashboards for notifications
THUMBNAIL_SELENIUM_USER = os.getenv("THUMBNAIL_SELENIUM_USER")
THUMBNAIL_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_KEY_PREFIX': 'superset_thumbnails',
    'CACHE_DEFAULT_TIMEOUT': 10000,
    'CACHE_REDIS_URL': f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_DB}"
}

# *************************************************************

