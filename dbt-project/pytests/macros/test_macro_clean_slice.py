# Standard Library
import os
import shlex
import subprocess

# Third Party
import pytest

DEPLOYMENT_ENV_VARS = ["DBT_CLOUD_PR_ID", "DBT_CLOUD_JOB_ID", "DBT_CLOUD_RUN_ID"]
DEVELOPMENT_ENV_VARS = ["DBT_CLOUD_GIT_BRANCH", "DBT_GIT_BRANCH"]
ALL_ENV_VARS = DEPLOYMENT_ENV_VARS + DEVELOPMENT_ENV_VARS


@pytest.mark.parametrize("is_deployment", [True, False], ids=["deploy", "develop"])
@pytest.mark.parametrize(
    "env_var_name",
    ["DBT_CLOUD_GIT_BRANCH", "DBT_GIT_BRANCH", None],
    ids=["env_var_dbt_cloud", "env_var_dbt", "env_var_none"],
)
@pytest.mark.parametrize("vars_value", [True, False], ids=["project_vars", "no_project_vars"])
def test_macro_clean_slice(is_deployment, env_var_name, vars_value, tmp_path):
    ########## Given

    branch_name = "feature/DPP-76-custom-naming-macros"
    clean_branch = "feature_DPP_76_custom_naming_macros"
    is_branch_defined = bool(vars_value or env_var_name)

    pr_id = "123"
    job_id = "456"
    run_id = "789"
    expected_ci_slice = f"PR{pr_id}_JOB{job_id}_RUN{run_id}"
    logging_marker = "Clean slice: "
    error_log_marker = "Error: Data Environment is non-PROD and no slice is defined"

    # Clean copy of environment variables to use in shell context
    env = os.environ.copy()
    for env_var_unset_key in ALL_ENV_VARS:
        if env_var_unset_key in env:
            del env[env_var_unset_key]

    # Conditionally set these values based on parametrised testing permutations
    if is_deployment:
        env["DBT_CLOUD_PR_ID"] = pr_id
        env["DBT_CLOUD_JOB_ID"] = job_id
        env["DBT_CLOUD_RUN_ID"] = run_id

    # Conditionally set the branch name
    if env_var_name:
        env[env_var_name] = branch_name

    args_flags = "--args '{\"debug_logging\": true}'"  # Needed to emit to stdout for testing

    # Conditionally set this value based on parametrised testing permutations
    vars_flags = f'--vars \'{{"git_branch": "{branch_name}"}}\'' if vars_value else ""

    command = f"uv run dbt run-operation clean_slice {args_flags} {vars_flags} --target-path {tmp_path}"

    ########## When
    output = subprocess.run(shlex.split(command), capture_output=True, text=True, env=env)

    ########## Then

    if not is_branch_defined and not is_deployment:
        # Unhappy path where no slice is defined in development environment
        # This is actually caused by macros/generate_schema_name.sql and not macros/clean_slice.sql
        # Still a valid and expected symptom in this situation when the project has this configuration.
        assert output.returncode == 2
        assert error_log_marker in output.stdout

    else:
        # Happy path where something is set to finally define a slice
        assert logging_marker in output.stdout
        out_lines = output.stdout.split("\n")
        # assert out_lines == []
        logging_lines = [line for line in out_lines if logging_marker in line]
        assert len(logging_lines) == 1

        if is_branch_defined:
            assert logging_lines[0].split(logging_marker)[1] == clean_branch
        else:
            if is_deployment:
                # When in a deployment environment, expected the CI slice to be defined
                assert logging_lines[0].split(logging_marker)[1] == expected_ci_slice
