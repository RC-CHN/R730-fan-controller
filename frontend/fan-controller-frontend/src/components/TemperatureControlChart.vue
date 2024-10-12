<template>
    <div ref="chartContainer" class="chart-container"></div>
</template>

<script setup>
import * as echarts from 'echarts';
import { ref, onMounted, watch, nextTick } from 'vue';

const props = defineProps({
    curveData: Array,
});

const emit = defineEmits(['update-curve']);
const chartContainer = ref(null);
let chartInstance = null;
let data = []; // 用于存储数据点坐标

// 初始化图表
const initializeChart = () => {
    if (chartInstance) chartInstance.dispose();
    chartInstance = echarts.init(chartContainer.value);

    data = props.curveData.map(item => [item.temp, item.speed]);

    const option = {
        xAxis: {
            type: 'value',
            name: '温度',
            min: 0,
            max: 100,
        },
        yAxis: {
            type: 'value',
            name: '风扇速度',
            min: 0,
            max: 100,
        },
        series: [
            {
                type: 'line',
                data: data,
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 2,
                },
            },
        ],
    };

    chartInstance.setOption(option);

    // 添加可拖动的圆点
    addDraggablePoints();

    // 添加图表缩放和拖拽事件的监听，以保持 graphic 元素与图表同步
    chartInstance.on('dataZoom', updatePosition);
    chartInstance.on('move', updatePosition);

    // 当窗口大小变化时，重新渲染图表
    window.addEventListener('resize', () => {
        chartInstance.resize();
        updatePosition();
    });
};

// 添加可拖动的圆点
const addDraggablePoints = () => {
    chartInstance.setOption({
        graphic: data.map((item, index) => ({
            type: 'circle',
            position: chartInstance.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, item),
            shape: {
                r: 8,
            },
            invisible: false,
            draggable: true,
            z: 100,
            // 拖动事件
            ondrag: function (event) {
                const pos = chartInstance.convertFromPixel({ xAxisIndex: 0, yAxisIndex: 0 }, this.position);

                // 限制坐标范围
                let x = Math.max(0, Math.min(100, pos[0]));
                let y = Math.max(0, Math.min(100, pos[1]));

                // 坐标限制：确保 x 和 y 不超过相邻点
                if (index > 0) {
                    x = Math.max(data[index - 1][0] + 0.1, x); // +0.1 防止重合
                    y = Math.max(data[index - 1][1] + 0.1, y);
                }
                if (index < data.length - 1) {
                    x = Math.min(data[index + 1][0] - 0.1, x);
                    y = Math.min(data[index + 1][1] - 0.1, y);
                }

                // 更新数据点
                data[index] = [x, y];
                updateChart();
            },
            onmousemove: function () {
                chartInstance.getZr().setCursorStyle('pointer');
            },
            onmouseout: function () {
                chartInstance.getZr().setCursorStyle('default');
            },
            style: {
                fill: '#007BFF',
                stroke: '#FFFFFF',
                lineWidth: 2,
            },
        })),
    });
};

// 更新图表数据和可拖动点的位置
// const updateChart = () => {
//     chartInstance.setOption({
//         series: [
//             {
//                 data: data,
//             },
//         ],
//     });
//     updatePosition();
//     // 触发更新事件
//     const updatedData = data.map(([temp, speed]) => ({ temp, speed }));
//     emit('update-curve', updatedData);
// };
const updateChart = () => {
    chartInstance.setOption({
        series: [
            {
                data: data,
            },
        ],
    });
    updatePosition();
    // 触发更新事件
    const updatedData = data.map(([temp, speed]) => ({
        temp: Math.round(temp),
        speed: Math.round(speed),
    }));
    emit('update-curve', updatedData);
};
// 更新可拖动点的位置
const updatePosition = () => {
    chartInstance.setOption({
        graphic: data.map((item) => ({
            position: chartInstance.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, item),
        })),
    });
};

onMounted(() => {
    initializeChart();
});

// 监听 curveData 的变化，重新渲染图表
watch(
    () => props.curveData,
    async (newVal) => {
        data = newVal.map(item => [item.temp, item.speed]);
        if (chartInstance) {
            chartInstance.setOption({
                series: [
                    {
                        data: data,
                    },
                ],
            });
            // 需要等待下一次 DOM 更新后再更新 draggable points
            await nextTick();
            addDraggablePoints();
        } else {
            initializeChart();
        }
    }
);
</script>

<style scoped>
.chart-container {
    width: 100%;
    height: 400px;
    margin-right: 30px;
}
</style>