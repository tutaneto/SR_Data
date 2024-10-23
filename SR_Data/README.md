# SR_Data Financial Visualization System

A Python-based financial data visualization system that fetches data from various sources and generates insightful visualizations.

## Features

- Fetches financial data from multiple sources (BCB, Yahoo Finance, etc.)
- Generates various types of visualizations (graphs, charts, etc.)
- Supports automated data updates
- Includes local dependency management for portability

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tutaneto/SR_Data.git
   cd SR_Data
   ```

2. Run the setup script to create the local environment:
   ```bash
   ./setup_local_env.sh
   ```
   This will:
   - Create a virtual environment
   - Install all required dependencies locally
   - Set up the necessary configuration files

3. Verify the installation:
   ```bash
   python verify_dependencies.py
   ```

## Usage

1. Basic usage:
   ```bash
   python SR_Data.py
   ```

2. Run with specific mode:
   ```bash
   python SR_Data.py --mode MERC_FIN_AUTO_ROBO
   ```

3. Run tests:
   ```bash
   python test_financial_data.py
   python test_bcb_integration.py
   ```

## Configuration

The system uses several configuration files:

- `data/config/config.json`: Main configuration file
- `data/config/auto.csv`: Automation configuration

## Dependencies

All dependencies are managed locally within the project directory:
- Python packages in `lib/`
- System binaries in `bin/`

## Troubleshooting

Common issues and solutions:

1. BCB API Access:
   - Ensure proper date formatting in API requests
   - Check API endpoint configuration in config.json

2. Visualization Issues:
   - Verify that all required data files exist
   - Check graphics output directory permissions

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
