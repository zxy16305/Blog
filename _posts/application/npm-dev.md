---
title: npm publish && company use
date: 2018-12-28 17:06:27
tags:
categories:
-   node
-   javascript
---

npm的内部发包与使用
<!--more-->

# publish
## set publishConfig in package.json
```json
{
  "publishConfig": {
    "registry": "http://192.168.103.133:8080/repository/scooper-npmtrial/"
  }
}
```

## use scope name in package.json
```json
{
"name": "@scopertrail/scooper-npm-pack"
}
```

# use
## assign the scope with private registry
```commandline
npm config set @scoopertrail:registry http://192.168.103.133:8080/repository/scooper-npmtrial/```

## install package with scope
```commandline
npm install @scopertrail/scooper-npm-pack
```

# development
## write bin file
即npm install 之后，会在node_modules/.bin生成可调用脚本，在scripts里调用。常见如webpack，craco等。
### main script
目录建议单独创建bin目录用于存放脚本

1. js头部需申明 `#!/usr/bin/env node`，否则生成的bin是直接打开js
2. 在 `package.json`中申明
```json
{
    "bin":{
      "scpack":"./bin/scpack.js"
    }
}
```
上面一段表示npm install 后会生成可调用的脚本 `scpack`，路径指向 `<projectPath>/bin/scpack.js`

## devDependencies && dependencies
之前写react不管是什么依赖都加了 `-D`，但其实是有问题的，只不过react应用是webpack build完的产物，没有暴露问题。

`devDependencies`表示运行时不存在的依赖，如 `babel`等

所以publish的包在被install时，不会去下载这里面的依赖，所以要根据场景应用
