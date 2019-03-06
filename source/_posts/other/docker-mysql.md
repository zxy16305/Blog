---
title: docker
date: 2018-08-31 12:40:01
tags:
categories:
-   other
---

> 不同的现场可能有不同的数据库配置,此处使用docker
> see [docker.hub.mysql.cytopia](https://hub.docker.com/r/cytopia/mysql-5.6/)

<!-- more -->
# docker-mysql
## 镜像
随便拿一个 
```
docker pull cytopia/mysql-5.6
```
> 增加  registry.docker-cn.com ，可加速


## 启动容器
```
docker run \
    --name custom-container-name \
     -i \
    -p 0.0.0.0:3308:3306 \
    -e MYSQL_ROOT_PASSWORD=my-secret-pw \
    -t cytopia/mysql-5.6
```


## mysql用户配置

### 进入docker mysql
```
docker exec -it ${container id} /bin/bash

mysql -uroot -pmy-secret-pw
```

### 配置用户
```
create user shwoclear identified by 'showclear';
grant all privileges on *.* to showclear@'%' identified by 'showclear';
flush privileges;
```
# docker
## docker常用命令
### `docker update --restart=always <CONTAINER ID>`
修改某个已创建的container的属性
### `docker exec -it <CONTAINER ID> /bin/bash`
进入某个容器bash
### `docker ps -a`
查看所有容器 ，(居然不是`docker container`开头的)