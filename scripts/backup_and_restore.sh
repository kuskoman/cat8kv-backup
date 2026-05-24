#!/usr/bin/env bash
set -e

echo "=== cat8kv e2e flow test ==="
echo ""

echo "[1] Backup..."
cat8kv backup
echo ""

echo "[2] Backup with sync..."
cat8kv backup --sync
echo ""

echo "[3] Verify backup files exist..."
test -f backups/config.json     && echo "    [OK] config.json exists"
test -f backups/interfaces.json && echo "    [OK] interfaces.json exists"
test -f backups/hostname.json   && echo "    [OK] hostname.json exists"
echo ""

echo "[4] Restore from latest..."
cat8kv restore backups
echo ""

echo "[5] Backup again to verify state after restore..."
cat8kv backup
echo ""

echo "[6]" Print git log to verify commit history...
git -C ./git-backups log --oneline -n 5
echo ""

echo "=== All done ==="
