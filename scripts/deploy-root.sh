#!/usr/bin/env bash
set -euo pipefail
[[ $# == 1 && $1 =~ ^deploy\ sha256:[0-9a-f]{64}$ ]] || { echo 'Invalid deployment request.' >&2; exit 2; }
project_dir=/srv/projects/calculator
state_dir=/var/lib/calculator
exec 9>/run/lock/calculator-deploy.lock
flock -n 9 || { echo 'Another Calculator operation is running.' >&2; exit 1; }
[[ -s "$state_dir/database-restored" ]] || { echo 'Database restore is not verified; deployment refused.' >&2; exit 1; }
[[ -f "$project_dir/.env" ]] || { echo 'Environment file missing.' >&2; exit 1; }
export CALCULATOR_ENV_FILE="$project_dir/.env"
export CALCULATOR_IMAGE="duzer61/calculator@${1#deploy }"
compose=(/usr/bin/docker compose --env-file /dev/null --project-directory "$project_dir" -p calculator -f /etc/calculator/compose.yml)
step() {
    local label=$1; shift
    echo "$label"
    if ! "$@" >/dev/null 2>&1; then
        echo "$label failed. Raw output suppressed; existing data retained. No automatic database rollback." >&2
        exit 1
    fi
}
step 'Checking configuration' "${compose[@]}" config -q
step 'Pulling application image' "${compose[@]}" pull calculator
step 'Checking database' "${compose[@]}" up -d --wait --wait-timeout 120 --pull never db_django
umask 077
mkdir -p "$state_dir/backups"
backup="$state_dir/backups/predeploy-$(date -u +%Y%m%dT%H%M%SZ)-$$.dump"
echo 'Saving database before migrations'
if ! "${compose[@]}" exec -T db_django sh -ec 'exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc --no-owner --no-acl' >"$backup" 2>/dev/null; then
    echo 'Database backup failed; update refused.' >&2; exit 1
fi
[[ -s "$backup" ]] || { echo 'Empty backup; update refused.' >&2; exit 1; }
step 'Stopping Calculator gateway and application' "${compose[@]}" stop nginx calculator
step 'Checking Django configuration' "${compose[@]}" run --rm --no-deps calculator python manage.py check
step 'Applying committed Django migrations' "${compose[@]}" run --rm --no-deps calculator python manage.py migrate --noinput
step 'Checking migration state' "${compose[@]}" run --rm --no-deps calculator python manage.py migrate --check
step 'Collecting static assets' "${compose[@]}" run --rm --no-deps calculator python manage.py collectstatic --noinput
step 'Copying project static assets' "${compose[@]}" run --rm --no-deps calculator sh -ec 'cp -R /calculator_app/static/. /calculator_app/staticfiles/'
step 'Starting application' "${compose[@]}" up -d --no-deps --wait --wait-timeout 180 calculator
step 'Starting gateway' "${compose[@]}" up -d --no-deps --wait --wait-timeout 180 nginx
step 'Checking local HTTP' /usr/bin/curl --fail --silent --output /dev/null --header 'Host: collider.hopto.org' http://127.0.0.1:9000/
printf '%s\n' "$CALCULATOR_IMAGE" >"$state_dir/current-image"
echo 'Calculator deployment completed.'
