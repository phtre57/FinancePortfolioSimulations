<template>
  <div>
    <button @click="fetchData">Click to fetch data</button>
    <div v-if="data">{{ data }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      data: null,
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch('http://127.0.0.1:8000/portfolios/monte-carlo-sims?stocks=AAPL&stocks=GOOG&stocks=TSLA&weights=0.3&weights=0.4&weights=0.3&initial_value=10000');
        const data = await response.json();
        this.data = data;
        console.log(data); // Log data to console
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
  },
};
</script>
