# tests/conftest.py

import pytest
import logging
from utils.driver_utils import DriverManager
from config.settings import LOGGING_LEVEL, LOGGING_FORMAT

# Configure logging
logging.basicConfig(level=getattr(logging, LOGGING_LEVEL), format=LOGGING_FORMAT)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def driver_manager():
    """Fixture to provide driver manager for tests."""
    manager = DriverManager()
    yield manager
    manager.cleanup_driver()


@pytest.fixture(scope="function")
def driver(driver_manager):
    """Fixture to provide initialized driver for tests."""
    return driver_manager.initialize_driver()