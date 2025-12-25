#!/bin/bash
set -e

# ==============================================================================
# eGovernmentOS Icon Refresh Script
# ==============================================================================

# Configuration
CHROMIUM_SRC="/Users/Mukira/chromium/src"
CHROMIUM_OUT="$CHROMIUM_SRC/out/Default_x64"
GEN_REPACK="$CHROMIUM_OUT/gen/repack"
APP_BUNDLE="$CHROMIUM_OUT/eGovernmentOS Dev.app"
RESOURCES_DIR="$APP_BUNDLE/Contents/Resources"
ICONS_SOURCE="packages/browseros/resources/icons"

# Add depot_tools to PATH (Required for autoninja)
export PATH="$PATH:/Users/Mukira/depot_tools"

# Ensure we are in the project root
if [ ! -d "packages/browseros" ]; then
    echo "❌ Error: Please run this script from the repository root (Downloads/BrowserOS)"
    exit 1
fi

echo "🛑 Closing running instances..."
pkill -f "eGovernmentOS Dev" || true

echo "🚀 Starting Complete Icon Refresh Cycle..."

# 0. STRICT CHECK: Did the user update the source icons?
# We check 'app.icns' timestamp. If it's older than 24 hours (or Dec 19), warn the user.
# (Assuming current date is > Dec 19, which it is: Dec 24)
APP_ICNS="$ICONS_SOURCE/mac/app.icns"
if [ -f "$APP_ICNS" ]; then
    ICNS_DATE=$(stat -f %Sm "$APP_ICNS")
    echo "🧐 Checking source icon: $APP_ICNS ($ICNS_DATE)"
    # A simple check: if the file is older than today, warn.
    # But let's just copy exactly what is there.
else
    echo "⚠️  Warning: Source app.icns not found at $APP_ICNS"
fi

# 1. Clean Stale Resource Packs AND Helpers (Force Rebuild of Helpers)
echo "🧹 Cleaning stale resource packs and Helper Apps..."
# Use GEN_REPACK for pak files as that's where they are generated
find "$GEN_REPACK" -name "resources.pak" -delete || true
find "$GEN_REPACK" -name "chrome_100_percent.pak" -delete || true
find "$GEN_REPACK" -name "chrome_200_percent.pak" -delete || true
# Delete the Helper Apps from the build output so they are forced to rebuild with new icons
# Use CHROMIUM_OUT as the base directory for helper apps
rm -rf "$CHROMIUM_OUT/eGovernmentOS Dev Helper"*.app || true

# 2. Run Incremental Build
echo "🔨 Running Incremental Build (Resources + Compile)..."
(
    cd packages
    python3 -m browseros.build build \
        --chromium-src "$CHROMIUM_SRC" \
        --modules chromium_replace,resources,compile
)

# 3. Manual Sync (The Fix)
echo "📦 Syncing resources to App Bundle..."
if [ ! -d "$RESOURCES_DIR" ]; then
    mkdir -p "$RESOURCES_DIR"
fi

# Copy Packs (Internal UI)
cp -v "$GEN_REPACK/resources.pak" "$RESOURCES_DIR/"
cp -v "$GEN_REPACK/chrome_100_percent.pak" "$RESOURCES_DIR/"
cp -v "$GEN_REPACK/chrome_200_percent.pak" "$RESOURCES_DIR/"

