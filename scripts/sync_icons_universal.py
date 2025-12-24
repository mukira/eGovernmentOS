#!/usr/bin/env python3
import os
import shutil

# Source: Your new blue icons
SOURCE_DIR = "/Users/Mukira/Downloads/BrowserOS/packages/browseros/resources/icons"

# Destination Root: Chrome Theme dir
DEST_ROOT = "/Users/Mukira/chromium/src/chrome/app/theme"

def main():
    print("🔵 Starting Universal Icon Sync...")
    
    # 1. Build a map of Source File Name -> Full Source Path
    # We prioritize the root level icons, but also include 'linux' subdir if needed.
    # Actually, let's just make a flat map of filename -> path.
    # If duplicates exist (e.g. linux/logo_48 vs logo_48), we might need care.
    # For now, let's trust the root ones are the main ones.
    
    source_map = {}
    
    # Walk source to populate map
    for root, dirs, files in os.walk(SOURCE_DIR):
        for f in files:
            if f.endswith(".png"):
                # If we already have it, decision time. 
                # Use the one in the root if possible.
                if f not in source_map:
                    source_map[f] = os.path.join(root, f)
                else:
                    # If current is root, overwrite.
                    if root == SOURCE_DIR:
                         source_map[f] = os.path.join(root, f)

    print(f"📦 Loaded {len(source_map)} source icons.")

    # 2. Walk Destination and Overwrite
    replaced_count = 0
    
    # We only want to touch files inside 'chromium' or 'default_*' folders, 
    # generally avoiding 'google_chrome' unless we are rebranding that too (we are not supposed to, strictly, but safe to ignore).
    
    for root, dirs, files in os.walk(DEST_ROOT):
        # Optional: Skip google_chrome to avoid confusion, though usually harmless if we are building 'chrome' (open source) path.
        if "google_chrome" in root:
            continue
            
        for f in files:
            if f in source_map:
                dest_path = os.path.join(root, f)
                src_path = source_map[f]
                
                try:
                    shutil.copy2(src_path, dest_path)
                    # print(f"✅ Replaced: {dest_path}")
                    replaced_count += 1
                except Exception as e:
                    print(f"❌ Failed to replace {dest_path}: {e}")

    print(f"✨ Universal Sync Complete. Overwrote {replaced_count} icon files across all theme folders.")

if __name__ == "__main__":
    main()
