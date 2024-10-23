import os
import sys
import time
import logging
import pytest
import threading
from PIL import Image
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from libraries.server_manager import ServerManager
import SR_Data

class TestVisualizationPipeline:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test environment before each test"""
        self.graphics_dir = os.path.join(project_root, 'graphics')
        self.queue_dir = os.path.join(project_root, '..', 'wwwsec', 'output')
        self.queue_file = os.path.join(self.queue_dir, 'queue.txt')

        os.makedirs(self.graphics_dir, exist_ok=True)
        os.makedirs(self.queue_dir, exist_ok=True)

        self.server = ServerManager(self.queue_file, self.graphics_dir)
        yield
        self.server.reset_server()

    def write_command_to_queue(self, command):
        """Write a command to the queue file"""
        logger.info(f"Writing command to queue: {command}")
        with open(self.queue_file, 'w') as f:
            f.write(command)

    def verify_visualization_file(self, filename):
        """Verify that a visualization file exists and is valid"""
        filepath = os.path.join(self.graphics_dir, filename)
        logger.info(f"Verifying visualization file: {filepath}")

        assert os.path.exists(filepath), f"File not found: {filepath}"
        assert os.path.getsize(filepath) > 0, f"File is empty: {filepath}"

        try:
            with Image.open(filepath) as img:
                img.verify()
            logger.info(f"Verified file: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to verify file {filepath}: {str(e)}")
            return False

    def test_ipca_visualization(self):
        """Test IPCA visualization generation"""
        logger.info("Starting IPCA visualization test")

        server_thread = threading.Thread(
            target=SR_Data.main,
            args=(['--mode', 'MERC_FIN_AUTO_ROBO'],)
        )
        server_thread.daemon = True
        server_thread.start()

        try:
            time.sleep(2)
            self.write_command_to_queue("1 IPCA")

            max_wait = 30
            start_time = time.time()
            while time.time() - start_time < max_wait:
                if os.path.exists(os.path.join(self.graphics_dir, 'ipca.png')):
                    break
                time.sleep(1)

            assert self.verify_visualization_file('ipca.png'), "IPCA visualization verification failed"

        finally:
            self.server.reset_server()
            if server_thread.is_alive():
                with open(self.queue_file, 'w') as f:
                    f.write("EXIT")
                server_thread.join(timeout=5)

    def test_server_visualization_status(self):
        """Test server status reporting during visualization generation"""
        logger.info("Starting server status test")

        server_thread = threading.Thread(
            target=SR_Data.main,
            args=(['--mode', 'MERC_FIN_AUTO_ROBO', '--verbose'],)
        )
        server_thread.daemon = True
        server_thread.start()

        try:
            time.sleep(2)
            self.write_command_to_queue("1 IPCA")

            max_wait = 30
            start_time = time.time()
            status_seen = False

            while time.time() - start_time < max_wait:
                if self.server.get_status() == "Processing visualization":
                    status_seen = True
                    break
                time.sleep(1)

            assert status_seen, "Server did not report visualization processing status"

            while time.time() - start_time < max_wait:
                if self.server.get_status() == "Visualization complete":
                    break
                time.sleep(1)

            assert self.server.get_status() in ["Idle", "Visualization complete"], \
                   "Server did not complete visualization processing"

        finally:
            self.server.reset_server()
            if server_thread.is_alive():
                with open(self.queue_file, 'w') as f:
                    f.write("EXIT")
                server_thread.join(timeout=5)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