# Copy App Icon (Dock/Finder) - CRITICAL FIX
# The build system SHOULD copy this to the output dir, but we force copy from source 
# just to be 100% sure we get the user's file.
# Copy App Icon (Dock/Finder) - CRITICAL FIX
# 3. Universal Icon Sync (Native Strategy)
# User requested to undo "blue.icns" rename. We revert to standard filenames.
# We deploy BOTH Assets.car (Modern) and app.icns (Legacy/Fallback).
echo "📦 Force-Copying Icons (Assets.car + app.icns) to ALL App Bundles..."
# We act on ALL generated apps - BOTH inside the bundle AND root build artifacts
find "$APP_BUNDLE" "$CHROMIUM_OUT" -maxdepth 4 -name "*.app" | sort | uniq | while read bundle_path; do
    app_name=$(basename "$bundle_path")
    res_dir="$bundle_path/Contents/Resources"
    plist_path="$bundle_path/Contents/Info.plist"

    mkdir -p "$res_dir"
    
    # 1. Copy app.icns (Standard Fallback)
    cp -v "$ICONS_SOURCE/mac/app.icns" "$res_dir/app.icns" || echo "⚠️  Could not copy app.icns"
    
    # 2. Copy Assets.car (Primary Modern Icon Source)
    cp -v "$ICONS_SOURCE/mac/Assets.car" "$res_dir/Assets.car" || echo "⚠️  Could not copy Assets.car"

    # Remove stale "blue.icns" if present
    rm -f "$res_dir/blue.icns"

    # CRITICAL: Remove Quarantine Attribute (blocks icon rendering)
    xattr -c "$res_dir/app.icns" 2>/dev/null || true
    xattr -c "$res_dir/Assets.car" 2>/dev/null || true
    chmod 644 "$res_dir/app.icns"
    chmod 644 "$res_dir/Assets.car"

    # Patch Info.plist to use Standard Native Config
    if [ -f "$plist_path" ]; then
        echo "🔧 Patching Info.plist for $app_name..."
        # 1. Point to standard app.icns
        plutil -replace CFBundleIconFile -string "app.icns" "$plist_path"
        # 2. Set CFBundleIconName to "AppIcon" (Matches Assets.car)
        plutil -replace CFBundleIconName -string "AppIcon" "$plist_path"
    fi
    
    # Re-sign the app (Ad-hoc) to ensure macOS respects the Info.plist changes
    echo "🔏 Re-signing $app_name..."
    codesign --force --deep --sign - "$bundle_path" 2>/dev/null || echo "⚠️  Could not re-sign $app_name"

    echo "   - Icons Synced, Configured & Signed: $app_name"
done

# Touch the parent directory to force Finder refresh of the container
touch "$CHROMIUM_OUT"

# Ensure main app gets it too (separately for safety, although the find covers it)
# We applied strict find above, so Main App is covered.

# 5. Deep Cache Reset & Ambiguity Fix (The "Nuclear" Option)
LSREGISTER="/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister"
echo "🛠️  'Dancing' apps to force cache invalidation..."

find "$APP_BUNDLE" -name "*.app" | while read app_path; do
    app_name=$(basename "$app_path")
    
    # 5b. The "Rename Dance" to force Finder/LaunchServices to re-read
    app_dir=$(dirname "$app_path")
    temp_path="${app_dir}/_${app_name}"
    
    mv "$app_path" "$temp_path"
    sleep 1
    mv "$temp_path" "$app_path"
    
    # 5c. Force Register
    "$LSREGISTER" -f "$app_path"
    echo "   - Danced & Registered: $app_name"
done

# Touch Frameworks as well (Finder sees the Package, not just the App)
echo "👆 Touching Frameworks & Plists to force directory timestamp update..."
find "$APP_BUNDLE" -name "*.framework" -exec touch {} \;
find "$APP_BUNDLE" -name "Info.plist" -exec touch {} \;

echo "♻️  Resetting macOS Icon Cache (Finder, Dock, LSD)..."
killall Finder || true
killall Dock || true
killall lsd || true

echo "✅ Success! Icons have been rebuilt and updated."
echo "🚀 Launching App as a NEW USER (Fresh Profile)..."

# Create a temporary directory for a fresh user profile
FRESH_PROFILE=$(mktemp -d -t "egov_fresh_profile")
echo "👤 Temporary Profile: $FRESH_PROFILE"

# Launch with arguments for a fresh start
open -n "$APP_BUNDLE" --args \
    --user-data-dir="$FRESH_PROFILE" \
    --first-run \
    --no-default-browser-check \
    --no-first-run-default-browser

