#!/usr/bin/env python3
"""String replacement module for BrowserOS build system"""

import re
from ...common.module import CommandModule, ValidationError
from ...common.context import Context
from ...common.utils import log_info, log_success, log_error, log_warning


class StringReplacesModule(CommandModule):
    produces = []
    requires = []
    description = "Apply branding string replacements in Chromium"

    def validate(self, ctx: Context) -> None:
        if not ctx.chromium_src.exists():
            raise ValidationError(f"Chromium source not found: {ctx.chromium_src}")

    def execute(self, ctx: Context) -> None:
        log_info("\n🔤 Applying string replacements...")
        if not apply_string_replacements_impl(ctx):
            raise RuntimeError("Failed to apply string replacements")


import json
from pathlib import Path

# Load replacements from config
def load_branding_config(ctx: Context) -> list:
    config_path = ctx.root_dir / "resources/branding_config.json"
    if not config_path.exists():
        log_warning(f"⚠️  Config not found: {config_path}, using defaults")
        return []
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [(r["pattern"], r["replacement"]) for r in data.get("replacements", [])]
    except Exception as e:
        log_error(f"Failed to load branding config: {e}")
        return []

# Additional non-code files to rebrand (relative to browseros root)
additional_files = [
    "chromium_patches/chrome/app/app-Info.plist",
    "build/scripts/icon_generation/generate_icons.txt",
    "build/scripts/icon_generation/README.md",
]

# List of files to apply replacements to
target_files = [
    # UI strings
    "chrome/app/chromium_strings.grd",
    "chrome/app/settings_chromium_strings.grdp",
    "chrome/app/generated_resources.grd",
    "chrome/app/google_chrome_strings.grd",
    "components/components_chromium_strings.grd",
    "extensions/strings/extensions_strings.grd",
]

def apply_string_replacements_impl(ctx: Context) -> bool:
    """Internal implementation for applying string replacements"""

    success = True
    
    # Load dynamic replacements
    branding_replacements = load_branding_config(ctx)
    
    if not branding_replacements:
        # Fallback defaults if config missing (or empty)
        branding_replacements = [
            (r"BrowserOS", r"eGovernmentOS"),
            (r"Chrome", r"eGovernmentOS"),
            (r"Chromium", r"eGovernmentOS"),
        ]


    # Process Chromium source files
    for file_path in target_files:
        full_path = ctx.chromium_src / file_path

        if not full_path.exists():
            log_warning(f"  ⚠️  File not found: {file_path}")
            continue

        log_info(f"  • Processing: {file_path}")

        try:
            # Read the file content
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content
            replacement_count = 0

            # Apply each replacement
            for pattern, replacement in branding_replacements:
                matches = len(re.findall(pattern, content))
                if matches > 0:
                    content = re.sub(pattern, replacement, content)
                    replacement_count += matches
                    log_info(f"    ✓ Replaced {matches} occurrences of '{pattern}'")

            # Write back if changes were made
            if content != original_content:
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)
                log_success(f"    Updated with {replacement_count} total replacements")
            else:
                log_info("    No replacements needed")

        except Exception as e:
            log_error(f"    Error processing {file_path}: {e}")
            success = False

    # Process additional BrowserOS files (patches, docs, etc.)
    for file_path in additional_files:
        full_path = ctx.root_dir / file_path

        if not full_path.exists():
            log_warning(f"  ⚠️  File not found: {file_path}")
            continue

        log_info(f"  • Processing: {file_path}")

        try:
            # Read the file content
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content
            replacement_count = 0

            # Apply each replacement
            for pattern, replacement in branding_replacements:
                matches = len(re.findall(pattern, content))
                if matches > 0:
                    content = re.sub(pattern, replacement, content)
                    replacement_count += matches
                    log_info(f"    ✓ Replaced {matches} occurrences of '{pattern}'")

            # Write back if changes were made
            if content != original_content:
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)
                log_success(f"    Updated with {replacement_count} total replacements")
            else:
                log_info("    No replacements needed")

        except Exception as e:
            log_error(f"    Error processing {file_path}: {e}")
            success = False

    if success:
        log_success("✅ String replacements completed")
    else:
        log_error("String replacements failed")

    return success
