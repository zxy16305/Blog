---
title: springboot && jpa
date: 2018-11-07 
tags:
categories:
-   framework
---

适配记录
<!--more-->

# boot
## 配置文件
```java
@SpringBootApplication
@EnableJpaAuditing
@PropertySource(value = {
        "classpath:/config.yml",
        "classpath:/db.yml",
        "file:/${user.home}\\scooper\\${root.project.name}\\config.yml",//这里的 root.project.name 是配在内部application.yml里的
        "file:/${user.home}\\scooper\\${root.project.name}\\db.yml",
        "file:/icooper/config/${root.project.name}/db.yml",
        "file:/icooper/config/${root.project.name}/config.yml",
        "file:db.yml",
        "file:config.yml",
}, factory = YamlPropertySourceFactory.class,//实现类见下方
        ignoreResourceNotFound = true)
@PropertySource(value = {
        "classpath:/config.properties",
        "classpath:/db.properties",
        "file:/${user.home}\\scooper\\${root.project.name}\\config.properties",
        "file:/${user.home}\\scooper\\${root.project.name}\\db.properties",
        "file:/icooper/config/${root.project.name}/db.properties",
        "file:/icooper/config/${root.project.name}/config.properties",
        "file:db.properties",
        "file:config.properties",
},
        ignoreResourceNotFound = true)
public class SpringBootApplication{
   // ...
}
```

## YamlPropertySourceFactory
```java
package cn.com.scooper.scfmimport.system;

import org.springframework.beans.factory.config.YamlPropertiesFactoryBean;
import org.springframework.core.env.PropertiesPropertySource;
import org.springframework.core.env.PropertySource;
import org.springframework.core.io.support.EncodedResource;
import org.springframework.core.io.support.PropertySourceFactory;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.UnknownHostException;
import java.util.Properties;

public class YamlPropertySourceFactory implements PropertySourceFactory {
    @Override
    public PropertySource<?> createPropertySource(String name, EncodedResource resource) throws IOException {
        Properties propertiesFromYaml = loadYamlIntoProperties(resource);
        String sourceName = name != null ? name : resource.getResource().getFilename();
        return new PropertiesPropertySource(sourceName, propertiesFromYaml);    }

    private Properties loadYamlIntoProperties(EncodedResource resource) throws FileNotFoundException {
        try {
            YamlPropertiesFactoryBean factory = new YamlPropertiesFactoryBean();
            factory.setResources(resource.getResource());
            factory.afterPropertiesSet();
            return factory.getObject();
        } catch (IllegalStateException e) {
            // for ignoreResourceNotFound
            Throwable cause = e.getCause();
            if (cause instanceof FileNotFoundException)
                throw (FileNotFoundException) e.getCause();
            else if(cause instanceof UnknownHostException){
                throw new FileNotFoundException("环境不同");
            }
            throw e;
        }
    }
}
```

# spring data jpa
## 多数据源配置
> 参考 
>
> [Spring JPA – Multiple Databases](https://www.baeldung.com/spring-data-jpa-multiple-databases)
> [spring-boot - Configure Two DataSources](https://docs.spring.io/spring-boot/docs/2.1.0.RELEASE/reference/htmlsingle/#howto-two-datasources)

### datasource bean
```java
package cn.com.scooper.scfmimport.config;

import com.zaxxer.hikari.HikariDataSource;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
public class ConfigBean {
    @Bean("DATABASE_DB_OLD_SCFM")
    @ConfigurationProperties("scfm.previous.database")
    public HikariDataSource previousSCFM(){
        return DataSourceBuilder.create().type(HikariDataSource.class).build();
    }

    @Bean("DATABASE_DB_SC_core")
    @ConfigurationProperties("scooper.core.database")
    public HikariDataSource scCore(){
        return DataSourceBuilder.create().type(HikariDataSource.class).build();
    }

    @Primary
    @Bean("DATABASE_DB_INNER_SCFM")
    @ConfigurationProperties("scfm.new.database")
    public HikariDataSource newSCFM(){
        return DataSourceBuilder.create().type(HikariDataSource.class).build();
    }
}

```

### repository config
```java
package cn.com.scooper.scfmimport.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.orm.jpa.EntityManagerFactoryBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;


@Configuration
@EnableTransactionManagement
@EnableJpaRepositories(
        basePackages ={"cn.com.scooper.scfmimport.repository.inner"},//jpa repository路径
        entityManagerFactoryRef = "DB_INNER_SCFM_ManagerFactory",
        transactionManagerRef = "innerTransactionManager"
)
public class DbInnerScfmConfig {

    @Autowired
    @Qualifier("DATABASE_DB_INNER_SCFM")
    private DataSource dataSource;


    @Bean("DB_INNER_SCFM_ManagerFactory")
    public LocalContainerEntityManagerFactoryBean entityManagerFactoryBean(EntityManagerFactoryBuilder builder){
        HibernateJpaVendorAdapter hibernateJpaVendorAdapter = new HibernateJpaVendorAdapter();
        hibernateJpaVendorAdapter.setGenerateDdl(true);
        return builder
                .dataSource(dataSource)
                .packages("cn.com.scooper.scfmimport.entity.inner")//对应的entity路径
                .persistenceUnit("scfmNew")
                .build();
    }

    @Bean
    public PlatformTransactionManager innerTransactionManager(EntityManagerFactoryBuilder builder) {
        JpaTransactionManager transactionManager
                = new JpaTransactionManager();
        transactionManager.setEntityManagerFactory(
                entityManagerFactoryBean(builder).getObject());
        return transactionManager;
    }
}

```

## Entity mapping
需要注意的是，只有同一datasource的entity才能mapping。idea生成entity和其mapping。
### @ManyToMany
insert生效需要两方同时包含对方

