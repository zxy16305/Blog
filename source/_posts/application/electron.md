---
title: electron地图下载器
date: 2019-9-27 17:06:27
tags: map
categories:
-   application
---

涉及到
- nodejs
- electron
- nsis
- openlayer(或其他任意一种可自定义底图的工具)
- google map styleJson编码
- 瓦片坐标系和经纬度坐标系的转换
- 并发下载

<!--more-->

## nodejs

## electron
### react+electron
> [how-to-build-an-electron-app-using-create-react-app-and-electron-builder](https://www.codementor.io/randyfindley/how-to-build-an-electron-app-using-create-react-app-and-electron-builder-ss1k0sfer)

## openlayer
> 

## map styleJson编码
> [customizing-google-map-tile-server-url](https://stackoverflow.com/questions/29692737/customizing-google-map-tile-server-url)

## 瓦片坐标系转换
> [参考代码](https://github.com/CntChen/tile-lnglat-transform/blob/master/src/transform-class-slippy.js)

> [参考资料](http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames)

## 并发下载
> [流式下载](https://stackoverflow.com/a/57793181)

> [request模块使用](https://segmentfault.com/a/1190000000385867)

> [events模块](https://www.jianshu.com/p/79cdebed6ee5)

## 其他
### Chromium并发请求上限
虽然Chromium是写死的，但是electron使用的是修改过后的定制化的Chromium，通过添加 `ignore-connections-limit` flag取消并发上限
```javascript
app.commandLine.appendSwitch('ignore-connections-limit', 'www.google.cn/maps,www.google.cn,google.cn')
```
### 打包
由于electron-builder打包时报错，不能解析dependencies里的模块，所以打包时把这里删了就好了（认真）

