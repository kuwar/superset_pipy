# Troubleshooting Apache Superset with DuckDB

This document covers common issues and solutions when setting up and using Apache Superset with DuckDB as a data source.

## Table of Contents
1. [Superset Setup Issues](#superset-setup-issues)
2. [File Upload Configuration](#file-upload-configuration)
3. [DuckDB Integration Issues](#duckdb-integration-issues)
4. [MotherDuck vs. Local DuckDB](#motherduck-vs-local-duckdb)
5. [Connection String Formats](#connection-string-formats)
6. [Engine Parameters](#engine-parameters)
7. [Advanced Troubleshooting](#advanced-troubleshooting)

## Superset Setup Issues

### Configuration File Detection
- **Issue**: Superset fails to detect `superset_config.py`
- **Solution**: Export the path before running database upgrade
```bash
export SUPERSET_CONFIG_PATH=/path/to/your/superset_config.py
```

### Flask Application Location
- **Issue**: Error message "Could not locate a Flask application"
- **Solution**: Set the Flask application environment variable
```bash
export FLASK_APP=superset
```

### Dependency Issues
- **Issue**: Marshmallow version 4 incompatibility
- **Solution**: Downgrade to Marshmallow 3.26.1
```bash
pip install marshmallow==3.26.1
```

- **Issue**: "No PIL" warning
- **Solution**: Install Pillow library
```bash
pip install pillow
```

### Async Query Configuration
- **Issue**: `AsyncQueryTokenException: Please provide a JWT secret at least 32 bytes long`
- **Solution**: Set appropriate JWT tokens in `superset_config.py`
```python
# Add to superset_config.py
import os
from flask import Flask
SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "your-secret-key-at-least-32-bytes-long")
```

- **Issue**: Dashboard keeps loading when async queries are enabled
- **Solution**: Async queries require Redis for result querying and storage. Either:
  - Configure Redis properly, or
  - Set `GLOBAL_ASYNC_QUERIES = False` in `superset_config.py`

### File Upload Permissions
- **Issue**: "Enable 'Allow file uploads to database' in any database's settings"
- **Solution**: You must enable file upload for each database individually under the Security tab in the database settings

## File Upload Configuration

1. Install required packages:
```bash
pip install pandas xlrd openpyxl pyarrow
```

2. Add necessary settings in `superset_config.py`:
```python
# Allow file uploads for databases that support it
FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "ENABLE_JAVASCRIPT_CONTROLS": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DASHBOARD_NATIVE_FILTERS_SET": True,
    "EMBEDDABLE_CHARTS": True,
    "EMBEDDED_SUPERSET": True,
    "GLOBAL_ASYNC_QUERIES": False,  # Set to False to avoid Redis dependency
    "SQLLAB_BACKEND_PERSISTENCE": True,
    "THUMBNAILS": True,
    "ALLOW_ADHOC_SUBQUERY": True,
}

# File upload settings
UPLOAD_FOLDER = '/path/to/upload/folder'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'parquet'}
```

## DuckDB Integration Issues

### Installation
Install required packages:
```bash
pip install duckdb duckdb-engine
```

### Connection Testing Issues
- **Issue**: Infinite loading when testing the DuckDB connection
- **Root Cause**: DuckDB's automatic extension loading mechanism attempts to load the MotherDuck extension, causing connection issues
- **Solution**: Use proper connection string format and disable extension loading (see sections below)

## MotherDuck vs. Local DuckDB

### What is MotherDuck?
MotherDuck is a cloud-based analytics platform built on top of DuckDB. Recent versions of DuckDB automatically include the MotherDuck extension, which can cause issues when you're trying to use local DuckDB files.

### Common Symptoms of MotherDuck Issues:
- Error messages about authentication or token validation
- Error messages containing "motherduck_init"
- Infinite loading during connection tests without error messages
- Error: "Request failed: Your request is not authenticated. Please check your MotherDuck token"

## Connection String Formats

### Local DuckDB File (Absolute Path)
```
duckdb:///absolute/path/to/your/file.duckdb
```
Example:
```
duckdb:///Users/sauravkuwar/Documents/GIT/superset_pipy/_dw.duckdb
```

### Local DuckDB File (Relative Path)
Relative to the directory containing `superset_config.py`:
```
duckdb:///relative/path/to/file.duckdb
```
Example:
```
duckdb:///_dw.duckdb
```

### In-Memory Database
```
duckdb:///:memory:
```

### Important Connection String Notes:
- Use exactly THREE slashes (///) for local file paths
- Ensure the path is correct and the file exists
- Do not include "md:" in the path (this triggers MotherDuck connection)

## Engine Parameters

### Basic Configuration with Read-Only Mode
```json
{
  "connect_args": {
    "read_only": true
  }
}
```

### Disable Extension Loading (Recommended)
```json
{
  "connect_args": {
    "read_only": true,
    "disable_extension_loading": true
  }
}
```

### With Thread Configuration
```json
{
  "connect_args": {
    "read_only": true,
    "disable_extension_loading": true,
    "config": {
      "threads": 8
    }
  }
}
```

### Disable Autoloading Extensions
```json
{
  "connect_args": {
    "read_only": true,
    "config": {
      "autoinstall_known_extensions": false,
      "autoload_known_extensions": false
    }
  }
}
```

### Minimal In-Memory Configuration
```json
{"connect_args":{}}
```

## Advanced Troubleshooting

### Clear DuckDB Extensions Cache
If you continue to experience issues with MotherDuck extension, you can remove the extensions cache:
```bash
rm -rf ~/.duckdb/extensions
```

### Verify DuckDB File Validity
Check if your DuckDB file is valid:
```bash
duckdb /path/to/your/file.duckdb
```
If it opens successfully, the file is valid.

### Error Logs to Look For
- `duckdb.duckdb.InvalidInputException: Invalid Input Error: No open result set`
- `"DB engine Error This may be triggered by: Issue 1011 - Superset encountered an unexpected error"`
- `Invalid Input Error: Initialization function "motherduck_init" from file`
- `Your request is not authenticated. Please check your MotherDuck token`

### Connection Debugging
If none of the above solutions work, try enabling debug mode in Superset:
```bash
superset run -d
```

This will provide more detailed logs that might reveal what's happening during the connection test.

## Common Pitfalls to Avoid

1. **Using the wrong number of slashes in connection strings**
   - Three slashes (///) for local files
   - Four slashes (////) might be interpreted differently

2. **Missing or incorrect engine parameters**
   - Always include `"read_only": true` to avoid concurrency issues
   - Consider adding `"disable_extension_loading": true` to prevent MotherDuck interference

3. **Not clearing DuckDB extension cache after issues**
   - The ~/.duckdb/extensions directory may contain cached extensions causing problems

4. **Using a connection string that triggers MotherDuck**
   - Avoid using "md:" in your connection string
   - Avoid using URLs that look like cloud resources

5. **DuckDB version mismatches**
   - Ensure your duckdb and duckdb-engine packages are compatible versions