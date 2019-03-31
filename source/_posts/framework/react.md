---
title: react
date: 2018-10-04 07:57:47
tags: 学习 记录
categories:
-   framework
---

学一下 demo写一年

<!--more-->

## 基本概念
### component
### props
### state

## 脚手架使用
### create react app
在目录下使用 `npx create-react-app my-app`,创建名为 my-app 的项目

但是在隐藏了webpack的依赖后，使用起来不是很方便。这里通过 [craco](https://github.com/sharegate/craco) 来完成对webpack配置的覆写
> [react-app-rewired](https://github.com/timarney/react-app-rewired) 只支持到create-react-app 1.x
### create-react-app + craco
craco对create-react-app 的默认webpack配置完成复写
#### craco's plugin
+ CracoLessPlugin：开启webpack对less的编译
+ CracoAntDesignPlugin：引入less以及antd的css
+ CracoCesiumPlugin：引入cesium库材质及css
#### craco's babel config
主要是 `@babel/plugin-proposal-optional-chaining`，之后只要修改一下默认的eslint配置，不然无法使用 `function's optional`
#### craco's eslint config
引入eslint插件 [eslint-plugin-babel](https://github.com/babel/eslint-plugin-babel)，在eslint配置处关闭默认的rules，然后启动对应的定制化的rules

在这里的作用就是使eslint忽略部分无法识别的语法（如 `@babel/plugin-proposal-optional-chaining` 在function的情况）
## UI库 - ant designer
### 不支持 create-react-app 2.x的情况
TODO
## UI库 - 飞冰

## FAQ
### 构建篇
#### `npm run build`后 打包项目默认使用的是绝对路径怎么办
在package.json里加 `"homepage":"."`即可