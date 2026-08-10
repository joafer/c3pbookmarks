from __future__ import annotations

import html
import os
import re
import sqlite3
from contextvars import ContextVar
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles


DATA_DIR = Path(os.environ.get("C3PBOOKMARKS_DATA", "/app/data"))
DB_PATH = DATA_DIR / "c3pbookmarks.sqlite3"
STATIC_DIR = Path(__file__).parent.parent / "static"
PUBLIC_BASE_URL = os.environ.get("C3PBOOKMARKS_PUBLIC_URL", "").rstrip("/")
LANGUAGE_COOKIE = "c3pbookmarks_lang"
SUPPORTED_LANGUAGES = ("es", "en", "it", "pt", "de")
LANGUAGE_NAMES = {
    "es": "Español",
    "en": "English",
    "it": "Italiano",
    "pt": "Português",
    "de": "Deutsch",
}
LANGUAGE_FLAGS = {
    "es": '<svg class="language-flag" viewBox="0 0 24 16" aria-hidden="true"><path fill="#c60b1e" d="M0 0h24v4H0zM0 12h24v4H0z"/><path fill="#ffc400" d="M0 4h24v8H0z"/></svg>',
    "en": '<svg class="language-flag" viewBox="0 0 24 16" aria-hidden="true"><path fill="#012169" d="M0 0h24v16H0z"/><path stroke="#fff" stroke-width="4" d="M0 0l24 16M24 0L0 16"/><path stroke="#c8102e" stroke-width="2" d="M0 0l24 16M24 0L0 16"/><path stroke="#fff" stroke-width="6" d="M12 0v16M0 8h24"/><path stroke="#c8102e" stroke-width="3" d="M12 0v16M0 8h24"/></svg>',
    "it": '<svg class="language-flag" viewBox="0 0 24 16" aria-hidden="true"><path fill="#009246" d="M0 0h8v16H0z"/><path fill="#f1f2f1" d="M8 0h8v16H8z"/><path fill="#ce2b37" d="M16 0h8v16h-8z"/></svg>',
    "pt": '<svg class="language-flag" viewBox="0 0 24 16" aria-hidden="true"><path fill="#046a38" d="M0 0h10v16H0z"/><path fill="#da291c" d="M10 0h14v16H10z"/><circle cx="10" cy="8" r="3.1" fill="#ffcd00"/><circle cx="10" cy="8" r="2" fill="#fff"/></svg>',
    "de": '<svg class="language-flag" viewBox="0 0 24 16" aria-hidden="true"><path fill="#000" d="M0 0h24v5.33H0z"/><path fill="#d00" d="M0 5.33h24v5.34H0z"/><path fill="#ffce00" d="M0 10.67h24V16H0z"/></svg>',
}

app = FastAPI(title="C3PBookmarks")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

