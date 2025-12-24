#!/usr/bin/env python3
import os
import re

# User's Target Colors
# Primary Blue: #1266f1 (18, 102, 241)
# Gradient 1:   #2a75f3
# Gradient 2:   #4285f4
# Gradient 3:   #5a95f5
# Gradient 4:   #72a4f7

# Colors to Replace (Mapping Old -> New)
# We map the main orange to the main blue.
COLOR_MAP = {
    # Main Accent Orange -> Main Blue
    "FB651F": "1266F1", 
    "fb651f": "1266f1",
    
    # Secondary variations found in search (if any matching commonly used orange)
    # Adding common Chrome oranges just in case, but focusing on the one found.
}

# Directories to scan
SEARCH_DIRS = [
    "/Users/Mukira/Downloads/BrowserOS/packages/browseros",
    "/Users/Mukira/chromium/src/chrome/browser/resources",
    "/Users/Mukira/chromium/src/chrome/browser/ui/webui",
    "/Users/Mukira/chromium/src/chrome/app/theme"
]

EXTENSIONS = ('.cc', '.h', '.js', '.css', '.html', '.grd', '.json', '.mm')

def replace_colors_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Skipping {filepath}: {e}")
        return False

    original_content = content
    changes = 0

    # 1. Hex Replacement (Case Insensitive logic handled by map)
    for old_hex, new_hex in COLOR_MAP.items():
        # Replace #RRGGBB
        if f"#{old_hex}" in content:
            content = content.replace(f"#{old_hex}", f"#{new_hex}")
            changes += 1
        
        # Replace straight hex chars if it looks like a color (risky without context, staying safe with # prefix first)
        # However, WebUI sometimes uses %23FB651F (URL encoded).
        if f"%23{old_hex}" in content:
            content = content.replace(f"%23{old_hex}", f"%23{new_hex}")
            changes += 1

    # 2. RGB Replacement
    # #FB651F -> rgb(251, 101, 31)
    # Target: rgb(18, 102, 241)
    if "251, 101, 31" in content:
         content = content.replace("251, 101, 31", "18, 102, 241")
         content = content.replace("251,101,31", "18,102,241")
         changes += 1

    if content != original_content:
        print(f"🎨 Updating colors in: {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("🔵 Starting Theme Recolor: Orange (#FB651F) -> Blue (#1266F1)...")
    count = 0
    for directory in SEARCH_DIRS:
        if not os.path.exists(directory):
            print(f"⚠️ Directory not found: {directory}")
            continue
            
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(EXTENSIONS):
                    filepath = os.path.join(root, file)
                    if replace_colors_in_file(filepath):
                        count += 1
    
    print(f"✨ Color replacement complete. Modified {count} files.")

if __name__ == "__main__":
    main()
