#!/usr/bin/env python3
"""Resuelve credenciales MariaDB desde mariadb-schema.env en la raiz del proyecto."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ENV_FILE_NAME = 'mariadb-schema.env'
REQUIRED_KEYS = {
    'host': 'DB_HOST',
    'port': 'DB_PORT',
    'user': 'DB_USER',
    'password': 'DB_PASSWORD',
    'database': 'DB_NAME',
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Resuelve credenciales MariaDB desde mariadb-schema.env.'
    )
    parser.add_argument(
        '--format',
        choices=('shell', 'text'),
        default='shell',
        help='Formato de salida.',
    )
    parser.add_argument(
        '--database',
        help='Base de datos a usar en lugar de la resuelta desde el archivo.',
    )
    return parser.parse_args()


def find_project_root(start_path: Path) -> Path:
    current = start_path.resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if (candidate / '.git').exists() or (candidate / 'package.json').exists():
            return candidate

    return current


def parse_env_file(file_path: Path) -> dict[str, str]:
    env_vars: dict[str, str] = {}
    pattern = re.compile(r'^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$')

    for raw_line in file_path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue

        match = pattern.match(line)
        if not match:
            continue

        key, raw_value = match.groups()
        value = normalize_env_value(raw_value.strip())
        env_vars[key] = value

    return env_vars


def normalize_env_value(raw_value: str) -> str:
    if len(raw_value) >= 2 and raw_value[0] == raw_value[-1] and raw_value[0] in {'"', "'"}:
        quote = raw_value[0]
        value = raw_value[1:-1]
        if quote == '"':
            replacements = (
                ('\\n', '\n'),
                ('\\r', '\r'),
                ('\\t', '\t'),
                ('\\"', '"'),
                ("\\'", "'"),
                ('\\$', '$'),
                ('\\\\', '\\'),
            )
            for old_value, new_value in replacements:
                value = value.replace(old_value, new_value)
        return value.replace('\\$', '$').replace("\\'", "'").replace('\\"', '"')

    value = raw_value.split(' #', 1)[0].strip()
    return value.replace('\\$', '$')


def resolve_credentials(root_path: Path) -> tuple[dict[str, str], Path]:
    env_file_path = root_path / ENV_FILE_NAME
    if not env_file_path.exists():
        raise RuntimeError(f'No se encontro {ENV_FILE_NAME} en la raiz del proyecto.')

    env_vars = parse_env_file(env_file_path)
    resolved: dict[str, str] = {}

    for target_key, source_key in REQUIRED_KEYS.items():
        source_value = env_vars.get(source_key, '').strip()
        if not source_value:
            raise RuntimeError(f'Falta la variable {source_key} en {ENV_FILE_NAME}.')
        resolved[target_key] = source_value

    return resolved, env_file_path


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\\''") + "'"


def print_shell_exports(credentials: dict[str, str], env_file_path: Path) -> None:
    exports = {
        'DB_HOST': credentials['host'],
        'DB_PORT': credentials['port'],
        'DB_USER': credentials['user'],
        'DB_PASSWORD': credentials['password'],
        'DB_NAME': credentials['database'],
        'MARIADB_SKILL_SOURCE': str(env_file_path),
    }

    for key, value in exports.items():
        print(f'export {key}={shell_quote(value)}')


def print_text(credentials: dict[str, str], env_file_path: Path) -> None:
    print(f'source={env_file_path}')
    print(f'host={credentials["host"]}')
    print(f'port={credentials["port"]}')
    print(f'user={credentials["user"]}')
    print(f'database={credentials["database"]}')


def main() -> int:
    args = parse_args()
    try:
        root_path = find_project_root(Path.cwd())
        credentials, env_file_path = resolve_credentials(root_path)
    except RuntimeError as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1

    if args.database:
        credentials['database'] = args.database.strip()

    if args.format == 'text':
        print_text(credentials, env_file_path)
        return 0

    print_shell_exports(credentials, env_file_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())