---
title: 云服务器快速迁移策略
date: 2021-10-05 21:42:42
tags:
categories:
-   personal-learning
---

近期腾讯云到期了，新买了个折扣环境，折腾一下应用迁移，写点体会
<!--more-->

> 要想快速迁移就得用 docker，除了 docker 和 docker-compose，应用与坏境不存在其他耦合即可 
> 
> 迁移时拷贝整个 app 目录，拷贝完后逐个启动 docker-compose，再将域名解析切换到新环境即可。 
> 
> 部分启动时指定了域名连接的应用（比如 frp），需要重启

## frp
官方原则不上传到任何仓库，此处用 dockerfile 组装后由 docker-compose 启动。
应用包直接拷到目录下，迁移时整个目录拷走。

```dockerfile
FROM scratch
ARG ver=0.21.0
COPY ./frp_${ver}_linux_amd64/frps /frps
ENTRYPOINT ["/frps", "-c", "/frps.ini"]
```

```yaml
version: '3.1'
services:
    frps:
      build:
       context: ./
       dockerfile: Dockerfile
      network_mode: "host"
      restart: unless-stopped
      container_name: frps
      image: frps
      volumes:
        - "./frp_0.21.0_linux_amd64/frps.ini:/frps.ini"
```

## springboot
springboot 之前使用 executable jar + service 的方式管理启停，此处也改为 docker 管理。

由于开发环境和部署端不在同一个环境，所以没有使用自带的 docker 镜像打包功能。

```dockerfile
FROM openjdk:8-jdk-slim
COPY bill-manager.jar /
ENTRYPOINT ["java", "-jar","/bill-manager.jar"]
```

```yaml
version: '3.1'
services:
  bill-manager:
    build:
      context: ./
      dockerfile: Dockerfile
    environment:
      - JAVA_OPTS=-Xmx250m
    ports:
      - "9988:9988"
    restart: unless-stopped
    container_name: bill-manager
    image: bill-manager
    volumes:
      - "./application.properties:/application.properties"
      - "./localfile:/localfile"
      - "./logs:/logs"
```

## mysql
mysql 之前是 docker 管理，但没有用数据卷，这里补上

```yaml
version: '3.1'
services:
  mysql:
    image: mysql:5.7.35
    command: --default-authentication-plugin=mysql_native_password
    restart: always
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: ******
    volumes:
      - "./data:/var/lib/mysql"
      - "./conf:/etc/mysql/conf.d"
```