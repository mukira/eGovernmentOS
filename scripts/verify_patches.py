#!/usr/bin/env python3
import os
import sys

# Configuration
SRC_DIR = "/Users/Mukira/chromium/src"
PKG_DIR = "/Users/Mukira/Downloads/BrowserOS/packages/browseros"
PATCH_DIR = os.path.join(PKG_DIR, "chromium_patches")
FILE_DIR = os.path.join(PKG_DIR, "chromium_files")

def check_file_content(src_file, search_string):
    """
    Checks if a file contains a specific string.
    """
    try:
        with open(src_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if search_string in content:
                return True
    except FileNotFoundError:
        return False
    return False

def verify_patches():
    print("🔍 Verifying that crucial patches are applied...")
    
    missing_patches = []
    
    # 1. Check First Run Patch (Critical)
    first_run_file = os.path.join(SRC_DIR, "chrome/browser/chrome_browser_main.cc")
    if not check_file_content(first_run_file, "browseros-first-run"):
        print(f"❌ MISSING PATCH: First Run logic is missing in {first_run_file}")
        missing_patches.append("First Run Logic")
    else:
        print(f"✅ Verified: First Run Logic")

    # 2. Check Branding File (Critical)
    branding_file = os.path.join(SRC_DIR, "chrome/app/theme/chromium/BRANDING")
    if not check_file_content(branding_file, "MAC_CREATOR_CODE=eGov"):
         print(f"❌ MISSING/BAD PATCH: BRANDING file seems incorrect (MAC_CREATOR_CODE) in {branding_file}")
         missing_patches.append("BRANDING (MAC_CREATOR_CODE)")
    else:
         print(f"✅ Verified: BRANDING file")

    # 3. Check About Page Fix (Critical)
    about_page = os.path.join(SRC_DIR, "chrome/browser/resources/settings/about_page/about_page.html")
    if check_file_content(about_page, "abouteGovernmentOSVersion"):
         print(f"❌ BROKEN PATCH: About Page has corrupted variable 'abouteGovernmentOSVersion' in {about_page}")
         missing_patches.append("About Page Crash (Corrupted Variable)")
    elif check_file_content(about_page, "aboutBrowserOSVersion"):
         print(f"✅ Verified: About Page Variable (aboutBrowserOSVersion)")
    else:
         print(f"⚠️ Warning: Could not find about version variable in {about_page}")

    if missing_patches:
        print("\n❌ VERIFICATION FAILED. The following patches are missing or broken:")
        for p in missing_patches:
            print(f"   - {p}")
        sys.exit(1)
    else:
        print("\n✨ All critical patches verified successfully!")
        sys.exit(0)

if __name__ == "__main__":
    verify_patches()
