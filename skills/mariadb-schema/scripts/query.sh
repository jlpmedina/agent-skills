#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Uso:
  bash ./.agents/skills/mariadb-schema/scripts/query.sh [--database BASE] "SQL"

Restricciones:
  - Solo permite SHOW, DESCRIBE y DESC
  - SELECT solo sobre information_schema
  - Bloquea multiples sentencias
EOF
}

normalize_sql() {
  printf '%s' "$1" \
    | tr '\n' ' ' \
    | sed -E 's/[[:space:]]+/ /g' \
    | sed -E 's/^[[:space:]]+|[[:space:]]+$//g'
}

validate_sql() {
  local raw_sql="$1"
  local normalized_sql upper_sql statement sql_without_trailing_semicolon first_word

  normalized_sql="$(normalize_sql "$raw_sql")"
  if [[ -z "$normalized_sql" ]]; then
    echo "ERROR: Debes enviar una consulta." >&2
    return 1
  fi

  if [[ "$normalized_sql" == *"--"* ]] || [[ "$normalized_sql" == *"/*"* ]] || [[ "$normalized_sql" == *"#"* ]]; then
    echo "ERROR: La consulta no debe incluir comentarios." >&2
    return 1
  fi

  sql_without_trailing_semicolon="${normalized_sql%;}"
  if [[ "$sql_without_trailing_semicolon" == *";"* ]]; then
    echo "ERROR: Solo se permite una sentencia por ejecucion." >&2
    return 1
  fi

  upper_sql="$(printf '%s' "$sql_without_trailing_semicolon" | tr '[:lower:]' '[:upper:]')"
  first_word="${upper_sql%% *}"

  case "$first_word" in
    SHOW|DESCRIBE|DESC)
      return 0
      ;;
    SELECT)
      if [[ "$upper_sql" != *"INFORMATION_SCHEMA"* ]]; then
        echo "ERROR: SELECT solo puede consultar information_schema." >&2
        return 1
      fi

      if [[ "$upper_sql" == *"INTO OUTFILE"* ]] || [[ "$upper_sql" == *"INTO DUMPFILE"* ]] || [[ "$upper_sql" == *"LOAD DATA"* ]]; then
        echo "ERROR: La consulta incluye una operacion no permitida." >&2
        return 1
      fi

      return 0
      ;;
    *)
      echo "ERROR: Sentencia no permitida. Usa SHOW, DESCRIBE, DESC o SELECT sobre information_schema." >&2
      return 1
      ;;
  esac
}

DATABASE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --database)
      DATABASE="${2:?Falta valor para --database}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "ERROR: Opcion no soportada: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -ne 1 ]]; then
  usage >&2
  exit 1
fi

SQL="$1"
validate_sql "$SQL"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOLVE_ARGS=(--format shell)

if [[ -n "$DATABASE" ]]; then
  RESOLVE_ARGS+=(--database "$DATABASE")
fi

if ! command -v mariadb >/dev/null 2>&1; then
  echo "ERROR: No se encontro el CLI 'mariadb' en PATH." >&2
  exit 1
fi

eval "$(python3 "$SCRIPT_DIR/resolve_credentials.py" "${RESOLVE_ARGS[@]}")"

printf 'Usando credenciales desde %s\n' "$MARIADB_SKILL_SOURCE" >&2

# Ejecutar la consulta y capturar el exit code
# Exit code 130 (SIGINT) puede ocurrir por cierre prematuro del buffer del terminal
# pero no indica un error real si la consulta se ejecuto correctamente
mariadb \
  --host="$DB_HOST" \
  --port="$DB_PORT" \
  --user="$DB_USER" \
  --password="$DB_PASSWORD" \
  --default-character-set=utf8mb4 \
  --connect-timeout=5 \
  --table \
  "$DB_NAME" \
  --execute "$SQL" && exit_code=0 || exit_code=$?

if [[ $exit_code -eq 130 ]]; then
  exit 0
fi
exit $exit_code