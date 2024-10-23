#!/bin/bash

# Setup script for SR_Data local environment
set -e

echo "Setting up SR_Data local environment..."

# Create necessary directories
mkdir -p lib bin data/config graphics videos
mkdir -p ../wwwsec/output
mkdir -p data/{bc,ibge,fgv,anbima,digitado,filter,mt,cache}

# Create required files
touch ../wwwsec/output/queue.txt
touch data/config/auto.csv

# Setup Python virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies to local lib directory
pip install --target=./lib \
    numpy \
    pandas \
    matplotlib \
    plotly \
    requests \
    beautifulsoup4 \
    selenium \
    yfinance \
    moviepy \
    Pillow==9.5.0 \
    python-telegram-bot \
    pyTelegramBotAPI \
    ipywidgets

# Download and setup ffmpeg in bin directory
if [ "$(uname)" == "Darwin" ]; then
    # macOS
    brew install ffmpeg
    cp $(which ffmpeg) bin/
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Linux
    apt-get update && apt-get install -y ffmpeg
    cp $(which ffmpeg) bin/
fi

# Create default configuration
cat > data/config/config.json << EOL
{
    "bcb": {
        "sgs_endpoint": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json",
        "expectativas_endpoint": "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoAnuais"
    },
    "paths": {
        "graphics": "graphics",
        "videos": "videos",
        "data": "data"
    }
}
EOL

echo "Setup complete! Run 'python verify_dependencies.py' to verify the installation."
