# Standard Library
import json
import os
import shlex
import subprocess

# Third Party
import pytest


@pytest.mark.parametrize(
    "branch_env_var_name",
    ["DBT_CLOUD_GIT_BRANCH", "DBT_GIT_BRANCH", None],
    ids=["gitbranch_env_var_dbt_cloud", "gitbranch_env_var_dbt", "gitbranch_env_var_none"],
)
@pytest.mark.parametrize(
    "gitbranch_vars_value", [True, False], ids=["gitbranch_project_vars", "gitbranch_no_project_vars"]
)
@pytest.mark.parametrize(
    "data_env,expectation",
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
def test_macro_generate_schema_name(data_env, expectation, branch_env_var_name, gitbranch_vars_value, tmp_path):
    ##### Given
    branch_name = "feature/custom-naming-macros"
    clean_branch = "feature_custom_naming_macros".upper()
    cleaned_slice = f"{clean_branch}__" if expectation and expectation != "PROD" else ""

    env = os.environ.copy()
    for env_var_unset_key in ["DBT_CLOUD_GIT_BRANCH", "DBT_GIT_BRANCH"]:
        if env_var_unset_key in env:
            del env[env_var_unset_key]


    # Conditionally set these environment values based on parametrised testing permutations
    if branch_env_var_name:
        env[branch_env_var_name] = branch_name

    if data_env:
        env["DBT_ENV_TYPE"] = data_env

    # Conditionally set this value based on parametrised testing permutations
    vars_flags = f'--vars \'{{"git_branch": "{branch_name}"}}\'' if gitbranch_vars_value else ""

    #### When
    output = subprocess.run(
        shlex.split(f"uv run dbt compile --target-path {tmp_path} {vars_flags}"), capture_output=True, env=env
    )

    # Then
    if expectation is None:
        # Path where no manifest should get generated due to invalid context configurations
        assert output.returncode == 2
        assert "Error: Invalid DBT_ENV_TYPE value:" in output.stdout.decode("utf-8")

    elif not gitbranch_vars_value and not branch_env_var_name and expectation != "PROD":
        # No environment variables set to define a slice and in non-PROD environment.
        assert output.returncode == 2
        assert "Error: Data Environment is non-PROD and no slice is defined for " in output.stdout.decode("utf-8")

    else:
        # Path where manifest gets generated
        assert output.returncode == 0, f"dbt-compile error: {output.stdout.decode('utf-8')}"
        manifest = json.loads((tmp_path / "manifest.json").read_text())

        models = [
            model_values for model_key, model_values in manifest["nodes"].items() if model_key.startswith("model.")
        ]
        assert models != []
        model_details = models[0]
        model_config = model_details["config"]
        model_config_database = model_config["database"].upper()
        model_config_schema = model_config["schema"].upper()

        assert model_details["schema"] == f"{cleaned_slice}{model_config_schema}"
        assert model_details["database"] == f"{expectation}__{model_config_database}"
