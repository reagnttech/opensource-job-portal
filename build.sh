#!/usr/bin/env bash
# Build script for Render.com

set -o errexit  # Exit on error

echo "🔧 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️ Running database migrations..."
python manage_server.py migrate

echo "📊 Loading initial data..."
python manage_server.py loaddata industries || echo "Industries already loaded"
python manage_server.py loaddata qualification || echo "Qualifications already loaded" 
python manage_server.py loaddata skills || echo "Skills already loaded"
python manage_server.py loaddata countries || echo "Countries already loaded"
python manage_server.py loaddata states || echo "States already loaded"
python manage_server.py loaddata cities || echo "Cities already loaded"

echo "📁 Collecting static files..."
python manage_server.py collectstatic --noinput

echo "✅ Build completed successfully!" 