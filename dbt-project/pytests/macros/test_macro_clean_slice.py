# Standard Library
import os
import shlex
import subprocess

# Third Party
import pytest


@pytest.mark.parametrize(
    "env_var_name",
    ["DBT_CLOUD_GIT_BRANCH", "DBT_GIT_BRANCH", None],
    ids=["env_var_dbt_cloud", "env_var_dbt", "env_var_none"],
)
@pytest.mark.parametrize("vars_value", [True, False], ids=["project_vars", "no_project_vars"])
def test_macro_clean_slice(env_var_name, vars_value):
    # Given
    logging_marker = "Clean slice: "
    error_logging_marker = "Error: Data Environment is non-PROD and no slice is defined for"
    branch_name = "feature/custom-naming-macros"
    clean_branch = "feature_DPP_76_custom_naming_macros"
    env = os.environ.copy()
    for env_var_unset_key in ["DBT_CLOUD_GIT_BRANCH", "DBT_GIT_BRANCH"]:
        if env_var_unset_key in env:
            del env[env_var_unset_key]

    # Conditionally set this value based on parametrised testing permutations
    if env_var_name:
        env[env_var_name] = branch_name

    args_flags = "--args '{\"debug_logging\": true}'"  # Needed to emit to stdout for testing

    # Conditionally set this value based on parametrised testing permutations
    vars_flags = f'--vars \'{{"git_branch": "{branch_name}"}}\'' if vars_value else ""

    command = f"uv run dbt run-operation clean_slice {args_flags} {vars_flags}"

    # When
    output = subprocess.run(shlex.split(command), capture_output=True, text=True, env=env)

    # Then
    if not vars_value and not env_var_name:
        # No environment variables or project variables set, and the data environment defaults to DEV when not set
        # Assert error is thrown that a slice is not defined for non-PROD environments
        assert output.returncode == 2
        assert error_logging_marker in output.stdout

    else:
        # Happy path where something is set to finally define a slice
        assert logging_marker in output.stdout
        out_lines = output.stdout.split("\n")
        # assert out_lines == []
        logging_lines = [line for line in out_lines if logging_marker in line]

        assert len(logging_lines) == 1

        if not vars_value and not env_var_name:
            # No environment variables or project variables set, default is empty string
            assert logging_lines[0].split(logging_marker)[1] == ""
        else:
            assert logging_lines[0].split(logging_marker)[1] == clean_branch
