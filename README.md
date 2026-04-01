# Agent Skills

Coleccion de skills para agentes de IA (Claude Code, GitHub Copilot, etc.) que permiten interactuar con herramientas externas de forma segura y controlada.

---

## 📦 Skills disponibles

| Skill | Descripción |
|-------|-------------|
| [mariadb-schema](skills/mariadb-schema/) | Inspección de esquemas MariaDB/MySQL (solo lectura) |

---

## 🚀 Instalación

### Probar el repo localmente

Antes de publicarlo en GitHub, valida que el CLI detecta tus skills desde el filesystem:

```bash
# Desde la raiz de este repo
npx skills add . --list

# Instalar solo esta skill desde el repo local
npx skills add . --skill mariadb-schema
```

### Instalar desde GitHub

Para instalar desde una URL de GitHub, el repositorio debe existir y ser publico. Si GitHub devuelve `404` para:

```text
https://github.com/<usuario>/<repo>/archive/refs/heads/main.zip
```

el CLI no podra descargarlo. En ese caso:

- publica el repositorio, o
- usa la instalacion local mientras el repo siga privado

Cuando el repo ya este publicado, el flujo recomendado es:

```bash
# Instalar una skill especifica desde GitHub
npx skills add chenux/agent-skills --skill mariadb-schema

# Ver skills detectadas sin instalar
npx skills add chenux/agent-skills --list
```

### Instalacion manual

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

## 🔧 Configuracion

Cada skill puede requerir configuracion especifica. Consulta el `README.md` de cada skill para mas detalles.

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

## 📝 Requisitos para que el repo sea instalable

Para que `skills add` pueda descubrir e instalar skills desde este repositorio:

1. El repositorio debe ser publico si lo vas a instalar por URL de GitHub.
2. Las skills deben vivir en una ubicacion reconocida por el CLI. `skills/` es valida.
3. Cada skill debe tener un `SKILL.md` con frontmatter YAML valido.
4. El valor `name` del frontmatter debe coincidir con el nombre de la carpeta.
5. Los recursos del skill deben referenciarse con rutas relativas desde `SKILL.md`.

## 📝 Creando nuevas skills

Para agregar una nueva skill:

1. Crea un directorio en `skills/nombre-de-la-skill/`
2. Agrega un archivo `SKILL.md` con el frontmatter YAML requerido
3. Agrega un `README.md` con documentación de uso
4. Incluye scripts helper en `scripts/` si es necesario
5. Prueba el descubrimiento con `npx skills add . --list`

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
