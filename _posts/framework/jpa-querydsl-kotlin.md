---
title: querydsl-kotlin
date: 2019-01-23 
tags:
categories:
-   framework
---

简介在不使用entity mapping的情况下，使用querydsl完成复杂查询的例子
<!--more-->

# 名词
## kotlin
kotlin简单的看作是java的工具类就可以了，目前用的比较多的特性是lambda和拓展函数

## querydsl
强类型的自然语言的方式描述一个sql。

使用是会通过apt自动构建相应的QEntity

```kotlin
     val feeTravelEntity = QFeeTravelEntity.feeTravelEntity
     val projectEntity = QProjectEntity.projectEntity

     val factory = JPAQueryFactory(entityManager)

     val list = factory.select(feeTravelEntity, projectEntity)
             .from(feeTravelEntity)
             .leftJoin(projectEntity)
             .on(projectEntity.id.eq(
                     feeTravelEntity.projectId
             )).fetch()
```

## gradle
类似于maven的构建工具，因为maven中配置插件看得头大，故转到gradle

## apt,kapt
编译时注解，用的比较著名的有lombok

# 项目构建
使用[spring Initializr](https://start.spring.io/) 生成

# 项目节点
将以项目遇到的问题来叙述

## 初始化
这一部分包括了controller、service等一系列基础的bean的建立，只遇到了一点kotlin语法上的问题，包括泛型、获取javaClass、data class是否合适、一些小问题

## join分页查询
将项目转到jpa的初衷是避开mybatis原生sql的书写；同时之前配置了entity mapping后，缺失了太多的灵活性，在复杂关系（通常是由于数据库设计不当造成的）下，对sql的性能优化比较麻烦。
在不配置mapping的情况下，第一个controller就遇到了问题，join+分页怎么处理。

数据库不增加冗余字段的情况下，join是必须要走的。另外一种方案是先查出外键数组，然后查关联表，在代码中匹配，这就得不偿失了。。

## querydsl集成
querydsl采用apt的方式与项目集成，几乎是无侵入式的。在把项目转移到gradle后，加入相应的依赖，通过 `gradle build`后，build文件夹内会创建 `generated`文件夹，里面就是生成的代码

```groovy
//...
apply plugin: 'kotlin-kapt'
//...
dependencies {
    //...
    compile 'com.querydsl:querydsl-jpa:4.2.1'
    kapt "com.querydsl:querydsl-apt:4.2.1:jpa" // 使用kapt 激活querydsl apt工具
   //...
}

```
## 与jpa原生分页集成
在jpa项目里，官方已经提供了相应的工具类， `org.springframework.data.jpa.repository.support.Querydsl` ，相关api可直接看源码注释
```kotlin
    val feeTravelEntity = QFeeTravelEntity.feeTravelEntity
    val projectEntity = QProjectEntity.projectEntity

    val factory = JPAQueryFactory(entityManager)

    val select = factory.select(feeTravelEntity, projectEntity)
            .from(feeTravelEntity)
            .leftJoin(projectEntity)
            .on(projectEntity.id.eq(
                    feeTravelEntity.projectId
            ))

    val jpqlQuery = Querydsl(entityManager, PathBuilder(FeeTravelEntity::class.java, "feeTravelEntity"))
            .applyPagination(pageable, select)
    val fetch = jpqlQuery.fetch()
```

## 分页结果完善
分页结果还包括 total、page、size，这里使用total得再次查询
```kotlin
    val fetchCount = jpqlQuery.fetchCount()
    val pageImpl = PageImpl(fetch, pageable, fetchCount)
```

## jpa分页与公司规范适配
公司规范与jpa的分页字段名、结构都不一致，此处使用kotlin拓展函数实现转换

### 传入
```kotlin
//返回新的分页请求
fun Pageable.change(pageNum: Int? = this.pageNumber, pageSize: Int? = this.pageSize, sort: Sort? = this.sort): Pageable {
    return PageRequest.of(
            pageNum ?: this.pageNumber,
            pageSize ?: this.pageSize,
            sort ?: this.sort
    )
}
```
此处兼容原生pageable和项目迁移前的字段，sort使用pageable接受（还好原先没有加入sort、不然就蛋疼了）
```kotlin
    //实验jpa原生page传入的可行性
    @GetMapping("pageable")
    public fun testPageIn(@PageableDefault(size = 10, page = 0, sort = ["gmtCreate,desc", "id,desc"]) pageable: Pageable,
                          pageNum: Int?, pageSize: Int?, startTime: Date?, endTime: Date?): Pageable {
        return pageable.change(pageNum, pageSize)
    }
```
### 传出
```kotlin
//Page转换为公司规范返回结果
fun PageImpl<out Any>.toAPIPageJson(): APIPageJson<out Any> {
    return APIPageJson(this.content, this.totalElements, this.number, this.size)
}
```

```kotlin
//...
return pageImpl.toAPIPageJson()
```

# ...持续更新
