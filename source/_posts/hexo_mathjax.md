---
title: Hexo 添加 MathJax 支持
layout: post
date: 2017-04-09 16:00
tags: [tutorial]
math: 'no'
cdn: 'header-off'
header-img: "/imgs/default-post-cover.jpg"
subtitle: "Add the Support of MathJax in Hexo"
author: "Hailiang Dong"
---


## 背景介绍
HEXO是一个基于Node.Js的静态个人博客软件，可以将自己写的Markdown形式的文章渲染成静态网页。通过和Github结合，可以很方便的搭建自己的博客，具体可以参考[这篇文章][1]搭建。

在我们写博客的时候，难免要遇到公式，尤其是在写一些理论性比较强的博客的时候，这个时候我们就需要在网页上显示公式。如果你对Latex有一定的基础，那么MathJax就是一个很好的工具（事实上它就是目前最为广泛使用的网页公式渲染库）。

Hexo本身是不支持MathJax的，不过你可以通过下载一些支持MathJax的主题或者相应的MathJax插件来完成对数学公式的支持。不过这种方式的一个问题在于，MathJax的影响是针对所有文章的，并且由于MathJax的CDN都在国外，加载速度都会很慢。因此，你的所有文章加载速度都会变慢（因为需要从国外服务器加载MathJax的文件），即使有的文章里面根本不需要MathJax进行公式渲染。

本文接下来主要讲解如何以手动的方式添加MathJax支持，使其支持对单篇文章设置开关，这样没有公式的博客的加载速度不会受到一点影响。其次分享一个自己在网上找到的国内MathJax CDN源，从而大大加快MathJax的加载速度。

## 手动添加MathJax支持 （针对单篇文章）
要让网页支持MathJax，其实只要将以下JS代码添加进你的HTML即可，但是我们不能每次生成完静态网页后自己手动添加，那样子会累死人的。
```
<!-- mathjax config similar to math.stackexchange -->
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
    jax: ["input/TeX", "output/HTML-CSS"],   # 可以更改mathjax的默认输出样式
    tex2jax: {
        inlineMath: [ ['$', '$'] ],
        displayMath: [ ['$$', '$$']],
        processEscapes: true,
        skipTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
    },
    messageStyle: "none",
    "HTML-CSS": { preferredFont: "TeX", availableFonts: ["STIX","TeX"] }
});
</script>
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
```
为了能让Hexo自动为需要mathjax的文章添加该js代码，我们首先进入主题的`layout/_partial/`文件夹，创建一个叫做`mathjax.ejs`的文件，代码内容就是上面的JavaScript。

接下来，因为Hexo渲染你的文章的时候是通过`layout/post.ejs`进行的，我们只需要在代码的最后添加一个判断语句，如果该文章需要MathJax，我们就加载上面的`mathjax.ejs`即可。具体来说，将下面的代码添加到`post.ejs`尾部，注意不要添加到别的判断语句里面了。

```
<% if (page['math']){ %>
<%- partial('_partial/mathjax') %>
<% } %>
```

这样，就完成了Hexo 对 MathJax的支持，接下来再写文章的时候，只需要在文件的头部添加`mathjax：true` 即可对该文章开启公式渲染，在文章里面你就可以尽情的写公式了。

## 替换MathJax源
国外的MathJax源实在是太慢了，即使不会影响别的文章，有公式的文章加载时间要很久，要等很久自己书写的公式代码，才能转换成漂亮的公式。 有的时候，网络不好甚至无法加载，留下了一堆`$$`符号在那里，显得非常尴尬。

这里分享一个从网上找到的MathJax源，替换上面`mathjax.ejs`的最后一句为
```
<script type="text/javascript" src="http://mathjax.josephjctang.com/MathJax.js?config=TeX-MML-AM_HTMLorMML">
</script>
```
即可完成源的更改。

当然，如果你有自己的公网IP和24小时开机的电脑的话，也可以自己搭建一个镜像源。去[Github][2]上下载相应的代码，放在某一个目录下面，比如说`/home/xxx/www`。之后开一个HTTP服务器并将根目录指向`www`即可。

这样你就可以使用自己的源来加载MathJax，例如我自己也搭建了一个MathJax的镜像源，可以使用以下代码加载
```
<script type="text/javascript" src="mirror.hdong.space/mathjax/MathJax.js?config=TeX-MML-AM_HTMLorMML">
</script>
```



[1]:http://www.jianshu.com/p/465830080ea9
[2]:https://github.com/mathjax/MathJax