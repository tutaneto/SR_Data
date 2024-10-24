"""
Test script for SR_Data server management functionality
"""
import os
import sys
import time
import signal
import unittest
from datetime import datetime

from libraries.server_manager import ServerManager

class TestServerManagement(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        # Use default paths from ServerManager
        self.server = ServerManager()
        self.test_queue_file = self.server.queue_file
        self.test_graphics_dir = self.server.graphics_dir

        # Ensure directories exist
        os.makedirs(os.path.dirname(self.test_queue_file), exist_ok=True)
        os.makedirs(self.test_graphics_dir, exist_ok=True)

        # Create test queue file
        with open(self.test_queue_file, 'w') as f:
            f.write('0 0\n')

        # Verify initial status
        self.assertEqual(self.server.get_status(), "Idle")

    def tearDown(self):
        """Clean up after tests"""
        self.server.cleanup()

    def test_server_initialization(self):
        """Test server initialization"""
        self.assertTrue(self.server.running)
        self.assertTrue(os.path.exists(self.test_queue_file))
        self.assertTrue(os.path.exists(self.test_graphics_dir))

    def test_health_check(self):
        """Test server health check functionality"""
        self.assertTrue(self.server.check_health())
        self.assertEqual(self.server.get_status(), "Idle")

        # Test with missing queue file
        os.remove(self.test_queue_file)
        self.assertFalse(self.server.check_health())
        self.assertEqual(self.server.get_status(), "Error")
        self.assertIsNotNone(self.server.last_error)

        # Restore queue file
        with open(self.test_queue_file, 'w') as f:
            f.write('0 0\n')

    def test_reset_functionality(self):
        """Test server reset functionality"""
        # Create some temporary files
        temp_file = os.path.join(self.test_graphics_dir, 'test.tmp')
        with open(temp_file, 'w') as f:
            f.write('test data')

        # Write test command to queue
        with open(self.test_queue_file, 'w') as f:
            f.write('1 IPCA\n')

        # Set some test status
        self.server.set_status("Processing", "IPCA", "Test error")

        # Reset server
        self.server.reset_server()

        # Verify cleanup
        self.assertFalse(os.path.exists(temp_file))
        with open(self.test_queue_file, 'r') as f:
            self.assertEqual(f.read().strip(), '0 0')

        # Verify status reset
        self.assertEqual(self.server.get_status(), "Idle")
        self.assertIsNone(self.server.current_visualization)
        self.assertIsNone(self.server.last_error)

    def test_shutdown_handling(self):
        """Test graceful shutdown handling"""
        # Simulate shutdown signal
        self.server.handle_shutdown(signal.SIGTERM, None)

        # Verify server state
        self.assertFalse(self.server.running)
        with open(self.test_queue_file, 'r') as f:
            self.assertEqual(f.read().strip(), '0 0')

if __name__ == '__main__':
    unittest.main()
