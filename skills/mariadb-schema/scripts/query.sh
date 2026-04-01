#!/usr/bin/env bash
# query.sh — Ejecuta queries de solo lectura en MariaDB/MySQL
# Uso: bash query.sh HOST PORT USER PASSWORD DATABASE "SQL"

set -euo pipefail

HOST="${1:?Falta HOST}"
PORT="${2:?Falta PORT}"
USER="${3:?Falta USER}"
PASSWORD="${4:?Falta PASSWORD}"
DATABASE="${5:?Falta DATABASE}"
SQL="${6:?Falta SQL}"

# Bloquear queries de escritura antes de enviarlas al servidor
UPPER_SQL=$(echo "$SQL" | tr '[:lower:]' '[:upper:]')
for FORBIDDEN in "INSERT" "UPDATE" "DELETE" "DROP" "TRUNCATE" "ALTER" "CREATE" "GRANT" "REVOKE" "REPLACE" "LOAD DATA" "CALL" "EXEC"; do
  if echo "$UPPER_SQL" | grep -qw "$FORBIDDEN"; then
    echo "❌ ERROR: Query bloqueada — contiene '$FORBIDDEN'. Esta skill es solo de lectura." >&2
    exit 1
  fi
done

# Ejecutar con usuario de solo lectura (--skip-column-names para output limpio opcional)
mariadb \
  -h "$HOST" \
  -P "$PORT" \
  -u "$USER" \
  -p"$PASSWORD" \
  --default-character-set=utf8mb4 \
  --table \
  "$DATABASE" \
  -e "$SQL"
