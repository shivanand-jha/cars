const state = {
  cars: [],
  recommendations: [],
  selected: new Set(),
  preferences: {},
};

const $ = (selector) => document.querySelector(selector);

const fields = {
  buyerName: $("#buyerName"),
  budget: $("#budget"),
  familySize: $("#familySize"),
  usage: $("#usage"),
  bodyPreference: $("#bodyPreference"),
  mileage: $("#mileage"),
  safety: $("#safety"),
  features: $("#features"),
  notes: $("#notes"),
};

function money(value) {
  return `Rs ${Number(value).toFixed(1)}L`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function getPreferences() {
  return {
    budget_lakh: Number(fields.budget.value),
    family_size: Number(fields.familySize.value),
    usage: fields.usage.value,
    body_preference: fields.bodyPreference.value,
    mileage_priority: Number(fields.mileage.value),
    safety_priority: Number(fields.safety.value),
    feature_priority: Number(fields.features.value),
  };
}

function syncOutputs() {
  $("#budgetValue").textContent = `${fields.budget.value} lakh`;
  $("#mileageValue").textContent = fields.mileage.value;
  $("#safetyValue").textContent = fields.safety.value;
  $("#featureValue").textContent = fields.features.value;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || "Request failed");
  }
  return payload;
}

async function loadCars() {
  const payload = await api("/api/cars");
  state.cars = payload.cars;
  $("#carCount").textContent = `${state.cars.length} cars in dataset`;
}

async function rankCars(event) {
  if (event) event.preventDefault();
  state.preferences = getPreferences();
  const payload = await api("/api/recommend", {
    method: "POST",
    body: JSON.stringify(state.preferences),
  });
  state.recommendations = payload.recommendations;
  $("#summary").textContent = summaryText(state.preferences, state.recommendations);
  renderRecommendations();
  renderCompare();
}

function summaryText(preferences, recommendations) {
  const top = recommendations[0];
  if (!top) return "No recommendations available.";
  const usage = preferences.usage === "mixed" ? "mixed use" : `${preferences.usage} use`;
  return `${top.make} ${top.model} leads for a Rs ${preferences.budget_lakh}L budget, ${usage}, and safety priority ${preferences.safety_priority}/5.`;
}

function renderRecommendations() {
  const container = $("#recommendations");
  container.innerHTML = "";
  state.recommendations.slice(0, 6).forEach((car, index) => {
    const isSelected = state.selected.has(car.id);
    const card = document.createElement("article");
    card.className = `car-card${isSelected ? " selected" : ""}`;
    card.innerHTML = `
      <div>
        <div class="car-title">
          <h3>${index + 1}. ${escapeHtml(car.make)} ${escapeHtml(car.model)}</h3>
          <span class="tag">${escapeHtml(car.variant)}</span>
          <span class="score">${car.match_score}% match</span>
        </div>
        <p>${escapeHtml(car.review)}</p>
        <div class="metrics">
          <div class="metric"><strong>${money(car.price_lakh)}</strong><span>ex-showroom</span></div>
          <div class="metric"><strong>${car.mileage_kmpl} kmpl</strong><span>mileage</span></div>
          <div class="metric"><strong>${car.safety_rating}/5</strong><span>safety</span></div>
          <div class="metric"><strong>${escapeHtml(car.body_type)}</strong><span>${car.seats} seats</span></div>
        </div>
        <strong>Why it fits</strong>
        <ul class="reason-list">${car.reasons.map((reason) => `<li>${escapeHtml(reason)}</li>`).join("")}</ul>
        ${car.cautions.length ? `<ul class="caution-list">${car.cautions.map((caution) => `<li>${escapeHtml(caution)}</li>`).join("")}</ul>` : ""}
      </div>
      <div class="card-actions">
        <button type="button" data-select="${car.id}" class="${isSelected ? "is-selected" : ""}">
          ${isSelected ? "Selected" : "Compare"}
        </button>
        <span class="tag">${escapeHtml(car.fuel_type)}</span>
        <span class="tag">${escapeHtml(car.pros[0])}</span>
      </div>
    `;
    container.appendChild(card);
  });

  container.querySelectorAll("[data-select]").forEach((button) => {
    button.addEventListener("click", () => toggleSelected(button.dataset.select));
  });
}

