// --- Utilidades básicas ---
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

// --- Actualizar título de una subBagList ---
function updateSectionTitle(el) {
  const sectionId = el.dataset.sectionId;
  const title = el.value.trim();
  if (!sectionId || !title) return;

  fetch("/htmx/update-section-title/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `section_id=${sectionId}&title=${encodeURIComponent(title)}`
  })
  .then(res => res.json())
  .then(data => {
    if (!data.success) {
      console.error(data.error || "Error al guardar el título");
    } else {
      console.log(`Título actualizado: ${data.title}`);
    }
  })
  .catch(err => console.error("Error:", err));
}

// --- Quitar un item de una sección ---
function removeItemFromSection(sectionId, itemId) {
  if (!confirm("¿Quitar este item de la sección?")) return;

  fetch("/htmx/remove-item-from-section/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `section_id=${sectionId}&item_id=${itemId}`
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      // eliminar visualmente el item del DOM sin recargar toda la página
      const itemEl = document.querySelector(`[data-item-id='${itemId}']`);
      if (itemEl) itemEl.closest(".grid").remove();
    } else {
      console.error(data.error || "Error al quitar item");
    }
  })
  .catch(err => console.error("Error:", err));
}
