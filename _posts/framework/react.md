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
### create-react-app 中使用less/sass
> [create-react-app如何使用less/sass和react-css-modules?](https://github.com/FrankKai/FrankKai.github.io/issues/61)

总结而言就是使用 less-watch-compiler 和 node-sass-chokidar，那我甚至可以idea的file watcher

注意在 windows下，应使用 `\\`作为文件分隔符,否则会造成目录输出错误,例如
```batch
less-watch-compiler --run-once  src\\style\\less src\\style\\css
```
## UI库 - ant designer
### 不支持 create-react-app 2.x的情况
TODO
## UI库 - 飞冰

## FAQ
### 构建篇
#### `npm run build`后 打包项目默认使用的是绝对路径怎么办
在package.json里加 `"homepage":"."`即可