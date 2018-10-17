---
title: javascript
date: 2018-09-16 13:06:27
tags:
---
记录在查阅Cesium源码时的一些体会
<!--more-->
# javascript
## 基础
记录之前没有注意到的js用法
### `Object`
#### `Object.freeze`
#### [`Object.defineProperties`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperties)
```
var obj = {};
Object.defineProperties(obj, {
  'property1': {
    value: true,
    writable: true
  },
  'property2': {
    value: 'Hello',
    writable: false
  }
  // etc. etc.
});
```
### `function`
#### [`function.apply`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Function/apply)
调用一个函数
`func.apply(thisArg, [argsArray])`
#### [`function.call`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Function/call)
调用一个函数 
`fun.call(thisArg, arg1, arg2, ...)`
#### [`arguments`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Functions/arguments)
调用function的参数数组

### 

## 结构
### 工具类的取消
不同性质的工具单独成为模块，同性质的工具归为一类，没有大概念的的工具类
### 老浏览器的适配
用一个模块包装，如果不存在调用的方法，就手动实现，获取返回原函数防报错。
```javascript
//某个模块
    var defineProperties = Object.defineProperties;
    if (!definePropertyWorks || !defined(defineProperties)) {
        defineProperties = function(o) {
            return o;
        };
    }

    return defineProperties;
```

# 使用gulp合并js
注意直接下载gulp各依赖，babel的依赖会有问题（目前7.0.0尚未发布）
## 步骤
[npm仓库](https://www.npmjs.com/package/gulp-babel) 
```shell
yarn add --dev gulp-babel@7 babel-core babel-preset-env gulp
```
### 弃坑
看了cesium的打包方式，有点复杂。。。遂弃坑

# 使用webpack合并js
回到webpack

## 打包思路
1. 原理都类似，利用index.js来组织内部模块并对外输出,这个index.js可以手写，也可以程序字符串拼接（Cesium是这样生成的）
2. 另外Cesium.js不应该打包进来，应从外部引入
3. 公共资源copy到输出文件夹

## 配置
[思路](https://leamtrop.com/2017/06/03/build-a-library-with-webpack/)
核心思路从这篇文章开始，他最后输出的东西正是和Cesiumjs官方库一样的东西

需要注意一些版本的问题，以及在webpack4下，有一些以前的库是不能用的（说的就是你 `ExtractTextWebpackPlugin`), 可以去webpack官网找到对应的插件，底下会有更换提示。

### 打包
这次先写demo测试打包结果能否使用
#### js
打包js问题不大，需要注意的是[引用外部库](https://www.zhihu.com/question/33448231), 此外我们可以使用es6的方式组织模块，最后由babel编译成es2015。
#### css
打包卡住的问题，后翻阅官方文档时发现`ExtractTextWebpackPlugin`在只支持到webpack2，之后的需要用`mini-css-extract-plugin`代替。
### 开发
之前也是卡在开发这里。开发要求能够快速精准的debug，以及打包快速构建，所以有两个问题
#### 源码调试
打包需要打出source map,webpack的devtool就提供了多种源码格式，配置写上，打包就会出源码。

`source-map`是首先选择的，但在断点调试时会出现，断点没走到，但是程序已经运行的情况，经过多次调试，`eval-source-map`符合需求

#### 打压缩包
这里就出现了webpack怎么多种打包方式的问题，选择是写两份配置文件，然后通过`--config`参数来指定不同的配置文件

js选择`UglifyjsWebpackPlugin` ,css `mini-css-extract-plugin`，输出文件加个min，取消源码输出，就好了。

#### 开发构建
随后又出现问题，有时修改了代码，但是忘记build了。此时需要webpack的 --watch参数，保存即build。

热更新由于没什么必要，就没有深究。

贴出[个人开发配置](https://github.com/zxy16305/Cesiums/blob/master/webpack.dev.config.js)

[个人部署配置](https://github.com/zxy16305/Cesiums/blob/master/webpack.config.js)

## 坑