function toggleSelected(carId) {
  if (state.selected.has(carId)) {
    state.selected.delete(carId);
  } else if (state.selected.size < 3) {
    state.selected.add(carId);
  } else {
    $("#saveMessage").textContent = "Compare is capped at three cars to keep the decision focused.";
    $("#saveMessage").className = "message error";
    return;
  }
  $("#saveMessage").textContent = "";
  renderRecommendations();
  renderCompare();
}

function selectedCars() {
  return state.recommendations.filter((car) => state.selected.has(car.id));
}

function renderCompare() {
  const cars = selectedCars();
  const container = $("#compareTable");
  if (!cars.length) {
    container.className = "compare-empty";
    container.innerHTML = "No cars selected yet.";
    return;
  }
  container.className = "";
  const rows = [
    ["Price", (car) => money(car.price_lakh)],
    ["Mileage", (car) => `${car.mileage_kmpl} kmpl`],
    ["Safety", (car) => `${car.safety_rating}/5`],
    ["Best for", (car) => car.reasons[0]],
    ["Watch-out", (car) => car.cautions[0] || car.cons[0]],
  ];
  container.innerHTML = `
    <table class="compare-table">
      <thead>
        <tr><th>Decision factor</th>${cars.map((car) => `<th>${escapeHtml(car.make)} ${escapeHtml(car.model)}</th>`).join("")}</tr>
      </thead>
      <tbody>
        ${rows.map(([label, getter]) => `<tr><th>${label}</th>${cars.map((car) => `<td>${escapeHtml(getter(car))}</td>`).join("")}</tr>`).join("")}
      </tbody>
    </table>
  `;
}

async function saveShortlist() {
  const carIds = Array.from(state.selected);
  if (!carIds.length) {
    $("#saveMessage").textContent = "Select at least one car before saving.";
    $("#saveMessage").className = "message error";
    return;
  }
  const payload = await api("/api/shortlist", {
    method: "POST",
    body: JSON.stringify({
      buyer_name: fields.buyerName.value,
      preferences: state.preferences,
      car_ids: carIds,
      notes: fields.notes.value,
    }),
  });
  $("#saveMessage").textContent = `Saved shortlist #${payload.shortlist.id}.`;
  $("#saveMessage").className = "message ok";
  await loadShortlists();
}

async function loadShortlists() {
  const payload = await api("/api/shortlists");
  $("#savedCount").textContent = `${payload.shortlists.length} saved`;
  const container = $("#savedList");
  if (!payload.shortlists.length) {
    container.innerHTML = "<p>No saved sessions yet.</p>";
    return;
  }
  container.innerHTML = payload.shortlists.map((item) => {
    const date = new Date(item.created_at * 1000).toLocaleString();
    const cars = item.cars.map((car) => `${car.make} ${car.model}`).join(", ");
    return `
      <article class="saved-item">
        <h3>${escapeHtml(item.buyer_name)} - ${escapeHtml(date)}</h3>
        <p><strong>Cars:</strong> ${escapeHtml(cars)}</p>
        <p>${escapeHtml(item.notes || "No notes captured.")}</p>
      </article>
    `;
  }).join("");
}

function bindEvents() {
  $("#prefsForm").addEventListener("submit", rankCars);
  $("#saveBtn").addEventListener("click", saveShortlist);
  [fields.budget, fields.mileage, fields.safety, fields.features].forEach((field) => {
    field.addEventListener("input", syncOutputs);
  });
  [fields.budget, fields.familySize, fields.usage, fields.bodyPreference, fields.mileage, fields.safety, fields.features].forEach((field) => {
    field.addEventListener("change", rankCars);
  });
}

async function boot() {
  bindEvents();
  syncOutputs();
  await loadCars();
  await rankCars();
  await loadShortlists();
}

boot().catch((error) => {
  $("#recommendations").innerHTML = `<div class="message error">${error.message}</div>`;
});
