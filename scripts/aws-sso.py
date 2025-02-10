# ruff: noqa: E501
# /// script
# requires-python = ">=3.11"
# dependencies = [
# ]
# ///
# https://docs.astral.sh/uv/guides/scripts/#creating-a-python-script
# https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata
# Standard Library
import configparser
import hashlib
import logging
from pathlib import Path

log = logging.getLogger(__name__)

aws_config = Path("~/.aws/").expanduser()
aws_sso_cache = aws_config / "sso/cache"
aws_credentials_file = aws_config / "credentials"
aws_config_file = aws_config / "config"

credentials = aws_credentials_file.read_text()


def main():
    cache_files = [p.stem for p in list(aws_sso_cache.glob("*.json"))]
    log.info(cache_files)

    parser = configparser.ConfigParser()
    parser.read(aws_config_file)
    for section in parser.sections():
        log.info(f"Section: {section}")
        key = None
        hash = None

        if section.startswith("profile") and parser.has_option(section, "sso_session"):
            key = parser.get(section, "sso_session")

        elif section.startswith("sso-session") and parser.has_option(section, "sso_start_url"):
            key = parser.get(section, "sso_start_url")

        if key:
            hash_object = hashlib.sha1(key.encode())
            hash = hash_object.hexdigest()
            log.info(hash)
            if hash in cache_files:
                log.info("Cache hit")
                log.info(f"{key} = {hash}.json")
                log.info((aws_sso_cache / f"{hash}.json").read_text())
            else:
                log.info("Cache miss")

    # TODO: aws sso get-role-credentials --role-name <role-name> --account-id <account-id> --access-token <access-token> --region <region>
    # aws sso list-accounts --profile <profile> --no-paginate --access-token <access-token> --region <region>
    # aws sso list-account-roles --profile <profile> --no-paginate --access-token <access-token> --region <region> --account-id <account-id>


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s::%(name)s::%(levelname)s::%(module)s:%(lineno)d| %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    main()
