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
kotlin简单的看作是java的工具类就可以了，目前用的比较多的特性是lambda和拓展函数。而且可以选择编译成jdk6或者jdk8，使用时比较灵活（当然用了boot2就已经没有6了）

## querydsl
强类型的自然语言的方式描述一个sql。

使用是会通过apt自动构建相应的QEntity

以下为使用的一个例子，其中 `QFeeTravelEntity` 就是querydsl生成的

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

同lombok，另外需要注意idea需要开启 `Annotation processing`
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
## querydsl与jpa原生分页集成
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

此处sort需要用 `SortDefault`设定默认值, 直接写在 `PageableDefault`里的话，不能定义多个排序

这里常犯的一个错误是，直接在PageableDefault里的sort数组里写前端传入的参数，比如 ~~`@PageableDefault(size = 10, page = 0,sort=[ "id,asc", "name,desc" ])`~~

```kotlin
    //实验jpa原生page传入的可行性
    @GetMapping("pageable")
    public fun testPageIn(@PageableDefault(size = 10, page = 0)
                          @SortDefault.SortDefaults(value = [
                              SortDefault(value = ["gmtCreate"],direction = Sort.Direction.DESC),
                              SortDefault(value = ["id"],direction = Sort.Direction.DESC)
                          ])
                          pageable: Pageable,
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

## 默认生成项目的一些小问题
### ids for this class must be manually assigned before calling save()
jpa2生成的entity默认没有带上主键生成策略，添加 `@GeneratedValue(strategy = GenerationType.IDENTITY)`即可

另外kotlin的entity注意加到get方法上 
```kotlin
    @get:Id
    @get:Column(name = "id")
    @get:GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Int? = null
```

### controller返回date为时间戳
方法有很多，这里配置messageConverter
```kotlin
@Configuration
@EnableWebMvc
class WebConfig(
        private val authInterceptor: AuthInterceptor
) : WebMvcConfigurer {
    //...

    //定义时间格式转换器
    @Bean
    fun jackson2HttpMessageConverter(): MappingJackson2HttpMessageConverter {
        val converter = MappingJackson2HttpMessageConverter()
        val mapper = ObjectMapper()
        mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
        mapper.dateFormat = SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
        converter.objectMapper = mapper
        return converter
    }

    override fun configureMessageConverters(converters: MutableList<HttpMessageConverter<*>>) {
        converters.add(jackson2HttpMessageConverter())
        super.configureMessageConverters(converters)
    }
}
```

### 表单传入Date报错不能cast
使用 `InitBinder`
```kotlin
    @InitBinder
    protected fun initBinder(binder: WebDataBinder) {
        val dateFormat = SimpleDateFormat("yyyy-MM-dd HH:mm:dd")
        dateFormat.isLenient = false
        binder.registerCustomEditor(Date::class.java, CustomDateEditor(dateFormat, false))
    }
```

### java.sql.Date的问题
语义上这个类只包括日期，不含有时间，尽量避开。jackson默认转换的string，就不含有时间信息。建议使用 java.sql.timestamp，或者数据库设计时，注意一下。

### entity jpaAuditing不起作用
注解没开，在启动类加上 `@EnableJpaAuditing` 注解开启审计

### 注意字段与关键字的冲突
项目使用逻辑删除，因此数据库会存在 `is_delete` 字段，映射到kotlin Entity上也就是 `isDelete`字段，在反射取值时，被识别成了get方法而出现问题

随后改成delete，结果hql里的这个 `delete` 字段隐式报错了（编译通过，运行报错）；在搜索hql关键词转义符未果后，将字段名改为 `deleted`，报错消失

# ...持续更新
