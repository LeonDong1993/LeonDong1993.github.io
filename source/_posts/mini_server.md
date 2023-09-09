---
title: Ubuntu系统配置篇
layout: post
date: 2017-03-01 10:00
tags: [tutorial]
cdn: 'header-off'
header-img: "/imgs/default-post-cover.jpg"
subtitle: "Set up a Mini Ubuntu Personal Server"
author: "Leon Dong"
---

[1]: /figs/mini_server/webmin.jpg
[2]: /figs/mini_server/sysv_services.jpg
[3]:https://npm.taobao.org/mirrors/node

## 基本配置

有一些软件和事情基本上装完系统是必须需要装的，个人的习惯如下

> sudo apt-get install update
sudo apt-get install g++ vim ssh-server screen iftop git
sudo apt-get dist-upgrade #升级系统软件到最新版
git config --global user.name "xxx"
git config --global user.email "xxx"
ssh-keygen -t rsa -C "comment"

## 64位系统下运行32位程序

为了能在64位系统下运行32位程序，你需要显示的告诉系统你需要运行基于i386架构（32位）的程序。在此之后，更新系统的软件源，安装一些运行库即可。

> sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386

特别提醒一下，在Ubuntu 12.04等系统中，可以直接安装`ia32-libs`来代替以上三个软件包。但是该系统软件在Ubuntu 14.04等系统中已经移除，所以最好使用上面的方式进行安装。

## Deluge BT下载

Deluge可以是Linux下运用比较广泛的BT下载客户端，更重要的是它可以利用Web界面进行远程控制。要安装Deluge的话，建议直接使用官方的PPA仓库，然后同样更新软件源，安装Deluge的守护进程和网页控制端即可。

> add-apt-repository ppa:deluge-team/ppa
apt-get update
sudo apt-get install deluged deluge-web

输入以下命令即可启动Deluge的守护进程以及Web控制端

> deluged -q -p 13737 # 以quiet的方式启动守护进程，监听端口13737（自定义）
deluge-web -f -p 8080 # 开启网页控制端，端口自定义为8080

需要注意的是，deluge的守护进程貌似无法在bash里面直接结束，此时可以登录网页控制端在`connection`里面选择`stop daemon`即可。

## Webmin安装

Webmin是一个开源的基于网页的Unix/Linux系统管理工具。通过使用Webmin，你可以在浏览器上设置和安装所有的系统服务，同时还可以很方便的查看系统的运行状态。以下介绍通过官方软件园安装最新版Webmin的方法。

首先在`/etc/apt/sources.list`配置文件里面添加webmin的官方仓库

> deb http://download.webmin.com/download/repository sarge contrib
deb http://webmin.mirror.somersettechsolutions.co.uk/repository sarge contrib

之后添加GPG密钥

> sudo wget http://www.webmin.com/jcameron-key.asc
sudo apt-key add jcameron-key.asc

接下来就是类似的软件过程，运行以下的脚本即可

> sudo apt-get update
sudo apt-get install webmin
sudo ufw allow 10000 # 防火墙

安装完成后Webmin会自动启动，默认占用端口10000，打开浏览器并访问  https://your-ip:10000/ ，输入你的用户密码即可显示WebMin的主界面

![webmin main page][1]

现在，你就可以远程管理和配置你的Ubuntu服务器了。


## 系统服务管理

在Ubutnu里面可以利用`sysv-rc-conf`来管理系统的各项服务，可以很快捷的进行启动、暂停、开机自启等操作。其系统界面如下图所示

![sysv-rc-conf example][2]

按+可以直接启动服务，-直接停止服务，空格键可以控制开机自启，有一个X表示启用系统自启。

## Samba文件服务
先使用命令`sudo apt-get install samba`安装SAMBA软件，接下来的主要问题就是配置了。编辑samba的配置文件`/etc/samba/smb.conf`,在里面添加一个共享目录。

> [share]  # 共享的名字
path = /home/xxxx/xxxx #共享的路径
available = yes
browseable = yes
public = no # 不公开
writable = yes

Samba一个比较特殊的地方就是它由两个服务组成，要分别进行启动，运行

> service smbd restart
service nmbd restart

重启samba服务，此时在windows系统里面就可以使用`\\ip-addr`查看你的共享目录，由于设置了不公开，访问时需要账号密码。但是Samba服务和系统的账户是独立开的，因此你需要执行如下命令添加一个Samba用户。

> smbpasswd -a [username]

之后，你就可以愉快的使用Samba服务，方便的修改Linux服务器里面的文本文件了。


