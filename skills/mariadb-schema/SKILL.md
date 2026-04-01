---
name: mariadb-schema
description: "Inspeccion rapida y de solo lectura del esquema MariaDB/MySQL con el CLI mariadb. Usar cuando necesites tablas, columnas, describe, foreign keys, relaciones, SHOW CREATE TABLE o contexto de base de datos para crear modulos, tipos o agentes con mayor precision. Resuelve credenciales desde el .env raiz del proyecto con fallback determinista."
argument-hint: "Tabla objetivo o consulta de introspeccion. Solo permite SHOW, DESCRIBE y SELECT sobre information_schema."
---

# MariaDB Schema

Usa esta skill cuando necesites entender una base MariaDB/MySQL antes de crear modulos, acciones, tipos o consultas. Esta skill esta optimizada para:

- Encontrar credenciales rapido desde la raiz del repo sin `find`
- Ejecutar solo introspeccion de esquema
- Pedir la menor cantidad posible de informacion

## Flujo

1. Ejecuta la consulta mas pequena posible con [query.sh](./scripts/query.sh).
2. Empieza por `SHOW TABLES` o `DESCRIBE tabla`.
3. Si necesitas relaciones, consulta `information_schema.KEY_COLUMN_USAGE`.
4. Usa `SHOW CREATE TABLE` solo cuando hagan falta constraints o detalles finos.

## Credenciales

La resolucion de credenciales la hace [resolve_credentials.py](./scripts/resolve_credentials.py). El flujo es determinista y rapido:

1. Busca la raiz del proyecto subiendo desde el directorio actual hasta encontrar `.git` o `package.json`.
2. Lee solo `mariadb-schema.env` en esa raiz.
3. Exige un unico juego de credenciales con estas variables:
  - `DB_HOST`
  - `DB_PORT`
  - `DB_USER`
  - `DB_PASSWORD`
  - `DB_NAME`

La skill no usa `.env`, `.env.local` ni perfiles alternos.

## Uso

Consulta simple:

```bash
bash ./.agents/skills/mariadb-schema/scripts/query.sh "SHOW TABLES"
```

Cambiar la base sin tocar el `.env`:

```bash
bash ./.agents/skills/mariadb-schema/scripts/query.sh --database otra_base "SHOW TABLES"
```

## Consultas minimas recomendadas

Listar tablas:

```sql
SHOW TABLES;
```

Describir una tabla:

```sql
DESCRIBE nombre_tabla;
```

Columnas con mas detalle:

```sql
SHOW FULL COLUMNS FROM nombre_tabla;
```

Indices:

```sql
SHOW INDEX FROM nombre_tabla;
```

Relaciones de una tabla:

```sql
SELECT
  COLUMN_NAME,
  CONSTRAINT_NAME,
  REFERENCED_TABLE_NAME,
  REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'nombre_tabla'
  AND REFERENCED_TABLE_NAME IS NOT NULL;
```

Relaciones de toda la base:

```sql
SELECT
  TABLE_NAME,
  COLUMN_NAME,
  CONSTRAINT_NAME,
  REFERENCED_TABLE_NAME,
  REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = DATABASE()
  AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME, COLUMN_NAME;
```

DDL de una tabla:

```sql
SHOW CREATE TABLE nombre_tabla;
```

## Restricciones

- Permite `SHOW`, `DESCRIBE`, `DESC`
- Permite `SELECT` solo si consulta `information_schema`
- Bloquea multiples sentencias en una sola ejecucion
- No usar para `INSERT`, `UPDATE`, `DELETE`, `ALTER`, `DROP`, `CREATE`, `CALL` ni consultas de datos de negocio

## Criterio de cierre

La inspeccion esta completa cuando ya tienes:

1. Tablas involucradas
2. Columnas y tipos relevantes
3. Llaves e indices necesarios
4. Relaciones exactas para modelar el modulo