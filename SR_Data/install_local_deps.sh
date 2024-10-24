#!/bin/bash

# Create lib directory if it doesn't exist
mkdir -p lib

# List of required packages
PACKAGES=(
    "plotly==5.24.1"
    "pandas==2.2.3"
    "numpy==2.1.2"
    "pillow<11"
    "matplotlib==3.9.2"
    "kaleido==0.2.1"
    "ipywidgets"
    "yfinance==0.2.46"
    "requests==2.32.3"
)

# Install packages to lib directory
for package in "${PACKAGES[@]}"; do
    echo "Installing $package..."
    python3 -m pip install --target=./lib "$package"
done

echo "All packages installed successfully!"
