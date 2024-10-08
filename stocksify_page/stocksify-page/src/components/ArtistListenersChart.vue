// ArtistListenersChart.vue
<template>
  <div class="chart-container">
    <h1>Artist Listeners Over Time</h1>
    <input type="file" @change="handleFileUpload" accept=".csv">
    <div class="chart-wrapper">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
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
          maintainAspectRatio: false,
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
      window.addEventListener('resize', handleResize);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize);
      if (chart) {
        chart.destroy();
      }
    });

    const handleResize = () => {
      if (chart) {
        chart.resize();
      }
    };

    return {
      chartCanvas,
      handleFileUpload
    };
  }
}
</script>

<style scoped>
.chart-container {
  width: 160vh;
  height: 80vh;
  display: flex;
  flex-direction: column;
}

.chart-wrapper {
  flex-grow: 1;
  position: relative;
}

canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100% !important;
  height: 100% !important;
}
</style>