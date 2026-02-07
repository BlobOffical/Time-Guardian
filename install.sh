#!/bin/bash
# shellcheck shell=bash

# Exit on error
set -e

# Path to the commands directory
SOURCE_DIR="$(dirname "$0")/commands"

# Destination directory
DEST_DIR="/usr/local/bin"

# Check if commands directory exists
if [ ! -d "$SOURCE_DIR" ]; then
  echo "Error: commands directory not found at $SOURCE_DIR"
  exit 1
fi

# Copy all files to /usr/local/bin
echo "Copying files from $SOURCE_DIR to $DEST_DIR..."
for file in "$SOURCE_DIR"/*; do
  if [ -f "$file" ]; then
    echo "Installing $(basename "$file")..."
    sudo cp "$file" "$DEST_DIR/"
    sudo chmod +x "$DEST_DIR/$(basename "$file")"
  fi
done

echo "All commands installed successfully!"
