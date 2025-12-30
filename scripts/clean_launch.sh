#!/bin/bash
set -e

echo "🛑 Closing running instances..."
pkill -f "eGovernmentOS Dev" || true
pkill -f "BrowserOS" || true

echo "🧹 Cleaning Application Support..."
rm -rf "$HOME/Library/Application Support/BrowserOS"
rm -rf "$HOME/Library/Application Support/eGovernmentOS"
rm -rf "$HOME/Library/Application Support/eGovernmentOS Dev"

echo "🧹 Cleaning Caches..."
rm -rf "$HOME/Library/Caches/BrowserOS"
rm -rf "$HOME/Library/Caches/eGovernmentOS"
rm -rf "$HOME/Library/Caches/com.browseros.BrowserOS"
rm -rf "$HOME/Library/Caches/com.egovernmentos.dev.eGovernmentOS"

echo "🧹 Cleaning Temporary Profiles..."
rm -rf /tmp/egov_fresh_profile.* 2>/dev/null || true
rm -rf /tmp/browseros_verification_profile 2>/dev/null || true

echo "✅ All data cleared."

CHROMIUM_OUT="/Users/Mukira/chromium/src/out/Default_x64"
APP_BUNDLE="$CHROMIUM_OUT/eGovernmentOS Dev.app"

# Create a temporary directory for a fresh user profile
FRESH_PROFILE=$(mktemp -d -t "egov_fresh_profile")
echo "👤 Fresh Temporary Profile Created: $FRESH_PROFILE"

echo "🚀 Launching App as a NEW USER..."
open -n "$APP_BUNDLE" --args \
    --user-data-dir="$FRESH_PROFILE" \
    --first-run \
    --no-default-browser-check \
    --no-first-run-default-browser \
    --enable-logging=stderr \
    --v=1

echo "Done."
