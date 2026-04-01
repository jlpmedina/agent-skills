---
name: mariadb-schema
description: >
  Usa esta skill siempre que necesites inspeccionar el esquema de una base de datos MariaDB/MySQL
  para ayudar a crear módulos, agentes, o cualquier código que interactúe con esa base de datos.
  Triggers: cuando el usuario mencione "esquema", "tablas", "relaciones", "columnas", "base de datos",
  "mariadb", "mysql", "módulo", "modelo", o pida describir estructuras de datos. Esta skill extrae
  credenciales automáticamente del archivo .env.skill.mariadb en el directorio principal del proyecto.
  NUNCA ejecuta queries de escritura — solo lectura del esquema.
---

# MariaDB Schema Skill (Read-Only)

Esta skill permite inspeccionar el esquema de una base de datos MariaDB/MySQL de forma segura,
extrayendo solo la información necesaria para que los agentes sean más precisos al generar código.

---

## 1. Cargar credenciales

Busca el archivo `.env.skill.mariadb` en el directorio de trabajo actual o en el directorio raíz del proyecto:

```bash
# Buscar el archivo de credenciales
find . -maxdepth 3 -name ".env.skill.mariadb" 2>/dev/null | head -1
```

El archivo debe estar siempre en el **directorio de trabajo actual**. Tiene este formato:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=readonly_user
DB_PASSWORD=secret
DB_NAME=mi_base_de_datos
```

Carga las variables con el script helper:

```bash
python3 /home/claude/mariadb-schema/scripts/load_env.py /ruta/al/.env.skill.mariadb
```

O manualmente en bash:
```bash
export $(grep -v '^#' .env.skill.mariadb | xargs)
```

---

## 2. Ejecutar queries de esquema

Usa siempre el script `query.sh` para garantizar modo lectura. **NUNCA ejecutes INSERT, UPDATE, DELETE, DROP, ALTER ni DDL.**

```bash
bash /home/claude/mariadb-schema/scripts/query.sh "$DB_HOST" "$DB_PORT" "$DB_USER" "$DB_PASSWORD" "$DB_NAME" "SQL_AQUI"
```

---

## 3. Queries de referencia rápida

### Listar todas las tablas
```sql
SHOW TABLES;
```

### Describir una tabla (columnas, tipos, nulls, defaults, keys)
```sql
DESCRIBE nombre_tabla;
```
O más detallado:
```sql
SHOW FULL COLUMNS FROM nombre_tabla;
```

### Ver índices de una tabla
```sql
SHOW INDEX FROM nombre_tabla;
```

### Ver relaciones (foreign keys) de una tabla
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

### Ver TODAS las relaciones de la base de datos
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

### Ver la definición completa de una tabla (CREATE TABLE)
```sql
SHOW CREATE TABLE nombre_tabla;
```

### Ver resumen de todas las tablas con filas y engine
```sql
SELECT
  TABLE_NAME,
  ENGINE,
  TABLE_ROWS,
  TABLE_COMMENT
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME;
```

### Buscar columnas por nombre en toda la BD
```sql
SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND COLUMN_NAME LIKE '%termino_busqueda%'
ORDER BY TABLE_NAME;
```

---

## 4. Flujo recomendado para ayudar a crear un módulo

1. **Listar tablas** → entender el dominio
2. **DESCRIBE** de las tablas relevantes → columnas y tipos
3. **Foreign keys** → relaciones entre entidades
4. **SHOW CREATE TABLE** solo si se necesitan detalles de charset, engines o constraints especiales

Con esa información, genera el código del módulo con tipos precisos, relaciones correctas y nombres exactos de columnas.

---

## 5. Restricciones de seguridad

- ✅ SELECT en `information_schema`
- ✅ SHOW TABLES, SHOW COLUMNS, SHOW INDEX, SHOW CREATE TABLE, DESCRIBE
- ✅ SELECT en tablas de datos solo para inspeccionar una fila de ejemplo: `SELECT * FROM t LIMIT 1`
- ❌ INSERT, UPDATE, DELETE, DROP, TRUNCATE, ALTER, CREATE, GRANT, REVOKE
- ❌ Queries sin LIMIT en tablas de datos (solo en information_schema está permitido)
