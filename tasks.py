# Third Party
from invoke import task
# from invoke_common_tasks import *  # noqa


@task
def docs(c):
    """Automate documentation tasks."""
    c.run("md_toc --in-place github --header-levels 4 README.md")
