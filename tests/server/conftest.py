import pytest
import sys
import os
from pathlib import Path

# Add the project root to the Python path for imports
root_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(root_dir))

# Define pytest command line options if needed
def pytest_addoption(parser):
    parser.addoption(
        "--run-integration", 
        action="store_true", 
        default=False, 
        help="run integration tests"
    )

# Skip integration tests unless explicitly requested
def pytest_configure(config):
    config.addinivalue_line("markers", "integration: mark test as integration test")

def pytest_collection_modifyitems(config, items):
    if not config.getoption("--run-integration"):
        skip_integration = pytest.mark.skip(reason="need --run-integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)