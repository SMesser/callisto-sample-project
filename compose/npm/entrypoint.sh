#!/bin/bash
set -e

echo "Installing npm dependencies..."
npm install --silent
echo "Rebuilding node-sass..."
npm rebuild node-sass
echo "Running npm command"
exec npm "$@"
