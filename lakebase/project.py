from databricks.sdk import WorkspaceClient
from databricks.sdk.service.postgres import Project, ProjectSpec
from databricks.sdk.errors import NotFound


def ensure_project(
    name: str,
    display_name: str | None = None,
    pg_version: str = "17",
) -> None:
    """
    Ensure that a Lakebase project exists.

    This function checks whether a Lakebase Postgres project with the given
    ID already exists. If it exists, the function logs its current state and
    returns without making changes. If it does not exist, the project is
    created with the specified display name and PostgreSQL version.

    The operation is idempotent: running it multiple times will not recreate
    an existing project.

    Args:
        name: Lakebase project ID (not the full resource path).
        display_name: Human-readable project name shown in the UI.
            Defaults to the project ID if not provided.
        pg_version: PostgreSQL major version to provision for the project.
            Defaults to "17".

    Raises:
        databricks.sdk.errors.NotFound: Internally handled when determining
            whether the project exists.
    """
    w = WorkspaceClient()
    display_name = display_name or name

    try:
        project = w.postgres.get_project(
            name=f"projects/{name}"
        )
        print(
            f"Project already exists: "
            f"name={project.name}, "
            f"display_name={project.status.display_name}, "
            f"pg_version={project.status.pg_version}"
        )
        return

    except NotFound:
        print(f"Creating Lakebase project: {name}...")

    result = w.postgres.create_project(
        project_id=name,
        project=Project(
            spec=ProjectSpec(
                display_name=display_name,
                pg_version=pg_version,
            )
        ),
    ).wait()

    print(
        f"Created Lakebase project: "
        f"name={result.name}, "
        f"display_name={result.status.display_name}, "
        f"pg_version={result.status.pg_version}"
    )