TRANSLATIONS = {
    "es": {
        "language_select": "Idioma",
        "save_link": "Guardar enlace",
        "import_html": "Importar HTML",
        "add": "Añadir",
        "theme_change": "Cambiar tema",
        "home": "Inicio",
        "your_library": "Tu biblioteca personal",
        "bookmarks_one": "{count} marcador centralizado",
        "bookmarks_many": "{count} marcadores centralizados",
        "add_bookmark": "Añadir marcador",
        "search_placeholder": "Buscar por título, URL, carpeta o etiqueta…",
        "search_bookmarks": "Buscar marcadores",
        "search": "Buscar",
        "folders": "Carpetas",
        "collapse_folders": "Contraer carpetas",
        "create_folder": "Crear carpeta",
        "drop_root": "Suelta aquí para mover a la raíz",
        "all_bookmarks": "Todos los marcadores",
        "uncategorized": "Sin clasificar",
        "no_folders": "Todavía no hay carpetas.",
        "result_one": "{count} resultado",
        "result_many": "{count} resultados",
        "import_bookmarks_html": "Importar marcadores HTML",
        "empty_title": "Aún no hay marcadores.",
        "empty_help": "Importa un HTML del navegador o añade el primero.",
        "drag_bookmark": "Arrastra este marcador a una carpeta u otro marcador",
        "drag_bookmark_folder": "Arrastra este marcador a una carpeta",
        "edit_bookmark": "Editar marcador",
        "delete_bookmark": "Borrar marcador",
        "delete_folder": "Borrar carpeta",
        "empty_folder_only": "Solo se pueden borrar carpetas vacías",
        "rename_folder": "Renombrar carpeta",
        "create_subfolder": "Crear subcarpeta",
        "drop_folder": "Suelta aquí marcadores o carpetas",
        "organization": "Organización",
        "new_folder": "Nueva carpeta",
        "new_folder_help": "Puedes crear una carpeta o una ruta completa, por ejemplo:",
        "folder_path": "Ruta de carpeta",
        "cancel": "Cancelar",
        "create_folder_button": "Crear carpeta",
        "edit_folder": "Editar carpeta",
        "location": "Ubicación",
        "folder_update_help": "Sus marcadores y subcarpetas se actualizarán automáticamente.",
        "new_name": "Nuevo nombre",
        "icon_emoji": "Icono o emoji",
        "emoji_help": "Elige uno o escribe cualquier otro emoji.",
        "choose_emoji": "Elegir emoji",
        "remove_icon": "Quitar icono",
        "default_folder": "Abrir esta carpeta por defecto",
        "save_changes": "Guardar cambios",
        "modify_link": "Modificar enlace",
        "url": "URL",
        "title": "Título",
        "folder": "Carpeta",
        "tags": "Etiquetas",
        "notes": "Notas",
        "site_title": "Título del sitio",
        "tags_placeholder": "opcional, separadas, por, comas",
        "optional": "Opcional",
        "save": "Guardar",
        "quick_access": "Acceso rápido",
        "save_from_browser": "Guardar desde el navegador",
        "bookmarklet_help": "Instala este botón una sola vez. Después, desde cualquier página, púlsalo para abrir C3PBookmarks con la URL y el título ya rellenados.",
        "bookmarklet_button": "Guardar página en C3PBookmarks",
        "bookmarklet_step1": "Arrastra el botón a la barra de marcadores del navegador.",
        "bookmarklet_step2": "Visita cualquier página y pulsa el marcador instalado.",
        "bookmarklet_step3": "Elige la carpeta, añade etiquetas o notas y guarda.",
        "bookmarklet_manual": "Si no puedes arrastrarlo, crea un marcador manualmente con este nombre y copia como dirección el enlace del botón.",
        "migration": "Migración sencilla",
        "import_html_title": "Importar marcadores HTML",
        "import_html_help": "Exporta los marcadores desde tu navegador y sube aquí el archivo HTML. Los duplicados se omiten y se conserva la carpeta original.",
        "file_html": "Archivo HTML",
        "source_optional": "Origen (opcional)",
        "source_placeholder": "Chrome portátil, Firefox PC, etc.",
        "import": "Importar",
        "bookmark_saved": "Marcador guardado.",
        "duplicate_invalid": "Ese enlace ya existe o no es válido.",
        "folder_created": "Carpeta creada.",
        "valid_folder": "Indica un nombre de carpeta válido.",
        "cannot_edit_folder": "No se puede editar esa carpeta.",
        "valid_folder_no_slashes": "Indica un nombre de carpeta válido, sin barras.",
        "folder_renamed": "Carpeta renombrada.",
        "folder_not_editable": "La carpeta no existe o no se puede editar.",
        "folder_name_exists": "Ya existe una carpeta con ese nombre en esa ubicación.",
        "folder_moved": "La carpeta no existe o no se puede mover.",
        "destination_not_found": "La carpeta de destino no existe.",
        "folder_cycle": "No puedes mover una carpeta dentro de sí misma o de una descendiente.",
        "destination_name_exists": "Ya existe una carpeta con ese nombre en la ubicación de destino.",
        "bookmark_not_found": "Marcador no encontrado.",
        "same_folder_reorder": "Solo puedes reordenar marcadores dentro de la misma carpeta.",
        "folder_not_found": "Carpeta no encontrada.",
        "folder_level_reorder": "Solo puedes reordenar carpetas del mismo nivel.",
        "uncategorized_last": "Sin clasificar permanece siempre al final.",
        "folder_deleted": "Carpeta borrada; sus marcadores se han movido a Sin clasificar.",
        "uncategorized_protected": "La carpeta Sin clasificar no se puede borrar.",
        "folder_does_not_exist": "La carpeta no existe.",
        "folder_has_children": "No se puede borrar una carpeta que contiene subcarpetas.",
        "folder_has_bookmarks": "No se puede borrar una carpeta que contiene marcadores.",
        "html_read_error": "No se pudo leer el archivo HTML.",
        "import_finished": "Importación terminada: {added} añadidos, {skipped} duplicados o inválidos omitidos.",
        "root_folders": "Carpetas raíz",
    },
    "en": {
        "language_select": "Language", "save_link": "Save link", "import_html": "Import HTML", "add": "Add",
        "theme_change": "Change theme", "home": "Home", "your_library": "Your personal library",
        "bookmarks_one": "{count} centralized bookmark", "bookmarks_many": "{count} centralized bookmarks",
        "add_bookmark": "Add bookmark", "search_placeholder": "Search by title, URL, folder or tag…", "search_bookmarks": "Search bookmarks", "search": "Search",
        "folders": "Folders", "collapse_folders": "Collapse folders", "create_folder": "Create folder", "drop_root": "Drop here to move to the root", "all_bookmarks": "All bookmarks", "uncategorized": "Uncategorized", "no_folders": "There are no folders yet.",
        "result_one": "{count} result", "result_many": "{count} results", "import_bookmarks_html": "Import HTML bookmarks", "empty_title": "No bookmarks yet.", "empty_help": "Import browser HTML or add your first bookmark.",
        "drag_bookmark": "Drag this bookmark to a folder or another bookmark", "drag_bookmark_folder": "Drag this bookmark to a folder", "edit_bookmark": "Edit bookmark", "delete_bookmark": "Delete bookmark", "delete_folder": "Delete folder", "empty_folder_only": "Only empty folders can be deleted", "rename_folder": "Rename folder", "create_subfolder": "Create subfolder", "drop_folder": "Drop bookmarks or folders here",
        "organization": "Organization", "new_folder": "New folder", "new_folder_help": "Create a folder or a complete path, for example:", "folder_path": "Folder path", "cancel": "Cancel", "create_folder_button": "Create folder", "edit_folder": "Edit folder", "location": "Location", "folder_update_help": "Its bookmarks and subfolders will be updated automatically.", "new_name": "New name", "icon_emoji": "Icon or emoji", "emoji_help": "Choose one or type any other emoji.", "choose_emoji": "Choose emoji", "remove_icon": "Remove icon", "default_folder": "Open this folder by default", "save_changes": "Save changes", "modify_link": "Edit link", "url": "URL", "title": "Title", "folder": "Folder", "tags": "Tags", "notes": "Notes", "site_title": "Site title", "tags_placeholder": "optional, comma-separated", "optional": "Optional", "save": "Save",
        "quick_access": "Quick access", "save_from_browser": "Save from browser", "bookmarklet_help": "Install this button once. Then press it on any page to open C3PBookmarks with the URL and title filled in.", "bookmarklet_button": "Save page to C3PBookmarks", "bookmarklet_step1": "Drag the button to your browser bookmarks bar.", "bookmarklet_step2": "Visit any page and press the installed bookmark.", "bookmarklet_step3": "Choose a folder, add tags or notes, and save.", "bookmarklet_manual": "If you cannot drag it, create a bookmark with this name and copy the button link as its address.",
        "migration": "Simple migration", "import_html_title": "Import HTML bookmarks", "import_html_help": "Export bookmarks from your browser and upload the HTML file here. Duplicates are skipped and the original folders are preserved.", "file_html": "HTML file", "source_optional": "Source (optional)", "source_placeholder": "Portable Chrome, Firefox PC, etc.", "import": "Import", "bookmark_saved": "Bookmark saved.", "duplicate_invalid": "That link already exists or is not valid.", "folder_created": "Folder created.", "valid_folder": "Enter a valid folder name.", "cannot_edit_folder": "That folder cannot be edited.", "valid_folder_no_slashes": "Enter a valid folder name without slashes.", "folder_renamed": "Folder renamed.", "folder_not_editable": "The folder does not exist or cannot be edited.", "folder_name_exists": "A folder with that name already exists here.", "folder_moved": "The folder does not exist or cannot be moved.", "destination_not_found": "The destination folder does not exist.", "folder_cycle": "You cannot move a folder inside itself or one of its descendants.", "destination_name_exists": "A folder with that name already exists at the destination.", "bookmark_not_found": "Bookmark not found.", "same_folder_reorder": "Bookmarks can only be reordered within the same folder.", "folder_not_found": "Folder not found.", "folder_level_reorder": "Folders can only be reordered at the same level.", "uncategorized_last": "Uncategorized always stays at the end.", "folder_deleted": "Folder deleted.", "uncategorized_protected": "The Uncategorized folder cannot be deleted.", "folder_does_not_exist": "The folder does not exist.", "folder_has_children": "A folder containing subfolders cannot be deleted.", "folder_has_bookmarks": "A folder containing bookmarks cannot be deleted.", "html_read_error": "The HTML file could not be read.", "import_finished": "Import finished: {added} added, {skipped} duplicates or invalid items skipped.", "root_folders": "Root folders",
    },
    "it": {
        "language_select": "Lingua", "save_link": "Salva link", "import_html": "Importa HTML", "add": "Aggiungi", "theme_change": "Cambia tema", "home": "Home", "your_library": "La tua biblioteca personale", "bookmarks_one": "{count} segnalibro centralizzato", "bookmarks_many": "{count} segnalibri centralizzati", "add_bookmark": "Aggiungi segnalibro", "search_placeholder": "Cerca per titolo, URL, cartella o tag…", "search_bookmarks": "Cerca segnalibri", "search": "Cerca", "folders": "Cartelle", "collapse_folders": "Comprimi cartelle", "create_folder": "Crea cartella", "drop_root": "Rilascia qui per spostare nella radice", "all_bookmarks": "Tutti i segnalibri", "uncategorized": "Senza categoria", "no_folders": "Non ci sono ancora cartelle.", "result_one": "{count} risultato", "result_many": "{count} risultati", "import_bookmarks_html": "Importa segnalibri HTML", "empty_title": "Non ci sono ancora segnalibri.", "empty_help": "Importa l'HTML del browser o aggiungi il primo.", "drag_bookmark": "Trascina questo segnalibro su una cartella o un altro segnalibro", "drag_bookmark_folder": "Trascina questo segnalibro su una cartella", "edit_bookmark": "Modifica segnalibro", "delete_bookmark": "Elimina segnalibro", "delete_folder": "Elimina cartella", "empty_folder_only": "Si possono eliminare solo cartelle vuote", "rename_folder": "Rinomina cartella", "create_subfolder": "Crea sottocartella", "drop_folder": "Rilascia qui segnalibri o cartelle", "organization": "Organizzazione", "new_folder": "Nuova cartella", "new_folder_help": "Crea una cartella o un percorso completo, ad esempio:", "folder_path": "Percorso cartella", "cancel": "Annulla", "create_folder_button": "Crea cartella", "edit_folder": "Modifica cartella", "location": "Posizione", "folder_update_help": "I suoi segnalibri e sottocartelle verranno aggiornati automaticamente.", "new_name": "Nuovo nome", "icon_emoji": "Icona o emoji", "emoji_help": "Scegline una o scrivi qualsiasi altra emoji.", "choose_emoji": "Scegli emoji", "remove_icon": "Rimuovi icona", "default_folder": "Apri questa cartella per impostazione predefinita", "save_changes": "Salva modifiche", "modify_link": "Modifica link", "url": "URL", "title": "Titolo", "folder": "Cartella", "tags": "Tag", "notes": "Note", "site_title": "Titolo del sito", "tags_placeholder": "opzionali, separati da virgole", "optional": "Opzionale", "save": "Salva", "quick_access": "Accesso rapido", "save_from_browser": "Salva dal browser", "bookmarklet_help": "Installa questo pulsante una volta. Poi premilo su qualsiasi pagina per aprire C3PBookmarks con URL e titolo già compilati.", "bookmarklet_button": "Salva pagina in C3PBookmarks", "bookmarklet_step1": "Trascina il pulsante nella barra dei segnalibri del browser.", "bookmarklet_step2": "Visita una pagina e premi il segnalibro installato.", "bookmarklet_step3": "Scegli la cartella, aggiungi tag o note e salva.", "bookmarklet_manual": "Se non puoi trascinarlo, crea un segnalibro con questo nome e copia il link del pulsante come indirizzo.", "migration": "Migrazione semplice", "import_html_title": "Importa segnalibri HTML", "import_html_help": "Esporta i segnalibri dal browser e carica qui il file HTML. I duplicati vengono ignorati e le cartelle originali conservate.", "file_html": "File HTML", "source_optional": "Origine (opzionale)", "source_placeholder": "Chrome portatile, Firefox PC, ecc.", "import": "Importa", "bookmark_saved": "Segnalibro salvato.", "duplicate_invalid": "Il link esiste già o non è valido.", "folder_created": "Cartella creata.", "valid_folder": "Inserisci un nome di cartella valido.", "cannot_edit_folder": "Questa cartella non può essere modificata.", "valid_folder_no_slashes": "Inserisci un nome di cartella valido, senza barre.", "folder_renamed": "Cartella rinominata.", "folder_not_editable": "La cartella non esiste o non può essere modificata.", "folder_name_exists": "Esiste già una cartella con questo nome qui.", "folder_moved": "La cartella non esiste o non può essere spostata.", "destination_not_found": "La cartella di destinazione non esiste.", "folder_cycle": "Non puoi spostare una cartella dentro sé stessa o una discendente.", "destination_name_exists": "Esiste già una cartella con questo nome nella destinazione.", "bookmark_not_found": "Segnalibro non trovato.", "same_folder_reorder": "I segnalibri possono essere riordinati solo nella stessa cartella.", "folder_not_found": "Cartella non trovata.", "folder_level_reorder": "Le cartelle possono essere riordinate solo allo stesso livello.", "uncategorized_last": "Senza categoria resta sempre alla fine.", "folder_deleted": "Cartella eliminata.", "uncategorized_protected": "La cartella Senza categoria non può essere eliminata.", "folder_does_not_exist": "La cartella non esiste.", "folder_has_children": "Non puoi eliminare una cartella con sottocartelle.", "folder_has_bookmarks": "Non puoi eliminare una cartella con segnalibri.", "html_read_error": "Non è stato possibile leggere il file HTML.", "import_finished": "Importazione terminata: {added} aggiunti, {skipped} duplicati o non validi ignorati.", "root_folders": "Cartelle principali",
    },
    "pt": {
        "language_select": "Idioma", "save_link": "Guardar link", "import_html": "Importar HTML", "add": "Adicionar", "theme_change": "Mudar tema", "home": "Início", "your_library": "A sua biblioteca pessoal", "bookmarks_one": "{count} marcador centralizado", "bookmarks_many": "{count} marcadores centralizados", "add_bookmark": "Adicionar marcador", "search_placeholder": "Pesquisar por título, URL, pasta ou etiqueta…", "search_bookmarks": "Pesquisar marcadores", "search": "Pesquisar", "folders": "Pastas", "collapse_folders": "Recolher pastas", "create_folder": "Criar pasta", "drop_root": "Largue aqui para mover para a raiz", "all_bookmarks": "Todos os marcadores", "uncategorized": "Sem categoria", "no_folders": "Ainda não existem pastas.", "result_one": "{count} resultado", "result_many": "{count} resultados", "import_bookmarks_html": "Importar marcadores HTML", "empty_title": "Ainda não existem marcadores.", "empty_help": "Importe o HTML do navegador ou adicione o primeiro.", "drag_bookmark": "Arraste este marcador para uma pasta ou outro marcador", "drag_bookmark_folder": "Arraste este marcador para uma pasta", "edit_bookmark": "Editar marcador", "delete_bookmark": "Apagar marcador", "delete_folder": "Apagar pasta", "empty_folder_only": "Só é possível apagar pastas vazias", "rename_folder": "Renomear pasta", "create_subfolder": "Criar subpasta", "drop_folder": "Largue aqui marcadores ou pastas", "organization": "Organização", "new_folder": "Nova pasta", "new_folder_help": "Crie uma pasta ou um caminho completo, por exemplo:", "folder_path": "Caminho da pasta", "cancel": "Cancelar", "create_folder_button": "Criar pasta", "edit_folder": "Editar pasta", "location": "Localização", "folder_update_help": "Os seus marcadores e subpastas serão atualizados automaticamente.", "new_name": "Novo nome", "icon_emoji": "Ícone ou emoji", "emoji_help": "Escolha um ou escreva qualquer outro emoji.", "choose_emoji": "Escolher emoji", "remove_icon": "Remover ícone", "default_folder": "Abrir esta pasta por predefinição", "save_changes": "Guardar alterações", "modify_link": "Editar link", "url": "URL", "title": "Título", "folder": "Pasta", "tags": "Etiquetas", "notes": "Notas", "site_title": "Título do site", "tags_placeholder": "opcionais, separadas por vírgulas", "optional": "Opcional", "save": "Guardar", "quick_access": "Acesso rápido", "save_from_browser": "Guardar a partir do navegador", "bookmarklet_help": "Instale este botão uma vez. Depois, prima-o em qualquer página para abrir o C3PBookmarks com o URL e o título preenchidos.", "bookmarklet_button": "Guardar página no C3PBookmarks", "bookmarklet_step1": "Arraste o botão para a barra de marcadores do navegador.", "bookmarklet_step2": "Visite uma página e prima o marcador instalado.", "bookmarklet_step3": "Escolha a pasta, adicione etiquetas ou notas e guarde.", "bookmarklet_manual": "Se não o puder arrastar, crie um marcador com este nome e copie o link do botão como endereço.", "migration": "Migração simples", "import_html_title": "Importar marcadores HTML", "import_html_help": "Exporte os marcadores do navegador e carregue aqui o ficheiro HTML. Os duplicados são ignorados e as pastas originais são preservadas.", "file_html": "Ficheiro HTML", "source_optional": "Origem (opcional)", "source_placeholder": "Chrome portátil, Firefox PC, etc.", "import": "Importar", "bookmark_saved": "Marcador guardado.", "duplicate_invalid": "Esse link já existe ou não é válido.", "folder_created": "Pasta criada.", "valid_folder": "Indique um nome de pasta válido.", "cannot_edit_folder": "Essa pasta não pode ser editada.", "valid_folder_no_slashes": "Indique um nome de pasta válido, sem barras.", "folder_renamed": "Pasta renomeada.", "folder_not_editable": "A pasta não existe ou não pode ser editada.", "folder_name_exists": "Já existe uma pasta com esse nome aqui.", "folder_moved": "A pasta não existe ou não pode ser movida.", "destination_not_found": "A pasta de destino não existe.", "folder_cycle": "Não pode mover uma pasta para dentro de si própria ou de uma descendente.", "destination_name_exists": "Já existe uma pasta com esse nome no destino.", "bookmark_not_found": "Marcador não encontrado.", "same_folder_reorder": "Os marcadores só podem ser reordenados dentro da mesma pasta.", "folder_not_found": "Pasta não encontrada.", "folder_level_reorder": "As pastas só podem ser reordenadas no mesmo nível.", "uncategorized_last": "Sem categoria fica sempre no fim.", "folder_deleted": "Pasta apagada.", "uncategorized_protected": "A pasta Sem categoria não pode ser apagada.", "folder_does_not_exist": "A pasta não existe.", "folder_has_children": "Não é possível apagar uma pasta com subpastas.", "folder_has_bookmarks": "Não é possível apagar uma pasta com marcadores.", "html_read_error": "Não foi possível ler o ficheiro HTML.", "import_finished": "Importação concluída: {added} adicionados, {skipped} duplicados ou inválidos ignorados.", "root_folders": "Pastas raiz",
    },
    "de": {
        "language_select": "Sprache", "save_link": "Link speichern", "import_html": "HTML importieren", "add": "Hinzufügen", "theme_change": "Design ändern", "home": "Startseite", "your_library": "Ihre persönliche Bibliothek", "bookmarks_one": "{count} gespeicherter Bookmark", "bookmarks_many": "{count} gespeicherte Bookmarks", "add_bookmark": "Bookmark hinzufügen", "search_placeholder": "Nach Titel, URL, Ordner oder Tag suchen…", "search_bookmarks": "Bookmarks suchen", "search": "Suchen", "folders": "Ordner", "collapse_folders": "Ordner einklappen", "create_folder": "Ordner erstellen", "drop_root": "Hier ablegen, um in die oberste Ebene zu verschieben", "all_bookmarks": "Alle Bookmarks", "uncategorized": "Nicht kategorisiert", "no_folders": "Noch keine Ordner vorhanden.", "result_one": "{count} Ergebnis", "result_many": "{count} Ergebnisse", "import_bookmarks_html": "HTML-Bookmarks importieren", "empty_title": "Noch keine Bookmarks.", "empty_help": "Browser-HTML importieren oder den ersten Bookmark hinzufügen.", "drag_bookmark": "Diesen Bookmark auf einen Ordner oder einen anderen Bookmark ziehen", "drag_bookmark_folder": "Diesen Bookmark auf einen Ordner ziehen", "edit_bookmark": "Bookmark bearbeiten", "delete_bookmark": "Bookmark löschen", "delete_folder": "Ordner löschen", "empty_folder_only": "Nur leere Ordner können gelöscht werden", "rename_folder": "Ordner umbenennen", "create_subfolder": "Unterordner erstellen", "drop_folder": "Bookmarks oder Ordner hier ablegen", "organization": "Organisation", "new_folder": "Neuer Ordner", "new_folder_help": "Einen Ordner oder einen vollständigen Pfad erstellen, zum Beispiel:", "folder_path": "Ordnerpfad", "cancel": "Abbrechen", "create_folder_button": "Ordner erstellen", "edit_folder": "Ordner bearbeiten", "location": "Ort", "folder_update_help": "Die darin enthaltenen Bookmarks und Unterordner werden automatisch aktualisiert.", "new_name": "Neuer Name", "icon_emoji": "Symbol oder Emoji", "emoji_help": "Auswählen oder ein beliebiges anderes Emoji eingeben.", "choose_emoji": "Emoji auswählen", "remove_icon": "Symbol entfernen", "default_folder": "Diesen Ordner standardmäßig öffnen", "save_changes": "Änderungen speichern", "modify_link": "Link bearbeiten", "url": "URL", "title": "Titel", "folder": "Ordner", "tags": "Tags", "notes": "Notizen", "site_title": "Seitentitel", "tags_placeholder": "optional, durch Kommas getrennt", "optional": "Optional", "save": "Speichern", "quick_access": "Schnellzugriff", "save_from_browser": "Aus dem Browser speichern", "bookmarklet_help": "Diese Schaltfläche einmal installieren. Danach auf einer beliebigen Seite anklicken, um C3PBookmarks mit ausgefüllter URL und Titel zu öffnen.", "bookmarklet_button": "Seite in C3PBookmarks speichern", "bookmarklet_step1": "Die Schaltfläche in die Lesezeichenleiste des Browsers ziehen.", "bookmarklet_step2": "Eine beliebige Seite besuchen und das installierte Lesezeichen anklicken.", "bookmarklet_step3": "Ordner auswählen, Tags oder Notizen ergänzen und speichern.", "bookmarklet_manual": "Wenn Ziehen nicht möglich ist, ein Lesezeichen mit diesem Namen erstellen und den Link der Schaltfläche als Adresse kopieren.", "migration": "Einfache Migration", "import_html_title": "HTML-Bookmarks importieren", "import_html_help": "Bookmarks aus dem Browser exportieren und die HTML-Datei hier hochladen. Duplikate werden übersprungen und die ursprünglichen Ordner beibehalten.", "file_html": "HTML-Datei", "source_optional": "Quelle (optional)", "source_placeholder": "Portables Chrome, Firefox-PC usw.", "import": "Importieren", "bookmark_saved": "Bookmark gespeichert.", "duplicate_invalid": "Dieser Link existiert bereits oder ist ungültig.", "folder_created": "Ordner erstellt.", "valid_folder": "Bitte einen gültigen Ordnernamen eingeben.", "cannot_edit_folder": "Dieser Ordner kann nicht bearbeitet werden.", "valid_folder_no_slashes": "Bitte einen gültigen Ordnernamen ohne Schrägstriche eingeben.", "folder_renamed": "Ordner umbenannt.", "folder_not_editable": "Der Ordner existiert nicht oder kann nicht bearbeitet werden.", "folder_name_exists": "Ein Ordner mit diesem Namen existiert hier bereits.", "folder_moved": "Der Ordner existiert nicht oder kann nicht verschoben werden.", "destination_not_found": "Der Zielordner existiert nicht.", "folder_cycle": "Ein Ordner kann nicht in sich selbst oder einen Unterordner verschoben werden.", "destination_name_exists": "Ein Ordner mit diesem Namen existiert am Ziel bereits.", "bookmark_not_found": "Bookmark nicht gefunden.", "same_folder_reorder": "Bookmarks können nur innerhalb desselben Ordners sortiert werden.", "folder_not_found": "Ordner nicht gefunden.", "folder_level_reorder": "Ordner können nur auf derselben Ebene sortiert werden.", "uncategorized_last": "Nicht kategorisiert bleibt immer am Ende.", "folder_deleted": "Ordner gelöscht.", "uncategorized_protected": "Der Ordner Nicht kategorisiert kann nicht gelöscht werden.", "folder_does_not_exist": "Der Ordner existiert nicht.", "folder_has_children": "Ein Ordner mit Unterordnern kann nicht gelöscht werden.", "folder_has_bookmarks": "Ein Ordner mit Bookmarks kann nicht gelöscht werden.", "html_read_error": "Die HTML-Datei konnte nicht gelesen werden.", "import_finished": "Import abgeschlossen: {added} hinzugefügt, {skipped} Duplikate oder ungültige Einträge übersprungen.", "root_folders": "Hauptordner",
    },
}

