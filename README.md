# Agent Skills

Colección de skills para agentes de IA (Claude Code, GitHub Copilot, etc.) que permiten interactuar con herramientas externas de forma segura y controlada.

---

## 📦 Skills disponibles

| Skill | Descripción |
|-------|-------------|
| [mariadb-schema](skills/mariadb-schema/) | Inspección de esquemas MariaDB/MySQL (solo lectura) |

---

## 🚀 Instalación

### Usando skills-cli

La forma más fácil de instalar skills es con `skills-cli`:

```bash
# Instalar una skill específica
skills-cli install --repo https://github.com/tu-usuario/agent-skills --skills mariadb-schema
```

### Instalación manual

#### Global (para todos los proyectos)

```bash
# Copiar la skill al directorio global de Claude
cp -r skills/mariadb-schema/ ~/.claude/skills/
```

#### Por proyecto

```bash
# Copiar la skill al directorio del proyecto
cp -r skills/mariadb-schema/ .claude/skills/
```

---

## 📁 Estructura del proyecto

```
skills/
  mariadb-schema/
    README.md      # Documentación específica de la skill
    SKILL.md       # Definición de la skill (YAML + instrucciones)
    scripts/
      load_env.py  # Script para cargar variables de entorno
      query.sh     # Script para ejecutar queries
```

---

## 🔧 Configuración

Cada skill puede requerir configuración específica. Consulta el `README.md` de cada skill para más detalles.

### Ejemplo: mariadb-schema

Crea un archivo `.env.skill.mariadb` en tu proyecto:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=skill_readonly
DB_PASSWORD=tu_password_aqui
DB_NAME=nombre_de_tu_base
```

---

## 📝 Creando nuevas skills

Para agregar una nueva skill:

1. Crea un directorio en `skills/nombre-de-la-skill/`
2. Agrega un archivo `SKILL.md` con el frontmatter YAML requerido
3. Agrega un `README.md` con documentación de uso
4. Incluye scripts helper en `scripts/` si es necesario

---

## 🤝 Contribuir

1. Fork este repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-skill`)
3. Commit tus cambios (`git commit -m 'Add: nueva skill'`)
4. Push a la rama (`git push origin feature/nueva-skill`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT
