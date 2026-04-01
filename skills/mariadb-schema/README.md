# mariadb-schema skill

Skill de solo lectura para inspeccionar el esquema de una base de datos MariaDB/MySQL.
Disenada para que los agentes sean mas precisos al generar modulos, modelos y codigo que interactue con tu base de datos.

---

## ¿Qué hace?

- Lee la estructura de tablas, columnas, tipos y relaciones (foreign keys)
- Nunca ejecuta queries de escritura — tiene un guard que bloquea INSERT, UPDATE, DELETE, DROP, ALTER, etc.
- Carga las credenciales desde un archivo `.env.skill.mariadb` en tu proyecto
- Usa el CLI nativo `mariadb` (no `mysql`)

---

## Instalación

### Con Skills CLI

```bash
npx skills add . --skill mariadb-schema

# Cuando el repo ya sea publico
npx skills add chenux/agent-skills --skill mariadb-schema
```

Si GitHub responde `404` para el ZIP del branch `main`, el repo todavia no esta accesible publicamente y debes instalarlo desde una ruta local.

### Manual

```bash
cp -r mariadb-schema/ ~/.claude/skills/
```

### En un proyecto específico

```bash
cp -r mariadb-schema/ .claude/skills/
```

---

## Configuracion

Crea el archivo `.env.skill.mariadb` en el directorio del proyecto donde vayas a trabajar (el directorio actual desde donde ejecutas Claude Code):

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=skill_readonly
DB_PASSWORD=tu_password_aqui
DB_NAME=nombre_de_tu_base
```

> ⚠️ Agrega `.env.skill.mariadb` a tu `.gitignore` para no exponer credenciales.

```bash
echo ".env.skill.mariadb" >> .gitignore
```

---

## Crear usuario de solo lectura en MariaDB

Conéctate con un usuario administrador y ejecuta:

```sql
-- 1. Crear el usuario
CREATE USER 'skill_readonly'@'localhost' IDENTIFIED BY 'tu_password_seguro';

-- 2. Otorgar solo SELECT en la base de datos específica
GRANT SELECT ON nombre_de_tu_base.* TO 'skill_readonly'@'localhost';

-- 3. Aplicar cambios
FLUSH PRIVILEGES;
```

Si tu MariaDB está en otro host o en Docker, reemplaza `localhost` por `%` para permitir cualquier origen, o por la IP específica:

```sql
-- Acceso desde cualquier host (ej. Docker, red local)
CREATE USER 'skill_readonly'@'%' IDENTIFIED BY 'tu_password_seguro';
GRANT SELECT ON nombre_de_tu_base.* TO 'skill_readonly'@'%';
FLUSH PRIVILEGES;
```

### Verificar que el usuario solo puede leer

```sql
-- Conectarte como el usuario readonly y probar
-- Esto debe funcionar:
SELECT * FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'nombre_de_tu_base';

-- Esto debe fallar con "Access denied":
INSERT INTO cualquier_tabla VALUES (...);
```

### Ver permisos del usuario

```sql
SHOW GRANTS FOR 'skill_readonly'@'localhost';
```

### Revocar permisos (si necesitas eliminar el usuario)

```sql
REVOKE ALL PRIVILEGES ON nombre_de_tu_base.* FROM 'skill_readonly'@'localhost';
DROP USER 'skill_readonly'@'localhost';
FLUSH PRIVILEGES;
```

---

## Uso

Una vez instalada la skill y creado el `.env.skill.mariadb`, simplemente describe tu tarea a Claude:

- *"Describe la tabla `usuarios` y sus relaciones"*
- *"¿Qué tablas tiene la base de datos?"*
- *"Muestra todas las foreign keys del esquema"*
- *"Quiero crear un módulo CRUD para `productos`, ¿cómo está definida esa tabla?"*

Claude detectara automaticamente la skill y ejecutara las queries necesarias.

---

## Estructura de archivos

```
mariadb-schema/
├── SKILL.md              # Instrucciones para Claude (punto de entrada)
├── README.md             # Este archivo
└── scripts/
    ├── query.sh          # Ejecutor seguro con guard anti-escritura
    └── load_env.py       # Cargador de credenciales .env.skill.mariadb
```

---

## Seguridad

| Operación | Permitido |
|---|---|
| `SHOW TABLES` | ✅ |
| `DESCRIBE tabla` | ✅ |
| `SELECT` en `information_schema` | ✅ |
| `SHOW CREATE TABLE` | ✅ |
| `SELECT * FROM tabla LIMIT 1` | ✅ |
| `INSERT / UPDATE / DELETE` | ❌ Bloqueado |
| `DROP / TRUNCATE / ALTER` | ❌ Bloqueado |
| `GRANT / REVOKE` | ❌ Bloqueado |

El guard en `query.sh` valida la query **antes** de enviarla al servidor, como segunda capa de protección además del usuario readonly.
