---
title: 记一次webpack与typescript的使用
date: 2018-08-24 18:49:25
tags: 强迫症
email: zxy16305@gmail.com
categories:
-   framework
---

## 历程

组织前端模块并打包，首先想到的parcel，折腾了一天的parcel后，发现他对图片打包和ts的支持是在有点差，换回了webpack。
webpack的配置文件真的不是吹的...良好的开发习惯是要把配置文件再分模块，然后通过设置不同的环境（开发、线上），导入不同的配置。

未研究透彻，总之先做记录
首先先简单那看一下[官方教程](https://www.webpackjs.com/guides/typescript/)

<!-- more -->

## 文件架构

```
 css-module.d.ts
│  index.js
│  index.js.map
│  index.ts
│
├─css
│      displayControl.css
│      displayControl.css.d.ts
│      icon.css
│      icon.css.d.ts
│      layui-plus.css
│      layui-plus.css.d.ts
│      topo-main.css
│      topo-main.css.d.ts
│      vis-extend.css
│      vis-extend.css.d.ts
│
├─custom-dep
│  ├─jquery
│  ├─layui
│  └─scant
├─html
├─image
│  │  ico_camera.png
│  │  ico_server.png
│  │  ico_shebei.png
│  │  router.png
│  │  switch-l3.png
│  │  switch-st.png
│  │
│  ├─display
│  │      alarm.png
│  │
│  ├─icon
│  │      baocun.png
│  │      chexiao1.png
│  │      chexiao2.png
│  │      chexiao3.png
│  │      chongzuo1.png
│  │      chongzuo2.png
│  │      chongzuo3.png
│  │      daochu.png
│  │      fangda1.png
│  │      fangda2.png
│  │      fangyin1.png
│  │      fangyin2.png
│  │      icon_edit.png
│  │      icon_edit_blue.png
│  │      lianjiex1.png
│  │      lianjiex2.png
│  │      quanpin1.png
│  │      quanpin2.png
│  │      shanchu1.png
│  │      shanchu2.png
│  │      suoxiao1.png
│  │      suoxiao2.png
│  │      wenben1.png
│  │      wenben2.png
│  │      xuanze1.png
│  │      xuanze2.png
│  │      zishiyin1.png
│  │      zishiyin2.png
│  │
│  └─lines
│      ├─color
│      ├─dash
│      │      dash-4_3.png
│      │
│      └─width
└─ts
    ├─bottom
    │      Buttons.js
    │      Buttons.js.map
    │      Buttons.ts
    │      ZoomRange.js
    │      ZoomRange.js.map
    │      ZoomRange.ts
    │
    ├─data
    │      ApiManager.js
    │      ApiManager.js.map
    │      ApiManager.ts
    │      Config.js
    │      Config.js.map
    │      Config.ts
    │      ParamHolder.js
    │      ParamHolder.js.map
    │      ParamHolder.ts
    │
    ├─extend
    │      Icon.js
    │      Icon.js.map
    │      Icon.ts
    │      VisExtend.js
    │      VisExtend.js.map
    │      VisExtend.ts
    │
    ├─middle
    │      LeftNodeTool.js
    │      LeftNodeTool.js.map
    │      LeftNodeTool.ts
    │      RightWin.js
    │      RightWin.js.map
    │      RightWin.ts
    │
    ├─top
    │      Revert.js
    │      Revert.js.map
    │      Revert.ts
    │      SaveAndExport.js
    │      SaveAndExport.js.map
    │      SaveAndExport.ts
    │      TopVisTool.js
    │      TopVisTool.js.map
    │      TopVisTool.ts
    │
    └─util
            Utils.js
            Utils.js.map
            Utils.ts
```
以上是经过webpack编译后的src目录，将ts编译成了js
> 目录用windows命令 `tree /f` 生成

## 插件

webpack的功能几乎是通过插件完成的

### happypack
多线程打包，之前打包要花上20多秒不能忍，用了之后变成10来秒...无坑。唯一的坑就是`os.cpus()`需要`require('os')` :dog:

### url-loader
能将图片等资源转换成base64编码的url，注意大的图片还是采用file-loader的方式。

### typings-for-css-modules-loader
能正确解析ts下的css资源，即在index.ts中`require('./css/icon.css') `可以正确读取css

### extract-text-webpack-plugin
能够单独打包css，而不是将css直接写入html head，这会导致一瞬间的无样式状态。

### html-webpack-plugin
将打包后的js和css文件引入后输出

## FAQ(今日坑)

### 为什么我的ts无法引入css文件
因为ts是无法识别css模块的，根据webpack官方的typescript板块教程，也是给每一个***.css文件分别配了***.d.ts。
```typescript
declare module "*.svg" {//他是svg，css同理
  const content: any;
  export default content;
}
```
同样的,typings-for-css-modules-loader正是做了这个事情（大概还有别的）

### 为什么css中的图片url报错了
//TODO ...我看到过这个设置 但是没有记下来
我的解决方法是给
```css
.foo-css{
    background-image: url(xxx.png);
}
/*替换成*/
.foo-css{
    background-image: url("./xxx.png");
}
```
然后就可以了。。。。（玄学）

### 为什么我导入的css名称被编了hash码
这是为了防止重名，如果想使用原先的名称，只需要给typings-for-css-modules-loader配置:
```javascript 1.8
ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    use: {
                        loader: 'typings-for-css-modules-loader',
                        options: {
                            modules: true,
                            namedExport: true,
                            camelCase: true,
                            minimize: true,
                            localIdentName: '[local]'//此处  [path][name][local][hash]
                        }
                    }})
```
### 怎么导入第三方的非模块js
最简单的就是放在包外面，尤其是一些比较大的库，这个可以通过设置webpack的`externals`属性使用。
另外直接`var require1 = require('path.**.js')`是可以引入的，可以观察打包后的js文件，是否有引入。最好之后再`console.debug(require1)`一下（玄学）

### 为什么我ts导入了某个模块，但是不能使用
如果是全局window模块，可能是由于编译顺序导致的，或者试试上面的玄学。

此外每个用到模块的ts都需要导入！（大概是基础吧）

### 打包后的体积有点大啊
webpack配置文件需要配置开发者模式和部署模式，可以在部署模式中对uglifyjs-webpack-plugin做一些配置上的优化使其更小。再不行就服务端做压缩了。不过一般都是由于大量的第三方库使包变大的（我项目中visjs 600kb..）

### 不知道怎么组织项目结构
可以直接使用ts的脚手架，然后自己改一改就好了。（然后改了2天）
