// ArtistListenersChart.vue
<template>
  <div>
    <h1>Artist Listeners Over Time</h1>
    <input type="file" @change="handleFileUpload" accept=".csv">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';

export default {
  setup() {
    const chartCanvas = ref(null);
    let chart = null;

    const handleFileUpload = (event) => {
      const file = event.target.files[0];
      const reader = new FileReader();

      reader.onload = (e) => {
        const csv = e.target.result;
        const data = parseCSV(csv);
        updateChart(data);
      };

      reader.readAsText(file);
    };

    const parseCSV = (csv) => {
      const lines = csv.split('\n');
      const headers = lines[0].split(',');
      const dates = [];
      const datasets = {};

      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        if (values.length === headers.length) {
          dates.push(values[0]);
          for (let j = 1; j < headers.length; j++) {
            if (!datasets[headers[j]]) {
              datasets[headers[j]] = [];
            }
            datasets[headers[j]].push(parseInt(values[j]));
          }
        }
      }

      return { dates, datasets };
    };

    const updateChart = (data) => {
      if (chart) {
        chart.destroy();
      }

      const datasets = Object.keys(data.datasets).map(artist => ({
        label: artist,
        data: data.datasets[artist],
        borderColor: getRandomColor(),
        fill: false
      }));

      chart = new Chart(chartCanvas.value, {
        type: 'line',
        data: {
          labels: data.dates,
          datasets: datasets
        },
        options: {
          responsive: true,
          title: {
            display: true,
            text: 'Artist Listeners Over Time'
          }
        }
      });
    };

    const getRandomColor = () => {
      return '#' + Math.floor(Math.random()*16777215).toString(16);
    };

    onMounted(() => {
      // Chart initialization can be done here if needed
    });

    return {
      chartCanvas,
      handleFileUpload
    };
  }
}
</script>