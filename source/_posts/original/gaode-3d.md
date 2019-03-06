---
title: 记录高德使用3d api
date: 2019-01-27 23:36:27
tags:
categories:
-   original
---

高德地图3d目前处于比较原始的阶段，有幸接触到底层3d的绘制
<!--more-->

# api
## AMap.Object3D.Mesh
描述一个三维Mesh对象，基本无抽象，使用顶点位置和定点颜色描述geometry，同时支持纹理。

# 底层
Web端的3d基本基于WebGl，也有少部分用canvas计算实现的（性能低），而WebGl又基于OpenGl ES，基本学习了OpenGl，就对底层的绘制有了了解。

简单应用中，任意的3d对象都可以使用三角形进行拼接，因此 `Mesh` 基本可以实现所有想要的模型。

三角形描述时有几点讲究
1. 绕法

绕法涉及到 `背面剔除`，是优化渲染的一种方式。OpenGl中使用顶点绕序（winding order），来确定哪个面是背面。
2. 顶点重用

举个例子，理论上拼接一个n个三角形的三角条，只需要n+2个顶点即可。过多顶点会导致渲染过慢。
> https://blog.csdn.net/chenxiqilin/article/details/52145158

以下为一个横向扫描效果的例子~~（凑篇幅）~~
```javascript
this.drawRangeScanV2 = function (map, precision) {
                if (!precision) precision = 50;

                function buildRange(width, height) {
                    function getOpacity(scale) {
                        // return Math.pow(scale, 0.3);
                        // y = x ^ 0.3 的反函数
                        return Math.exp(1 / 0.3 * Math.log(scale));
                    }

                    var rect = new AMap.Object3D.Mesh();
                    rect.transparent = true;
                    rect.backOrFront = 'front';

                    var geometry = rect.geometry;
                    var unit = width / precision;

                    geometry.vertices.push(0 - width / 2, height/2, 0);
                    geometry.vertices.push(unit - width / 2, -height/2, 0);

                    geometry.vertexColors.push(0, 1, 0.2, 0);
                    geometry.vertexColors.push(0, 1, 0.2, 0);

                    for (var i = 0; i < precision; i++) {
                        var y3 = 0
                        if (i % 2 === 0) {
                            y3 = height/2
                            geometry.faces.push(i, i + 1, i + 2)

                        } else {
                            y3 = -height/2
                            geometry.faces.push(i + 1, i, i + 2)
                        }
                        geometry.vertices.push((i + 2) * unit - width / 2, y3, 0);

                        geometry.vertexColors.push(0, 1, 0.2, getOpacity(i / precision));
                    }
                    return rect
                }

                var rect = buildRange(1500, 1900);
                rect.position(map.getCenter());

                var object3Dlayer = new AMap.Object3DLayer();
                map.add(object3Dlayer);

                object3Dlayer.add(rect);
                var orignalArray = rect.geometry.vertices.slice(0);
                var originalColorsArray = rect.geometry.vertexColors.slice(0);
                var cancelFlag = window.requestAnimationFrame(scan);
                function scan() {
                    var temp = rect;

                    var number = (new Date().getTime() % 3000);

                    for (var i = 0; i < precision +2 ; i++) {
                        temp.geometry.vertices[3 * i] = orignalArray[i * 3] + toothFuntion(number, 4000, 3000)


                        if (temp.geometry.vertices[3 * i] < -1500 || temp.geometry.vertices[3 * i] > 1600) {
                            // console.log(rect.geometry.vertices[3 * i]);
                            temp.geometry.vertexColors[4 * i + 3] = 0;
                        } else {
                            temp.geometry.vertexColors[4 * i + 3] = originalColorsArray[4 * i + 3];
                        }
                    }
                    temp.needUpdate = true;
                    temp.reDraw();
                    temp = null;

                    // return AMap.Util.requestAnimFrame(scan);
                    cancelFlag = window.requestAnimationFrame(scan);
                }
                function toothFuntion(x, A, T) {
                    return A / T * (x % T) - A / 2 - A / 10;
                }

                var  isScanStop = false;

                return {
                    pauseScan: function () {
                        cancelFlag && window.cancelAnimationFrame(cancelFlag);
                    },
                    continueScan: function () {
                        cancelFlag = window.requestAnimationFrame(scan);
                    },
                    destroy: function () {
                        isScanStop = true;
                        buildRange = null;

                        // AMap.Util.cancelAnimFrame(cancelId);
                        // scan = null;
                        cancelFlag && window.cancelAnimationFrame(cancelFlag);
                        orignalArray = null;
                        originalColorsArray = null;

                        object3Dlayer && object3Dlayer.remove(rect)
                        object3Dlayer && object3Dlayer.clear()
                        object3Dlayer && map && map.remove(object3Dlayer)
                        object3Dlayer = null;
                        rect = null;
                    }
                }
            }
```
