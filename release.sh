#!/usr/bin/env bash

# Exit immediately if a command fails
set -e

# 1. Setup a temporary workspace
TMP_DIR=$(mktemp -d -t release-XXXXXX)
echo "📦 Working in temporary directory: $TMP_DIR"

# Ensure cleanup happens even if the script crashes
trap 'rm -rf "$TMP_DIR"; echo "🧹 Cleaned up $TMP_DIR"' EXIT

# 2. Create the zips inside the tmp directory
# We use full paths or relative paths to ensure zip captures the right files
zip -r "$TMP_DIR/shared_db.zip" Packages/shared_db
zip -r "$TMP_DIR/shared_models.zip" Packages/shared_models
zip -r "$TMP_DIR/shared_schemas.zip" Packages/shared_schemas
zip -r "$TMP_DIR/shared_utils.zip" Packages/shared_utils

# 3. Get the secret from Seahorse/Keyring

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: Could not find GITHUB_TOKEN in Seahorse/Keyring."
    exit 1
fi

# 4. Run ghr pointing to the tmp directory
ghr -t "$GITHUB_TOKEN" \
    -u SpanishSyntax \
    -r your-repo-name \
    -replace \
    v1.2.4 "$TMP_DIR/"
