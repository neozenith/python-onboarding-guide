# Testcontainers + PyTest

<!--TOC-->

- [Testcontainers + PyTest](#testcontainers--pytest)
  - [Pytest Fixtures Using TestContainers](#pytest-fixtures-using-testcontainers)
    - [`tests/conftest.py`](#testsconftestpy)
    - [`tests/test_example.py`](#teststest_examplepy)

<!--TOC-->

## Pytest Fixtures Using TestContainers

Make a test fixture available for the duration of the entire pytest `session` when you have the following in your `conftest.py`.

Assuming you have a `docker-compose.yml` in `containers/docker/docker-compose.yml`.

### `tests/conftest.py`
```python
# Third Party
import pytest
from testcontainers.compose import DockerCompose

@pytest.fixture(name="dockercompose", scope="session")
def _docker_compose():
    with DockerCompose(context="containers/docker/", compose_file_name="docker-compose.yml", pull=True, build=True) as compose:
        compose.wait_for("http://localhost:8080/")
        yield compose

```

And here is an example test using it:

### `tests/test_example.py`
```python
# Third Party
import pytest
import aiohttp
import base64

HOST = "http://localhost:8080/"
BASIC_AUTH = base64.b64encode("testuser:insecurepassword".encode()).decode()

headers={"Authorization": f"Basic {BASIC_AUTH}"}


@pytest.mark.asyncio
@pytest.mark.docker
async def test_example(dockercompose) -> None:
    """Start docker compose fixture and run endpoint check."""
    print(headers)
    async with aiohttp.ClientSession() as session:
        async with session.get(HOST, headers=headers) as response:
            data = await response.json()
    
    assert len(data) > 0
```

Since this test is [`mark`ed as `docker` with a custom marker](https://docs.pytest.org/en/stable/example/markers.html#mark-examples) you can use the marks selector from `pytest`. Eg

```sh
python3 -m pytest -m docker
```
