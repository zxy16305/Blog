---
title: springboot引入项目信息
date: 2019-02-14 22:18:46
categories:
-   framework
---
需要在application.properties中引用项目信息（项目名、项目版本），但希望和依赖管理工具（maven\gradle）自动同步
<!--more-->

# MANIFEST.MF
> [wiki解释](https://zh.wikipedia.org/wiki/%E6%B8%85%E5%8D%95%E6%96%87%E4%BB%B6)

受到banner.txt利用MANIFEST.MF的启发，只需要在打包时写入项目信息就好了。

## bootwar\bootjar
```groovy
bootWar{
    manifest{
        attributes(
                'Implementation-Version': version,
                'Implementation-Title': rootProject.name
        )
    }
}

bootJar{
    manifest{
        attributes(
                'Implementation-Version': version,
                'Implementation-Title': rootProject.name
        )
    }
}
```

## 引用MANIFEST.MF
```kotlin
@Configuration
@PropertySource(value = [
    "META-INF/MANIFEST.MF",
    "classpath:/config.properties",
    "classpath:/db.properties",
    "file:/\${user.home}\\scooper\\\${root.project.name}\\config.properties",
    "file:/\${user.home}\\scooper\\\${root.project.name}\\db.properties",
    "file:/icooper/config/\${root.project.name}/db.properties",
    "file:/icooper/config/\${root.project.name}/config.properties",
    "file:db.properties",
    "file:config.properties"], ignoreResourceNotFound = true)
open class AppConfig
```

## application.properties 中使用
冒号后为默认值

```properties
root.project.name=${Implementation-Title:scfm-rest}
root.project.version=${Implementation-Version:notfound}

spring.swagger.version=${root.project.version}
spring.swagger.title=${root.project.name}
```