TRANSLATIONS["en"]["folder_deleted"] = "Folder deleted; its bookmarks were moved to Uncategorized."
TRANSLATIONS["it"]["folder_deleted"] = "Cartella eliminata; i suoi segnalibri sono stati spostati in Senza categoria."
TRANSLATIONS["pt"]["folder_deleted"] = "Pasta apagada; os seus marcadores foram movidos para Sem categoria."
TRANSLATIONS["de"]["folder_deleted"] = "Ordner gelöscht; seine Bookmarks wurden nach Nicht kategorisiert verschoben."

CURRENT_LANGUAGE: ContextVar[str] = ContextVar("c3pbookmarks_language", default="es")
CURRENT_LOCATION: ContextVar[str] = ContextVar("c3pbookmarks_location", default="/")


def normalize_language(value: str | None) -> str:
    return value if value in SUPPORTED_LANGUAGES else "es"


def current_language() -> str:
    return CURRENT_LANGUAGE.get()


def t(key: str, **values: object) -> str:
    text = TRANSLATIONS.get(current_language(), TRANSLATIONS["es"]).get(key)
    if text is None:
        text = TRANSLATIONS["es"].get(key, key)
    return text.format(**values) if values else text


def count_label(key: str, count: int) -> str:
    return t(f"{key}_{'one' if count == 1 else 'many'}", count=count)


