---
title: Ubuntu14.04 搭建 IPSec VPN
layout: post
date: 2017-04-09 12:30
tags: [tutorial]
math: 'no'
cdn: 'header-off'
header-img: "/imgs/default-post-cover.jpg"
subtitle: "Set up IPSec VPN in Ubuntu 14.04"
author: "Hailiang Dong"
---

[1]:https://my.oschina.net/isnail/blog/363151
[2]:https://linux.cn/article-3409-1.html
[3]:http://www.miui.com/thread-7026709-1-1.html
[4]:http://www.server110.com/linux/201310/2201.html
[5]:https://github.com/xelerance/Openswan/issues/75
[6]:http://www.linuxdiyf.com/linux/29184.html
[7]:https://tieba.baidu.com/p/4330272360
[8]:http://jingyan.baidu.com/article/cb5d610500dcfa005c2fe080.html
[9]:http://blog.csdn.net/fxismonk/article/details/50826452
[10]:http://www.zhujiceping.com/20148.html


## 背景
现在PPTP-VPN已经不安全了，虽然[搭建PPTP服务][1]很简单，安全对于我们一般用户来说也不说很在意，但是比较麻烦的是MAC OSX以及IOS的最新版本已经强制将PPTP服务从系统中移除，无法使用之前便捷的VPN服务，因此搭建一个新一代安全的VPN服务还是很有必要的。

## L2TP/IPsec VPN的问题
其实一开始的时候，我是打算搭建L2TP服务器的。就个人了解来说，这个用的还比较广，听得比较多，自然认为搭建比较简单，也找到了一些很[官方的教程][2]，但是接下来一堆坑就出现了。

搭建到一半，[IPsec的验证就失败][6]，在百度上查询相应的错误，得知是缺少必要的软件包。 不过我安装了之后依旧无法通过验证，网上也没找到相关的配置教程（可能是不同电脑不一样）。最后发现配置一下软件包`rng-tool`，将`/etc/default/rng-tools`的配置改成`HRNGDEVICE=/dev/urandom`才能正常通过验证。成功搭建完毕后，搭建好的VPN无法成功启动，具体原因是我的系统是Ubuntu14.04的，教程是为12.04设计的，相应的软件包版本不一样，而且Ubuntu 14.04里面的默认源里面的openswan貌似[还有BUG][4]，于是乎进一步在[Github上][5]找到了这个问题，更改了一下配置才解决该问题。

终于可以连接后，我发现只有WINDOWS可以100%成功链接，我的安卓机子一个可以连接(MIUI8 ANDROID 5.1)，一个不行(MIUI8 ANDROID 6.0)，这个问题不止我一个人遇到，可以参考[这里][3]。搭建好后拿室友的Iphone测试了一下可以连接，结果当我女朋友想用她的手机连接的时候又不知道怎么就挂了，再次拿室友的Iphone测试，竟然也不行了。

总之，L2TP部署中遇到太多的坑了，于是去网上了解了一下别的VPN，发现IPsec非常符合我的要求，因为我的主要目的就是为我女朋友（苹果系列，不支持PPTP）搭建一个可以使用的VPN服务器。

## IPsec部署 - 苹果&安卓
如果你部署的服务器仅仅想提供给安卓，苹果以及MAC用户使用的话，那其实还是很简单的，因为他们都可以用XAUTH的方式进行认证。

话不多说，直接开始具体的配置过程。首先，你需要安装一些软件包，使用这个命令即可：
```
apt-get install strongswan strongswan-plugin-xauth-generic
```
安装完之后你的系统应该就可以运行`ipsec`命令了，这个就是你的VPN服务的控制程序了。不过先别急，为了能提供VPN服务，你还需要进行配置。

首先配置IPsec连接，利用`vim`或者其他工具编辑配置文件`/etc/ipsec.conf`，填入以下配置
```
config setup
    cachecrls=yes
    uniqueids=yes
conn ios_android
    keyexchange=ikev1
    authby=xauthpsk #支持上述所有客户端，不支持WINDOWS
    xauth=server
    left=xxx.xxx.xxx.xxx  # 外网IP
    leftsubnet=0.0.0.0/0
    right=%any
    rightdns=223.5.5.5
    rightsourceip=10.0.15.0/24 # 别人连接你的VPN，你分配给他的内部IP地址段
    auto=add
```
接下来，配置你的连接密钥已经客户的用户名密码信息，编辑文件`/etc/ipsec.secrets`,填入以下配置
```
: PSK "miyao"
test : XAUTH "pwd"
```
到这里你就完成所有的配置了。是的，你没有听错，真的是相当的简单。接下来，执行命令`ipsec start`即可启动VPN服务，理论上应该是没有什么错误的。

对于安卓来说，连接方式可以参考[这里][7]，具体要主要类型要选择`IPsec XAUTH PSK`， 预共享密钥就是miyao，账号密码就是上面的test和pwd，服务器地址你服务器的外网IP。

对于苹果(MAC IOS)用户来说也是一样的，可以参考[这里][8]，填写方法和安卓一样，类型选择`Cisco IPsec`， 群组名称可以不填。

## 兼容 Windows (WP)
如果想让你的VPN服务器同时能兼容Windows客户端，这个就很复杂了。Windows要求以证书的形式验证服务器的安全性，想要连接的话还必须要导入一个证书，然后服务端也需要相应的进行一些更改，下面来具体一步步的分析。

