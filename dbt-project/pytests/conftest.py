# Standard Library
import shlex
import subprocess

# Third Party
import pytest


@pytest.fixture(scope="session")
def dependencies():
    # Setup
    subprocess.run(shlex.split("uv run dbt deps"), capture_output=True)
