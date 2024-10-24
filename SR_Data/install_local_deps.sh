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
    "ipywidgets"
    "yfinance==0.2.46"
    "requests==2.32.3"
)

# Install packages to lib directory
for package in "${PACKAGES[@]}"; do
    echo "Installing $package..."
    python3 -m pip install --target=./lib "$package"
done

# Download and install kaleido separately
echo "Installing kaleido..."
KALEIDO_VERSION="0.2.1"
mkdir -p lib/kaleido_temp
cd lib/kaleido_temp

# Download kaleido based on platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    KALEIDO_URL="https://github.com/plotly/Kaleido/releases/download/v${KALEIDO_VERSION}/kaleido-${KALEIDO_VERSION}-darwin-x64.zip"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    KALEIDO_URL="https://github.com/plotly/Kaleido/releases/download/v${KALEIDO_VERSION}/kaleido-${KALEIDO_VERSION}-linux-x64.zip"
else
    echo "Unsupported platform: $OSTYPE"
    exit 1
fi

# Download and extract kaleido
curl -L -o kaleido.zip "$KALEIDO_URL"
unzip kaleido.zip
mv kaleido ../
cd ..
rm -rf kaleido_temp

echo "All packages installed successfully!"
