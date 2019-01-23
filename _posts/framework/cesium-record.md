---
title: cesium注意事项
date: 2019-01-23 22:18:46
categories:
-   framework
---
近期项目需要，多次对其调优。记录，警示。

<!--more-->
# 怎么搜索问题(指一些bug，使用方法直接走官方教程和api文档以及公司大佬)
1. [github](https://github.com/AnalyticalGraphicsInc/cesium) issue中搜索关键字
2. [官方社区](https://groups.google.com/forum/#!forum/cesium-dev)
3. google搜索关键字
4. google搜索webgl关键字

# 通用
## drillPick后pickPosition获取不到模型上点位的问题
调用 `scene.render()`解决，[参考](https://github.com/AnalyticalGraphicsInc/cesium/issues/5622)
```javascript
scene.drillPick(position)
scene.render();
var positionReturn = scene.pickPosition(position);
```
# IE11
ie可是个噩梦
## 打开直接报错
注意IE11的版本，早期IE11没有完全支持WebGl（现在也没有..)

可以先写个最简单的demo（tileset + camera flyTo），看看是否还会报错，报错就升级IE；没报错再从代码找原因
## UrlTemplateImageryProvider在gis返回空图片时内存泄露
直到1.53版本依然没有修复

通过重建demo复现法得到，源码未看。解决方案是使用google在线地图，或者gisServer做出相应的默认图片处理。

`http://www.google.cn/maps/vt?lyrs=s&gl=cn&x={x}&y={y}&z={z}`

添加`gl=cn`得到国区为火星坐标系的底图

## 内存占用过高
ie内存占用达到一定大小就会崩溃

内存占用一般是tileset导致的，限制其最大的缓存可以缓解，注意缓存仍然可突破这个大小，当画面内tile大小超过缓存大小时，仍会加载；移出画面，就会被释放到最大缓存。
```javascript
var tileset = new Cesium.Cesium3DTileset({
    url: '/zhxq-tiles/tileset.json',
    maximumMemoryUsage: 200,
});
```

## 不流畅
既然你不流畅，干脆直接把帧率调低点好了...
```javascript
var map = new Cesium.Viewer('common-gis-map', {
    //...
    targetFrameRate: 48
});
```

# 持续更新...