@app.middleware("http")
async def language_middleware(request: Request, call_next):
    language = normalize_language(request.cookies.get(LANGUAGE_COOKIE))
    language_token = CURRENT_LANGUAGE.set(language)
    location = request.url.path + (f"?{request.url.query}" if request.url.query else "")
    location_token = CURRENT_LOCATION.set(location)
    try:
        return await call_next(request)
    finally:
        CURRENT_LANGUAGE.reset(language_token)
        CURRENT_LOCATION.reset(location_token)


@app.get("/language")
def set_language(lang: str = "es", next_url: str = "/") -> RedirectResponse:
    language = normalize_language(lang)
    if not next_url.startswith("/") or next_url.startswith("//"):
        next_url = "/"
    response = RedirectResponse(url=next_url, status_code=303)
    response.set_cookie(LANGUAGE_COOKIE, language, max_age=31536000, samesite="lax")
    return response

def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def db() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def normalize_url(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if not re.match(r"^[a-z][a-z0-9+.-]*://", value, re.I):
        value = "https://" + value
    try:
        parsed = urlsplit(value)
        host = (parsed.hostname or "").lower()
        if not host:
            return value.lower().rstrip("/")
        port = parsed.port
        netloc = host
        if port and not ((parsed.scheme.lower() == "http" and port == 80) or (parsed.scheme.lower() == "https" and port == 443)):
            netloc += f":{port}"
        path = parsed.path or "/"
        if path != "/":
            path = path.rstrip("/")
        query = urlencode(sorted(parse_qsl(parsed.query, keep_blank_values=True)))
        return urlunsplit((parsed.scheme.lower(), netloc, path, query, ""))
    except ValueError:
        return value.lower().rstrip("/")


def normalize_folder(value: str, default: str = "") -> str:
    parts = [part.strip() for part in value.split(" / ") if part.strip()]
    return " / ".join(parts) or default


def favicon_url(value: str) -> str:
    candidate = value.strip()
    if not re.match(r"^[a-z][a-z0-9+.-]*://", candidate, re.I):
        candidate = "https://" + candidate
    try:
        parsed = urlsplit(candidate)
        if not parsed.hostname:
            return ""
        return urlunsplit((parsed.scheme.lower(), parsed.netloc, "/favicon.ico", "", ""))
    except ValueError:
        return ""


class BookmarkHTMLParser(HTMLParser):
    """Parse the Netscape HTML bookmark format exported by major browsers."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.folder_stack: list[str] = []
        self.pending_folder: str | None = None
        self.in_h3 = False
        self.h3_buffer: list[str] = []
        self.in_a = False
        self.a_url = ""
        self.a_buffer: list[str] = []
        self.a_attrs: dict[str, str] = {}
        self.items: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attributes = {key.lower(): (value or "") for key, value in attrs}
        if tag == "h3":
            self.in_h3 = True
            self.h3_buffer = []
        elif tag == "dl" and self.pending_folder is not None:
            self.folder_stack.append(self.pending_folder)
            self.pending_folder = None
        elif tag == "a":
            self.in_a = True
            self.a_url = attributes.get("href", "").strip()
            self.a_attrs = attributes
            self.a_buffer = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "h3" and self.in_h3:
            self.in_h3 = False
            self.pending_folder = " ".join("".join(self.h3_buffer).split()) or "Sin nombre"
        elif tag == "dl" and self.folder_stack:
            self.folder_stack.pop()
        elif tag == "a" and self.in_a:
            self.in_a = False
            title = " ".join("".join(self.a_buffer).split()) or self.a_url
            self.items.append(
                {
                    "url": self.a_url,
                    "title": title,
                    "folder": " / ".join(self.folder_stack) or "Sin clasificar",
                }
            )

    def handle_data(self, data: str) -> None:
        if self.in_h3:
            self.h3_buffer.append(data)
        elif self.in_a:
            self.a_buffer.append(data)


def init_db() -> None:
    with db() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS folders (
                path TEXT PRIMARY KEY,
                position INTEGER NOT NULL DEFAULT 0,
                icon TEXT NOT NULL DEFAULT '',
                is_default INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                normalized_url TEXT NOT NULL,
                title TEXT NOT NULL,
                folder TEXT NOT NULL DEFAULT 'Sin clasificar',
                position INTEGER NOT NULL DEFAULT 0,
                icon TEXT NOT NULL DEFAULT '',
                tags TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                source TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE UNIQUE INDEX IF NOT EXISTS idx_bookmarks_normalized_url
                ON bookmarks(normalized_url);
            CREATE VIRTUAL TABLE IF NOT EXISTS bookmarks_fts USING fts5(
                title, url, folder, tags, notes, content=''
            );
            """
        )
        columns = {row[1] for row in connection.execute("PRAGMA table_info(bookmarks)").fetchall()}
        if "position" not in columns:
            connection.execute("ALTER TABLE bookmarks ADD COLUMN position INTEGER NOT NULL DEFAULT 0")
            for folder_row in connection.execute("SELECT DISTINCT folder FROM bookmarks").fetchall():
                rows = connection.execute(
                    "SELECT id FROM bookmarks WHERE folder=? ORDER BY title COLLATE NOCASE, id",
                    (folder_row[0],),
                ).fetchall()
                for position, row in enumerate(rows):
                    connection.execute("UPDATE bookmarks SET position=? WHERE id=?", (position, row[0]))
        if "icon" not in columns:
            connection.execute("ALTER TABLE bookmarks ADD COLUMN icon TEXT NOT NULL DEFAULT ''")
        folder_columns = {row[1] for row in connection.execute("PRAGMA table_info(folders)").fetchall()}
        if "position" not in folder_columns:
            connection.execute("ALTER TABLE folders ADD COLUMN position INTEGER NOT NULL DEFAULT 0")
            folder_rows = connection.execute("SELECT path FROM folders ORDER BY path COLLATE NOCASE").fetchall()
            for parent in {row[0].rsplit(" / ", 1)[0] if " / " in row[0] else "" for row in folder_rows}:
                siblings = [row[0] for row in folder_rows if (row[0].rsplit(" / ", 1)[0] if " / " in row[0] else "") == parent]
                for position, path in enumerate(sorted(siblings, key=str.casefold)):
                    connection.execute("UPDATE folders SET position=? WHERE path=?", (position, path))
        if "icon" not in folder_columns:
            connection.execute("ALTER TABLE folders ADD COLUMN icon TEXT NOT NULL DEFAULT ''")
        if "is_default" not in folder_columns:
            connection.execute("ALTER TABLE folders ADD COLUMN is_default INTEGER NOT NULL DEFAULT 0")
        for row in connection.execute("SELECT DISTINCT folder FROM bookmarks").fetchall():
            ensure_folder_path(connection, row[0])


def ensure_folder_path(connection: sqlite3.Connection, value: str) -> str:
    path = normalize_folder(value)
    if not path:
        return ""
    parts = path.split(" / ")
    for index in range(1, len(parts) + 1):
        folder_path = " / ".join(parts[:index])
        parent = folder_path.rsplit(" / ", 1)[0] if " / " in folder_path else ""
        siblings = connection.execute("SELECT path, position FROM folders").fetchall()
        sibling_positions = [
            row["position"] for row in siblings
            if (row["path"].rsplit(" / ", 1)[0] if " / " in row["path"] else "") == parent
        ]
        position = max(sibling_positions, default=-1) + 1
        connection.execute(
            "INSERT OR IGNORE INTO folders(path, position, created_at) VALUES (?, ?, ?)",
            (folder_path, position, now()),
        )
    return path


