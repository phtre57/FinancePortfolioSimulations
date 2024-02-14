<template>
  <div class="simulation-inputs">
    <el-button :disabled="loading" type="primary" @click="fetchData">
      Simulate
      <el-icon class="el-icon--right"><DataLine /></el-icon>
      <el-icon v-if="loading" class="el-icon--right"><Loading /></el-icon>
    </el-button>
  </div>
  <div>
    <canvas id="myChart"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

const url = 'http://127.0.0.1:8000/portfolios/monte-carlo-sims'
const request = {
  "stocks": ["AAPL", "GOOG", "TSLA"],
  "weights": [0.3, 0.4, 0.3],
  "initial_value": 10000
}

export default {
  data() {
    return {
      loading: false,
      simulations: null,
      chart: null,
    };
  },
  methods: {
    async fetchData() {
      try {
        this.loading = true
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(request),
        });
        const data = await response.json();
        this.simulations = data.simulations;
        this.destroyChart()
        this.createChart();
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        this.loading = false
      }
    },
    destroyChart() {
      if (this.chart) {
        this.chart.destroy();
        this.chart = null;
      }
    },
    createChart() {
      const ctx = document.getElementById('myChart').getContext('2d');
      this.chart = new Chart(ctx, {
        type: 'line', // Change chart type if needed
        data: {
          labels: [...Array(this.simulations[0].length).keys()], // Generate labels
          datasets: this.simulations.map((simulation, index) => ({
            label: `Simulation ${index + 1}`,
            data: simulation,
            backgroundColor: 'rgba(' + this.getRandomColor() + ', 0.2)',
            borderColor: 'rgba(' + this.getRandomColor() + ', 1)',
          })),
        },
        options: {
          plugins: {
            legend: {
                display: false,
            }
          }
        },
      });
    },
    getRandomColor() {
      // Generate random color for each line
      return Math.floor(Math.random() * 255) + ',' + Math.floor(Math.random() * 255) + ',' + Math.floor(Math.random() * 255);
    },
  },
  beforeUnmount() {
    this.destroyChart();
  },
};
</script>

<style scoped>

.simulation-inputs {
  padding-bottom: 4rem;
  display: flex;
  justify-content: flex-end;
}
</style>