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
        
        if "aboutBrowserOSVersion" in content:
            # Protect this specific variable name from being renamed
            # We temporarily replace it with a placeholder, do the main replace, then restore it
            placeholder = "___PROTECTED_VAR_VERSION___"
            content = content.replace("aboutBrowserOSVersion", placeholder)
            
            for old, new in REPLACEMENTS:
                if old in content:
                    matches = content.count(old)
                    content = content.replace(old, new)
                    count += matches
            
            # Restore the protected variable
            content = content.replace(placeholder, "aboutBrowserOSVersion")
        else:
             # Standard replacement path
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

import shutil

def validate_and_fix_branding(filepath):
    """
    Reads a BRANDING file and ensures it uses MAC_CREATOR_CODE instead of CREATOR.
    Returns the fixed content.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        fixed_lines = []
        modified = False
        for line in lines:
            if line.startswith("CREATOR="):
                fixed_lines.append(line.replace("CREATOR=", "MAC_CREATOR_CODE="))
                modified = True
            else:
                fixed_lines.append(line)
        
        if modified:
            print(f"   🔧 Auto-fixed 'CREATOR' -> 'MAC_CREATOR_CODE' in {os.path.basename(filepath)}")
            return "".join(fixed_lines)
        return "".join(lines)
    except Exception as e:
        print(f"   ⚠️ Could not validate {filepath}: {e}")
        return None

def sync_branding_files():
    """
    Syncs the BRANDING files from 'resources/' (Source of Truth) to:
    1. 'chromium_files/' (Build System Source)
    2. 'chromium/src/' (Active Build Dir)
    
    AND fixes common content errors (like CREATOR vs MAC_CREATOR_CODE) during the copy.
    """
    print("🔄 Syncing & Validating BRANDING files...")
    
    # Source: resources/chromium_files (Source of Truth)
    src_base = "/Users/Mukira/Downloads/BrowserOS/packages/browseros/resources/chromium_files"
    
    # Dest 1: chromium_files (Used by build system)
    dst_pkg_base = "/Users/Mukira/Downloads/BrowserOS/packages/browseros/chromium_files"
    
    # Dest 2: chromium/src (Used by ninja)
    dst_src_base = "/Users/Mukira/chromium/src"
    
    files_to_sync = [
        "chrome/app/theme/chromium/BRANDING",
        "chrome/app/theme/chromium/BRANDING.debug",
    ]
    
    for rel_path in files_to_sync:
        src = os.path.join(src_base, rel_path)
        dst_pkg = os.path.join(dst_pkg_base, rel_path)
        dst_src = os.path.join(dst_src_base, rel_path)
        
        if os.path.exists(src):
            # 1. Read & Fix Content
            content = validate_and_fix_branding(src)
            if content:
                # 2. Write to Package Build Dir
                os.makedirs(os.path.dirname(dst_pkg), exist_ok=True)
                with open(dst_pkg, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✓ Synced Package Source: {rel_path}")
                
                # 3. Write to Active Build Dir
                os.makedirs(os.path.dirname(dst_src), exist_ok=True)
                with open(dst_src, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✓ Synced Build Dir: {rel_path}")
        else:
            print(f"   ⚠️  Source not found: {src}")

def main():
    print("🚀 Starting Universal 'BrowserOS' -> 'eGovernmentOS' Rename...")
    
    # 1. Sync Branding Files First
    sync_branding_files()

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
