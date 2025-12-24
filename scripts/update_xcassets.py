#!/usr/bin/env python3
import os
import shutil
import subprocess

# Paths
SOURCE_ICONS_DIR = "/Users/Mukira/Downloads/BrowserOS/packages/browseros/resources/icons"
TARGET_ASSETS_DIR = "/Users/Mukira/Downloads/BrowserOS/packages/browseros/resources/icons/mac/Assets.xcassets/AppIcon.appiconset"

# Map of Target Filename -> (Source Filename, Target Resolution if manual resize needed)
ICON_MAPPING = {
    "app-iOS-Default-1024x1024@1x.png": ("product_logo_1024.png", 1024),
    "app-iOS-Default-128x128@1x.png":   ("product_logo_128.png", 128),
    "app-iOS-Default-128x128@2x.png":   ("product_logo_256.png", 256),
    "app-iOS-Default-16x16@1x.png":     ("product_logo_16.png", 16),
    "app-iOS-Default-16x16@2x.png":     ("product_logo_32.png", 32),
    "app-iOS-Default-20x20@2x.png":     ("product_logo_256.png", 40), # Resize needed
    "app-iOS-Default-20x20@3x.png":     ("product_logo_256.png", 60), # Resize needed
    "app-iOS-Default-256x256@1x.png":   ("product_logo_256.png", 256),
    "app-iOS-Default-256x256@2x.png":   ("product_logo_1024.png", 512), # Resize down from 1024
    "app-iOS-Default-29x29@2x.png":     ("product_logo_256.png", 58), # Resize needed
    "app-iOS-Default-29x29@3x.png":     ("product_logo_256.png", 87), # Resize needed
    "app-iOS-Default-32x32@1x.png":     ("product_logo_32.png", 32),
    "app-iOS-Default-32x32@2x.png":     ("product_logo_64.png", 64),
    "app-iOS-Default-38x38@2x.png":     ("product_logo_256.png", 76), # Resize
    "app-iOS-Default-38x38@3x.png":     ("product_logo_256.png", 114), # Resize
    "app-iOS-Default-40x40@2x.png":     ("product_logo_256.png", 80), # Resize
    "app-iOS-Default-40x40@3x.png":     ("product_logo_256.png", 120), # Resize
    "app-iOS-Default-512x512@1x.png":   ("product_logo_1024.png", 512), # Resize
    "app-iOS-Default-60x60@2x.png":     ("product_logo_256.png", 120), # Resize
    "app-iOS-Default-60x60@3x.png":     ("product_logo_256.png", 180), # Resize
    "app-iOS-Default-64x64@2x.png":     ("product_logo_128.png", 128),
    "app-iOS-Default-64x64@3x.png":     ("product_logo_192.png", 192),
    "app-iOS-Default-68x68@2x.png":     ("product_logo_256.png", 136), # Resize
    "app-iOS-Default-76x76@2x.png":     ("product_logo_256.png", 152), # Resize
    "app-iOS-Default-83.5x83.5@2x.png": ("product_logo_256.png", 167), # Resize
}

def resize_image(src_path, dest_path, size):
    # check if sips exists
    cmd = ["sips", "-z", str(size), str(size), src_path, "--out", dest_path]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"❌ Failed to resize {src_path} -> {dest_path}: {e}")
        return False

def main():
    print("🎨 Updating Assets.xcassets with Blue Icons...")
    
    count = 0
    for target_name, (src_name, size) in ICON_MAPPING.items():
        src_path = os.path.join(SOURCE_ICONS_DIR, src_name)
        target_path = os.path.join(TARGET_ASSETS_DIR, target_name)
        
        if not os.path.exists(src_path):
            print(f"⚠️ Source missing: {src_name}")
            continue
            
        # Copy or Resize
        # If sizes match naturally (approx), just copy? 
        # Actually sips is fast, let's just use sips for everything to ensure correct metadata dimensions,
        # OR just copy if 1:1 map exists to avoid recompression loss.
        
        # Simple heuristic: if src filename contains the exact resolution, assume it's good.
        if f"_{size}.png" in src_name:
             shutil.copy2(src_path, target_path)
             # print(f"✅ Copied: {target_name}")
        else:
             # Resize needed
             resize_image(src_path, target_path, size)
             # print(f"✅ Resized: {target_name}")
        count += 1
        
    print(f"✨ Updated {count} icons in Assets.xcassets")

if __name__ == "__main__":
    main()
