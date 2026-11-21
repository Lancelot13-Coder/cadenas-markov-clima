(() => {
  const dataElement = document.getElementById("distribution-chart-data");
  const canvas = document.getElementById("distribution-chart");
  if (!dataElement || !canvas || typeof Chart === "undefined") return;

  const chartData = JSON.parse(dataElement.textContent);
  const colors = ["#176b66", "#b47519", "#4564a1"];
  const datasets = chartData.datasets.map((dataset, index) => ({
    ...dataset,
    borderColor: colors[index],
    backgroundColor: colors[index],
    borderWidth: 3,
    pointRadius: 4,
    tension: 0.2,
  }));

  new Chart(canvas, {
    type: "line",
    data: { labels: chartData.labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      scales: {
        y: { min: 0, max: 1, title: { display: true, text: "Probabilidad" } },
        x: { title: { display: true, text: "Pasos" } },
      },
      plugins: { legend: { position: "bottom" } },
    },
  });
})();
