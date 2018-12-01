---
title: frp内网穿透
date: 2018-10-01 17:06:27
tags:
categories:
-   application
---

脱离向日葵的渣画质
<!--more-->

# 其他工具
## ngrok
ngrok也是同类的一个工具，但他的客户端是服务端编译得到的，内置了公私钥，但使用时不是那么方便

# 配置
## 服务端
首先准备一台公网ip的服务器，实验用的带宽为10m。随后在服务器上下载对应系统的frp。

[fatedier/frp](https://github.com/fatedier/frp/releases)

解压后配置`frp.ini`,换一个端口

## 客户端
### 3389 windows自带远程 
客户端下载frp，配置
```
[common]
server_addr = 服务端ip
server_port = 服务端端口

[ssh]
type = tcp
local_ip = 127.0.0.1
local_port = 3389
remote_port = 6000

[socks5]
type = tcp
remote_port = 6003
plugin = socks5
plugin_user = scoks5账号        
plugin_passwd = socks5密码
use_encryption = true
use_compression = true

```
3389是window远程的默认端口，连接时连接对方配置的 `server_addr:remote_port`即可

### socks5
socks5的配置也如上所示，连接时配置socks5-server为服务器ip，端口为[socks5]的remote_port
相关工具推荐 `profixier`
