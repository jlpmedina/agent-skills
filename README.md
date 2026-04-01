# Agent Skills

Coleccion de skills para agentes de IA (Claude Code, GitHub Copilot, etc.) que permiten interactuar con herramientas externas de forma segura y controlada.

---

## 📦 Skills disponibles

| Skill | Descripción |
|-------|-------------|
| [mariadb-schema](skills/mariadb-schema/) | Inspección de esquemas MariaDB/MySQL (solo lectura) |

---

## 🚀 Instalación

### Prerrequisito: CLI de skills

```bash
pipx install skills-cli
```

### Instalar skills en un proyecto

Desde la raiz de tu proyecto:

```bash
# Instalar todas las skills del repo
skills install https://github.com/jlpmedina/agent-skills.git --subpath skills --dest ./.agents/skills

# Instalar solo mariadb-schema
skills install https://github.com/jlpmedina/agent-skills.git --subpath skills/mariadb-schema --dest ./.agents/skills

# Instalar como symlink (desde un clone local del repo)
skills install /ruta/a/agent-skills --subpath skills --dest ./.agents/skills --link
```

### Ver skills instaladas

```bash
skills list
```

---

## 📁 Estructura del proyecto

```
skills/
  mariadb-schema/
    SKILL.md       # Definición de la skill (frontmatter YAML + instrucciones)
    scripts/
      resolve_credentials.py  # Resuelve credenciales desde mariadb-schema.env
      query.sh                # Ejecuta queries contra la base de datos
```

Para agregar una nueva skill:

1. Crea un directorio en `skills/nombre-de-la-skill/`
2. Agrega un archivo `SKILL.md` con frontmatter YAML valido
3. Incluye scripts helper en `scripts/` si es necesario
4. Valida con `skills validate skills/nombre-de-la-skill`

---

## 🔧 Configuracion

### mariadb-schema

Crea un archivo `mariadb-schema.env` en la raiz de tu proyecto:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=skill_readonly
DB_PASSWORD=tu_password_aqui
DB_NAME=nombre_de_tu_base
```

### Crear usuario de solo lectura en MariaDB/MySQL

Para mayor seguridad, crea un usuario dedicado con permisos de solo lectura:

```sql
-- Conectate como root o admin
mariadb -u root -p

-- Crear usuario de solo lectura
CREATE USER 'skill_readonly'@'%' IDENTIFIED BY 'una_password_segura';

-- Otorgar solo permisos de SELECT
GRANT SELECT ON tu_base_de_datos.* TO 'skill_readonly'@'%';

-- Si necesitas acceso a information_schema (generalmente automatico)
GRANT SELECT ON information_schema.* TO 'skill_readonly'@'%';

-- Aplicar cambios
FLUSH PRIVILEGES;
```

**Notas de seguridad:**
- El usuario solo puede ejecutar `SELECT`, nunca `INSERT`, `UPDATE`, `DELETE` ni `DROP`
- Usa `'%'` como host solo si la conexion es remota; para local usa `'localhost'` o `'127.0.0.1'`
- Rota la password periodicamente y actualiza el `mariadb-schema.env`
- Si usas MySQL 8+, la sintaxis es la misma

---

## 📄 Licencia

MIT
