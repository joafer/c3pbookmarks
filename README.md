# C3PBookmarks

Biblioteca personal de marcadores web-first, sencilla y autoalojable. Permite guardar enlaces, organizarlos en carpetas y subcarpetas, buscarlos, importar marcadores HTML del navegador y usar un bookmarklet para guardar la página actual.

Proyecto gratuito y de código abierto. Puedes usarlo, modificarlo y autoalojarlo sin coste.

La aplicación se distribuye vacía: no incluye marcadores, base de datos, credenciales ni configuración de ninguna instalación concreta.

## Características

- Interfaz responsive con modo claro/oscuro.
- Alta y edición manual de marcadores, etiquetas, notas e iconos.
- Importación de HTML exportado por Chrome, Firefox y otros navegadores.
- Búsqueda global mediante SQLite FTS5.
- Carpetas y subcarpetas con renombrado, iconos, carpeta predeterminada y orden manual.
- Arrastrar y soltar para mover y ordenar carpetas y marcadores.
- Selector de idioma en español, inglés, italiano, portugués y alemán.
- Bookmarklet para guardar enlaces desde cualquier página sin instalar una extensión.
- Persistencia local en SQLite y despliegue sencillo con Docker Compose.

La importación conserva caracteres especiales y Unicode en nombres, títulos, etiquetas y notas, incluidos `&`, `%`, `?`, `#`, comillas, acentos y emojis. Las rutas generadas para carpetas se codifican correctamente para que esos nombres sigan siendo navegables.

En una ruta de carpetas, la secuencia ` / ` (espacio, barra, espacio) se interpreta como separador de niveles. Es la convención que permite representar subcarpetas exportadas por el navegador.

Al borrar una carpeta desde el menú, se borra también su rama de subcarpetas, pero los marcadores se conservan y pasan a `Sin clasificar`. Esa carpeta está protegida y no se puede borrar.

## Uso rápido con Docker Compose

Requisitos: Docker Engine y Docker Compose v2.

```bash
docker compose up -d --build
```

Abre <http://localhost:8000>. La aplicación creará automáticamente una base SQLite vacía en `data/` al arrancar.

Para instalar en otro puerto, copia la configuración de ejemplo y cambia el puerto publicado:

```bash
cp .env.example .env
# Edita C3PBOOKMARKS_HOST_PORT, por ejemplo 8080
docker compose up -d --build
```

El fichero `compose.yaml` usa el puerto 8000 dentro del contenedor y permite cambiar solo el puerto del equipo anfitrión.

Para detenerla:

```bash
docker compose down
```

Para actualizar una instalación existente después de descargar una nueva versión:

```bash
git pull
docker compose up -d --build
```

Los datos se guardan en `data/`. Esa carpeta está excluida del repositorio mediante `.gitignore`, por lo que los marcadores personales no deben publicarse por accidente.

## Ejecutar sin Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Después, abre <http://localhost:8000>.

## Bookmarklet

Abre `/bookmarklet` desde la instalación y arrastra el botón a la barra de marcadores del navegador. Si la aplicación está detrás de un dominio público o un proxy, define antes `C3PBOOKMARKS_PUBLIC_URL` en el entorno:

```bash
C3PBOOKMARKS_PUBLIC_URL=https://marcadores.example.com docker compose up -d --build
```

Si no se define, el bookmarklet usa automáticamente la URL desde la que se haya abierto la página.

Para usar otro puerto en el mismo equipo, crea un `.env` a partir de `.env.example` y cambia `C3PBOOKMARKS_HOST_PORT`.

## Importación y datos

Exporta los marcadores desde Chrome, Firefox u otro navegador en formato HTML y usa `Importar HTML`. Se omiten enlaces duplicados o inválidos y se conservan las carpetas originales.

Los nombres, títulos, etiquetas, notas y URLs admiten Unicode, acentos, emojis y caracteres como `&`, `%`, `?`, `#`, comillas y `+`. La única convención especial es ` / ` dentro de una ruta, que representa una subcarpeta.

## Copias de seguridad y seguridad

- La base de datos se crea en `data/c3pbookmarks.sqlite3`.
- Para hacer una copia, detén la aplicación y copia ese archivo.
- No publiques nunca la carpeta `data/` si contiene tus marcadores.
- La aplicación no incorpora autenticación. Para exponerla en Internet, añade autenticación, HTTPS y control de acceso en un proxy inverso.
- El volumen `data/` está excluido de Git y del contexto de construcción de Docker para reducir el riesgo de publicar o empaquetar datos personales.

Ejemplo de copia y restauración:

```bash
docker compose down
mkdir -p backups
cp data/c3pbookmarks.sqlite3 backups/c3pbookmarks-$(date +%F).sqlite3
docker compose up -d
```

Para restaurar, detén la aplicación, sustituye `data/c3pbookmarks.sqlite3` por una copia válida y vuelve a arrancarla.

## Licencia

Este proyecto se publica bajo la licencia MIT. Consulta [LICENSE](LICENSE).

## Apoyar el proyecto

C3PBookmarks es gratuito. Si te resulta útil, puedes apoyar su mantenimiento mediante [Buy Me a Coffee](https://buymeacoffee.com/joafer).

## Contribuir

Las mejoras, correcciones y propuestas son bienvenidas. Antes de enviar cambios, comprueba que:

- no contienen datos personales, marcadores reales ni secretos;
- la aplicación arranca desde una base de datos vacía;
- `data/` y los ficheros locales quedan fuera del control de versiones.
