#!/usr/bin/env python3
"""
load_env.py — Carga credenciales desde .env.skill.mariadb y las imprime como variables de entorno.

El archivo .env.skill.mariadb debe estar en el directorio de trabajo actual (donde se ejecuta el comando).

Uso:
    eval "$(python3 load_env.py)"

O para obtener un dict en Python:
    from load_env import load_env
    creds = load_env()
"""

import sys
import re
from pathlib import Path


def load_env() -> dict:
    """Carga y parsea el archivo .env.skill.mariadb desde el directorio de trabajo actual."""
    env_file = Path.cwd() / ".env.skill.mariadb"

    if not env_file.exists():
        print(f"❌ No se encontró .env.skill.mariadb en el directorio actual: {Path.cwd()}", file=sys.stderr)
        sys.exit(1)

    creds = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            match = re.match(r'^([A-Z_][A-Z0-9_]*)=(.*)$', line)
            if match:
                key, value = match.groups()
                value = value.strip('"').strip("'")
                creds[key] = value

    required = ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing = [k for k in required if k not in creds]
    if missing:
        print(f"❌ Faltan claves en .env.skill.mariadb: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    return creds


if __name__ == "__main__":
    creds = load_env()
    for key, value in creds.items():
        safe_value = value.replace("'", "'\\''")
        print(f"export {key}='{safe_value}'")
