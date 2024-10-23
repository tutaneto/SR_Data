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
    def __init__(self, queue_file: str, graphics_dir: str):
        self.queue_file = queue_file
        self.graphics_dir = graphics_dir
        self.running = True
        self.start_time = datetime.now()
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

            self.logger.info("Cleanup completed successfully")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")

    def log_server_status(self) -> None:
        """Log current server status and metrics"""
        uptime = datetime.now() - self.start_time
        self.logger.info(f"Server Status - Uptime: {uptime}")

    def check_health(self) -> bool:
        """Check server health status"""
        try:
            # Check if queue file is accessible
            if not os.path.exists(self.queue_file):
                self.logger.error("Queue file not found")
                return False

            # Check if graphics directory is writable
            if not os.access(self.graphics_dir, os.W_OK):
                self.logger.error("Graphics directory not writable")
                return False

            return True
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            return False

    def reset_server(self) -> None:
        """Reset server state and clear temporary data"""
        self.logger.info("Initiating server reset...")
        self.cleanup()
        self.running = True
        self.start_time = datetime.now()
        self.logger.info("Server reset completed")
