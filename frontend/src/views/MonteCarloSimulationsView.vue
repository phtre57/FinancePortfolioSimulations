<template>
  <div>
    <el-form>
      <el-form-item label="Asset">
        <el-col :span="10">
            <el-input type="text" id="ticker" v-model="newTicker" placeholder="Enter ticker symbol" required />
        </el-col>

        <el-col :span="2" class="centered">
          <span class="text-gray-500">-</span>
        </el-col>

        <el-col :span="10">
          <el-input type="number" id="weight" v-model="newWeight" placeholder="Enter weight" required />
        </el-col>

        <el-col :span="2" class="left">
          <el-button type="primary" @click="addTicker">
            <el-icon><Plus /></el-icon>
          </el-button>
        </el-col>
      </el-form-item>
    </el-form>

    <el-space alignment="start" size="large" direction="vertical" v-if="tickers.length > 0">
      <div v-for="(ticker, index) in tickers" :key="index">
        <el-space size="large" direction="horizontal">
          <span>{{ ticker.symbol }} ({{ ticker.weight }})</span>
          <el-button type="danger" size="small" circle @click="removeTicker(index)">
          <el-icon><Delete /></el-icon>
        </el-button>
        </el-space>
      </div>

      <el-button :disabled="loading" type="primary" @click="fetchData">
        Simulate
        <el-icon class="el-icon--right"><DataLine /></el-icon>
        <el-icon v-if="loading" class="el-icon--right"><Loading /></el-icon>
      </el-button>
    </el-space>
  </div>

  <div class="chart-container">
    <canvas id="myChart"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

const url = 'http://127.0.0.1:8000/portfolios/monte-carlo-sims'

export default {
  data() {
    return {
      loading: false,
      simulations: null,
      numberOfSimulations: 0,
      numberOfDays: 0,
      VaR: null,
      lines: [],
      chart: null,
      newTicker: '',
      newWeight: '',
      tickers: [],
    };
  },
  methods: {
    addTicker() {
      this.tickers.push({
        symbol: this.newTicker.toUpperCase(),
        weight: this.newWeight,
      });
      this.newTicker = '';
      this.newWeight = '';
    },
    removeTicker(index) {
      this.tickers.splice(index, 1);
    },
    async fetchData() {
      try {
        const request = {
          stocks: this.tickers.map((ticker) => ticker.symbol),
          weights: this.tickers.map((ticker) => ticker.weight),
          initial_value: 10000,
        }
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
        this.lines = [data.VaR]
        this.VaR = data.VaR;
        this.numberOfSimulations = data.number_of_simulations;
        this.numberOfDays = data.number_of_days;
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
      const simulationsDataSets = this.simulations.map((simulation, index) => ({
        label: `Simulation ${index + 1}`,
        data: simulation,
        backgroundColor: 'rgba(' + this.getRandomColor() + ', 0.2)',
        borderColor: 'rgba(' + this.getRandomColor() + ', 1)',
      }))
      // const VarDatasets = [{
      //   label: 'VaR',
      //   data: new Array(this.numberOfDays).fill(this.VaR),
      //   borderColor: 'red',
      //   backgroundColor: 'red',
      //   pointRadius: 0,
      //   lineTension: 0,
      //   width: '10px',
      //   z: 10000,
      // }];
      // const datasets = this.lines.map((VaR) => ({
      //   label: 'VaR',
      //   data: new Array(this.numberOfDays).fill(VaR),
      //   borderColor: 'red',
      //   backgroundColor: 'red',
      //   pointRadius: 0,
      //   lineTension: 0,
      //   width: '10px',
      //   z: 10000,
      // }))
      this.chart = new Chart(ctx, {
        type: 'line', // Change chart type if needed
        data: {
          labels: [...Array(this.numberOfDays).keys()], // Generate labels
          datasets: simulationsDataSets
          // datasets: VarDatasets.concat(simulationsDataSets),
          // datasets: VarDatasets,
          // datasets: datasets
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

.centered {
  display: flex;
  justify-content: center;
}

.left {
  display: flex;
  justify-content: end;
}

.chart-container {
  margin-top: 4rem;
  position: relative;
  width: 100%;
}

</style>