### 服务端部署 - 认证方式
为了让IPsec能支持Windows，我们还需要安装一个插件，以支持微软的认证方式`eap-mschapv2`
```
sudo apt-get install strongswan-plugin-eap-mschapv2
```
一开始我以为之前安装的strongswan已经自带了，并且很多教程也没有提到这个事情（因为他们都是直接编译源码安装的strongswan，直接开启了`eap-mschapv2`支持）。通过查看系统日志`/var/log/syslog`发现每次连接的时候都会出现`error loading eap-mschapv2` 才意识到这个问题。

除了认证方式的问题，还有一大堆关于证书的问题要解决，windows客户端连接不仅仅需要用户密码以及密钥的认证，还需要证书的认证，具体的原理我暂时也没有弄得很清楚，这里引用别人博客里面关于证书配置的内容

###  服务端部署 - 证书配置( 转自[这里][9])
每一个完整的 ssl 证书都有一个公钥和一个私钥。公钥是在网络上传输的，而私钥是藏好用来和接收到的公钥配对的（因此私钥里也有整个公钥，用来配对）。
生成CA证书的私钥，并使用私钥，签名CA证书
```
ipsec pki --gen --outform pem > ca.pem
ipsec pki --self --in ca.pem --dn "C=CN, O=VPN, CN=StrongSwan CA" --ca --lifetime 3650 --outform pem >ca.cert.pem
```
这里C 表示国家名，同样还有 ST 州/省名，L 地区名，STREET（全大写） 街道名。O 表示组织名。CN 为通用名

生成服务器证书所需的私钥,并用CA证书签发服务器证书
```
ipsec pki --gen --outform pem > server.pem
ipsec pki --pub --in server.pem | ipsec pki --issue --lifetime 1200 --cacert ca.cert.pem \
    --cakey ca.pem --dn "C=CN, O=VPN, CN=vpn.linsir.org" \
    --san="x.x.x.x" --san="vpn.linsir.org" --flag serverAuth --flag ikeIntermediate \
    --outform pem > server.cert.pem
```
这里C、O的值要跟第一步的一致，CN值及--san值是服务器公网地址或url,另外这里可以设置多个--san值。否则会出现错误 13801:IKE身份验证凭证不可接受.

生成客户端证书
```
 ipsec pki --gen --outform pem > client.pem
     ipsec pki --pub --in client.pem | ipsec pki --issue --cacert ca.cert.pem \
    --cakey ca.pem --dn "C=CN, O=VPN, CN=VPN Client" \
    --outform pem > client.cert.pem
```
这里C、O的值要跟第一步的一致

生成 pkcs12 证书 pkcs12 证书用来导入手机或电脑的，**这个过程会让你输入密码，到时候客户端导入证书时需要输入**
```
openssl pkcs12 -export -inkey client.pem -in client.cert.pem -name "VPN Client"\
         -certfile ca.cert.pem -caname "vpn.linsir.org"  -out client.cert.p12
```
安装证书
把证书复制到strongswan目录下。
```
cp -r ca.cert.pem /etc/strongswan/ipsec.d/cacerts/
cp -r server.cert.pem /etc/strongswan/ipsec.d/certs/
cp -r server.pem /etc/strongswan/ipsec.d/private/
cp -r client.cert.pem /etc/strongswan/ipsec.d/certs/
cp -r client.pem /etc/strongswan/ipsec.d/private/
```
### 服务端部署 - 配置文件
配置完证书后，服务端只需要再增加一个提供给windows的链接以及相应的用户和密码，具体如下。
首先在`/etc/ipsec.conf`中加一个新的连接
```
conn win7
    keyexchange=ikev2
    ike=aes256-sha1-modp1024!
    rekey=no
    left=xxx.xxx.xxx.xxx  # 外网IP
    leftauth=pubkey
    leftsubnet=0.0.0.0/0
    leftcert=server.cert.pem
    right=%any
    rightauth=eap-mschapv2
    rightdns=223.5.5.5
    rightsourceip=10.0.15.0/24
    rightsendcert=never
    eap_identity=%any
    auto=add
```

其次更改密钥文件
```
: PSK "miyao"
: RSA server.pem  # 证书验证

test: XAUTH "pwd"
win: EAP "pwd"  # for windows login
```
这样就可以完成所以服务端的配置了。

### Win 系列客户端连接
Win系列（包括Windows7以上，WP等系统）直接采用内建的ikev2方式进行连接。不过在连接前必须导入之前生成的`client.cert.p12`文件，具体的配置方式可以参考[这里][10]。WindowsXp及以下的系统需要借助第三方软件 Shrew Soft VPN Client 。

## 总结
总的来说，Cisco IPSec 的配置还是相对比较简单的，如果只要兼容IOS以及安卓，那么配置可以在10分钟内完成，而且连接速度又快又稳定。为了兼容Windows客户端，也可以在搭建一个PPTP服务器，同时运行两个VPN服务端，教程可以参考[这里][1]。

在程序运行中，可以随时运行命令`ipsec statusall`查看当前的连接情况。

## 参考文献
[使用 Strongswan 架设 Ipsec VPN CSDN](http://blog.csdn.net/zzsfqiuyigui/article/details/39533479)
[使用 Strongswan 架设 Ipsec VPN opensuse ](https://zh.opensuse.org/index.php?title=SDB:Setup_Ipsec_VPN_with_Strongswan&variant=zh)
[CentOS7下Strongswan架设IPSec-CSDN.NET](http://blog.csdn.net/fxismonk/article/details/50826452)
[Ubuntu 14.04 搭建 Cisco IPSec VPN 服务器教程- CSDN.NET](http://blog.csdn.net/infsafe/article/details/45041969)