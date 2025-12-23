#!/bin/bash
set -e

# run_egovernmentos_fresh.sh
# Automates launching eGovernmentOS with a fresh profile (clears caches).
# Usage: ./scripts/run_egovernmentos_fresh.sh

# Ensure depot_tools is in PATH
export PATH="$HOME/depot_tools:$PATH"

echo "🚀 Checking for eGovernmentOS Application..."

# Clear Caches & Profile (Extensive Clean)
echo "🧹 Clearing ALL application profiles, caches, and state..."

# 1. Main Profile Data
rm -rf "$HOME/Library/Application Support/eGovernmentOS"*
rm -rf "$HOME/Library/Application Support/BrowserOS"*

# 2. Caches
rm -rf "$HOME/Library/Caches/eGovernmentOS"*
rm -rf "$HOME/Library/Caches/BrowserOS"*
rm -rf "$HOME/Library/Caches/com.browseros.dev"*

# 3. Saved Application State (Window positions, etc.)
rm -rf "$HOME/Library/Saved Application State/com.browseros.dev"*
rm -rf "$HOME/Library/Saved Application State/eGovernmentOS"*

# 4. Preferences (Plist files)
rm -f "$HOME/Library/Preferences/com.browseros.dev"*
rm -f "$HOME/Library/Preferences/eGovernmentOS"*

# 5. HTTP Storages & WebKit
rm -rf "$HOME/Library/HTTPStorages/com.browseros.dev"*
rm -rf "$HOME/Library/WebKit/com.browseros.dev"*

echo "   ✓ All data cleared (Factory Reset)"

APP_PATH="/Users/Mukira/chromium/src/out/Default_x64/eGovernmentOS Dev.app"

if [ -d "$APP_PATH" ]; then
    echo "🚀 Launching eGovernmentOS Dev..."
    open "$APP_PATH"
else
    echo "⚠️  App bundle not found at: $APP_PATH"
    echo "   Please run the build command manually first:"
    echo "   cd packages/browseros && python3 -m build.browseros build ... --modules ..."
    exit 1
fi
