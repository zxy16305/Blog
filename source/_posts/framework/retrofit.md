---
title: retrofit
date: 2018-12-06 07:57:47
tags: 
categories:
-   framework
---
踩坑 && 记录

<!--more-->

## okClient 拦截器无法使用session bean
### solution
重写runnable和callable，注入request域
[accessing-scoped-proxy-beans-within-threads-of](https://stackoverflow.com/questions/1528444/accessing-scoped-proxy-beans-within-threads-of)
