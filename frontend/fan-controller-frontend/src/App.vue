<template>
  <div class="container">
    <!-- 模式切换 -->
    <div class="mode-switch">
      <el-switch v-model="isFixedMode" active-text="固定模式" inactive-text="动态模式" @change="handleModeChange"></el-switch>
    </div>

    <!-- 功能区域 -->
    <div class="main-content">
      <!-- 温控区 -->
      <div class="control-area">
        <!-- 上块：标题 -->
        <div class="section-title">
          <h3>温控设置</h3>
        </div>
        <!-- 下块：内容，横向排列 -->
        <div class="section-content">
          <template v-if="!isFixedMode">

            <!-- 温控曲线设置折线图 -->
            <div class="chart-section">
              <temperature-control-chart :curve-data="fanCurve" @update-curve="updateFanCurve" />
            </div>
            <!-- 节点数目滑块，上下排列 -->
            <div class="node-count-slider">
              <p>设置曲线节点数目：{{ nodeCount }}</p>
              <el-slider v-model="nodeCount" :min="2" :max="9" vertical height="200px" @change="updateNodeCount" />
              <el-button type="primary" class="confirm-button" @click="confirmCurveSettings">
                确认曲线设置
              </el-button>
            </div>
          </template>
          <template v-else>
            <!-- 固定转速滑块，横向排列 -->
            <div class="fixed-speed-section">
              <div class="speed-slider">
                <h3>手动设置固定风扇转速</h3>
                <el-slider v-model="fixedSpeed" :min="0" :max="100" @change="updateFanSpeed" />
                <p>当前风扇速度：{{ fixedSpeed }}%</p>
              </div>
              <el-button type="primary" class="confirm-button" @click="confirmFixedSpeedSettings">
                确认定速设置
              </el-button>
            </div>
          </template>
        </div>
      </div>

      <!-- 历史数据展示区 -->
      <div class="history-area">
        <!-- 上块：标题 -->
        <div class="section-title">
          <h3>历史温度数据</h3>
        </div>
        <!-- 下块：内容，横向排列 -->
        <div class="section-content">
          <temperature-history-chart :data="temperatureHistory" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { ElSwitch, ElSlider, ElButton } from 'element-plus';
import TemperatureControlChart from './components/TemperatureControlChart.vue';
import TemperatureHistoryChart from './components/TemperatureHistoryChart.vue';

const isFixedMode = ref(false);
const fixedSpeed = ref(50);
const nodeCount = ref(4); // 默认节点数目

// 根据节点数目初始化风扇曲线数据
const initializeFanCurve = (count) => {
  const temps = [];
  const speeds = [];
  const step = 100 / (count - 1);
  for (let i = 0; i < count; i++) {
    temps.push(i * step);
    speeds.push(i * step);
  }
  return temps.map((temp, index) => ({ temp, speed: speeds[index] }));
};

const fanCurve = ref(initializeFanCurve(nodeCount.value));

// 模拟的历史温度数据
const temperatureHistory = ref([
  { time: '10:00', temperature: 22 },
  { time: '10:05', temperature: 25 },
  { time: '10:10', temperature: 28 },
  { time: '10:15', temperature: 30 },
  { time: '10:20', temperature: 27 },
  { time: '10:25', temperature: 26 },
]);

// 更新风扇曲线
const updateFanCurve = (newCurve) => {
  fanCurve.value = newCurve;
  console.log('Updated fan curve:', fanCurve.value);
};

// 更新固定转速
const updateFanSpeed = (speed) => {
  console.log('Updated fixed speed to:', speed);
};

// 确认曲线设置
const confirmCurveSettings = () => {
  console.log('Confirmed curve settings:', fanCurve.value);
};

// 确认定速设置
const confirmFixedSpeedSettings = () => {
  console.log('Confirmed fixed speed:', fixedSpeed.value);
};

// 处理模式切换
const handleModeChange = (newMode) => {
  console.log('Switched to', newMode ? 'fixed' : 'dynamic', 'mode');
};

// 更新节点数目
const updateNodeCount = (count) => {
  nodeCount.value = count;
  fanCurve.value = initializeFanCurve(count);
};
</script>

<style scoped>
/* 容器样式 */
.container {
  display: flex;
  flex-direction: column;
  height: 90vh;
  width: 90vw;
  background-color: #2c2c2c;
  color: #ffffff;
  border-radius: 10px;
  /* 添加圆角 */
  overflow: hidden;
  margin: auto;
  /* 居中显示 */
}

/* 模式切换区域 */
.mode-switch {
  padding: 10px;
  background-color: #1f1f1f;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

/* 主内容区域 */
.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 温控区样式 */
.control-area {
  flex: 2;
  display: flex;
  flex-direction: column;
  background-color: #333333;
  box-shadow: inset -1px 0 0 #444;
  max-width: 60%;
  min-width: 40%;
  /* 添加最小宽度 */
  box-sizing: border-box;
  border-radius: 10px;
  /* 添加圆角 */
  margin: 10px;
  /* 添加外边距 */
}

/* 上块：标题 */
.control-area .section-title {
  padding: 10px;
  background-color: #444;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

/* 下块：内容，横向排列 */
.control-area .section-content {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 10px;
  margin: 30px;
  overflow: hidden;
}

/* 节点数滑块 */
.node-count-slider {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 150px;
  margin-right: 20px;
}

/* 确认按钮 */
.confirm-button {
  margin-top: 10px;
}

/* 温控曲线图 */
.chart-section {
  flex: 1;
  max-height: 400px;
  overflow: hidden;
}

/* 固定转速滑块，横向排列 */
.fixed-speed-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

/* 速度滑块部分 */
.speed-slider {
  flex: 1;
  margin-right: 20px;
}

/* 历史数据展示区样式 */
.history-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #3a3a3a;
  box-shadow: inset 1px 0 0 #444;
  overflow-y: auto;
  border-radius: 10px;
  /* 添加圆角 */
  margin: 10px;
  /* 添加外边距 */
  box-sizing: border-box;
}

/* 上块：标题 */
.history-area .section-title {
  padding: 10px;
  background-color: #444;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

/* 下块：内容，横向排列 */
.history-area .section-content {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 10px;
  overflow: hidden;
}

/* 添加动画效果 */
.control-area,
.history-area {
  transition: all 0.3s ease;
}

/* 边框阴影 */
.control-area {
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.5);
}

.history-area {
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.5);
}

/* 为所有容器添加圆角 */
.mode-switch,
.main-content {
  border-radius: 10px;
}

/* 滑块样式 */
.el-slider {
  margin-top: 10px;
}
</style>
