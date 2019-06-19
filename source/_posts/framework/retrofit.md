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

### solution2
session bean问题很大，使用spring session代理到redis时，cglib代理下的bean会保存他的代理对象到redis，然后反序列化的时候就出问题了。

线程池的配置方案不变，在拦截其中获取session的方法：
`Object currentUser = servletRequest.getSession().getAttribute("currentUser");`