---
title: springboot
date: 2018-12-11 15:57:47
tags: 
categories:
-   framework
---


<!--more-->
# 配置
## 时间\数据大小
[Properties Conversion](https://docs.spring.io/spring-boot/docs/2.1.1.RELEASE/reference/htmlsingle/#boot-features-external-config-conversion)

# spring-base
## aop
### problem
使用spring cache时，同一个bean内的一个方法调用另一个启用了缓存的方法时，缓存没有起作用
### solution
1. 使用j2ee注入 `@Resource`注入自身，从注入的bean中调用方法
```java
@Service
@RequiredArgsConstructor
public class CommonGisPositionDataServiceImpl implements CommonGisPositionDataService {
    private final CommonGisPositionService commonGisPositionService;
    
    @Resource
    private  CommonGisPositionDataService commonGisPositionDataService;
    
     @Override
     @Cacheable(value = {"position-info"},unless = "#result == null")
     public GisPosition getPosition(GisPosition gisPosition){
        //...
        return  gisPosition;
     }
     
     public GisPosition putCache(GisPosition gisPosition){
         commonGisPositionDataService.getPosition(gisPosition);
     }
}
```
2. 强制使用Aspect或者CGLIB
