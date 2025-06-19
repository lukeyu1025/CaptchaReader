#!/usr/bin/env bash
# Download sample images dataset for PyCaptcha-Toolkit
set -e

TARGET_DIR="$(dirname "$0")/../images"
mkdir -p "$TARGET_DIR"

URL=${1:-"https://github.com/lukeyu1025/CaptchaReader/releases/latest/download/images.zip"}

echo "Downloading images from $URL"

curl -L "$URL" -o /tmp/images.zip
unzip -o /tmp/images.zip -d "$TARGET_DIR"
rm /tmp/images.zip

echo "Images downloaded to $TARGET_DIR"
