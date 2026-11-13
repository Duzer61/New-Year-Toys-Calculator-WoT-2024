#!/usr/bin/env bash
set -euo pipefail
[[ $EUID == 0 && $# == 0 ]] || { echo 'Run with sudo, without arguments.' >&2; exit 2; }
source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
# No edits to shared services, Career Tracker, SSH daemon, firewall, or existing Nginx sites.
for path in /etc/calculator /var/lib/calculator /srv/projects/calculator /usr/local/sbin/calculator-deploy /usr/local/sbin/calculator-deploy-entry /usr/local/sbin/calculator-restore /etc/sudoers.d/calculator-deploy /usr/local/sbin/calculator-authorize-key; do
    [[ ! -e $path ]] || { echo "Refusing to overwrite existing path: $path" >&2; exit 1; }
done
! getent passwd calculator-deploy >/dev/null || { echo 'Deployment user already exists; stop for review.' >&2; exit 1; }
[[ -z $(docker ps -aq --filter label=com.docker.compose.project=calculator) ]] || { echo 'Calculator containers already exist; stop for review.' >&2; exit 1; }
[[ -z $(docker volume ls -q --filter label=com.docker.compose.project=calculator) ]] || { echo 'Calculator volumes already exist; stop for review.' >&2; exit 1; }
! ss -H -lnt 'sport = :9000' | read -r _ || { echo 'Port 9000 is occupied.' >&2; exit 1; }
[[ $(sha256sum "$source_dir/restore/calculator_db.dump" | cut -d' ' -f1) == b8cf743b6ab61964b97d0ec819ba02913fc62b19a59f356413173e77ddca754e ]] || { echo 'Dump checksum mismatch.' >&2; exit 1; }
install -d -o root -g root -m 755 /etc/calculator /srv/projects/calculator
install -d -o root -g root -m 700 /var/lib/calculator /var/lib/calculator/restore /var/lib/calculator/backups
install -o root -g root -m 644 "$source_dir/compose.yml" /etc/calculator/compose.yml
install -o root -g root -m 644 "$source_dir/nginx.conf" /etc/calculator/nginx.conf
install -o root -g root -m 644 "$source_dir/verify.sql" /etc/calculator/verify.sql
install -o root -g root -m 644 "$source_dir/verification.sha256" /etc/calculator/verification.sha256
install -o root -g root -m 644 "$source_dir/.env.example" /srv/projects/calculator/.env.example
install -o root -g root -m 600 "$source_dir/restore/calculator_db.dump" /var/lib/calculator/restore/calculator_db.dump
install -o root -g root -m 755 "$source_dir/scripts/deploy-root.sh" /usr/local/sbin/calculator-deploy
install -o root -g root -m 755 "$source_dir/scripts/deploy-entry.sh" /usr/local/sbin/calculator-deploy-entry
install -o root -g root -m 755 "$source_dir/scripts/restore-root.sh" /usr/local/sbin/calculator-restore
install -o root -g root -m 755 "$source_dir/scripts/authorize-key.sh" /usr/local/sbin/calculator-authorize-key
useradd --system --create-home --home-dir /var/lib/calculator-deploy --shell /bin/bash calculator-deploy
# Root owns home and authorized_keys, so the deployment account cannot change its restrictions.
chown root:root /var/lib/calculator-deploy
chmod 755 /var/lib/calculator-deploy
install -d -o root -g root -m 755 /var/lib/calculator-deploy/.ssh
sudoers=$(mktemp)
trap 'rm -f "$sudoers"' EXIT
printf 'calculator-deploy ALL=(root) NOPASSWD: /usr/local/sbin/calculator-deploy\n' >"$sudoers"
visudo -cf "$sudoers" >/dev/null
install -o root -g root -m 440 "$sudoers" /etc/sudoers.d/calculator-deploy
echo 'Calculator files installed. No containers started. No real .env created. No SSH key authorized. Nginx unchanged.'
