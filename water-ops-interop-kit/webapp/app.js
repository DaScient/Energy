async function loadReport() {
  const res = await fetch("../reports/latest_report.json", { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to load report: ${res.status}`);
  return await res.json();
}

function fmt(v) {
  if (v === null || v === undefined) return "";
  if (typeof v === "number") {
    if (Math.abs(v) >= 1000) return v.toFixed(0);
    return v.toFixed(4).replace(/0+$/,"").replace(/\.$/,"");
  }
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

function renderKPIs(el, metrics) {
  el.innerHTML = "";
  const items = [
    { key: "leak_likelihood_score", label: "Leak likelihood" },
    { key: "pump_specific_energy_kj_m3", label: "Pump specific energy (kJ/m3)" },
    { key: "water_quality_risk_index", label: "Water quality risk" },
  ];

  for (const item of items) {
    const box = document.createElement("div");
    box.className = "kpi";
    const label = document.createElement("div");
    label.className = "label";
    label.textContent = item.label;

    const v = metrics[item.key]?.value;
    const value = document.createElement("div");
    value.className = "value";
    value.textContent = v === null || v === undefined ? "-" : fmt(v);

    const note = document.createElement("div");
    note.className = "note";
    note.textContent = metrics[item.key]?.notes || "";

    box.appendChild(label);
    box.appendChild(value);
    box.appendChild(note);
    el.appendChild(box);
  }
}

function plotGauges(metrics) {
  const leak = metrics.leak_likelihood_score?.value;
  const wq = metrics.water_quality_risk_index?.value;

  const gauge1 = {
    type: "indicator",
    mode: "gauge+number",
    value: leak ?? 0,
    title: { text: "Leak likelihood" },
    gauge: { axis: { range: [0, 1] } }
  };

  const gauge2 = {
    type: "indicator",
    mode: "gauge+number",
    value: wq ?? 0,
    title: { text: "Water quality risk" },
    gauge: { axis: { range: [0, 1] } }
  };

  const layout = { margin: { t: 36, r: 20, b: 20, l: 20 }, paper_bgcolor: "transparent", plot_bgcolor: "transparent" };
  Plotly.newPlot("chart1", [gauge1], layout, { displayModeBar: false });
  Plotly.newPlot("chart2", [gauge2], layout, { displayModeBar: false });
}

async function main() {
  const summaryEl = document.getElementById("summary");
  const kpisEl = document.getElementById("kpis");
  const metricsEl = document.getElementById("metricsTable");
  const pluginsEl = document.getElementById("plugins");
  const eventsEl = document.getElementById("events");

  const report = await loadReport();

  const p = report.payload || {};
  renderKV(summaryEl, [
    ["System", p.system_id || ""],
    ["Asset", `${p.asset_id || ""} (${p.asset_type || ""})`],
    ["Timestamp (UTC)", p.timestamp_utc || ""],
  ]);

  const metrics = report.metrics || {};
  renderKPIs(kpisEl, metrics);

  const metricRows = Object.entries(metrics).map(([k, v]) => ({
    metric: k,
    value: v?.value === undefined ? "" : fmt(v.value),
    notes: v?.notes || ""
  }));
  renderTable(metricsEl, ["metric", "value", "notes"], metricRows);

  const pluginRows = (report.plugin_results || []).map(pr => ({
    plugin: pr.name,
    ok: pr.ok ? "true" : "false",
    metadata: JSON.stringify(pr.metadata || {})
  }));
  renderTable(pluginsEl, ["plugin", "ok", "metadata"], pluginRows);

  const events = p.events || [];
  const eventRows = events.map(e => ({
    type: e.type, severity: e.severity, message: e.message, source: e.source
  }));
  if (eventRows.length) renderTable(eventsEl, ["type","severity","message","source"], eventRows);
  else eventsEl.innerHTML = "<div class='muted'>No events in payload.</div>";

  plotGauges(metrics);
}

document.getElementById("reloadBtn").addEventListener("click", () => main().catch(err => alert(err)));
main().catch(err => alert(err));
