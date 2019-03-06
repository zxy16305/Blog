---
title: 记录
date: 2018-10-14 15:36:27
tags:
categories:
-   scooper
---

记录公司项目中遇到的一些问题

<!--more-->

# 前端
## ocx
### ocx插件挡住了弹窗
> [div层被OCX控件Object遮挡问题的解决](https://my.oschina.net/4k9LCGA/blog/382169)

依此博客所言，在弹窗div内部嵌入一个空的iframe来遮挡ocx控件，同时弹窗又可以遮挡iframe，就完成了弹窗遮挡ocx的操作。
`<iframe id="iframe1" src="about:blank" frameBorder="0" marginHeight="0" marginWidth="0" style="position:absolute; visibility:inherit; top:0px;left:0px;width:100%; height:100%;z-index:-1; filter:alpha(opacity=0);"></iframe>
 </div>`

# 后台
## java
### kotlin下lombok不工作
idea apt默认关闭，打开就好。 setting 搜索 `processors`