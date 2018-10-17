---
title: scss
date: 2018-09-21 22:26:30
tags:
---

出于需要用css来绘制带角的对话框，如果用纯css来写，重复量太多，维护性较低。
印象中less、scss都可以解决这个问腿，不过less功能稍差一些，因此选择scss。

<!--more-->

scss即sass的一种变形，官网的配色可谓是十分骚包。但我是在idea下开发，那直接去看jetbrain上的教程了。
> [教程地址](https://www.jetbrains.com/help/idea/transpiling-compass-to-css.html)

# 环境搭建
## 安装 [Ruby](https://rubyinstaller.org/downloads/)

## 安装Compass
启动命令行
```bat
gem install compass
```

## 利用file watcher进行自动编译
> 我记得goland出来前，idea写go也靠这个东西
0. 进入到项目文件夹,对项目进行scss初始化
    ```batch
    compass init
    ```
1. 打开file watcher界面，添加一个scss监听
2. 设置compass文件路径，一般在$RUBY_HOME\bin\compass | compass.bat
3. 设置启动参数
    ```batch
    windows: compile $UnixSeparators($ProjectFileDir$)$
    linux: compile $ProjectFileDir$
    ```
4. 我的话会关闭auto-save...的高级选项

# 使用 
随后就是在 `$ProjectFileDir$\scss` 里写scss，保存后编译到 `$ProjectFileDir$\css`中

## 自用scss目录结构
.

.

.

.

# ....
好麻烦 要不我还是用less吧......