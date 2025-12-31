#!/bin/bash
set -e

# ==============================================================================
# Bundle BrowserOS Server with Browser
# ==============================================================================
# This script packages the BrowserOS server to run natively within the browser

# Configuration
CHROMIUM_OUT="/Users/Mukira/chromium/src/out/Default_x64"
APP_BUNDLE="$CHROMIUM_OUT/eGovernmentOS Dev.app"
RESOURCES_BASE="$APP_BUNDLE/Contents/Resources"
SERVER_BUNDLE="$RESOURCES_BASE/BrowserOSServer/default"
SERVER_SOURCE="/Users/Mukira/Downloads/BrowserOS/BrowserOS-agent"

# Check if app bundle exists
if [ ! -d "$APP_BUNDLE" ]; then
    echo "❌ Error: App bundle not found at $APP_BUNDLE"
    echo "   Please build the browser first using fix_icons.sh"
    exit 1
fi

# Check if server source exists
if [ ! -d "$SERVER_SOURCE" ]; then
    echo "❌ Error: Server source not found at $SERVER_SOURCE"
    exit 1
fi

echo "🚀 Bundling BrowserOS Server with Browser..."

# Create directory structure
echo "📁 Creating bundle directories..."
mkdir -p "$SERVER_BUNDLE/resources/bin"

# Build the server
echo "🔨 Building BrowserOS server from monorepo..."
cd "$SERVER_SOURCE"

# Check if Bun is installed
if ! command -v bun &> /dev/null; then
    echo "❌ Error: Bun runtime not found"
    echo "   Install from: https://bun.sh"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing server dependencies..."
    bun install
fi

# Build the server as a standalone binary
# TARGET: bun-darwin-arm64 (since user is on Mac ARM)
# ENTRY: apps/server/src/index.ts (Monorepo structure)
echo "🏗️  Compiling standalone server binary..."

# Detect Architecture
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    TARGET="bun-darwin-arm64"
else
    TARGET="bun-darwin-x64"
fi
echo "   Detected Architecture: $ARCH -> Target: $TARGET"

# Use --env inline to bake in env vars
# FORCE NODE_ENV=production to avoid loading pino-pretty
NODE_ENV=production bun build apps/server/src/index.ts \
    --compile \
    --outfile "$SERVER_BUNDLE/resources/bin/browseros_server" \
    --target "$TARGET" \
    --minify \
    --external "*?binary" \
    --external "node-pty"
    # pino-pretty is NOT needed in production (NODE_ENV=production)

# Make executable
chmod +x "$SERVER_BUNDLE/resources/bin/browseros_server"

# Copy runtime dependencies (ONLY node-pty is needed now)
echo "📦 Installing runtime dependencies (node-pty)..."
TEMP_BUILD_DIR="dist/temp_build"
rm -rf "$TEMP_BUILD_DIR"
mkdir -p "$TEMP_BUILD_DIR"

# Create a minimal package.json for runtime deps
(
    cd "$TEMP_BUILD_DIR"
    bun init -y
    # Use trusted installs for native modules
    bun add node-pty --trust
)

mkdir -p "$SERVER_BUNDLE/resources/bin/node_modules"
cp -R "$TEMP_BUILD_DIR/node_modules/"* "$SERVER_BUNDLE/resources/bin/node_modules/"

# Cleanup
rm -rf "$TEMP_BUILD_DIR"

# Copy resources directory (if needed by server)
# In monorepo, resources might be in apps/server/resources or just copied
echo "📋 Copying server resources..."
if [ -d "apps/server/resources" ]; then
    cp -r "apps/server/resources/"* "$SERVER_BUNDLE/resources/" 2>/dev/null || true
fi

# Copy default config if available, renaming to config.json
if [ -f "apps/server/config.sample.json" ]; then
    echo "⚙️  Copying default configuration..."
    cp "apps/server/config.sample.json" "$SERVER_BUNDLE/resources/config.json"
fi

# Verify the binary
if [ ! -f "$SERVER_BUNDLE/resources/bin/browseros_server" ]; then
    echo "❌ Error: Failed to create server binary"
    exit 1
fi

BINARY_SIZE=$(du -h "$SERVER_BUNDLE/resources/bin/browseros_server" | cut -f1)
echo "✅ Server binary created: $BINARY_SIZE"

# Test the binary
echo "🧪 Testing server binary..."
"$SERVER_BUNDLE/resources/bin/browseros_server" --help &> /dev/null && \
    echo "✅ Server binary is valid" || \
    echo "⚠️  Warning: Server binary may not be functioning correctly"

echo ""
echo "✅ SUCCESS! BrowserOS Server bundled successfully"
echo "📍 Location: $SERVER_BUNDLE/resources/bin/browseros_server"
echo ""