def ordered_folder_paths(connection: sqlite3.Connection) -> list[str]:
    children: dict[str, list[tuple[str, str, int]]] = {}
    for row in connection.execute("SELECT path, position FROM folders").fetchall():
        path = row[0]
        parent = path.rsplit(" / ", 1)[0] if " / " in path else ""
        name = path.rsplit(" / ", 1)[-1]
        children.setdefault(parent, []).append((name, path, row[1]))

    ordered: list[str] = []

    def walk(parent: str) -> None:
        siblings = sorted(
            children.get(parent, []),
            key=lambda item: (item[0].casefold() == "sin clasificar", item[2], item[0].casefold()),
        )
        for _, path, _ in siblings:
            ordered.append(path)
            walk(path)

    walk("")
    return ordered


def folder_select_options(connection: sqlite3.Connection, selected: str = "") -> str:
    paths = ordered_folder_paths(connection)
    icons = {row[0]: row[1] for row in connection.execute("SELECT path, icon FROM folders").fetchall()}
    options = []
    for path in paths:
        level = path.count(" / ")
        icon = icons.get(path, "").strip()
        name = t("uncategorized") if path == "Sin clasificar" else path.rsplit(" / ", 1)[-1]
        label = ("　" * level) + (f"{icon} " if icon else "") + name
        is_selected = " selected" if path == selected else ""
        options.append(f'<option value="{esc(path)}"{is_selected}>{esc(label)}</option>')
    return "".join(options)


