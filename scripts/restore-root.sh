#!/usr/bin/env bash
set -euo pipefail
[[ $# == 0 ]] || { echo 'This command takes no arguments.' >&2; exit 2; }
project_dir=/srv/projects/calculator
state_dir=/var/lib/calculator
dump_file="$state_dir/restore/calculator_db.dump"
expected_sha256=b8cf743b6ab61964b97d0ec819ba02913fc62b19a59f356413173e77ddca754e
exec 9>/run/lock/calculator-deploy.lock
flock -n 9 || { echo 'Another Calculator operation is running.' >&2; exit 1; }
[[ ! -e "$state_dir/database-restored" ]] || { echo 'Already restored; re-import refused.' >&2; exit 1; }
[[ -f "$project_dir/.env" && -f "$dump_file" ]] || { echo 'Environment file or dump missing.' >&2; exit 1; }
actual=$(sha256sum "$dump_file")
[[ ${actual%% *} == "$expected_sha256" ]] || { echo 'Dump checksum mismatch.' >&2; exit 1; }
export CALCULATOR_ENV_FILE="$project_dir/.env"
compose=(/usr/bin/docker compose --env-file /dev/null --project-directory "$project_dir" -p calculator -f /etc/calculator/compose.yml)
if ! "${compose[@]}" config -q >/dev/null 2>&1 || ! "${compose[@]}" up -d --wait --wait-timeout 120 db_django >/dev/null 2>&1; then
    echo 'Database startup/configuration failed; raw output suppressed.' >&2; exit 1
fi
query() {
    "${compose[@]}" exec -T db_django sh -ec 'exec psql -X -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -At' 2>/dev/null
}
count=$(query <<'SQL'
SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE c.relkind IN ('r','p','v','m','f','S') AND n.nspname NOT IN ('pg_catalog','information_schema') AND n.nspname NOT LIKE 'pg_toast%';
SQL
)
[[ $count == 0 ]] || { echo 'Database is not empty; import refused.' >&2; exit 1; }
echo 'Restoring Calculator in one transaction'
if ! "${compose[@]}" exec -T db_django sh -ec 'exec pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --no-acl --single-transaction --exit-on-error' <"$dump_file" >/dev/null 2>&1; then
    echo 'Restore failed and transaction rolled back. Application not started.' >&2; exit 1
fi
# Read every expected count and migration identifier, but never user record contents.
result=$(query </etc/calculator/verify.sql) || { echo 'Verification failed; imported data retained.' >&2; exit 1; }
actual=$(printf '%s\n' "$result" | sha256sum)
expected=$(</etc/calculator/verification.sha256)
[[ ${actual%% *} == "$expected" ]] || { echo 'Verification mismatch; imported data retained, deployment blocked.' >&2; exit 1; }
umask 077
printf 'dump_sha256=%s\nverification_sha256=%s\n' "$expected_sha256" "$expected" >"$state_dir/database-restored"
echo 'Restore verified: 13 tables, 13 users, 13 albums, 10 selections, 23 migrations. Application not started.'
