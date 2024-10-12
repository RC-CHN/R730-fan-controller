<template>
    <div ref="chartContainer" class="chart-container"></div>
  </template>
  
  <script setup>
  import * as echarts from 'echarts';
  import { ref, onMounted, watch } from 'vue';
  
  const props = defineProps({
    data: Array
  });
  
  const chartContainer = ref(null);
  let chartInstance = null;
  
  // 初始化图表
  const initializeChart = () => {
    if (chartInstance) chartInstance.dispose();
    chartInstance = echarts.init(chartContainer.value);
  
    const option = {
      xAxis: {
        type: 'category',
        data: props.data.map(item => item.time),
        name: '时间'
      },
      yAxis: {
        type: 'value',
        name: '温度 (°C)'
      },
      series: [
        {
          type: 'line',
          data: props.data.map(item => item.temperature),
          smooth: true,
          symbol: 'none'
        }
      ]
    };
  
    chartInstance.setOption(option);
  };
  
  onMounted(() => {
    initializeChart();
  });
  
  watch(() => props.data, initializeChart);
  </script>
  
  <style scoped>
  .chart-container {
    width: 100%;
    height: 400px;
  }
  </style>
  