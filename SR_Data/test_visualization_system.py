import os
import sys
import json
from pathlib import Path

# Ensure we're using local dependencies
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

def verify_directories():
    """Verify required directories exist."""
    required_dirs = ['graphics', '../wwwsec/output']
    for dir_path in required_dirs:
        os.makedirs(os.path.join(os.path.dirname(__file__), dir_path), exist_ok=True)
    return True

def create_test_request():
    """Create a test visualization request."""
    queue_path = os.path.join(os.path.dirname(__file__), '../wwwsec/output/queue.txt')
    with open(queue_path, 'w') as f:
        f.write('1 IPCA\n')
    return True

def verify_template_config():
    """Verify template configuration is properly loaded."""
    from libraries.template_config import TemplateConfig
    config = TemplateConfig()
    assert hasattr(config, 'TEMPLATE_CODES'), "TEMPLATE_CODES not found in TemplateConfig"
    assert 'IPCA' in config.TEMPLATE_CODES, "IPCA template code not found"
    return True

def verify_graphics_generation():
    """Verify graphics can be generated."""
    import SR_Data
    import argparse
    import traceback
    import logging

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    try:
        # Initialize arguments
        args = argparse.Namespace()
        args.mode = 'MERC_FIN_AUTO_ROBO'
        args.auto_file = 'auto'
        args.reset = False

        # Verify queue file exists and contains correct data
        queue_path = os.path.join(os.path.dirname(__file__), '../wwwsec/output/queue.txt')
        if not os.path.exists(queue_path):
            raise FileNotFoundError(f"Queue file not found at {queue_path}")

        with open(queue_path, 'r') as f:
            queue_content = f.read().strip()
            logger.debug(f"Queue file contents: {queue_content}")
            if queue_content != '1 IPCA':
                raise ValueError(f"Unexpected queue content: {queue_content}")

        # Ensure graphics directory exists
        graphics_dir = os.path.join(os.path.dirname(__file__), 'graphics')
        os.makedirs(graphics_dir, exist_ok=True)
        logger.debug(f"Graphics directory ensured at: {graphics_dir}")

        # Run main program
        logger.debug("Starting SR_Data.main()")
        SR_Data.main(args)
        logger.debug("Completed SR_Data.main()")

        # Verify graphics output
        if not os.path.exists(graphics_dir):
            raise FileNotFoundError(f"Graphics directory not found at {graphics_dir}")

        files = os.listdir(graphics_dir)
        logger.debug(f"Files in graphics directory: {files}")

        if not files:
            raise Exception("No files generated in graphics directory")

        ipca_files = [f for f in files if f.lower().startswith('ipca')]
        if not ipca_files:
            raise Exception(f"IPCA graphic not found in generated files: {files}")

        logger.debug(f"Found IPCA files: {ipca_files}")
        return True

    except Exception as e:
        logger.error(f"Error generating graphics: {str(e)}")
        logger.error("Traceback:")
        traceback.print_exc()
        return False

def main():
    """Run all verification tests."""
    # Set up logging at the start
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    tests = [
        ('Directory Structure', verify_directories),
        ('Test Request Creation', create_test_request),
        ('Template Configuration', verify_template_config),
        ('Graphics Generation', verify_graphics_generation)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            logger.info(f"Starting test: {test_name}")
            result = test_func()
            status = 'PASS' if result else 'FAIL'
            logger.info(f"Test {test_name} completed with status: {status}")
        except Exception as e:
            status = 'ERROR'
            logger.error(f"Error in {test_name}: {str(e)}", exc_info=True)
        results.append((test_name, status))

    logger.info("\nTest Results:")
    logger.info("-" * 40)
    for test_name, status in results:
        logger.info(f"{test_name:.<30}{status}")

    # Also print results to stdout for visibility
    print("\nTest Results:")
    print("-" * 40)
    for test_name, status in results:
        print(f"{test_name:.<30}{status}")

    return all(status == 'PASS' for _, status in results)

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
