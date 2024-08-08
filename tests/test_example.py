# Standard Library
import base64

# Third Party
import aiohttp
import pytest

HOST = "http://localhost:8080/"
BASIC_AUTH = base64.b64encode(b"testuser:insecurepassword").decode()

headers = {"Authorization": f"Basic {BASIC_AUTH}"}


@pytest.mark.asyncio
@pytest.mark.docker
async def test_example(dockercompose) -> None:
    """Start docker compose fixture and run endpoint check."""
    print(headers)
    async with aiohttp.ClientSession() as session, session.get(HOST, headers=headers) as response:
        data = await response.json()

    assert len(data) > 0