## Node.JS

首先Node.JS可以有三种不同的安装方式，源码安装（推荐），Binary安装，软件源安装。其中最省事的当然是使用软件源安装，直接运行`sudo apt-get install nodejs npm`即可。但是这样直接安装的版本一般都不是最新的，不推荐这种方式。

第二种方式是直接将编译的好的二进制文件解压到系统即可，这种方式也比较简单，但是有些时候会报一些莫名其妙的错误（我两台机子同时这样安装，一台成功，另一台失败，NPM安装软件时总是报错，目前未解决该问题）。Binary安装的具体步骤是:

- 首先到官网下载对应系统架构的二进制安装包，然后直接解压到你想要的安装位置
- 这时候你就会看到bin文件夹里面已经有了node和npm的可执行文件了，不过只能在该文件夹下运行
- 建立可执行文件的符号链接，例如`ln -s xxxx/bin/node /usr/local/bin/node`，然后就可以在任意地方直接运行了。

第三种方式是我比较推荐的，就是直接源码编译安装。对于有些特殊的系统架构，例如MIPS等等，只能自己编译源码安装了。具体步骤如下：

- 首先到下载源码包，然后直接解压到你想要的安装位置，这里推荐[淘宝镜像][3]下载你想要的任意版本
- 解压改压缩包`tar xvf node-xxx.tar.gz`并cd到相应的文件夹下面
- 先执行`./configure --prefix=xxxx`，这里面xxxx就是你想安装的位置，当然也可以不指定，直接使用默认的位置。
- 编译NodeJS，直接执行`make -j4 && make install`即可。如果想卸载，直接在目录下运行`make uninstall`即可干干净净的删除。

安装完Node.JS和NPM后，第一件事情一定是配置一下NPM，尤其是NPM的软件源。在用户的根目录创建文件`.npmrc`，加入如下配置:

> registry=https://registry.npm.taobao.org/ # 使用淘宝的镜像源，速度快，稳定
prefix=/xxxx/xxx/xxx  # node的软件包安装位置
cache=/tmp/npm_cache # 缓存文件的存放位置

接下来就可以安装需要的node软件包了，比如我就先把hexo安装了。

## http 服务

Http服务器有很多选择，个人对Apache那种重量级的http服务器需求比较低，因此我选择了lighttpd。它是众多OpenSource轻量级的web server中较为优秀的一个。支持FastCGI, CGI, URL重写, Alias等重要功能。

> sudo apt-get install lighttpd   #安装lighttpd

安装后系统会自动启动lighttpd，打开 http://localhost 即可预览。修改配置文件`/etc/lighttpd/lighttpd.conf`，修改里面的`server.document-root`选项即可实现对指定Web网页的根目录。使用命令`sudo /etc/init.d/lighttpd restart`重启服务即可生效

如果想在一个机子上挂在多个网页到不同的端口，可以使用一下配置创建一个新的主机

> $SERVER["socket"] == ":8000" {
  server.document-root = "/var/www/xxx/"
}

如果想在一个服务器上挂在多个虚拟主机，可以使用如下命令
> $HTTP["host"] == "mathjax.hdong.space" {
server.document-root        = "/var/www/xxx/"
}

## 其他杂项配置

### 优化BASH使用体验

Bash默认情况下在自动补全上区分大小写的，这个在实际使用中很不方便，在用户根目录创建文件`.inputrc`，添加以下配置即可变成大小写不敏感的方式。

> set match-hidden-files off
set show-all-if-ambiguous on
set completion-ignore-case on
"\e[A": history-search-backward
"\e[B": history-search-forward


### 开启root用户远程SSH登陆功能

更改`/etc/ssh/sshd_config`配置文件，将`PermitRootLogin`之后的值改成yes即可，之后重启SSH服务或者直接重启系统即可生效。

### HOME和END按键变成了~

这个问题我也不知道怎么回事，貌似只有在root用户下并配置了BASH优化才会出现的问题。直接使用快捷键`ctrl+a`以及`ctrl+e`即可代替上述两个按键的功能。

### 常用的BASHRC配置
> alias 'ps'='ps -ef | grep -v "\[.*\]"'
export PATH=$PATH:/path/to/my/bin/

## 参考博文
[lighttpd安装配置详解-鸟哥のlinux-ChinaUnix博客](http://blog.chinaunix.net/uid-25266990-id-127946.html)
[采用Hexo在github上部署个人轻博客](http://www.jianshu.com/p/7a6f0d1451a3)
