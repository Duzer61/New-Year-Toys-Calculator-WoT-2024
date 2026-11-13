#!/usr/bin/env bash
set -euo pipefail
[[ $EUID == 0 && $# == 1 && -f $1 ]] || { echo 'Usage: sudo calculator-authorize-key /path/to/public-key.pub' >&2; exit 2; }
# Only explicit public-key files; do not accidentally open a private key.
[[ $1 == *.pub ]] || { echo 'Only .pub public key files accepted.' >&2; exit 2; }
mapfile -t lines <"$1"
[[ ${#lines[@]} == 1 && ${lines[0]} =~ ^ssh-ed25519\ [A-Za-z0-9+/=]+(\ .*)?$ ]] || { echo 'Expected one Ed25519 public key.' >&2; exit 2; }
/usr/bin/ssh-keygen -lf "$1" >/dev/null 2>&1 || { echo 'Invalid public key.' >&2; exit 2; }
target=/var/lib/calculator-deploy/.ssh/authorized_keys
[[ ! -e "$target" ]] || { echo 'Key already configured; refusing overwrite.' >&2; exit 1; }
umask 077
printf 'restrict,command="/usr/local/sbin/calculator-deploy-entry" %s\n' "${lines[0]}" >"$target"
chown root:root "$target"
chmod 600 "$target"
echo 'Restricted Calculator deployment public key installed.'
