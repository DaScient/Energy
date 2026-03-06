async function loadReport() {
  const res = await fetch("../reports/latest_report.json", { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to load report: ${res.status}`);
  return await res.json();
}

function fmt(v) {
  if (v === null || v === undefined) return "-";
  if (typeof v === "number") return v.toFixed(3).replace(/0+$/,"").replace(/\.$/,"");
  return String(v);
}

function renderKV(el, pairs) {
  el.innerHTML = "";
  for (const [k, v] of pairs) {
    const kDiv = document.createElement("div");
    kDiv.className = "k";
    kDiv.textContent = k;
    const vDiv = document.createElement("div");
    vDiv.className = "v";
    vDiv.textContent = v;
    el.appendChild(kDiv);
    el.appendChild(vDiv);
  }
}

function renderTable(el, columns, rows) {
  const table = document.createElement("table");
  const thead = document.createElement("thead");
  const trh = document.createElement("tr");
  for (const c of columns) {
    const th = document.createElement("th");
    th.textContent = c;
    trh.appendChild(th);
  }
  thead.appendChild(trh);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");
  for (const r of rows) {
    const tr = document.createElement("tr");
    for (const c of columns) {
      const td = document.createElement("td");
      td.textContent = r[c] ?? "";
      tr.appendChild(td);
    }
    tbody.appendChild(tr);
  }
  table.appendChild(tbody);

  el.innerHTML = "";
  el.appendChild(table);
}

function renderKPIs(el, ew) {
  el.innerHTML = "";
  const items = [
    { label: "Early Warning Index", value: ew.early_warning_index, note: ew.alert ? "ALERT" : "Normal" },
    { label: "Wastewater ratio", value: ew.wastewater_ratio, note: "vs baseline median" },
    { label: "Positivity (latest)", value: ew.positivity_latest, note: "if available" },
    { label: "Method", value: (ew.interpretation || "").slice(0, 80) + "...", note: "" },
  ];
  for (const it of items) {
    const box = document.createElement("div");
    box.className = "kpi";
    const label = document.createElement("div");
    label.className = "label";
    label.textContent = it.label;
    const value = document.createElement("div");
    value.className = "value";
    value.textContent = fmt(it.value);
    const note = document.createElement("div");
    note.className = "note";
    note.textContent = it.note || "";
    box.appendChild(label);
    box.appendChild(value);
    box.appendChild(note);
    el.appendChild(box);
  }
}

function plotTrends(z) {
  const x = ["incidence", "syndromic", "wastewater", "capacity"];
  const y = [z.incidence, z.syndromic, z.wastewater, z.capacity].map(v => Number(v || 0));
  const trace = { x, y, type: "bar" };
  const layout = { title: "Robust z-trends (latest vs median)", paper_bgcolor: "transparent", plot_bgcolor: "transparent", margin: { t: 50, r: 20, b: 40, l: 40 } };
  Plotly.newPlot("chart1", [trace], layout, { displayModeBar: false });
}

async function main() {
  const inputsEl = document.getElementById("inputs");
  const ewiEl = document.getElementById("ewi");
  const pluginsEl = document.getElementById("plugins");

  const report = await loadReport();

  const s = report.inputs_summary || {};
  renderKV(inputsEl, [
    ["Incidence rows", String(s.incidence_rows || 0)],
    ["Capacity rows", String(s.capacity_rows || 0)],
    ["Wastewater rows", String(s.wastewater_rows || 0)],
    ["Suppression k", String(s.suppression_k || "")],
  ]);

  const pr = report.plugin_results || [];
  const ew = pr.find(p => p.name === "early_warning")?.data || {};
  renderKPIs(ewiEl, ew);

  const z = ew.z_trends || { incidence: 0, syndromic: 0, wastewater: 0, capacity: 0 };
  plotTrends(z);

  const rows = pr.map(p => ({
    plugin: p.name,
    ok: p.ok ? "true" : "false",
    metadata: JSON.stringify(p.metadata || {}),
  }));
  renderTable(pluginsEl, ["plugin","ok","metadata"], rows);
}

document.getElementById("reloadBtn").addEventListener("click", () => main().catch(err => alert(err)));
main().catch(err => alert(err));
