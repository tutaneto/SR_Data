"""
Server Manager Module for SR_Data
Handles server state, monitoring, and graceful shutdown
"""
import os
import signal
import sys
import time
from datetime import datetime
import logging
from typing import Optional

class ServerManager:
    def __init__(self, queue_file: str = None, graphics_dir: str = None):
        # Set default paths relative to module location
        module_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(module_dir)

        self.queue_file = queue_file or os.path.join(project_dir, '..', 'wwwsec', 'output', 'queue.txt')
        self.graphics_dir = graphics_dir or os.path.join(project_dir, 'graphics')

        # Initialize status tracking
        self.running = True
        self.start_time = datetime.now()
        self.current_status = "Idle"
        self.current_visualization = None
        self.last_error = None

        self.setup_logging()
        self.setup_signal_handlers()

    def setup_logging(self):
        """Configure logging for server monitoring"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('SR_Data_Server.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('SR_Data')

    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def handle_shutdown(self, signum: int, frame) -> None:
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}. Starting graceful shutdown...")
        self.running = False
        self.cleanup()

    def cleanup(self) -> None:
        """Perform cleanup operations before shutdown"""
        try:
            # Clear queue file
            if os.path.exists(self.queue_file):
                with open(self.queue_file, 'w') as f:
                    f.write('0 0\n')

            # Remove temporary files
            temp_files = [f for f in os.listdir(self.graphics_dir) if f.endswith('.tmp')]
            for temp_file in temp_files:
                try:
                    os.remove(os.path.join(self.graphics_dir, temp_file))
                except Exception as e:
                    self.logger.error(f"Error removing temp file {temp_file}: {str(e)}")

            # Reset status tracking
            self.current_status = "Idle"
            self.current_visualization = None
            self.last_error = None

            self.logger.info("Cleanup completed successfully")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")
            self.last_error = str(e)

    def set_status(self, status: str, visualization: str = None, error: str = None) -> None:
        """Update server status with visualization information"""
        self.current_status = status
        if visualization:
            self.current_visualization = visualization
        if error:
            self.last_error = error
        self.log_server_status()

    def get_status(self) -> str:
        """Get current server status"""
        return self.current_status

    def get_visualization_status(self) -> dict:
        """Get detailed visualization status information"""
        return {
            'status': self.current_status,
            'current_visualization': self.current_visualization,
            'last_error': self.last_error,
            'uptime': str(datetime.now() - self.start_time)
        }

    def log_server_status(self) -> None:
        """Log current server status and metrics"""
        uptime = datetime.now() - self.start_time
        status_info = (
            f"Server Status - Uptime: {uptime}, "
            f"Status: {self.current_status}, "
            f"Visualization: {self.current_visualization or 'None'}"
        )
        if self.last_error:
            status_info += f", Last Error: {self.last_error}"
        self.logger.info(status_info)

    def check_health(self) -> bool:
        """Check server health status"""
        try:
            # Check if queue file is accessible
            if not os.path.exists(self.queue_file):
                self.logger.error("Queue file not found")
                self.set_status("Error", error="Queue file not found")
                return False

            # Check if graphics directory is writable
            if not os.access(self.graphics_dir, os.W_OK):
                self.logger.error("Graphics directory not writable")
                self.set_status("Error", error="Graphics directory not writable")
                return False

            if self.current_status == "Error":
                self.set_status("Idle")
            return True
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            self.set_status("Error", error=str(e))
            return False

    def reset_server(self) -> None:
        """Reset server state and clear temporary data"""
        self.logger.info("Initiating server reset...")
        self.cleanup()
        self.running = True
        self.start_time = datetime.now()
        self.current_status = "Idle"
        self.current_visualization = None
        self.last_error = None
        self.logger.info("Server reset completed")
