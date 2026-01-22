#!/usr/bin/env bash

# 1. Zip the directories (exactly like your YAML)
zip -r shared_db.zip Packages/shared_db
zip -r shared_models.zip Packages/shared_models
zip -r shared_schemas.zip Packages/shared_schemas
zip -r shared_utils.zip Packages/shared_utils

# 2. Get the secret from Seahorse/Keyring (No hardcoded tokens!)
export GITHUB_TOKEN=$(secret-tool lookup service github user SpanishSyntax)

# 3. Run ghr (pointing to your local user and repo)
# -replace allows you to re-run it if you mess up a zip
ghr -t "$GITHUB_TOKEN" \
    -u SpanishSyntax \
    -r your-repo-name \
    -replace \
    v1.0.0 ./*.zip
