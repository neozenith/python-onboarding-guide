# Standard Library
import json
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
    "branch_env_var_name",
    ["DBT_CLOUD_GIT_BRANCH", "DBT_GIT_BRANCH", None],
    ids=["gitbranch_env_var_dbt_cloud", "gitbranch_env_var_dbt", "gitbranch_env_var_none"],
)
@pytest.mark.parametrize(
    "gitbranch_vars_value", [True, False], ids=["gitbranch_project_vars", "gitbranch_no_project_vars"]
)
@pytest.mark.parametrize(
    "data_env,expected_data_env",
    [
        # Valid cases
        ("DEV", "DEV"),
        ("TEST", "TEST"),
        ("test", "TEST"),
        ("PROD", "PROD"),
        ("prod", "PROD"),
        ("", "DEV"),
        (None, "DEV"),
        # Invalid cases
        ("INVALID", None),
    ],
)
def test_macro_generate_schema_name(
    data_env, expected_data_env, branch_env_var_name, gitbranch_vars_value, is_deployment, tmp_path
):
    ########## Given
    branch_name = "feature/DPP-76-custom-naming-macros"
    clean_branch = "feature_DPP_76_custom_naming_macros".upper()
    is_branch_defined = bool(gitbranch_vars_value or branch_env_var_name)
    cleaned_slice = f"{clean_branch}__" if expected_data_env and expected_data_env != "PROD" else ""
    pr_id = "123"
    job_id = "456"
    run_id = "789"
    expected_ci_slice = (
        f"PR{pr_id}_JOB{job_id}_RUN{run_id}__" if expected_data_env and expected_data_env != "PROD" else ""
    )

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
    if branch_env_var_name:
        env[branch_env_var_name] = branch_name

    if data_env:
        env["DBT_ENV_TYPE"] = data_env

    # Conditionally set this value based on parametrised testing permutations
    vars_flags = f'--vars \'{{"git_branch": "{branch_name}"}}\'' if gitbranch_vars_value else ""

    command = f"uv run dbt parse --no-partial-parse --target-path {tmp_path} {vars_flags}"

    ########## When

    output = subprocess.run(shlex.split(command), capture_output=True, env=env)

    ########## Then

    if expected_data_env is None:
        # Path where no manifest should get generated due to invalid context configurations
        assert output.returncode == 2, f"""Parsing succeeded when it should have thrown an Invalid DBT_ENV_TYPE error. 
        dbt output: {output.stdout.decode("utf-8")}"""

        assert "Error: Invalid DBT_ENV_TYPE value:" in output.stdout.decode("utf-8")

    elif not is_branch_defined and not is_deployment and expected_data_env != "PROD":
        # No environment variables set to define a slice and in non-PROD environment.
        assert output.returncode == 2, f"""Parsing succeeded when it should have thrown an Invalid Slice error:
        {output.stdout.decode("utf-8")}"""
        assert "Error: Data Environment is non-PROD and no slice is defined for " in output.stdout.decode("utf-8")

    else:
        # Path where manifest gets generated
        assert output.returncode == 0, f"dbt-parse error: {output.stdout.decode('utf-8')}"
        manifest = json.loads((tmp_path / "manifest.json").read_text())

        models = [
            model_values for model_key, model_values in manifest["nodes"].items() if model_key.startswith("model.")
        ]
        assert models != []
        model_details = models[0]
        model_config = model_details["config"]
        model_config_database = model_config["database"].upper()
        model_config_schema = model_config["schema"].upper()

        # Regardless of if it is deployment or development, if a branch is defined then use it.
        if is_branch_defined:
            assert model_details["schema"] == f"{cleaned_slice}{model_config_schema}"
        else:
            # When a branch is not defined and it is a deployment, then the CI slice should be used.
            if is_deployment:
                assert model_details["schema"] == f"{expected_ci_slice}{model_config_schema}"

        assert model_details["database"] == f"{model_config_database}_{expected_data_env}"
