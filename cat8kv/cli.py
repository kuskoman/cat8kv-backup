from pathlib import Path

import click

from cat8kv.backup import load, save, BACKUPS_DIR
from cat8kv.client import RestconfClient
from cat8kv.config import load_config, load_git_config
from cat8kv.git import sync


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option("--sync", "do_sync", is_flag=True, default=False, help="Sync to local Git repo after backup.")
def backup(do_sync: bool) -> None:
    config = load_config()
    client = RestconfClient(config)

    click.echo("Fetching configuration...")
    hostname = client.get_hostname()
    device_config = client.get_config()
    interfaces = client.get_interfaces()

    device_dir = save(hostname, device_config, interfaces)
    click.echo(f"[OK] Saved: {device_dir}/{{config,interfaces,hostname}}.json")

    if do_sync:
        git_config = load_git_config()
        sync(device_dir, git_config)
        click.echo(f"[OK] Synced to: {git_config.repo_path}")


@cli.command()
@click.argument("directory", default=str(BACKUPS_DIR), type=click.Path(exists=True, file_okay=False, path_type=Path))
def restore(directory: Path) -> None:
    config = load_config()
    client = RestconfClient(config)

    click.echo(f"Loading backup from: {directory}/config.json")
    device_config = load(directory)
    hostname = device_config["Cisco-IOS-XE-native:native"]["hostname"]

    click.echo(f"Restoring configuration to: {hostname}")
    client.restore_config(device_config)
    click.echo("[OK] Configuration restored")