def add_bookmark(connection: sqlite3.Connection, item: dict[str, str]) -> bool:
    normalized = normalize_url(item.get("url", ""))
    if not normalized:
        return False
    timestamp = now()
    folder = ensure_folder_path(connection, item.get("folder", "Sin clasificar").strip() or "Sin clasificar")
    position = connection.execute("SELECT COALESCE(MAX(position), -1) + 1 FROM bookmarks WHERE folder=?", (folder or "Sin clasificar",)).fetchone()[0]
    try:
        cursor = connection.execute(
            """
            INSERT INTO bookmarks
                (url, normalized_url, title, folder, position, icon, tags, notes, source, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["url"].strip(),
                normalized,
                item.get("title", "").strip() or item["url"].strip(),
                folder or "Sin clasificar",
                position,
                item.get("icon", "").strip()[:8],
                item.get("tags", "").strip(),
                item.get("notes", "").strip(),
                item.get("source", "").strip(),
                timestamp,
                timestamp,
            ),
        )
        row_id = cursor.lastrowid
        connection.execute(
            "INSERT INTO bookmarks_fts(rowid, title, url, folder, tags, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (row_id, item.get("title", ""), item["url"], folder, item.get("tags", ""), item.get("notes", "")),
        )
        return True
    except sqlite3.IntegrityError:
        return False


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


EMOJI_CHOICES = (
    ("🏠", "Casa"), ("💼", "Trabajo"), ("⭐", "Favorito"), ("📁", "Carpeta"),
    ("🖥️", "Ordenador"), ("🌐", "Web"), ("🔧", "Herramientas"), ("🔒", "Seguridad"),
    ("📚", "Documentación"), ("💰", "Finanzas"), ("🎬", "Vídeos"), ("🧪", "Pruebas"),
)


def emoji_picker_controls(value: str = "") -> str:
    buttons = "".join(
        f'<button type="button" data-emoji="{esc(emoji)}" title="{esc(label)}">{esc(emoji)}</button>'
        for emoji, label in EMOJI_CHOICES
    )
    return f'''<input name="icon" value="{esc(value)}" maxlength="8" placeholder="🏠  💼  ⭐">
      <span class="field-help">{esc(t("emoji_help"))}</span>
      <span class="emoji-picker" data-emoji-picker aria-label="{esc(t("choose_emoji"))}">{buttons}<button type="button" data-emoji="" title="{esc(t("remove_icon"))}" aria-label="{esc(t("remove_icon"))}">×</button></span>'''


def language_selector() -> str:
    option_items = []
    for code, name in LANGUAGE_NAMES.items():
        current = ' aria-current="page"' if code == current_language() else ""
        flag = LANGUAGE_FLAGS[code]
        href = f'/language?{urlencode({"lang": code, "next_url": CURRENT_LOCATION.get()})}'
        option_items.append(
            f'<a href="{esc(href)}"{current} title="{esc(name)}" aria-label="{esc(name)}">{flag}</a>'
        )
    options = "".join(option_items)
    return f'''<details class="language-menu">
        <summary class="language-trigger" title="{esc(t("language_select"))}" aria-label="{esc(t("language_select"))}">🌐</summary>
        <div class="language-options">{options}</div>
      </details>'''


def page(title: str, body: str, *, query: str = "", message: str = "") -> HTMLResponse:
    notice = f'<div class="notice">{esc(message)}</div>' if message else ""
    language = current_language()
    return HTMLResponse(
        f"""<!doctype html>
<html lang="{language}" data-theme="auto">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#18212f">
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" href="/static/brand-mark.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/static/style.css">
  <title>{esc(title)} · C3PBookmarks</title>
</head>
<body>
  <header class="topbar">
    <a class="brand" href="/">C3PBookmarks</a>
    <nav>
      <a href="/bookmarklet">{esc(t("save_link"))}</a>
      <a href="/import">{esc(t("import_html"))}</a>
      <a href="/add">{esc(t("add"))}</a>
      {language_selector()}
      <button class="theme-button" id="theme-toggle" type="button" title="{esc(t("theme_change"))}">◐</button>
    </nav>
  </header>
  <main class="shell">
    {notice}
    {body}
  </main>
  <script src="/static/app.js"></script>
</body>
</html>"""
    )


def bookmark_card(row: sqlite3.Row, return_folder: str = "", return_q: str = "") -> str:
    tags = "".join(f'<span class="tag">{esc(tag.strip())}</span>' for tag in row["tags"].split(",") if tag.strip())
    custom_icon = (row["icon"] or "").strip()
    favicon = "" if custom_icon else favicon_url(row["url"])
    edit_params = {key: value for key, value in (("return_folder", return_folder), ("return_q", return_q)) if value}
    edit_href = f"/bookmarks/{row['id']}/edit?{urlencode(edit_params)}" if edit_params else f"/bookmarks/{row['id']}/edit"
    favicon_html = (
        f'<img class="bookmark-favicon" src="{esc(favicon)}" alt="" loading="lazy" referrerpolicy="no-referrer">'
        if favicon
        else ""
    )
    icon_html = f'<span class="bookmark-custom-icon" aria-hidden="true">{esc(custom_icon)}</span>' if custom_icon else f'{favicon_html}<span class="bookmark-favicon-fallback" aria-hidden="true">🔗</span>'
    return f"""<article class="bookmark-card" draggable="true" data-bookmark-id="{row['id']}" data-bookmark-folder="{esc(row['folder'])}" title="{esc(t('drag_bookmark'))}">
  <div class="bookmark-main">
    <div class="bookmark-title-row">{icon_html}<a class="bookmark-title" href="{esc(row['url'])}" target="_blank" rel="noopener noreferrer">{esc(row['title'])}</a></div>
    <div class="bookmark-meta"><span>{esc(row['folder'])}</span>{tags}</div>
  </div>
  <div class="bookmark-actions">
    <a class="edit-button" href="{esc(edit_href)}" title="{esc(t('edit_bookmark'))}" aria-label="{esc(t('edit_bookmark'))}">✎</a>
    <form class="delete-form" method="post" action="/bookmarks/{row['id']}/delete">
      <button class="delete-button" type="submit" title="{esc(t('delete_bookmark'))}" aria-label="{esc(t('delete_bookmark'))}">×</button>
    </form>
  </div>
</article>"""


def render_folder_tree(folders: list[tuple[str, int, int, str]], selected: str = "") -> str:
    tree: dict[str, dict] = {}
    positions = {folder: position for folder, _, position, _ in folders}
    icons = {folder: icon for folder, _, _, icon in folders}
    for folder, count, _, _ in folders:
        node = tree
        parts = [part.strip() for part in folder.split(" / ") if part.strip()]
        for part in parts:
            node = node.setdefault(part, {"_count": 0, "_children": {}, "_position": 0})["_children"]
        cursor = tree
        path_parts: list[str] = []
        for part in parts:
            entry = cursor[part]
            entry["_count"] += count
            path_parts.append(part)
            current_path = " / ".join(path_parts)
            entry["_position"] = positions.get(current_path, 0)
            entry["_icon"] = icons.get(current_path, "")
            cursor = entry["_children"]

    def render(nodes: dict[str, dict], prefix: str = "") -> str:
        output = "<ul>"
        for name in sorted(nodes, key=lambda value: (value.casefold() == "sin clasificar", nodes[value]["_position"], value.casefold())):
            entry = nodes[name]
            path_name = f"{prefix} / {name}" if prefix else name
            active = " active" if path_name == selected else ""
            has_children = bool(entry["_children"])
            toggle = (
                f'<button class="folder-toggle" type="button" data-folder-toggle data-folder-key="{esc(path_name)}" aria-expanded="true">▾</button>'
                if has_children
                else '<span class="folder-toggle-spacer"></span>'
            )
            can_delete = path_name != "Sin clasificar"
            delete_control = (
                f'<form class="folder-delete-form" method="post" action="/folders/delete"><input type="hidden" name="path" value="{esc(path_name)}"><button class="folder-delete-button" type="submit" title="{esc(t("delete_folder"))}" aria-label="{esc(t("delete_folder"))}">×</button></form>'
                if can_delete
                else f'<button class="folder-delete-button" type="button" disabled title="{esc(t("uncategorized_protected"))}">×</button>'
            )
            edit_control = (
                f'<a class="folder-edit-button" href="/folders/edit?{urlencode({"path": path_name})}" title="{esc(t("rename_folder"))}" aria-label="{esc(t("rename_folder"))}">✎</a>'
                if path_name != "Sin clasificar"
                else ""
            )
            add_control = f'<a class="folder-add-button" href="/folders/new?{urlencode({"parent": path_name})}" title="{esc(t("create_subfolder"))}" aria-label="{esc(t("create_subfolder"))}">+</a>'
            draggable = ' draggable="true"' if path_name != "Sin clasificar" else ""
            icon = entry.get("_icon", "").strip()
            icon_markup = f'<span class="folder-icon" aria-hidden="true">{esc(icon)}</span>' if icon else ""
            display_name = t("uncategorized") if path_name == "Sin clasificar" else name
            output += f'<li><div class="folder-row">{toggle}<a class="folder-link folder-drop-target{active}" data-folder-path="{esc(path_name)}" data-folder-parent="{esc(path_name)}" href="/?{urlencode({"folder": path_name})}" title="{esc(t("drop_folder"))}"{draggable}><span class="folder-label">{icon_markup}<span>{esc(display_name)}</span></span><small>{entry["_count"]}</small></a><span class="folder-actions">{edit_control}{add_control}{delete_control}</span></div>'
            if entry["_children"]:
                output += f'<div class="folder-children" data-folder-children="{esc(path_name)}">{render(entry["_children"], path_name)}</div>'
            output += "</li>"
        return output + "</ul>"

    return render(tree)


def find_rows(connection: sqlite3.Connection, q: str = "", folder: str = "") -> list[sqlite3.Row]:
    if q.strip():
        terms = [re.sub(r'[^\w.-]', "", word) for word in q.split()]
        terms = [term for term in terms if term]
        if not terms:
            return []
        match = " AND ".join(f'"{term}"*' for term in terms)
        return connection.execute(
            """SELECT b.* FROM bookmarks b JOIN bookmarks_fts f ON f.rowid=b.id
               WHERE bookmarks_fts MATCH ? ORDER BY b.title COLLATE NOCASE, b.id LIMIT 250""",
            (match,),
        ).fetchall()
    if folder:
        return connection.execute(
            "SELECT * FROM bookmarks WHERE folder=? OR folder LIKE ? ORDER BY position, title COLLATE NOCASE, id LIMIT 250",
            (folder, folder + " / %"),
        ).fetchall()
    return connection.execute("SELECT * FROM bookmarks ORDER BY title COLLATE NOCASE, id LIMIT 250").fetchall()


def rebuild_search_index(connection: sqlite3.Connection) -> None:
    connection.execute("DROP TABLE IF EXISTS bookmarks_fts")
    connection.execute("""CREATE VIRTUAL TABLE bookmarks_fts USING fts5(
        title, url, folder, tags, notes, content=''
    )""")
    rows = connection.execute("SELECT id, title, url, folder, tags, notes FROM bookmarks").fetchall()
    connection.executemany(
        "INSERT INTO bookmarks_fts(rowid, title, url, folder, tags, notes) VALUES (?, ?, ?, ?, ?, ?)",
        [(row["id"], row["title"], row["url"], row["folder"], row["tags"], row["notes"]) for row in rows],
    )


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def home(q: str = "", folder: str = "", message: str = "") -> HTMLResponse:
    with db() as connection:
        folder_rows = connection.execute("SELECT path, position, icon, is_default FROM folders").fetchall()
        bookmark_rows = connection.execute("SELECT folder FROM bookmarks").fetchall()
        folder_counts = {row[0]: [0, row[1]] for row in folder_rows}
        for bookmark_row in bookmark_rows:
            bookmark_folder = bookmark_row[0]
            for path in folder_counts:
                # Cada marcador cuenta directamente en su carpeta. El árbol
                # suma después los hijos una sola vez para los contadores de
                # las carpetas padre.
                if bookmark_folder == path:
                    folder_counts[path][0] += 1
        if not q.strip() and not folder.strip():
            folder = next((row[0] for row in folder_rows if row[3]), "")
        if q.strip():
            folder = ""
        rows = find_rows(connection, q, folder)
        total = connection.execute("SELECT COUNT(*) FROM bookmarks").fetchone()[0]

    folder_icons = {row[0]: row[2] for row in folder_rows}
    folder_menu = render_folder_tree(
        [(path, values[0], values[1], folder_icons.get(path, "")) for path, values in folder_counts.items()],
        folder,
    )
    cards = "".join(bookmark_card(row, folder if not q.strip() else "", q if q.strip() else "") for row in rows)
    empty = f'<div class="empty"><strong>{esc(t("empty_title"))}</strong><br>{esc(t("empty_help"))}</div>' if not rows else ""
    body = f"""<section class="hero">
  <div><p class="eyebrow">{esc(t("your_library"))}</p><h1 class="product-heading"><img src="/static/brand-mark.svg" alt="" aria-hidden="true">Super Bookmark Manager</h1><p class="muted">{esc(count_label("bookmarks", total))}</p></div>
  <a class="primary-button" href="/add">+ {esc(t("add_bookmark"))}</a>
</section>
<form class="searchbar" method="get" action="/" data-auto-search>
  <input class="search-input" type="search" name="q" value="{esc(q)}" placeholder="{esc(t("search_placeholder"))}" aria-label="{esc(t("search_bookmarks"))}" autofocus>
  <input type="hidden" name="folder" value="{esc(folder)}">
  <noscript><button class="primary-button" type="submit">{esc(t("search"))}</button></noscript>
</form>
<div class="workspace">
  <aside class="folder-sidebar">
    <div class="sidebar-heading"><strong>{esc(t("folders"))}</strong><span class="sidebar-actions"><button id="collapse-folders" type="button" title="{esc(t("collapse_folders"))}">−</button><a href="/folders/new" title="{esc(t("create_folder"))}" aria-label="{esc(t("create_folder"))}">+</a></span></div>
    <a class="folder-link folder-drop-target all-folders{' active' if not folder else ''}" data-folder-parent="" href="/" title="{esc(t("drop_root"))}"><span>▣ {esc(t("all_bookmarks"))}</span><small>{total}</small></a>
    {folder_menu or f'<p class="sidebar-empty">{esc(t("no_folders"))}</p>'}
  </aside>
  <section class="content-column">
    <div class="results-panel">
      <div class="list-heading"><span id="result-count">{esc(count_label("result", len(rows)))}</span><a href="/import">{esc(t("import_bookmarks_html"))}</a></div>
      <section class="bookmark-list" id="bookmark-list">{cards}{empty}</section>
    </div>
  </section>
</div>"""
    return page("Inicio", body, query=q, message=message)


@app.get("/api/search")
def api_search(q: str = "", folder: str = "") -> JSONResponse:
    with db() as connection:
        rows = find_rows(connection, q, folder)
    return JSONResponse(
        {
            "count": len(rows),
            "results": [
                {
                    "id": row["id"],
                    "title": row["title"],
                    "url": row["url"],
                    "icon": row["icon"] or "",
                    "favicon": favicon_url(row["url"]),
                    "folder": row["folder"],
                    "tags": [tag.strip() for tag in row["tags"].split(",") if tag.strip()],
                }
                for row in rows
            ],
        }
    )


@app.post("/bookmarks/{bookmark_id}/delete")
def delete_bookmark(bookmark_id: int) -> RedirectResponse:
    with db() as connection:
        connection.execute("DELETE FROM bookmarks WHERE id=?", (bookmark_id,))
        rebuild_search_index(connection)
    return RedirectResponse(url="/", status_code=303)


@app.post("/bookmarks/{bookmark_id}/move")
def move_bookmark(bookmark_id: int, folder: str = Form(...)) -> JSONResponse:
    normalized_folder = normalize_folder(folder, "Sin clasificar")
    with db() as connection:
        bookmark = connection.execute("SELECT id, folder FROM bookmarks WHERE id=?", (bookmark_id,)).fetchone()
        if not bookmark:
            return JSONResponse({"ok": False, "error": t("bookmark_not_found")}, status_code=404)
        ensure_folder_path(connection, normalized_folder)
        position = connection.execute("SELECT COALESCE(MAX(position), -1) + 1 FROM bookmarks WHERE folder=?", (normalized_folder,)).fetchone()[0]
        connection.execute(
            "UPDATE bookmarks SET folder=?, position=?, updated_at=? WHERE id=?",
            (normalized_folder, position, now(), bookmark_id),
        )
        rebuild_search_index(connection)
    return JSONResponse({"ok": True, "folder": normalized_folder})


@app.post("/bookmarks/reorder")
def reorder_bookmark(bookmark_id: int = Form(...), target_id: int = Form(...)) -> JSONResponse:
    with db() as connection:
        moved = connection.execute("SELECT id, folder FROM bookmarks WHERE id=?", (bookmark_id,)).fetchone()
        target = connection.execute("SELECT id, folder FROM bookmarks WHERE id=?", (target_id,)).fetchone()
        if not moved or not target:
            return JSONResponse({"ok": False, "error": t("bookmark_not_found")}, status_code=404)
        if moved["id"] == target["id"]:
            return JSONResponse({"ok": True})
        if moved["folder"] != target["folder"]:
            return JSONResponse({"ok": False, "error": t("same_folder_reorder")}, status_code=400)
        rows = connection.execute(
            "SELECT id FROM bookmarks WHERE folder=? ORDER BY position, title COLLATE NOCASE, id",
            (moved["folder"],),
        ).fetchall()
        ordered = [row[0] for row in rows if row[0] != moved["id"]]
        ordered.insert(ordered.index(target["id"]), moved["id"])
        for position, row_id in enumerate(ordered):
            connection.execute("UPDATE bookmarks SET position=?, updated_at=? WHERE id=?", (position, now(), row_id))
        rebuild_search_index(connection)
    return JSONResponse({"ok": True})


@app.get("/folders/new", response_class=HTMLResponse)
def new_folder_form(parent: str = "") -> HTMLResponse:
    parent = normalize_folder(parent)
    body = f"""<section class="form-wrap">
  <p class="eyebrow">{esc(t("organization"))}</p><h1>{esc(t("new_folder"))}</h1>
  <p class="muted">{esc(t("new_folder_help"))} <code>Trabajo / Servidores</code>.</p>
  <form class="card-form" method="post" action="/folders">
    <label>{esc(t("folder_path"))}<input name="path" value="{esc(parent)}" placeholder="Trabajo / Servidores" required autofocus></label>
    <div class="form-actions"><a href="/">{esc(t("cancel"))}</a><button class="primary-button" type="submit">{esc(t("create_folder_button"))}</button></div>
  </form>
</section>"""
    return page(t("new_folder"), body)


@app.post("/folders")
def create_folder(path: str = Form(...)) -> RedirectResponse:
    normalized = normalize_folder(path)
    if not normalized:
        return RedirectResponse(url=f"/?{urlencode({'message': t('valid_folder')})}", status_code=303)
    with db() as connection:
        ensure_folder_path(connection, normalized)
    return RedirectResponse(url=f"/?{urlencode({'message': t('folder_created')})}", status_code=303)


@app.get("/folders/edit", response_class=HTMLResponse)
def edit_folder_form(path: str = "") -> HTMLResponse:
    normalized = normalize_folder(path)
    with db() as connection:
        folder_row = connection.execute("SELECT path, icon, is_default FROM folders WHERE path=?", (normalized,)).fetchone()
    if not folder_row or normalized == "Sin clasificar":
        return RedirectResponse(url=f"/?{urlencode({'message': t('cannot_edit_folder')})}", status_code=303)
    parent = normalized.rsplit(" / ", 1)[0] if " / " in normalized else t("root_folders")
    name = normalized.rsplit(" / ", 1)[-1]
    icon = folder_row["icon"] or ""
    is_default = bool(folder_row["is_default"])
    body = f"""<section class="form-wrap">
  <p class="eyebrow">{esc(t("organization"))}</p><h1>{esc(t("edit_folder"))}</h1>
  <p class="muted">{esc(t("location"))}: <strong>{esc(parent)}</strong>. {esc(t("folder_update_help"))}</p>
  <form class="card-form" method="post" action="/folders/rename">
    <input type="hidden" name="old_path" value="{esc(normalized)}">
    <label>{esc(t("new_name"))}<input name="name" value="{esc(name)}" required autofocus></label>
    <label>{esc(t("icon_emoji"))}
      {emoji_picker_controls(icon)}
    </label>
    <label class="checkbox-label"><input type="checkbox" name="default_folder" value="1"{' checked' if is_default else ''}> {esc(t("default_folder"))}</label>
    <div class="form-actions"><a href="/">{esc(t("cancel"))}</a><button class="primary-button" type="submit">{esc(t("save_changes"))}</button></div>
  </form>
</section>"""
    return page(t("rename_folder"), body)


@app.post("/folders/rename")
def rename_folder(old_path: str = Form(...), name: str = Form(...), icon: str = Form(""), default_folder: str = Form("")) -> RedirectResponse:
    old_path = normalize_folder(old_path)
    new_name = " ".join(name.split())
    new_icon = icon.strip()[:8]
    make_default = default_folder in {"1", "true", "on"}
    if not new_name or "/" in new_name:
        return RedirectResponse(url=f"/?{urlencode({'message': t('valid_folder_no_slashes')})}", status_code=303)
    parent = old_path.rsplit(" / ", 1)[0] if " / " in old_path else ""
    new_path = f"{parent} / {new_name}" if parent else new_name
    message = t("folder_renamed")
    with db() as connection:
        if old_path == "Sin clasificar" or not connection.execute("SELECT 1 FROM folders WHERE path=?", (old_path,)).fetchone():
            message = t("folder_not_editable")
        elif new_path != old_path and connection.execute("SELECT 1 FROM folders WHERE path=? OR path LIKE ? LIMIT 1", (new_path, new_path + " / %")).fetchone():
            message = t("folder_name_exists")
        else:
            folder_rows = connection.execute(
                "SELECT path FROM folders WHERE path=? OR path LIKE ? ORDER BY LENGTH(path) DESC",
                (old_path, old_path + " / %"),
            ).fetchall()
            bookmark_rows = connection.execute(
                "SELECT id, folder FROM bookmarks WHERE folder=? OR folder LIKE ?",
                (old_path, old_path + " / %"),
            ).fetchall()
            for row in folder_rows:
                replacement = new_path + row["path"][len(old_path):]
                connection.execute("UPDATE folders SET path=? WHERE path=?", (replacement, row["path"]))
            for row in bookmark_rows:
                replacement = new_path + row["folder"][len(old_path):]
                connection.execute("UPDATE bookmarks SET folder=?, updated_at=? WHERE id=?", (replacement, now(), row["id"]))
            if make_default:
                connection.execute("UPDATE folders SET is_default=0")
            connection.execute("UPDATE folders SET icon=?, is_default=? WHERE path=?", (new_icon, int(make_default), new_path))
            rebuild_search_index(connection)
    return RedirectResponse(url=f"/?{urlencode({'message': message})}", status_code=303)


@app.post("/folders/move")
def move_folder(path: str = Form(...), parent: str = Form("")) -> JSONResponse:
    old_path = normalize_folder(path)
    parent_path = normalize_folder(parent)
    with db() as connection:
        if old_path == "Sin clasificar" or not connection.execute("SELECT 1 FROM folders WHERE path=?", (old_path,)).fetchone():
            return JSONResponse({"ok": False, "error": t("folder_moved")}, status_code=400)
        if parent_path and not connection.execute("SELECT 1 FROM folders WHERE path=?", (parent_path,)).fetchone():
            return JSONResponse({"ok": False, "error": t("destination_not_found")}, status_code=400)
        if parent_path == old_path or parent_path.startswith(old_path + " / "):
            return JSONResponse({"ok": False, "error": t("folder_cycle")}, status_code=400)
        name = old_path.rsplit(" / ", 1)[-1]
        new_path = f"{parent_path} / {name}" if parent_path else name
        if new_path == old_path:
            return JSONResponse({"ok": True, "path": new_path})
        if connection.execute("SELECT 1 FROM folders WHERE path=? OR path LIKE ? LIMIT 1", (new_path, new_path + " / %")).fetchone():
            return JSONResponse({"ok": False, "error": t("destination_name_exists")}, status_code=409)
        sibling_rows = connection.execute("SELECT path, position FROM folders").fetchall()
        sibling_positions = [
            row["position"] for row in sibling_rows
            if (row["path"].rsplit(" / ", 1)[0] if " / " in row["path"] else "") == parent_path
        ]
        new_position = max(sibling_positions, default=-1) + 1
        folder_rows = connection.execute(
            "SELECT path, position FROM folders WHERE path=? OR path LIKE ? ORDER BY LENGTH(path) DESC",
            (old_path, old_path + " / %"),
        ).fetchall()
        bookmark_rows = connection.execute(
            "SELECT id, folder FROM bookmarks WHERE folder=? OR folder LIKE ?",
            (old_path, old_path + " / %"),
        ).fetchall()
        for row in folder_rows:
            replacement = new_path + row["path"][len(old_path):]
            position = new_position if row["path"] == old_path else row["position"]
            connection.execute("UPDATE folders SET path=?, position=? WHERE path=?", (replacement, position, row["path"]))
        for row in bookmark_rows:
            replacement = new_path + row["folder"][len(old_path):]
            connection.execute("UPDATE bookmarks SET folder=?, updated_at=? WHERE id=?", (replacement, now(), row["id"]))
        rebuild_search_index(connection)
    return JSONResponse({"ok": True, "path": new_path})


@app.post("/folders/reorder")
def reorder_folder(folder_path: str = Form(...), target_path: str = Form(...)) -> JSONResponse:
    folder_path = normalize_folder(folder_path)
    target_path = normalize_folder(target_path)
    with db() as connection:
        if folder_path == "Sin clasificar" or target_path == "Sin clasificar":
            return JSONResponse({"ok": False, "error": t("uncategorized_last")}, status_code=400)
        moved = connection.execute("SELECT path FROM folders WHERE path=?", (folder_path,)).fetchone()
        target = connection.execute("SELECT path FROM folders WHERE path=?", (target_path,)).fetchone()
        if not moved or not target:
            return JSONResponse({"ok": False, "error": t("folder_not_found")}, status_code=404)
        parent = folder_path.rsplit(" / ", 1)[0] if " / " in folder_path else ""
        target_parent = target_path.rsplit(" / ", 1)[0] if " / " in target_path else ""
        if parent != target_parent:
            return JSONResponse({"ok": False, "error": t("folder_level_reorder")}, status_code=400)
        siblings = connection.execute(
            "SELECT path FROM folders WHERE path=? OR path LIKE ?",
            (parent, parent + " / %") if parent else ("", "%"),
        ).fetchall()
        sibling_paths = [row[0] for row in siblings if (row[0].rsplit(" / ", 1)[0] if " / " in row[0] else "") == parent]
        sibling_paths.sort(key=lambda path: (connection.execute("SELECT position FROM folders WHERE path=?", (path,)).fetchone()[0], path.casefold()))
        sibling_paths.remove(folder_path)
        sibling_paths.insert(sibling_paths.index(target_path), folder_path)
        for position, path in enumerate(sibling_paths):
            connection.execute("UPDATE folders SET position=? WHERE path=?", (position, path))
    return JSONResponse({"ok": True})


@app.post("/folders/delete")
def delete_folder(path: str = Form(...)) -> RedirectResponse:
    normalized = normalize_folder(path)
    message = t("folder_deleted")
    with db() as connection:
        if normalized == "Sin clasificar":
            message = t("uncategorized_protected")
        elif not connection.execute("SELECT 1 FROM folders WHERE path=?", (normalized,)).fetchone():
            message = t("folder_does_not_exist")
        else:
            subtree_pattern = normalized + " / %"
            connection.execute(
                "UPDATE bookmarks SET folder=?, updated_at=? WHERE folder=? OR folder LIKE ?",
                ("Sin clasificar", now(), normalized, subtree_pattern),
            )
            connection.execute(
                "DELETE FROM folders WHERE path=? OR path LIKE ?",
                (normalized, subtree_pattern),
            )
            rebuild_search_index(connection)
    return RedirectResponse(url=f"/?{urlencode({'message': message})}", status_code=303)


@app.get("/bookmarks/{bookmark_id}/edit", response_class=HTMLResponse)
def edit_form(bookmark_id: int, return_folder: str = "", return_q: str = "") -> HTMLResponse:
    with db() as connection:
        row = connection.execute("SELECT * FROM bookmarks WHERE id=?", (bookmark_id,)).fetchone()
        folder_options = folder_select_options(connection, row["folder"] if row else "")
    if not row:
        return RedirectResponse(url="/", status_code=303)
    return_params = {}
    if return_q.strip():
        return_params["q"] = return_q.strip()
    elif return_folder.strip():
        return_params["folder"] = normalize_folder(return_folder)
    cancel_href = f"/?{urlencode(return_params)}" if return_params else "/"
    icon = row["icon"] or ""
    body = f"""<section class="form-wrap">
  <p class="eyebrow">{esc(t("edit_bookmark"))}</p><h1>{esc(t("modify_link"))}</h1>
  <form class="card-form" method="post" action="/bookmarks/{bookmark_id}/edit">
    <input type="hidden" name="return_folder" value="{esc(return_folder)}">
    <input type="hidden" name="return_q" value="{esc(return_q)}">
    <label>{esc(t("url"))}<input name="url" type="url" value="{esc(row['url'])}" required autofocus></label>
    <label>{esc(t("title"))}<input name="title" value="{esc(row['title'])}"></label>
    <label>{esc(t("icon_emoji"))}
      {emoji_picker_controls(icon)}
    </label>
    <label>{esc(t("folder"))}<select name="folder">{folder_options}</select></label>
    <label>{esc(t("tags"))}<input name="tags" value="{esc(row['tags'])}"></label>
    <label>{esc(t("notes"))}<textarea name="notes" rows="4">{esc(row['notes'])}</textarea></label>
    <div class="form-actions"><a href="{esc(cancel_href)}">{esc(t("cancel"))}</a><button class="primary-button" type="submit">{esc(t("save_changes"))}</button></div>
  </form>
</section>"""
    return page(t("edit_bookmark"), body)


@app.post("/bookmarks/{bookmark_id}/edit")
def update_bookmark(
    bookmark_id: int,
    url: str = Form(...),
    title: str = Form(""),
    icon: str = Form(""),
    folder: str = Form("Sin clasificar"),
    tags: str = Form(""),
    notes: str = Form(""),
    return_folder: str = Form(""),
    return_q: str = Form(""),
) -> RedirectResponse:
    normalized = normalize_url(url)
    normalized_folder = normalize_folder(folder, "Sin clasificar")
    with db() as connection:
        try:
            current = connection.execute("SELECT folder, position FROM bookmarks WHERE id=?", (bookmark_id,)).fetchone()
            if not current:
                return RedirectResponse(url="/", status_code=303)
            ensure_folder_path(connection, normalized_folder)
            position = current["position"]
            if current["folder"] != normalized_folder:
                position = connection.execute("SELECT COALESCE(MAX(position), -1) + 1 FROM bookmarks WHERE folder=?", (normalized_folder,)).fetchone()[0]
            connection.execute(
                """UPDATE bookmarks SET url=?, normalized_url=?, title=?, folder=?, position=?, icon=?, tags=?, notes=?, updated_at=?
                   WHERE id=?""",
                (url.strip(), normalized, title.strip() or url.strip(), normalized_folder, position, icon.strip()[:8], tags.strip(), notes.strip(), now(), bookmark_id),
            )
            rebuild_search_index(connection)
        except sqlite3.IntegrityError:
            params = {key: value for key, value in (("return_folder", return_folder), ("return_q", return_q)) if value}
            suffix = f"?{urlencode(params)}" if params else ""
            return RedirectResponse(url=f"/bookmarks/{bookmark_id}/edit{suffix}", status_code=303)
    params = {}
    if return_q.strip():
        params["q"] = return_q.strip()
    elif return_folder.strip():
        params["folder"] = normalize_folder(return_folder)
    return RedirectResponse(url=f"/?{urlencode(params)}" if params else "/", status_code=303)


def form_page(url: str = "", title: str = "", folder: str = "", icon: str = "", tags: str = "", notes: str = "", message: str = "", folder_options: str = "") -> HTMLResponse:
    body = f"""<section class="form-wrap">
  <p class="eyebrow">{esc(t("add_bookmark"))}</p><h1>{esc(t("save_link"))}</h1>
  <form class="card-form" method="post" action="/bookmarks">
    <label>{esc(t("url"))}<input name="url" type="url" value="{esc(url)}" placeholder="https://ejemplo.com" required autofocus></label>
    <label>{esc(t("title"))}<input name="title" value="{esc(title)}" placeholder="{esc(t("site_title"))}"></label>
    <label>{esc(t("icon_emoji"))}
      {emoji_picker_controls(icon)}
    </label>
    <label>{esc(t("folder"))}<select name="folder">{folder_options}</select></label>
    <label>{esc(t("tags"))}<input name="tags" value="{esc(tags)}" placeholder="{esc(t("tags_placeholder"))}"></label>
    <label>{esc(t("notes"))}<textarea name="notes" rows="4" placeholder="{esc(t("optional"))}">{esc(notes)}</textarea></label>
    <div class="form-actions"><a href="/">{esc(t("cancel"))}</a><button class="primary-button" type="submit">{esc(t("save"))}</button></div>
  </form>
</section>"""
    return page(t("add"), body, message=message)


@app.get("/add", response_class=HTMLResponse)
def add_form(url: str = "", title: str = "") -> HTMLResponse:
    with db() as connection:
        options = folder_select_options(connection, "Sin clasificar")
    return form_page(url=url, title=title, folder="Sin clasificar", folder_options=options)


@app.get("/bookmarklet", response_class=HTMLResponse)
def bookmarklet_page(request: Request) -> HTMLResponse:
    base_url = PUBLIC_BASE_URL or str(request.base_url).rstrip("/")
    bookmarklet = (
        "javascript:(()=>{const u=location.href;location.href='"
        + base_url
        + "/add?url='+encodeURIComponent(u)+'&title='+encodeURIComponent(document.title)})()"
    )
    body = f"""<section class="form-wrap">
  <p class="eyebrow">{esc(t("quick_access"))}</p><h1>{esc(t("save_from_browser"))}</h1>
  <p class="muted">{esc(t("bookmarklet_help"))}</p>
  <div class="card-form bookmarklet-card">
    <a class="primary-button bookmarklet-link" href="{esc(bookmarklet)}" draggable="true">{esc(t("bookmarklet_button"))}</a>
    <ol class="bookmarklet-steps">
      <li>{esc(t("bookmarklet_step1"))}</li>
      <li>{esc(t("bookmarklet_step2"))}</li>
      <li>{esc(t("bookmarklet_step3"))}</li>
    </ol>
    <p class="muted">{esc(t("bookmarklet_manual"))}</p>
  </div>
</section>"""
    return page(t("save_from_browser"), body)


@app.post("/bookmarks")
def create_bookmark(
    url: str = Form(...),
    title: str = Form(""),
    icon: str = Form(""),
    folder: str = Form("Sin clasificar"),
    tags: str = Form(""),
    notes: str = Form(""),
) -> RedirectResponse:
    with db() as connection:
        inserted = add_bookmark(connection, {"url": url, "title": title, "icon": icon, "folder": folder, "tags": tags, "notes": notes, "source": "manual"})
    message = t("bookmark_saved") if inserted else t("duplicate_invalid")
    return RedirectResponse(url=f"/?{urlencode({'message': message})}", status_code=303)


@app.get("/import", response_class=HTMLResponse)
def import_form() -> HTMLResponse:
    body = """<section class="form-wrap">
  <p class="eyebrow">{migration}</p><h1>{title}</h1>
  <p class="muted">{help}</p>
  <form class="card-form" method="post" action="/import" enctype="multipart/form-data">
    <label>{file_html}<input name="bookmark_file" type="file" accept=".html,.htm,text/html" required></label>
    <label>{source}<input name="source" placeholder="{source_placeholder}"></label>
    <div class="form-actions"><a href="/">{cancel}</a><button class="primary-button" type="submit">{import_button}</button></div>
  </form>
</section>"""
    body = body.format(migration=esc(t("migration")), title=esc(t("import_html_title")), help=esc(t("import_html_help")), file_html=esc(t("file_html")), source=esc(t("source_optional")), source_placeholder=esc(t("source_placeholder")), cancel=esc(t("cancel")), import_button=esc(t("import")))
    return page(t("import"), body)


@app.post("/import", response_class=HTMLResponse)
async def import_bookmarks(bookmark_file: UploadFile = File(...), source: str = Form("")) -> HTMLResponse:
    content = await bookmark_file.read()
    parser = BookmarkHTMLParser()
    try:
        parser.feed(content.decode("utf-8", errors="replace"))
    except Exception as exc:
        return page(t("import"), f"<div class=\"empty\">{esc(t('html_read_error'))}</div>", message=str(exc))
    added = 0
    skipped = 0
    with db() as connection:
        for item in parser.items:
            item["source"] = source.strip() or bookmark_file.filename or "importación HTML"
            if add_bookmark(connection, item):
                added += 1
            else:
                skipped += 1
    message = t("import_finished", added=added, skipped=skipped)
    return RedirectResponse(url=f"/?{urlencode({'message': message})}", status_code=303)


@app.get("/manifest.json")
def manifest() -> JSONResponse:
    return JSONResponse(
        {
            "name": "C3PBookmarks",
            "short_name": "Bookmarks",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#f6f7fb",
            "theme_color": "#18212f",
            "icons": [],
        }
    )
