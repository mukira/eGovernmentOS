
import os
import re

file_path = "/Users/Mukira/chromium/src/chrome/browser/ui/browser_actions.cc"
blue_color = "SkColorSetRGB(0x1a, 0x73, 0xe8)"

with open(file_path, "r") as f:
    content = f.read()

# Patch Chat Icon
# Allow more flexibility in whitespace and ensure closing paren is matched
chat_pattern = r"(vector_icons::kChatOrangeIcon,\s+kActionSidePanelShowThirdPartyLlm,\s+bwi,\s+true)\)\s+\.Build\(\)\);"
chat_replacement = f"\\1)\n            .SetImage(ui::ImageModel::FromVectorIcon(vector_icons::kChatOrangeIcon, {blue_color}))\n            .Build());"

# Patch Hub Icon
hub_pattern = r"(vector_icons::kClashOfGptsIcon)\)\s+\.Build\(\)\);"
hub_replacement = f"\\1)\n            .SetImage(ui::ImageModel::FromVectorIcon(vector_icons::kClashOfGptsIcon, {blue_color}))\n            .Build());"

new_content = re.sub(chat_pattern, chat_replacement, content, flags=re.MULTILINE)
new_content = re.sub(hub_pattern, hub_replacement, new_content, flags=re.MULTILINE)

if content == new_content:
    print("No changes made. Patterns might not match.")
else:
    with open(file_path, "w") as f:
        f.write(new_content)
    print("Successfully patched browser_actions.cc")
