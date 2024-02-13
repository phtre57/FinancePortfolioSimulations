<template>
  <div class="simulation-inputs">
    <el-button type="primary" @click="fetchData">
      Simulate <el-icon class="el-icon--right"><Coin /></el-icon>
    </el-button>
  </div>
  <div>
    <canvas id="myChart"></canvas>
  </div>
</template>

<script>
import { Coin } from '@element-plus/icons-vue'
import Chart from 'chart.js/auto';

const url = 'http://127.0.0.1:8000/portfolios/monte-carlo-sims?stocks=AAPL&stocks=GOOG&stocks=TSLA&weights=0.3&weights=0.4&weights=0.3&initial_value=10000'

export default {
  data() {
    return {
      simulations: null,
      chart: null,
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch(url);
        const data = await response.json();
        console.log(data)
        this.simulations = data.simulations;
        this.createChart();
      } catch (error) {
        console.error('Error fetching data:', error);
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
};
</script>

<style scoped>
.simulation-inputs {
  padding-bottom: 4rem;
}
</style>