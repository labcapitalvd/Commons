#!/usr/bin/env bash
set -e

# Usage: fetch.sh <github_repo> <filename>
# Example: ./fetch.sh LABCapital-IIP/IIP-Commons shared_db.zip

GITHUB_REPO="$1"
FILENAME="$2"
GITHUB_TOKEN="$3"

if [ -z "$GITHUB_REPO" ]; then
    echo "❌ Error: No GITHUB_REPO provided."
    exit 1
fi

if [ -z "$FILENAME" ]; then
    echo "❌ Error: No FILENAME provided."
    exit 1
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: No GITHUB_TOKEN provided."
    exit 1
fi 

echo "Fetching $FILENAME from $GITHUB_REPO..."

# Get latest release tag
LATEST_TAG=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
    "https://api.github.com/repos/$GITHUB_REPO/tags" | jq -r '.[0].name')

# Get asset ID for the filename
ASSET_ID=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
    "https://api.github.com/repos/$GITHUB_REPO/releases/tags/$LATEST_TAG" \
    | jq -r --arg name "$FILENAME" '.assets[] | select(.name==$name) | .id')

# Download the asset
curl -L -H "Authorization: Bearer $GITHUB_TOKEN" \
     -H "Accept: application/octet-stream" \
     -o "$FILENAME" \
     "https://api.github.com/repos/$GITHUB_REPO/releases/assets/$ASSET_ID"

# Install if Python package
pip install "$FILENAME"
