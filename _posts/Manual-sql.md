---
title: 手写sql技巧记录
date: 2018-09-02 13:47:08
tags: 
---

> 但我并不推荐手写sql，当你交接给别人后就会知道为什么......

<!-- more -->

背景: 老项目，重构无力，只能去接受他了
## 高阶语法（不可维护之语法）
1. case
2. 

## 统计

## WHERE 1 条件拼接
```java
String sql =  " WHERE 1 "; 
if(foo1) sql += " AND foo1=? "
if(foo2) sql += " AND foo2=? "
```