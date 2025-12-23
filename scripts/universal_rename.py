#!/usr/bin/env python3
import os
import sys

# Configuration
REPLACEMENTS = [
    ("BrowserOS", "eGovernmentOS"),
]

# Extensions to IGNORE (Code files)
IGNORE_EXTENSIONS = {
    '.cc', '.xc', '.h', '.hh', '.hpp', '.c', '.cpp', '.m', '.mm', 
    '.py', '.pyc', '.js', '.ts', '.java', '.jar', '.class', 
    '.sh', '.bash', '.zsh', '.gn', '.gni', '.ninja', 
    '.o', '.obj', '.a', '.dylib', '.so', '.dll', '.exe', 
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.icns', '.pdf',
    '.zip', '.tar', '.gz', '.pak', '.bin'
}

# Specific Extensions to TARGET (Resource files)
TARGET_EXTENSIONS = {
    '.grd', '.grdp', '.xtb', '.json', '.xml', '.plist', 
    '.txt', '.md', '.html', '.css', '.svg'
}

TARGET_DIRS = [
    "/Users/Mukira/chromium/src",
    "/Users/Mukira/Downloads/BrowserOS/packages/browseros"
]

def is_target_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in IGNORE_EXTENSIONS:
        return False
    # If explicit target extension, OR if it has no extension (often config files)
    if ext in TARGET_EXTENSIONS or ext == "":
        return True
    return False

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        count = 0
        
        for old, new in REPLACEMENTS:
            if old in content:
                matches = content.count(old)
                content = content.replace(old, new)
                count += matches
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Replaced {count} strings in: {filepath}")
            return count
    except Exception as e:
        # Ignore binary read errors etc.
        pass
    return 0

def main():
    print("🚀 Starting Universal 'BrowserOS' -> 'eGovernmentOS' Rename...")
    print("   (Skipping code/binary files, targeting resources/strings/docs)")
    
    total_files = 0
    total_replaced = 0
    
    for root_dir in TARGET_DIRS:
        if not os.path.exists(root_dir):
            print(f"⚠️ Directory not found: {root_dir}")
            continue
            
        print(f"📂 Scanning: {root_dir}...")
        
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip hidden directories like .git
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            
            for filename in filenames:
                if filename.startswith('.'): continue
                
                filepath = os.path.join(dirpath, filename)
                
                if is_target_file(filename):
                    replacements = process_file(filepath)
                    if replacements > 0:
                        total_replaced += replacements
                        total_files += 1

    print(f"\n✨ Done! Updated {total_files} files with {total_replaced} replacements.")

if __name__ == "__main__":
    main()
