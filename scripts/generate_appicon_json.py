import json
import os

target_dir = "packages/browseros/resources/icons/mac/Assets.xcassets/AppIcon.appiconset"
json_path = os.path.join(target_dir, "Contents.json")

# Map available files to macOS slots
images = [
    {
        "size": "16x16",
        "idiom": "mac",
        "filename": "app-iOS-Default-16x16@1x.png",
        "scale": "1x"
    },
    {
        "size": "16x16",
        "idiom": "mac",
        "filename": "app-iOS-Default-16x16@2x.png",
        "scale": "2x"
    },
    {
        "size": "32x32",
        "idiom": "mac",
        "filename": "app-iOS-Default-32x32@1x.png",
        "scale": "1x"
    },
    {
        "size": "32x32",
        "idiom": "mac",
        "filename": "app-iOS-Default-32x32@2x.png",
        "scale": "2x"
    },
    {
        "size": "128x128",
        "idiom": "mac",
        "filename": "app-iOS-Default-128x128@1x.png",
        "scale": "1x"
    },
    {
        "size": "128x128",
        "idiom": "mac",
        "filename": "app-iOS-Default-128x128@2x.png",
        "scale": "2x"
    },
    {
        "size": "256x256",
        "idiom": "mac",
        "filename": "app-iOS-Default-256x256@1x.png",
        "scale": "1x"
    },
    {
        "size": "256x256",
        "idiom": "mac",
        "filename": "app-iOS-Default-256x256@2x.png",
        "scale": "2x"
    },
    {
        "size": "512x512",
        "idiom": "mac",
        "filename": "app-iOS-Default-512x512@1x.png",
        "scale": "1x"
    },
    {
        "size": "512x512",
        "idiom": "mac",
        "filename": "app-iOS-Default-1024x1024@1x.png",
        "scale": "2x"
    }
]

content = {
    "images": images,
    "info": {
        "version": 1,
        "author": "xcode"
    }
}

print(f"Writing Contents.json to {json_path}")
with open(json_path, "w") as f:
    json.dump(content, f, indent=2)
print("Done.")
