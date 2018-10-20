---
title: nginx
date: 2018-10-20 13:06:27
tags:
categories:
-   application
---
记录nginx常用配置 及 一些小坑

<!--more-->

# 配置
## 基本示例
### http端口转发 解决跨域问题
```nginx
http {
    include       mime.types;
    default_type  application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                '"$http_referer" $status $body_bytes_sent $request_body '
                '"$http_user_agent" "$http_x_forwarded_for" "$http_Cookie"';
				
    access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       8080;
        server_name  0.0.0.0;

        #charset koi8-r;

      #  access_log  logs/host.access.log  main;

		location ^~ /dispatch-web/{
			proxy_pass http://192.168.101.233:8080/dispatch-web/;    
			proxy_set_header Upgrade $http_upgrade;
			proxy_set_header Connection "upgrade";
			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_http_version 1.1;
		}
	
		location /{
			proxy_pass http://127.0.0.1:8090;
		}
		
    }
}
```
### mysql\ssh 等tcp流代理
```nginx
stream {
	upstream srf-mysql {
        hash $remote_addr consistent;
        server 192.168.101.233:3309 max_fails=3 fail_timeout=30s;
    }	
	upstream ssh {
        server 192.168.101.233:22;
    }

	server {
        listen 3309;
        proxy_connect_timeout 30s;
        proxy_timeout 600s;
        proxy_pass srf-mysql;
    }

    server { #里面可以有多个监听服务，配置监听端口和代理的ip和端口就可以进行tcp代理了。  
        listen 2233;
        proxy_pass ssh;
        proxy_connect_timeout 1h;
        proxy_timeout 1h;
    }
}
```
### 本地静态资源代理(http)
#### linux
```nginx
        server{
                listen 80;
                server_name blog.kiswich.top;
                location /{
                        root /root/applications/hexo/public;
                        autoindex on;
                }
        }

```
#### windows
windows下比较特殊
```nginx
		 location ^~ /3D_Tiles/{
                      root  D:/githubResp/tiles/;
          }
```
注意此处的 `3D_Tiles` 为 `D:/githubResp/tiles/` 下的一个文件夹， 访问`http://localhost:8080/3D_Tiles/tileset.json` , 相当于访问 `D:\githubResp\tiles\3D_Tiles\tileset.json`