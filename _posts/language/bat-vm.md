---
title: bat-vm
date: 2018-09-07 10:33:27
tags:
categories:
-   language
---
有一个需要虚拟机随系统开关的需求
> [VMware怎么开机自启动,关机自动挂起虚拟机](http://blog.51cto.com/singoe/1972417)

> [用批处理(bat)同时运行多个程序的方法](https://zww.me/archives/25386)
<!-- more -->
# FQA
## 默认开启的是图形化界面怎么办

关闭图形化 `sudo systemctl set-default multi-user.target`

恢复图形化 `sudo systemctl set-default graphical.target`

> [Ubuntu 16.04 开机默认命令行界面](https://wiki.zthxxx.me/wiki/%E6%8A%80%E6%9C%AF%E5%BC%80%E5%8F%91/Linux/Ubuntu/Ubuntu-16-%E5%BC%80%E6%9C%BA%E9%BB%98%E8%AE%A4%E5%91%BD%E4%BB%A4%E8%A1%8C%E7%95%8C%E9%9D%A2/)

## 虚拟机 无法打开内核设备
cmd输入
```
net start vmci && net start vmx86 && net start VMnetuserif && sc config vmci=auto && sc config vmx86=auto && sc config VMnetuserif=auto
```
