# Third Party
import pytest
from testcontainers.compose import DockerCompose


@pytest.fixture(name="dockercompose", scope="session")
def _docker_compose():
    with DockerCompose(
        context="containers/docker/", compose_file_name="docker-compose.yml", pull=True, build=True
    ) as compose:
        compose.wait_for("http://localhost:8080/")
        yield compose
