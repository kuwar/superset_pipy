### Random key
openssl rand -base64 42

### Start Celery Workers
celery --app=superset.tasks.celery_app:app worker --pool=prefork -O fair -c 4

### Start Celery Beat (Optional, for Scheduled Tasks)
celery --app=superset.tasks.celery_app:app beat

**NOTE:** It's important that all worker nodes and web servers in your Superset cluster share a 
common metadata database, and that there is only one instance of celery beat running in your entire 
setup. Otherwise, background jobs might get scheduled multiple times.
