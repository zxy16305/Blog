---
title: jmeter记录
date: 2019-06-19 17:06:27
tags:
categories:
-   application
---

记一次jmeter页面测试

<!--more-->

# JSON Properties 提取
## 需求
+ 在下一个接口中要使用上一个接口的返回值
+ 例如分页列表展示详情
## 方案
### JSON Extractor
`JSON Extractor`提取所需要的值
> 例如 $.data.list[*] 、 $.data.list[*].id

但是由于jmeter properties中存储的是字符串，需要进一步解析

使用 `__javaScript`函数 , `${__javaScript((${configSectorBuilding}).buildingId)}`，其中 `configSectorBuilding` 是一个json字符串

# jmeter salve 部署
1. `wget http://mirror-hk.koddos.net/apache//jmeter/binaries/apache-jmeter-5.1.1.tgz`
2. `export RMI_HOST_DEF=-Djava.rmi.server.hostname=XXX.XXX.XXX.XXX`
3. 修改jmeter.properties, `server.rmi.ssl.disable=true`

# jmeter单机多进程测试
单进程大量的线程，在默认的JVM配置下，会严重影响性能。

## 启动本地salve
`.\\bin\\jmeter -Dserver_port={port} -s -j jmeter-server-{port}.log`

其中 `port` 指使用的端口，多进程需要手动指定

### 回传返回值
`.\\bin\\jmeter -Dserver_port={port} -s -j jmeter-server-{port}.log -Jmode=Standard`


## 启动本地GUI
`.\\bin\\jmeter.bat \"-Jremote_hosts={remote_ports}\"`
其中 `remote_ports` 为所有本地port.join(",")

## 简例
每个进程都会用掉1G多的内存，不要开太多

```python
import os

post_list = [22200, 22201, 22202, 22203, 22204, 22205, 22206, 22207]
local_list = []

for port in post_list:
    local_list.append("127.0.0.1:" + str(port))
    print( "ready to start {port}".format(port=str(port)))
    os.popen(".\\bin\\jmeter -Dserver_port={port} -s -j jmeter-server-{port}.log".format(port=str(port)))

remote_ports = ",".join(local_list)
print ("ready to start GUI {port}".format(port=str(remote_ports)))
os.popen(".\\bin\\jmeter.bat \"-Jremote_hosts={remote_ports}\"".format(remote_ports=remote_ports))

```

