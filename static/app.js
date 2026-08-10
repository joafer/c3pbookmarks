(() => {
  const root = document.documentElement;
  const language = root.lang || "es";
  const translations = {
    es: {
      result_one: "{count} resultado", result_many: "{count} resultados", uncategorized: "Sin clasificar", no_results: "No hay resultados.", try_search: "Prueba otra búsqueda o selecciona una carpeta.",
      drag_bookmark_folder: "Arrastra este marcador a una carpeta", edit_bookmark: "Editar marcador", delete_bookmark: "Borrar marcador", confirm_bookmark: "¿Borrar este marcador?", confirm_folder: "¿Borrar esta carpeta y mover sus marcadores a Sin clasificar?", uncategorized_last: "Sin clasificar permanece siempre al final.", move_folder_error: "No se pudo mover la carpeta.", reorder_bookmark_error: "No se pudo reordenar el marcador.", move_bookmark_error: "No se pudo mover el marcador.", select_all: "Seleccionar todos", select_bookmark: "Seleccionar marcador", selected_count: "{count} seleccionados", move_selected: "Mover seleccionados", move_to: "Mover a…", delete_selected: "Borrar seleccionados", confirm_delete_selected: "¿Borrar los {count} marcadores seleccionados?", bulk_error: "No se pudieron aplicar las acciones seleccionadas."
    },
    en: {
      result_one: "{count} result", result_many: "{count} results", uncategorized: "Uncategorized", no_results: "No results.", try_search: "Try another search or select a folder.",
      drag_bookmark_folder: "Drag this bookmark to a folder", edit_bookmark: "Edit bookmark", delete_bookmark: "Delete bookmark", confirm_bookmark: "Delete this bookmark?", confirm_folder: "Delete this folder and move its bookmarks to Uncategorized?", uncategorized_last: "Uncategorized always stays at the end.", move_folder_error: "The folder could not be moved.", reorder_bookmark_error: "The bookmark could not be reordered.", move_bookmark_error: "The bookmark could not be moved.", select_all: "Select all", select_bookmark: "Select bookmark", selected_count: "{count} selected", move_selected: "Move selected", move_to: "Move to…", delete_selected: "Delete selected", confirm_delete_selected: "Delete the {count} selected bookmarks?", bulk_error: "The selected actions could not be applied."
    },
    it: {
      result_one: "{count} risultato", result_many: "{count} risultati", uncategorized: "Senza categoria", no_results: "Nessun risultato.", try_search: "Prova un'altra ricerca o seleziona una cartella.",
      drag_bookmark_folder: "Trascina questo segnalibro su una cartella", edit_bookmark: "Modifica segnalibro", delete_bookmark: "Elimina segnalibro", confirm_bookmark: "Eliminare questo segnalibro?", confirm_folder: "Eliminare questa cartella e spostare i suoi segnalibri in Senza categoria?", uncategorized_last: "Senza categoria resta sempre alla fine.", move_folder_error: "Non è stato possibile spostare la cartella.", reorder_bookmark_error: "Non è stato possibile riordinare il segnalibro.", move_bookmark_error: "Non è stato possibile spostare il segnalibro.", select_all: "Seleziona tutti", select_bookmark: "Seleziona segnalibro", selected_count: "{count} selezionati", move_selected: "Sposta selezionati", move_to: "Sposta in…", delete_selected: "Elimina selezionati", confirm_delete_selected: "Eliminare i {count} segnalibri selezionati?", bulk_error: "Non è stato possibile applicare le azioni selezionate."
    },
    pt: {
      result_one: "{count} resultado", result_many: "{count} resultados", uncategorized: "Sem categoria", no_results: "Não existem resultados.", try_search: "Tente outra pesquisa ou selecione uma pasta.",
      drag_bookmark_folder: "Arraste este marcador para uma pasta", edit_bookmark: "Editar marcador", delete_bookmark: "Apagar marcador", confirm_bookmark: "Apagar este marcador?", confirm_folder: "Apagar esta pasta e mover os seus marcadores para Sem categoria?", uncategorized_last: "Sem categoria fica sempre no fim.", move_folder_error: "Não foi possível mover a pasta.", reorder_bookmark_error: "Não foi possível reordenar o marcador.", move_bookmark_error: "Não foi possível mover o marcador.", select_all: "Selecionar todos", select_bookmark: "Selecionar marcador", selected_count: "{count} selecionados", move_selected: "Mover selecionados", move_to: "Mover para…", delete_selected: "Apagar selecionados", confirm_delete_selected: "Apagar os {count} marcadores selecionados?", bulk_error: "Não foi possível aplicar as ações selecionadas."
    },
    de: {
      result_one: "{count} Ergebnis", result_many: "{count} Ergebnisse", uncategorized: "Nicht kategorisiert", no_results: "Keine Ergebnisse.", try_search: "Eine andere Suche versuchen oder einen Ordner auswählen.",
      drag_bookmark_folder: "Diesen Bookmark auf einen Ordner ziehen", edit_bookmark: "Bookmark bearbeiten", delete_bookmark: "Bookmark löschen", confirm_bookmark: "Diesen Bookmark löschen?", confirm_folder: "Diesen Ordner löschen und seine Bookmarks nach Nicht kategorisiert verschieben?", uncategorized_last: "Nicht kategorisiert bleibt immer am Ende.", move_folder_error: "Der Ordner konnte nicht verschoben werden.", reorder_bookmark_error: "Der Bookmark konnte nicht sortiert werden.", move_bookmark_error: "Der Bookmark konnte nicht verschoben werden.", select_all: "Alle auswählen", select_bookmark: "Bookmark auswählen", selected_count: "{count} ausgewählt", move_selected: "Ausgewählte verschieben", move_to: "Verschieben nach…", delete_selected: "Ausgewählte löschen", confirm_delete_selected: "Die {count} ausgewählten Bookmarks löschen?", bulk_error: "Die ausgewählten Aktionen konnten nicht angewendet werden."
    },
    fr: {
      result_one: "{count} résultat", result_many: "{count} résultats", uncategorized: "Non classés", no_results: "Aucun résultat.", try_search: "Essayez une autre recherche ou sélectionnez un dossier.",
      drag_bookmark_folder: "Faites glisser ce favori vers un dossier", edit_bookmark: "Modifier le favori", delete_bookmark: "Supprimer le favori", confirm_bookmark: "Supprimer ce favori ?", confirm_folder: "Supprimer ce dossier et déplacer ses favoris vers Non classés ?", uncategorized_last: "Les éléments non classés restent toujours à la fin.", move_folder_error: "Le dossier n’a pas pu être déplacé.", reorder_bookmark_error: "Le favori n’a pas pu être réordonné.", move_bookmark_error: "Le favori n’a pas pu être déplacé.", select_all: "Tout sélectionner", select_bookmark: "Sélectionner le favori", selected_count: "{count} sélectionnés", move_selected: "Déplacer la sélection", move_to: "Déplacer vers…", delete_selected: "Supprimer la sélection", confirm_delete_selected: "Supprimer les {count} favoris sélectionnés ?", bulk_error: "Les actions sélectionnées n’ont pas pu être appliquées."
    }
  };
  const ui = translations[language] || translations.es;
  const tr = (key, values = {}) => Object.entries(values).reduce((text, [name, value]) => text.replace(`{${name}}`, value), ui[key] || key);
  const countLabel = (count) => tr(count === 1 ? "result_one" : "result_many", { count });
  const folderLabel = (folder) => folder === "Sin clasificar" ? tr("uncategorized") : folder;
  const bulkToolbar = document.querySelector("[data-bulk-toolbar]");
  const selectedBookmarkIds = () => [...document.querySelectorAll("[data-bookmark-select]:checked")].map((input) => input.value);
  const updateBulkToolbar = () => {
    if (!bulkToolbar) return;
    const checkboxes = [...document.querySelectorAll("[data-bookmark-select]")];
    const selected = checkboxes.filter((input) => input.checked);
    const selectAll = bulkToolbar.querySelector("[data-select-all]");
    const count = selected.length;
    bulkToolbar.hidden = checkboxes.length === 0;
    bulkToolbar.querySelector("[data-selection-count]").textContent = tr("selected_count", { count });
    bulkToolbar.querySelector("[data-bulk-move]").disabled = count === 0;
    bulkToolbar.querySelector("[data-bulk-delete]").disabled = count === 0;
    if (selectAll) {
      selectAll.checked = checkboxes.length > 0 && count === checkboxes.length;
      selectAll.indeterminate = count > 0 && count < checkboxes.length;
    }
  };
  const bulkAction = async (action) => {
    const ids = selectedBookmarkIds();
    if (!ids.length) return;
    if (action === "delete" && !window.confirm(tr("confirm_delete_selected", { count: ids.length }))) return;
    const form = new FormData();
    ids.forEach((id) => form.append("bookmark_ids", id));
    if (action === "move") {
      const folder = bulkToolbar.querySelector("[data-bulk-folder]").value;
      if (!folder) return;
      form.set("folder", folder);
    }
    const endpoint = action === "delete" ? "/bookmarks/bulk/delete" : "/bookmarks/bulk/move";
    try {
      const response = await fetch(endpoint, { method: "POST", body: form });
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.error || tr("bulk_error"));
      }
      window.location.reload();
    } catch (error) {
      window.alert(error.message || tr("bulk_error"));
    }
  };
  if (bulkToolbar) {
    bulkToolbar.querySelector("[data-select-all]").addEventListener("change", (event) => {
      document.querySelectorAll("[data-bookmark-select]").forEach((input) => { input.checked = event.target.checked; });
      updateBulkToolbar();
    });
    bulkToolbar.querySelector("[data-bulk-move]").addEventListener("click", () => bulkAction("move"));
    bulkToolbar.querySelector("[data-bulk-delete]").addEventListener("click", () => bulkAction("delete"));
  }
  document.addEventListener("change", (event) => {
    if (event.target.matches?.("[data-bookmark-select]")) updateBulkToolbar();
  });

  const saved = localStorage.getItem("c3pbookmarks-theme");
  if (saved) root.dataset.theme = saved;
  const button = document.getElementById("theme-toggle");
  if (button) button.addEventListener("click", () => {
    const current = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = current;
    localStorage.setItem("c3pbookmarks-theme", current);
  });

  const wireFavicon = (image, fallback) => {
    const loaded = () => { fallback.hidden = true; };
    const failed = () => { image.hidden = true; fallback.hidden = false; };
    image.addEventListener("load", loaded);
    image.addEventListener("error", failed);
    if (image.complete) (image.naturalWidth ? loaded : failed)();
  };
  document.querySelectorAll(".bookmark-favicon").forEach((image) => wireFavicon(image, image.nextElementSibling));

  const searchForm = document.querySelector("[data-auto-search]");
  const searchInput = document.querySelector(".search-input");
  if (searchForm && searchInput) {
    let timer;
    let request;
    const resultsPanel = document.querySelector(".results-panel");
    const resultsList = document.getElementById("bookmark-list");
    const resultCount = document.getElementById("result-count");
    const isMobile = window.matchMedia("(max-width: 700px)").matches;

    const renderResults = (data) => {
      if (!resultsList || !resultCount) return;
      resultCount.textContent = countLabel(data.count);
      resultsList.replaceChildren();
      if (!data.results.length) {
        const empty = document.createElement("div");
        empty.className = "empty";
        empty.innerHTML = `<strong>${tr("no_results")}</strong><br>${tr("try_search")}`;
        resultsList.appendChild(empty);
        updateBulkToolbar();
        return;
      }
      for (const item of data.results) {
        const card = document.createElement("article");
        card.className = "bookmark-card";
        card.draggable = true;
        card.dataset.bookmarkId = item.id;
        card.dataset.bookmarkFolder = item.folder;
        card.title = tr("drag_bookmark_folder");
        const selectWrap = document.createElement("label");
        selectWrap.className = "bookmark-select-wrap";
        const select = document.createElement("input");
        select.className = "bookmark-select";
        select.type = "checkbox";
        select.dataset.bookmarkSelect = "";
        select.value = item.id;
        select.setAttribute("aria-label", tr("select_bookmark"));
        selectWrap.appendChild(select);
        card.appendChild(selectWrap);
        const main = document.createElement("div");
        main.className = "bookmark-main";
        const titleRow = document.createElement("div");
        titleRow.className = "bookmark-title-row";
        if (item.icon) {
          const customIcon = document.createElement("span");
          customIcon.className = "bookmark-custom-icon";
          customIcon.setAttribute("aria-hidden", "true");
          customIcon.textContent = item.icon;
          titleRow.appendChild(customIcon);
        } else if (item.favicon) {
          const favicon = document.createElement("img");
          favicon.className = "bookmark-favicon";
          favicon.src = item.favicon;
          favicon.alt = "";
          favicon.loading = "lazy";
          favicon.referrerPolicy = "no-referrer";
          titleRow.appendChild(favicon);
          const fallback = document.createElement("span");
          fallback.className = "bookmark-favicon-fallback";
          fallback.setAttribute("aria-hidden", "true");
          fallback.textContent = "🔗";
          titleRow.appendChild(fallback);
          wireFavicon(favicon, fallback);
        } else {
          const fallback = document.createElement("span");
          fallback.className = "bookmark-favicon-fallback";
          fallback.setAttribute("aria-hidden", "true");
          fallback.textContent = "🔗";
          titleRow.appendChild(fallback);
        }
        const title = document.createElement("a");
        title.className = "bookmark-title";
        title.href = item.url;
        title.target = "_blank";
        title.rel = "noopener noreferrer";
        title.textContent = item.title;
        const meta = document.createElement("div");
        meta.className = "bookmark-meta";
        const folder = document.createElement("span");
        folder.textContent = folderLabel(item.folder);
        meta.appendChild(folder);
        for (const tagValue of item.tags) {
          const tag = document.createElement("span");
          tag.className = "tag";
          tag.textContent = tagValue;
          meta.appendChild(tag);
        }
        titleRow.appendChild(title);
        main.append(titleRow, meta);
        card.appendChild(main);
        const actions = document.createElement("div");
        actions.className = "bookmark-actions";
        const editLink = document.createElement("a");
        editLink.className = "edit-button";
        const returnParams = new URLSearchParams();
        const currentParams = new URLSearchParams(window.location.search);
        if (currentParams.get("q")) returnParams.set("return_q", currentParams.get("q"));
        if (currentParams.get("folder")) returnParams.set("return_folder", currentParams.get("folder"));
        const editQuery = returnParams.toString();
        editLink.href = `/bookmarks/${item.id}/edit${editQuery ? `?${editQuery}` : ""}`;
        editLink.title = tr("edit_bookmark");
        editLink.setAttribute("aria-label", tr("edit_bookmark"));
        editLink.textContent = "✎";
        actions.appendChild(editLink);
        const deleteForm = document.createElement("form");
        deleteForm.className = "delete-form";
        deleteForm.method = "post";
        deleteForm.action = `/bookmarks/${item.id}/delete`;
        deleteForm.addEventListener("submit", (event) => {
          if (!window.confirm(tr("confirm_bookmark"))) event.preventDefault();
        });
        const deleteButton = document.createElement("button");
        deleteButton.className = "delete-button";
        deleteButton.type = "submit";
        deleteButton.title = tr("delete_bookmark");
        deleteButton.setAttribute("aria-label", tr("delete_bookmark"));
        deleteButton.textContent = "×";
        deleteForm.appendChild(deleteButton);
        actions.appendChild(deleteForm);
        card.appendChild(actions);
        resultsList.appendChild(card);
      }
      updateBulkToolbar();
    };

    const performSearch = async () => {
      const query = searchInput.value.trim();
      const folderInput = searchForm.querySelector('input[name="folder"]');
      if (folderInput) folderInput.value = "";
      if (request) request.abort();
      request = new AbortController();
      try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`, { signal: request.signal });
        if (!response.ok) return;
        const data = await response.json();
        renderResults(data);
        if (isMobile) {
          document.body.classList.toggle("has-results", Boolean(query));
          if (resultsPanel) resultsPanel.hidden = !query;
        }
        window.history.replaceState({}, "", query ? `/?q=${encodeURIComponent(query)}` : "/");
      } catch (error) {
        if (error.name !== "AbortError") console.warn("No se pudo actualizar la búsqueda", error);
      }
    };

    searchInput.addEventListener("input", () => {
      window.clearTimeout(timer);
      timer = window.setTimeout(performSearch, 250);
    });
  }

  updateBulkToolbar();

  document.querySelectorAll(".delete-form").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(tr("confirm_bookmark"))) event.preventDefault();
    });
  });

  document.querySelectorAll(".folder-delete-form").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(tr("confirm_folder"))) event.preventDefault();
    });
  });

  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(form.dataset.confirm)) event.preventDefault();
    });
  });

  document.addEventListener("dragstart", (event) => {
    const folderLink = event.target.closest?.(".folder-link[data-folder-path][draggable='true']");
    if (folderLink) {
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("application/x-c3p-folder", folderLink.dataset.folderPath);
      event.dataTransfer.setData("text/plain", folderLink.dataset.folderPath);
      folderLink.classList.add("dragging");
      return;
    }
    const card = event.target.closest?.(".bookmark-card[draggable='true']");
    if (!card) return;
    const bookmarkId = card.dataset.bookmarkId;
    const draggedIds = card.querySelector("[data-bookmark-select]")?.checked ? selectedBookmarkIds() : [bookmarkId];
    event.dataTransfer.effectAllowed = "move";
    event.dataTransfer.setData("application/x-c3p-bookmarks", draggedIds.join(","));
    event.dataTransfer.setData("application/x-c3p-bookmark", bookmarkId);
    event.dataTransfer.setData("text/plain", draggedIds.join(","));
    document.querySelectorAll(".bookmark-card").forEach((candidate) => {
      if (draggedIds.includes(candidate.dataset.bookmarkId)) candidate.classList.add("dragging");
    });
  });
  document.addEventListener("dragend", (event) => {
    document.querySelectorAll(".bookmark-card.dragging").forEach((card) => card.classList.remove("dragging"));
    event.target.closest?.(".folder-link")?.classList.remove("dragging");
    document.querySelectorAll(".drag-over").forEach((link) => link.classList.remove("drag-over"));
  });
  document.addEventListener("dragover", (event) => {
    const folderLink = event.target.closest?.(".folder-drop-target");
    if (folderLink) {
      event.preventDefault();
      event.dataTransfer.dropEffect = "move";
      folderLink.classList.add("drag-over");
      return;
    }
    const targetCard = event.target.closest?.(".bookmark-card[draggable='true']");
    if (targetCard) {
      event.preventDefault();
      event.dataTransfer.dropEffect = "move";
      targetCard.classList.add("reorder-over");
    }
  });
  document.addEventListener("dragleave", (event) => {
    const folderLink = event.target.closest?.(".folder-drop-target");
    if (folderLink && !folderLink.contains(event.relatedTarget)) folderLink.classList.remove("drag-over");
    const targetCard = event.target.closest?.(".bookmark-card[draggable='true']");
    if (targetCard && !targetCard.contains(event.relatedTarget)) targetCard.classList.remove("reorder-over");
  });
  document.addEventListener("drop", async (event) => {
    const folderLink = event.target.closest?.(".folder-drop-target");
    const targetCard = event.target.closest?.(".bookmark-card[draggable='true']");
    if (!folderLink && !targetCard) return;
    event.preventDefault();
    folderLink?.classList.remove("drag-over");
    targetCard?.classList.remove("reorder-over");
    const draggedFolder = event.dataTransfer.getData("application/x-c3p-folder");
    const draggedBookmark = event.dataTransfer.getData("application/x-c3p-bookmark");
    if (draggedFolder && folderLink) {
      const targetPath = folderLink.dataset.folderPath || "";
      if (draggedFolder === targetPath) return;
      if (targetPath === "Sin clasificar") {
        window.alert(tr("uncategorized_last"));
        return;
      }
      const form = new FormData();
      const sourceParent = draggedFolder.includes(" / ") ? draggedFolder.slice(0, draggedFolder.lastIndexOf(" / ")) : "";
      const targetParent = targetPath.includes(" / ") ? targetPath.slice(0, targetPath.lastIndexOf(" / ")) : "";
      const sameLevel = Boolean(targetPath) && sourceParent === targetParent;
      const endpoint = sameLevel ? "/folders/reorder" : "/folders/move";
      if (sameLevel) {
        form.set("folder_path", draggedFolder);
        form.set("target_path", targetPath);
      } else {
        form.set("path", draggedFolder);
        form.set("parent", folderLink.dataset.folderParent || "");
      }
      try {
        const response = await fetch(endpoint, { method: "POST", body: form });
        if (!response.ok) {
          const data = await response.json().catch(() => ({}));
          throw new Error(data.error || tr("move_folder_error"));
        }
        window.location.reload();
      } catch (error) {
        window.alert(error.message || tr("move_folder_error"));
      }
      return;
    }
    const draggedBookmarksValue = event.dataTransfer.getData("application/x-c3p-bookmarks");
    const draggedBookmarkIds = (draggedBookmarksValue || draggedBookmark || event.dataTransfer.getData("text/plain"))
      .split(",")
      .map((value) => value.trim())
      .filter((value, index, values) => /^\d+$/.test(value) && values.indexOf(value) === index);
    if (!draggedBookmarkIds.length) return;
    if (draggedBookmarkIds.length > 1 && (folderLink || targetCard)) {
      const destination = folderLink?.dataset.folderPath || targetCard?.dataset.bookmarkFolder || "";
      if (!destination) return;
      const form = new FormData();
      draggedBookmarkIds.forEach((id) => form.append("bookmark_ids", id));
      form.set("folder", destination);
      try {
        const response = await fetch("/bookmarks/bulk/move", { method: "POST", body: form });
        if (!response.ok) {
          const data = await response.json().catch(() => ({}));
          throw new Error(data.error || tr("move_bookmark_error"));
        }
        window.location.reload();
      } catch (error) {
        window.alert(error.message || tr("move_bookmark_error"));
      }
      return;
    }
    const bookmarkId = draggedBookmarkIds[0];
    if (targetCard && targetCard.dataset.bookmarkId !== bookmarkId) {
      const form = new FormData();
      form.set("bookmark_id", bookmarkId);
      form.set("target_id", targetCard.dataset.bookmarkId);
      try {
        const response = await fetch("/bookmarks/reorder", { method: "POST", body: form });
        if (!response.ok) {
          const data = await response.json().catch(() => ({}));
          throw new Error(data.error || tr("reorder_bookmark_error"));
        }
        window.location.reload();
      } catch (error) {
        window.alert(error.message || tr("reorder_bookmark_error"));
      }
      return;
    }
    const form = new FormData();
    form.set("folder", folderLink.dataset.folderPath);
    try {
      const response = await fetch(`/bookmarks/${encodeURIComponent(bookmarkId)}/move`, { method: "POST", body: form });
      if (!response.ok) throw new Error("move failed");
      window.location.reload();
    } catch (_) {
      window.alert(tr("move_bookmark_error"));
    }
  });

  const folderStateKey = "c3pbookmarks-collapsed-folders";
  let collapsed = new Set();
  try { collapsed = new Set(JSON.parse(localStorage.getItem(folderStateKey) || "[]")); } catch (_) {}
  const saveFolderState = () => localStorage.setItem(folderStateKey, JSON.stringify([...collapsed]));
  document.querySelectorAll("[data-folder-toggle]").forEach((toggle) => {
    const children = toggle.closest(".folder-row")?.nextElementSibling;
    const key = toggle.dataset.folderKey;
    const setOpen = (open) => {
      if (!children) return;
      children.hidden = !open;
      toggle.setAttribute("aria-expanded", String(open));
      toggle.textContent = open ? "▾" : "▸";
      if (open) collapsed.delete(key); else collapsed.add(key);
    };
    setOpen(!collapsed.has(key));
    toggle.addEventListener("click", () => { setOpen(children.hidden); saveFolderState(); });
  });
  const collapseAll = document.getElementById("collapse-folders");
  if (collapseAll) collapseAll.addEventListener("click", () => {
    document.querySelectorAll("[data-folder-toggle]").forEach((toggle) => {
      const children = toggle.closest(".folder-row")?.nextElementSibling;
      const key = toggle.dataset.folderKey;
      if (children) children.hidden = true;
      toggle.setAttribute("aria-expanded", "false");
      toggle.textContent = "▸";
      collapsed.add(key);
    });
    saveFolderState();
  });

  document.querySelectorAll("[data-emoji-picker]").forEach((picker) => {
    const input = picker.closest("label")?.querySelector('input[name="icon"]');
    if (!input) return;
    const firstGrapheme = (value) => {
      if (typeof Intl !== "undefined" && Intl.Segmenter) {
        const segments = new Intl.Segmenter(undefined, { granularity: "grapheme" }).segment(value);
        return segments[Symbol.iterator]().next().value?.segment || "";
      }
      return Array.from(value).slice(0, 1).join("");
    };
    picker.querySelectorAll("[data-emoji]").forEach((button) => {
      button.addEventListener("click", () => {
        input.value = firstGrapheme(button.dataset.emoji || "");
        input.focus();
      });
    });
    input.addEventListener("input", () => {
      const first = firstGrapheme(input.value);
      if (input.value !== first) input.value = first;
    });
  });

  // Los marcadores siempre se abren en una pestaña nueva; la aplicación queda abierta.
  if (window.matchMedia("(max-width: 700px)").matches) {
    const params = new URLSearchParams(window.location.search);
    const results = document.querySelector(".results-panel");
    const hasSelectedFolder = Boolean(document.querySelector(".folder-link.active:not(.all-folders)"));
    const hasResults = Boolean(params.get("q") || params.get("folder") || hasSelectedFolder);
    document.body.classList.toggle("has-results", hasResults);
    if (results) results.hidden = !hasResults;
    document.querySelectorAll(".folder-link").forEach((link) => {
      link.addEventListener("click", (event) => {
        event.stopPropagation();
        window.location.assign(link.href);
      });
    });
  }
})();
