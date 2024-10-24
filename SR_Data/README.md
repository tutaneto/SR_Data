# SR_Data Financial Visualization System

A Python-based financial data visualization system that fetches data from various sources and generates insightful visualizations.

## Features

- Fetches financial data from multiple sources (BCB, Yahoo Finance, etc.)
- Generates various types of visualizations (graphs, charts, etc.)
- Supports queue-based visualization requests with continuous processing
- Provides automated data updates and real-time visualization generation
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

1. Start the visualization server in continuous processing mode:
   ```bash
   python SR_Data.py --mode MERC_FIN_AUTO_ROBO
   ```
   This will start the server and monitor for visualization requests.

2. Request visualizations through the queue system:
   ```bash
   # Generate IPCA (inflation) visualization
   echo "1 IPCA" > ../wwwsec/output/queue.txt

   # Generate GDP visualization
   echo "2 PIB" > ../wwwsec/output/queue.txt

   # Generate SELIC rate visualization
   echo "3 SELIC" > ../wwwsec/output/queue.txt
   ```
   Generated visualizations will be saved in the `graphics/` directory.

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

1. Queue Processing Issues:
   - Verify queue.txt exists in ../wwwsec/output/ directory
   - Check file permissions on queue.txt and graphics directory
   - Ensure correct command format (e.g., "1 IPCA", "2 PIB")
   - Check SR_Server_Errors.txt for detailed error logs
   - Verify server is running in MERC_FIN_AUTO_ROBO mode

2. BCB API Access:
   - Ensure proper date formatting in API requests
   - Check API endpoint configuration in config.json
   - Verify network connectivity to BCB servers
   - Check for API rate limiting or access restrictions

3. Visualization Issues:
   - Verify that all required data files exist
   - Check graphics output directory permissions
   - Ensure sufficient disk space for output files
   - Verify matplotlib and plotly dependencies are installed correctly

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
