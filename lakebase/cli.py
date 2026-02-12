import argparse
import yaml
from pathlib import Path

from lakebase.project import ensure_project


def load_metadata(path: str) -> dict:
    """
    Load Lakebase metadata YAML file.

    Args:
        path: Path to metadata YAML file.

    Returns:
        Parsed YAML configuration as dictionary.

    Raises:
        FileNotFoundError: If metadata file does not exist.
        yaml.YAMLError: If YAML parsing fails.
    """
    file_path = Path(path).resolve()

    print(f"Loading metadata from {file_path}")

    with open(file_path) as f:
        return yaml.safe_load(f)


def deploy_project(lakebase_cfg: dict) -> None:
    """
    Ensure Lakebase project exists.

    Args:
        lakebase_cfg: Lakebase configuration section.
    """
    project_cfg = lakebase_cfg["project"]

    ensure_project(
        name=project_cfg["name"],
        display_name=project_cfg.get("display_name"),
        pg_version=project_cfg.get("pg_version", "17"),
    )


def deploy_from_metadata(cfg: dict) -> None:
    """
    Deploy Lakebase components from metadata.

    Execution order:
    1. Project
    2. Compute
    3. Synced tables

    Args:
        cfg: Parsed metadata configuration.
    """
    lakebase_cfg = cfg["lakebase"]

    deploy_project(lakebase_cfg)


def main() -> None:
    """
    CLI entry point for Lakebase deployment.

    Example:
        uv run lakebase-deploy --metadata metadata/dev.yml
    """
    parser = argparse.ArgumentParser(
        description="Deploy Lakebase Autoscaling infrastructure"
    )

    parser.add_argument(
        "--metadata",
        required=True,
        help="Path to Lakebase metadata YAML file",
    )

    args = parser.parse_args()

    cfg = load_metadata(args.metadata)

    deploy_from_metadata(cfg)

    print("Lakebase deployment finished")
