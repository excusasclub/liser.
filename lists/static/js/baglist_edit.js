// --- Utilidades básicas ---
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

// --- Modal de confirmación estilo Liser ---
function liserConfirm(message, onConfirm) {
  const modal = document.getElementById("liser-modal");
  const msg = document.getElementById("liser-modal-message");
  const btnConfirm = document.getElementById("liser-modal-confirm");
  const btnCancel = document.getElementById("liser-modal-cancel");

  msg.textContent = message;
  modal.classList.remove("hidden");

  function close() {
    modal.classList.add("hidden");
    btnConfirm.removeEventListener("click", confirmHandler);
    btnCancel.removeEventListener("click", cancelHandler);
  }

  function confirmHandler() {
    close();
    onConfirm();
  }

  function cancelHandler() {
    close();
  }

  btnConfirm.addEventListener("click", confirmHandler);
  btnCancel.addEventListener("click", cancelHandler);
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
function removeItemFromSection(sectionId, itemId, event) {
  if (event) event.preventDefault();

  liserConfirm("¿Quieres quitar este item de la sublista?", () => {
    fetch("/htmx/remove-item-from-section/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `section_id=${sectionId}&item_id=${itemId}`
    })
    .then(r => r.json())
    .then(d => {
      if (d.success) {
        const row = document.querySelector(`[data-item-id='${itemId}']`);
        if (row) row.remove();
      } else {
        console.error(d.error || "Error al quitar item");
      }
    })
    .catch(console.error);
  });
}

// --- Eliminar una sección completa ---
function deleteSection(sectionId) {
  liserConfirm("¿Eliminar esta sublista? Los items no se eliminarán, solo se desasociarán.", () => {
    fetch("/htmx/delete-section/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `section_id=${sectionId}`
    })
    .then(r => r.json())
    .then(d => {
      if (d.success) {
        const section = document.querySelector(`[data-section-id='${sectionId}']`)?.closest("section");
        if (section) section.remove();
      } else {
        console.error(d.error || "Error al eliminar la sección");
      }
    })
    .catch(console.error);
  });
}
// Desplegar opciones de una subBagList
function toggleSectionOptions(sectionId) {
  const panel = document.getElementById(`section-options-${sectionId}`);
  if (!panel) return;
  panel.classList.toggle("hidden");
}

// Actualizar descripción
function updateSectionDescription(el) {
  const sectionId = el.dataset.sectionId;
  const desc = el.value.trim();
  fetch("/htmx/update-section-description/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `section_id=${sectionId}&description=${encodeURIComponent(desc)}`
  })
  .then(r => r.json())
  .then(d => {
    if (!d.success) console.error(d.error || "Error al actualizar descripción");
  });
}

// Actualizar posición
function updateSectionPosition(el) {
  const sectionId = el.dataset.sectionId;
  const pos = el.value.trim();
  fetch("/htmx/update-section-position/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `section_id=${sectionId}&position=${pos}`
  })
  .then(r => r.json())
  .then(d => {
    if (!d.success) console.error(d.error || "Error al actualizar posición");
  });
}
// --- Selector de items ---
function closeItemPicker() {
  document.querySelector("#item-picker").innerHTML = "";
}

function searchItems() {
  const query = document.querySelector("#item-search").value.trim();
  const sectionId = document
    .querySelector("#item-picker-container")
    ?.dataset.sectionId;

  fetch(`/htmx/item-picker-search/?q=${encodeURIComponent(query)}&section_id=${sectionId}`)
    .then((r) => r.text())
    .then((html) => {
      document.querySelector("#item-list").innerHTML = html;
    })
    .catch(console.error);
}

function associateItem(sectionId, itemId) {
  liserConfirm("¿Asociar este item a la subBagList?", () => {
    fetch("/htmx/associate-item/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `section_id=${sectionId}&item_id=${itemId}`,
    })
      .then((r) => r.json())
      .then((d) => {
        if (d.success) {
          closeItemPicker();
          location.reload();
        } else {
          console.error(d.error || "Error al asociar el item");
        }
      })
      .catch(console.error);
  });
}


