# Deployment Guide for Render.com

## Fixed Issues

✅ **Database Connection**: Now supports `DATABASE_URL` environment variable  
✅ **Redis Configuration**: Uses `REDIS_URL` for caching and Celery  
✅ **WSGI Configuration**: Proper initialization order  
✅ **Build Process**: Separate build script for migrations  
✅ **Static Files**: Conditional S3/local storage based on AWS credentials  
✅ **Elasticsearch**: Optional configuration with fallback to simple backend  
✅ **Local URLs**: Only loaded in debug mode (no more production warnings)  

## Render Configuration

### Environment Variables

Set these in your Render service dashboard:

```env
DATABASE_URL=postgresql://peeljobs_db_user:34@dpg-432-a.oregon-postgres.render.com/c4432xd2
REDIS_URL=redis://default:432432@grand-dd-432432d.upstash.io:6379
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=opensource-job-portal-1.onrender.com,.onrender.com
```

### Build Configuration

**Build Command:**
```bash
./build.sh
```

**Start Command:**
```bash
gunicorn jobsp.wsgi:application
```

### Required Files

- ✅ `build.sh` - Handles migrations and static files
- ✅ `manage_server.py` - Production management commands  
- ✅ `jobsp/wsgi.py` - Fixed WSGI configuration
- ✅ `requirements.txt` - Added `dj-database-url==2.3.0`

## What Was Fixed

### 1. Database Configuration

**Before:** Using individual DB_* environment variables
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),  # ❌ Empty in Render
        "USER": os.getenv("DB_USER"),  # ❌ Empty in Render
        # ...
    }
}
```

**After:** Parsing DATABASE_URL properly
```python
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}  # ✅
```

### 2. Redis Configuration  

**Before:** Only using CELERY_BROKER_URL
```python
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
```

**After:** Using REDIS_URL for both Celery and Cache
```python
REDIS_URL = os.getenv("REDIS_URL")
if REDIS_URL:
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.redis.RedisCache", "LOCATION": REDIS_URL}}
```

### 3. WSGI Initialization

**Before:** Running migrations during WSGI startup (❌ Bad practice)
```python
django.setup()  # Wrong order
# migrations here - causes connection errors
os.environ["DJANGO_SETTINGS_MODULE"] = "jobsp.settings_server"  # Too late
```

**After:** Proper initialization order
```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobsp.settings_server")  # First
application = get_wsgi_application()  # Then create app
# No migrations in WSGI
```

### 4. Settings Loading

**Before:** Always loading local settings (even in production)
```python
try:
    from .settings_local import *  # ❌ Always loaded
    print("Local development settings loaded")  # ❌ Shows in prod logs
```

**After:** Only load local settings in development
```python
if DEBUG and not DATABASE_URL:  # ✅ Conditional loading
    try:
        from .settings_local import *
```

## Testing the Fix

You can test locally with:

```bash
# Set environment variables
export DATABASE_URL=postgresql://user:pass@localhost/dbname
export REDIS_URL=redis://localhost:6379/0
export DEBUG=False

# Run build script
./build.sh

# Start server
gunicorn jobsp.wsgi:application
```

## Deployment Steps

1. **Update your Render service**:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn jobsp.wsgi:application`

2. **Set environment variables** in Render dashboard:
   - `DATABASE_URL` (from your PostgreSQL service)
   - `REDIS_URL` (from your Redis service)  
   - `DEBUG=False`
   - `SECRET_KEY` (generate a new one)

3. **Deploy**: Push your changes and trigger a new deployment

The database connection errors should be resolved! 🎉 