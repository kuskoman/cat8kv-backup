# cat8kv-backup

Backup and restore Cisco Cat8000v configuration via RESTCONF. Saves three predictable files per run:

- `backups/config.json` — full native configuration
- `backups/interfaces.json` — interface configuration
- `backups/hostname.json` — hostname

Optionally commits changes to a local git repository, giving you a full history of configuration diffs.

The project is currently designed to work with only one machine. If you need to manage multiple devices, you can run multiple instances of the tool with different `.env` files and backup directories and orchestrate them with a script or cron jobs.

## Requirements

- Python 3.13+
- Cisco Catalyst 8000v running IOS XE 17.12+, with RESTCONF enabled
- Tested against [Cisco DevNet Sandbox: IOS XE on Catalyst 8000v](https://devnetsandbox.cisco.com) (reservable, requires VPN access via Cisco Secure Client)

## Commands

``` bash
cat8kv backup           # fetch and save config
cat8kv backup --sync    # fetch, save, and commit to git repo
cat8kv restore [FILE]   # restore from backup file
```

## Configuration

Copy `.env.example` to `.env` and fill in your device details:

```bash
cp .env.example .env
```

```env
DEVICE_HOST=192.168.1.1
DEVICE_USERNAME=developer
DEVICE_PASSWORD=yourpassword
DEVICE_PORT=443
GIT_REPO_PATH=./git-backups
GIT_COMMITTER_NAME=cat8kv-backup
GIT_COMMITTER_EMAIL=cat8kv-backup@local
```

---

## Setup: Local (development)

Requires Python 3.13+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Run:

```bash
cat8kv backup
cat8kv backup --sync
cat8kv restore backups/cat8000v/latest.json
```

---

## Setup: Local

```bash
pip install .
```

Run:

```bash
cat8kv backup
cat8kv backup --sync
cat8kv restore backups/cat8000v/latest.json
```

---

## Setup: Docker

Build the image:

```bash
docker build -t cat8kv-backup .
```

Backup:

```bash
docker run --rm --env-file .env -v "$(pwd)/backups:/app/backups" cat8kv-backup backup
```

Restore:

```bash
docker run --rm --env-file .env -v "$(pwd)/backups:/app/backups" cat8kv-backup restore backups/cat8000v/latest.json
```

### Git sync in Docker

Syncing to a git repository from inside Docker may fail with permission errors (`chmod`/`chown`) depending on the host filesystem and how the volume is mounted. If you need git history, run `cat8kv backup --sync` locally instead of inside the container.

If you still want to try it, mount the git repo volume:

```bash
docker run --rm --env-file .env \
  -v "$(pwd)/backups:/app/backups" \
  -v "$(pwd)/git-backups:/app/git-backups" \
  cat8kv-backup backup --sync
```

## Testing

Run offline unit tests:

```bash
pytest tests/ -v
```

Run e2e flow test (requires VPN and active sandbox):

```bash
./scripts/test_flow.sh
```
