---
title: node抓取网页内容
date: 2019-10-27 1:30:27
tags: node
categories:
-   application
---

在学术中需要特定的统计资料时，如果没有现成的统计结果，首先得获取相关数据。好在学术类的网站相对是可爬取的

<!--more-->

# 所用框架
## [superagent](https://github.com/visionmedia/superagent)
一个http request框架

## [cheerio](https://github.com/cheeriojs/cheerio)
一个类似jquery selector的html解析框架

## [bagpipe](https://github.com/JacksonTian/bagpipe)
一个异步调用限频的工具

# 历程
## 网页内容分析
通过dev tool分析http url和相关传参，再通过console分析html内容。只要开发者不特意屏蔽，基本没什么问题。

这里遇到个在js去计算a标签的href的，不过相关的参数都在a标签里。。。

## 频率限制
由于需要爬取的内容不小（4000多个请求），在异步时会直接请求，此时直接被服务端拒绝了相关请求。
之前地图下载器也有遇到过这个情况，当时的情况是通过计算已经把url全部定下来了，剩下的只是开了多个事件总线，在一个事件中下载完成后，触发下一个事件，以类似多消费者的模式，完成的异步限频。

但是这次下载的url是不定的，最好的实现就是在http请求处加一层代理，超过限制的请求则加入队列等待

bagpipe则会添加任务后，尝试着调用，如果当前任务已超过限制，则保存相关函数和回调。同时他对你传入的回调加了层包装，使其触发下一次回调（没有想清楚为什么不在他那里执行包装代码）。

但是可能会触发最大函数调用栈，使用下面这段代码测得调用栈大概是1万多，还是有风险的
```javascript
function computeMaxCallStackSize() {
        try {
            return 1 + computeMaxCallStackSize();
        } catch (e) {
            // Call stack overflow
            return 1;
        }
    }
```
