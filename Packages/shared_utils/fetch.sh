#!/usr/bin/env bash
set -e

# Usage: fetch.sh <github_repo> <filename>
# Example: ./fetch.sh SpanishSyntax/Commons shared_db.zip

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

# Get tags for the filename
RESPONSE_TAGS=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/$GITHUB_REPO/tags")

LATEST_TAG=$(echo "$RESPONSE_TAGS" | jq -r '.[0].name // empty')

if [ -z "$LATEST_TAG" ] || [ "$LATEST_TAG" == "null" ]; then
  echo "❌ Error: Could not find tags for $GITHUB_REPO. API Response: $RESPONSE_TAGS"
  exit 1
fi

echo "Latest tag is: $LATEST_TAG"


# Get asset ID for the filename
RESPONSE_ASSETS=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/$GITHUB_REPO/releases/tags/$LATEST_TAG")

ASSET_ID=$(echo "$RESPONSE_ASSETS" | jq -r --arg name "$FILENAME" '.assets[] | select(.name==$name) | .id')

if [ -z "$ASSET_ID" ] || [ "$ASSET_ID" == "null" ]; then
  echo "❌ Error: Could not find tags for $GITHUB_REPO. API Response: $RESPONSE_ASSETS"
  exit 1
fi

echo "Asset ID is: $ASSET_ID"

# Download the asset
curl -L -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/octet-stream" \
  -o "$FILENAME" \
  "https://api.github.com/repos/$GITHUB_REPO/releases/assets/$ASSET_ID"

# Install if Python package
pip install "$FILENAME"
