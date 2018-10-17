---
title: javascript
date: 2018-09-17 13:06:27
tags:
---
记录一些简单的linux
<!--more-->

# 常规
## 开机自启
方法很多，这里用一种脚本启动的方式
1. 创建autostart.sh，开头的内容为
```shell
#!/bin/bash
#description:开机自启脚本
/usr/local/webServer/nginx/sbin/nginx # 启动nginx
```
2. 给脚本执行权限 ,`chmod +x autostart.sh`
3. 观察`/etc/rc.d/rc.local` 或 `/etc/rc.local`有无执行权限，若没有则加上
4. 打开 `/etc/rc.d/rc.local` 或 `/etc/rc.local`,末尾添加执行autostart.sh的命令
> 但是遇到了卡在某个命令的情况