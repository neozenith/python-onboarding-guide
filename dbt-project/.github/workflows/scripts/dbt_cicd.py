# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests",
#   "types-requests"
# ]
# ///
# https://docs.astral.sh/uv/guides/scripts/#creating-a-python-script
# https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata
# Adapted from https://github.com/dbt-labs/jaffle-shop/blob/main/.github/workflows/scripts/dbt_cloud_run_job.py
import asyncio
import json
import logging
import os

import requests

# Set up logging
log = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# get environment variables
# ------------------------------------------------------------------------------

# Required environment variables
api_base = os.getenv("DBT_CLOUD_HOST", "cloud.getdbt.com")
api_key = os.environ["DBT_CLOUD_SERVICE_TOKEN"]
account_id = os.environ["DBT_ACCOUNT_ID"]
project_id = os.environ["DBT_PROJECT_ID"]
job_id = os.environ["DBT_CLOUD_JOB_ID"]


# Optional environment variables
job_cause = os.getenv("DBT_JOB_CAUSE", "API-triggered job")
git_branch = os.getenv("DBT_JOB_BRANCH", None)
git_sha = os.getenv("DBT_JOB_SHA", None)
github_pr_id = os.getenv("GITHUB_PR_ID", None)
schema_override = os.getenv("DBT_JOB_SCHEMA_OVERRIDE", None)


req_auth_header = {"Authorization": f"Token {api_key}"}
req_job_url = f"https://{api_base}/api/v2/accounts/{account_id}/jobs/{job_id}/run/"
run_status_map = {  # dbt run statuses are encoded as integers. This map provides a human-readable status
    1: "Queued",
    2: "Starting",
    3: "Running",
    10: "Success",
    20: "Error",
    30: "Cancelled",
}

type AuthHeader = dict[str, str | int]


async def run_job(
    url: str,
    headers: AuthHeader,
    cause: str,
    branch: str | None = None,
    github_pr_id: str | None = None,
    git_sha: str | None = None,
    schema_override: str | None = None,
) -> int:
    """Runs a dbt job and returns the run id."""
    req_payload = {"cause": cause}

    if github_pr_id:
        req_payload["github_pull_request_id"] = int(github_pr_id)

    if git_sha:
        req_payload["git_sha"] = git_sha

    if schema_override:
        req_payload["schema_override"] = schema_override.replace("-", "_").replace("/", "_")

    # trigger job
    log.info(f"Triggering job:\n\turl: {url}\n\tpayload:\n{json.dumps(req_payload, indent=2)}")

    response = requests.post(url, headers=headers, json=req_payload)
    response_json = response.json()
    log.debug(json.dumps(response_json, indent=2))
    run_id: int = response_json["data"]["id"]
    return run_id


async def get_run_status(url: str, headers: AuthHeader) -> str:
    """Gets the status of a running dbt job."""
    response = requests.get(url, headers=headers)
    run_status_code: int = response.json()["data"]["status"]
    run_status = run_status_map[run_status_code]
    return run_status


async def main():
    log.info("Beginning request for job run...")

    # run job
    run_id: int = 0
    try:
        run_id = await run_job(
            req_job_url, req_auth_header, job_cause, git_branch, github_pr_id, git_sha, schema_override
        )
    except Exception as e:
        log.error(f"ERROR! - Could not trigger job:\n {e}")
        raise e

    # build status check url and run status link
    req_status_url = f"https://{api_base}/api/v2/accounts/{account_id}/runs/{run_id}/"
    run_status_link = f"https://{api_base}/deploy/{account_id}/projects/{project_id}/runs/{run_id}/"

    # update user with status link
    log.info(f"Job running! See job status at {run_status_link}")

    # check status indefinitely with an initial wait period
    await asyncio.sleep(30)
    while True:
        status = await get_run_status(req_status_url, req_auth_header)
        log.info(f"Run status -> {status}")

        if status in ["Error", "Cancelled"]:
            raise Exception(f"Run failed or canceled. See why at {run_status_link}")

        if status == "Success":
            log.info(f"Job completed successfully! See details at {run_status_link}")
            return

        await asyncio.sleep(10)


if __name__ == "__main__":
    log_level = logging.DEBUG if os.getenv("LOG_LEVEL", None) == "DEBUG" else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s::%(name)s::%(levelname)s::%(module)s:%(lineno)d| %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    log.info(f"""
        Configuration:
        api_base: {api_base}
        account_id: {account_id}
        project_id: {project_id}
        job_id: {job_id}
        job_cause: {job_cause}
        git_branch: {git_branch}
        git_sha: {git_sha}
        github_pr_id: {github_pr_id}
        schema_override: {schema_override}
    """)
    asyncio.run(main())
