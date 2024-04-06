#!/bin/bash

# Load the installed_path from package.json
INSTALLED_PATH=$(jq -r '.installed_path' package.json)

# Define the GitHub repository details
OWNER="Baeldung"
REPO="kotlin-tutorials"
REF="master"

# Download the tarball from GitHub
curl -L "https://api.github.com/repos/$OWNER/$REPO/tarball/$REF" -o package.tar.gz

# Extract the tarball to the installed_path
mkdir -p "$INSTALLED_PATH"
tar -xzf package.tar.gz -C "$INSTALLED_PATH" --strip-components=1

# Clean up the downloaded tarball
rm package.tar.gz
