---
title: 记一次对cesium的拓展
date: 2018-08-28 22:18:46
tags: 天下代码一大抄
---

对cesium绘画拓展的再次拓展

<!-- more -->

# 资料记录

1. [官方基础教程](https://cesiumjs.org/tutorials/Cesium-Workshop/)
1. [官方API文档](https://cesiumjs.org/Cesium/Build/Documentation/Cartesian3.html)
0. [官方demo-绘制](https://cesiumjs.org/Cesium/Build/Apps/Sandcastle/index.html?src=Drawing%20on%20Terrain.html)
1. [cesium中的坐标转换](https://blog.csdn.net/qq_34149805/article/details/78393540)
2. [SashT/cesium-drawhelper](https://github.com/SashT/cesium-drawhelper)
3. [调整后的drawHelper](https://github.com/K-UTIL/cesium-drawhelper)

# 问题

## 高程点位圈选精度很低，地面点位没有这个问题

### 验证思路：
获取转换后的xyz坐标，再转换回去和原来的经纬度进行比较 :dog: