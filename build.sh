#!/usr/bin/env bash
# Build script for Render.com

set -o errexit  # Exit on error

echo "🔧 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🔍 Testing Redis connection..."
python test_redis.py || echo "⚠️ Redis test failed, will use fallback cache"

echo "🗄️ Running database migrations..."
python manage_server.py migrate

echo "📊 Loading initial data..."
# Temporarily disable Haystack signals during data loading to avoid Elasticsearch errors
export HAYSTACK_SIGNAL_PROCESSOR=haystack.signals.BaseSignalProcessor

python manage_server.py loaddata industries || echo "Industries already loaded"
python manage_server.py loaddata qualification || echo "Qualifications already loaded" 
python manage_server.py loaddata skills || echo "Skills already loaded"
python manage_server.py loaddata countries || echo "Countries already loaded"
python manage_server.py loaddata states || echo "States already loaded"
python manage_server.py loaddata cities || echo "Cities already loaded"

# Re-enable Haystack signals
unset HAYSTACK_SIGNAL_PROCESSOR

echo "📁 Collecting static files..."
python manage_server.py collectstatic --noinput

echo "✅ Build completed successfully!" 