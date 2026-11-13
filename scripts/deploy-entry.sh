#!/usr/bin/env bash
set -euo pipefail
if [[ ${SSH_ORIGINAL_COMMAND:-} =~ ^deploy\ sha256:[0-9a-f]{64}$ ]]; then
    exec /usr/bin/sudo -n /usr/local/sbin/calculator-deploy "$SSH_ORIGINAL_COMMAND"
fi
echo 'Only deploy sha256:<64 lowercase hexadecimal characters> is allowed.' >&2
exit 2
