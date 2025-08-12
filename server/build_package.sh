#!/bin/bash

# Build script for safedit package
set -e

echo "Building safedit package with frontend..."

# Change to client directory and build frontend
echo "Building frontend..."
cd ../client
npm run build

# Copy frontend assets to server static directory
echo "Copying frontend assets..."
rm -rf ../server/safedit/static/*
cp -r dist/* ../server/safedit/static/

# Change to server directory
cd ../server

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Build the package
echo "Building Python package..."
python -m build

# Check the package
echo "Checking package..."
python -m twine check dist/*

echo "Package built successfully!"
echo "Files created:"
ls -la dist/

echo ""
echo "To publish to PyPI:"
echo "  python -m twine upload dist/*"
echo ""
echo "To install locally:"
echo "  pip install dist/safedit-*.whl"