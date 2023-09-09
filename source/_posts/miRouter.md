---
title: 小米路由器Mini配置汇总
layout: post
date: 2016-10-07 23:00
tags: [tutorial]
cdn: 'header-off'
header-img: "/imgs/default-post-cover.jpg"
subtitle: "Management and Configuration for Xiaomi Router Mini"
author: "Leon Dong"
---

[1]: http://www.miwifi.com/miwifi_download.html
[2]: http://www.miui.com/thread-2600824-1-1.html
[3]: http://bbs.xiaomi.cn/t-10437841
[4]: http://downloads.openwrt.org.cn/PandoraBox/Xiaomi-Mini-R1CM/
[5]: http://pan.baidu.com/s/1bX2dEQ
[6]: http://tieba.baidu.com/p/3618514879
[7]: http://pan.baidu.com/s/1bpaNRt1
[8]: http://luyou.xunlei.com/thread-2216-1-1.html
[9]: /figs/default/thunder.jpg
[10]: http://yuancheng.xunlei.com


## 刷入 Openwrt

小米路由器要刷openwrt的话，主要分成以下几步：
- 首先去[小米路由器官网][1]下载最新的开发版固件，把路由器固件升级成开发版系统，只要在你的路由器设置菜单里面选择手动升级系统即可，具体请参考[这里][2]
- 刷好开发版后，用手机连接路由器，下载小米路由器APP，安装打开，按步骤绑定你的路由器（和你的小米账号绑定），之后就可以下载SSH工具了
- 接下来去[小米路由器官网][1]，点击开放下面的开启SSH工具，下载SSH工具包，刷入路由器（将SSH文件放在U盘根目录，按住路由器上的reset重启刷入），开启SSH权限，具体过程可以参考[这里][3]

至此，你的准备工作已经完毕。因为这一部分网上的教程实在太多了，而且一般也不会有什么坑，所以就不仔细介绍了。

接下来，去openwrt中文网下载小米的[openwrt固件][4]，建议选择里面的stable版本，在2016年10月7日时有两个稳定版本r512和r1024. r1024版本比较纯净一点，基本上只集成了一些基本的功能，空闲空间大，比较适合老手折腾。r512版本集合了shadowsocks，transmission，迅雷等工具，更方便使用。而且实测过程中r512版本在折腾的过程中不太会出现莫名其妙的错误（后面会有一些解释），对于自己想加入Python等功能的来说也更方便配置。由于openwrt中文网貌似不太稳定，有时候上不去。为此，我把两个版本的固件上传到了[百度云][5]，欢迎下载。

下载好固件之后，就是要利用WINSCP等工具把固件传到路由器里面，如果熟悉Linux的话也可以使用scp命令。一般来说可以放到`/tmp`下面，貌似这里是挂在RAM上的，所以空间还比较大，具体可参考[百度贴吧][6]。接下来，利用SSH工具进入小米路由器，输入命令
```bash
mtd -r write /tmp/PandoraBox_r1024.bin firmware
```
然后坐等系统重启，openwrt就刷好啦。不过可能上述命令无法执行（估计路由器出厂批次不同的问题），提示`couldnot open mtd device：firmware cant open device for writing`错误，这个时候吧上面的最后一个firmware更改成OS1即可刷入。

## 安装 Python

路由器安装了Python之后可玩性就大大增加了，对于动手能力强的programmer可以玩出很多花样，128MB的内存也足够大部分Python程序运行了。在安装python前，得先插个U盘，因为python总体来说占用空间比较大，直接往ROM那剩余的几个MB里面安装可能空间不够，另外以后安装其他软件就会比较麻烦。插完U盘后建议设置一下挂载点（用HUB挂多个设备容易区分），这个可以参考后面的**自定义挂载点**部分。
为了将程序安装进入我们的外置U盘，还需要编辑openwrt包管理器opkg的配置文件`/etc/opkg.conf`。这里面主要有两个地方需要修改

> dest root /
dest ram /tmp
lists_dir ext /usb/opkg-lists  # 1 建议修改这一行
option overlay_root /overlay
dest usb /usb/opkg/　# 2 添加这一行
src/gz r2_base http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/base
src/gz r2_management http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/management

第一个地方是我建议修改的，这样使用`opkg update`之后，可以把软件仓库的信息保存的USB设备里面，以后就不用每次重启都要更新了，况且还可能突然连不上这个官方的软件源。第二个地方是必须添加的，后面的路径 `/usb/opkg`改成你U盘里面的某一个文件夹的路径即可。
接下来，执行`opkg update`更新软件源。完成后，依次输入以下指令即可完成python的安装。
```bash
Wget http://downloads.openwrt.org.cn/PandoraBox/ralink/packages/base/libc_0.9.33.2-1_ramips_24kec.ipk
opkg -d usb install libc_0.9.33.2-1_ramips_24kec.ipk # 标注
opkg -d usb install libreadline
opkg -d usb install python
opkg -d usb install python-json
opkg -d usb install python-curl
opkg -d usb install python-openssl
```
上面的标注表示手动安装libc，貌似opkg包管理器无法自动安装，所以我们先用wget下载下来，然后本地安装（r1024版本默认已安装）。接下来几行命令都是依次从软件源里面安装相应的软件，如果有依赖的软件也会自动安装。安装完了之后别急着输入python，因为我们把python安装到了usb设备上面，所以需要配置一下链接库的路径来让系统找到python所需要的链接库在哪里。简单来说就是将下面两行添加到`/etc/profile`文件中。

> export PATH=$PATH:/usb/opkg/usr/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usb/opkg/usr/lib

添加完了之后执行`source /etc/profile`即可完成环境配置，这时候可以运行python来测试效果了。值得一提的是，第二行并不是所有情况都需要的，我在用r512固件是只加了第一行（网上大部分教程都是这样）就可以运行了。但是在r1024固件里面，会提示错误`can't open zlib.so.1`，最后找了很久的教程才找到是链接库路径的问题，添加上之后就完事了，总体来说安装python还是比较简单的。

## 安装 PPTP-VPN 服务器

在PandoraBox的软件库里面有PPTP-VPN服务器安装包，分别是

> pptpd - 1.4.0-1 - PopTop pptp server
pptpd-pandorabox - 1.4.0-1 - Modified PopTop pptp server.

个人建议直接安装第二个，貌似是针对PandoraBox进行了相应的优化，而且配置起来也非常简单。输入命令`opkg install pptpd-pandorabox`完成软件安装，值得一提的是不建议将这种服务级别的软件安装到USB里面去。一个原因是配置起来会比较麻烦，第二个是开机启动可能会失败。

安装完PPTP-VPN之后就是配置了，其配置文件为`/etc/config/pptpd`，用vim打开该文件，主要写入以下配置

> config service 'pptpd'
        option 'enabled' '1' # 设置为启用
        option 'localip' '192.168.0.1' # 设置PPTP网段IP
        option 'remoteip' '192.168.0.20-50' # 设置PPTP客户端的IP范围
        list 'dnssvrs' '192.168.1.1'  # 手动配置PPTP客户端的DNS服务器，可以忽略
config 'login' #配置一个用户
        option 'username' 'user'
        option 'password' 'pwd123'

配置完了PPTP-VPN服务器之后，还需要让VPN所处的网段`192.168.0.0/24`能通过路由器所处的网段进行上网，这需要借助于`iptables`。具体的设置只需要在用户防火墙配置文件`/etc/firewall.user`里面添加如下配置

> iptables -A forwarding_rule -s 192.168.0.0/24 -j ACCEPT # 接受转发
iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -j MASQUERADE  # 实现NAT网络转发
iptables -A INPUT -p gre -j ACCEPT #接受GRE协议

之后就可以利用命令`/etc/init.d/pptpd start`开启PPTP服务器即可。


## 安装迅雷远程下载

首先你需要去迅雷远程下载的[官网][8]下载相应的安装包，如果你的路由器也是小米路由Mini的话，可以直接在[百度云][7]里面下载即可。下载完之后，同样利用WINSCP或scp命令等方式将该文件传入路由器的一个目录（最好就是你将要安装的地方）里面，这里拿`/usb/app/`举例。利用`cd`命令进入该目录，输入`unzip Xware_1031.zip`便可以得到一堆文件。

这里面只有一个可执行文件portal，在命令行里面输入`./portal`即可运行迅雷了，命令的输出大概如下图所示

![portal run result][9]

注意这里面的`THE ACTIVE CODE IS: tgnudq`，复制这个激活码 tgnudq，打开[迅雷远程官网][10], 输入该激活码绑定该设备即可, 如果需要停止迅雷服务，在命令行输入`./portal -s`即可停止迅雷服务。如果你经常使用PT下载站，建议使用transmission来下载，迅雷一般是被屏蔽掉的。

## 其他设置

### U盘格式的问题

PandoraBox支持exFAT,ext4等文件系统，所以对于外置U盘可以选择很多文件系统。但是比较推荐的还是ext4文件系统，不推荐使用NTFS系统，因为这个在Linux里面可能性能表现会非常差。比较推荐的还是使用EXT系列的文件系统，这里就拿最新的ext4举例子。

首先是给U盘分区，直接输入`fdisk /dev/sdb`进行分区，具体的分区方式可以查看命令里面的帮助，文件系统的类型选择83-Linux即可。分完区后，利用`mkfs.ext4 ^has_hournal,extent /dev/sd1`对得到的分区进行格式化。值得一提的是，由于ext4是日志型文件系统，对U盘的损失可能比较大，所以需要加入`^has_hournal`参数禁用日志即可。

EXT4文件系统默认会占用一部分空间作为inode的信息存储使用，因此在U盘格式化成ext4文件系统后，可能有MB级别的数据占用，这个属于正常情况。

### 静态IP和DNS

当你的路由器里面安装了一些服务软件的时候（例如Web服务，VPN服务），你可能希望你的路由器有一个固定的IP地址，但是你的上层网络可能采用的DHCP的方式给你分配的IP地址，所以有的时候对网络进行了一些改动之后，IP地址可能会发生变化。为了固定IP，可以在`/etc/config/network`里面直接进行设置

> config interface 'wan'
        option ifname 'eth0.2'
        option proto 'static'
        option macaddr 'f0:b4:29:d8:0d:1d'
        option ipaddr 'xxx.xxx.xxx.xxx' # 你需要的静态IP
        option netmask '255.255.255.0'
        option gateway 'xxx.xxx.xxx.xxx' # 网关地址
        option dns 'xxx.xxx.xxx.xxx' # Dns 服务器地址

配置完成后，输入`/etc/init.d/network restart`即可生效。

### Samba服务用户设置

PandoraBox默认是集成了Samba服务的，也就是说你可以在Windows系统里面以网上邻居的方式直接访问路由器的数据。你可以在配置文件`/etc/config/samba`里面加入如下配置来启用一个共享

> config sambashare
        option auto '1'
        option name 'dong'
        option path '/usb'
        option read_only 'no'
        option guest_ok 'no'
        option create_mask '0666'
        option dir_mask '0755'

一般情况下，我们是不希望该共享是公开的，也就是说需要密码进行访问。但是当你输入你用来登陆路由器的账号密码之后，却发现无法登陆，原因是samba的用户密码是区别于系统的用户密码的。为了添加一个有效的samba用户可以使用`smbpasswd -a [username]`命令。系统将会提示为该用户设置samba密码，之后你便可以使用该用户进行登陆了。

### 自启动脚本

PandoraBox内部有一个开机自己脚本`/etc/rc.local`，将自己想执行的命令放入该脚本中，便可以起到开机自启的效果。值得注意的是，在启动的脚本的第一行最好需要添加命令`source /etc/profile`对环境变量进行更新，否则装在usb里面的程序可能无法执行，例如先前说到的Python。

还有一个问题就是，由于USB加载可能比自启脚本还要慢，当自启脚本里面使用了USB里面安装的软件时候，可能会因此导致运行失败，因此需要在命令之间加入`sleep xx`强制让脚本等待xx秒来让USB存储系统初始化完成。

> sleep 10
source /etc/profile
nice -n 12 /etc/init.d/pptpd start
nice -n 13 /etc/init.d/samba start
nice -n 13 /etc/init.d/vsftpd start
nice -n 15 /usb/xware/portal > /tmp/ThunderInfo
sleep 40
nice -n 12 python /usb/dong/code/checker.py &
python /usb/dong/code/reportIP.py &
date >> /tmp/dong_StartInfo.log
echo "Finished start rc.local" >> /tmp/StartInfo.log

上面是我使用的开机脚本，由于ftp和samba以及pptp等服务可能对CPU造成较大的负担（例如连着PPTP-VPN下载东西），启动脚本里面利用了`nice -n xx [command]`命令来让command以xx的调度优先级进行启动。当该值比较大的时候，优先级低，系统不容易卡死。


### Crontab 配置

Crontab可以让你周期性的执行某一个任务，而不需要你手动的进行启动。只要定义时间规则系统就可以自动执行相应的命令，例如

> 58 23 * * * . /etc/profile; /usb/dong/script/daily.sh

该脚本表示在每天的23：58分执行daily脚本，注意中间的`. /etc/profile;`部分，由于该脚本调用了装在USB里面的python，在执行时必须有相应的环境变量支持，因此必须加入该配置。

### 系统文件夹剖析

在这些配置过程中，我们使用的最多的就是/etc文件夹，里面涵盖了系统所有的配置。其中`config`里面包含了所有服务的配置文件，例如PPTP-VPN、NETWORK、FTP、SAMBA等等。
`init.d`里面包含了所有服务的控制脚本，因此我们可以使用`/etc/init.d/vsftp start`来启动FTP服务，类似的指令还有`start|stop|enable|disable`。
`rc.d`里面包含了所有开机启动服务的控制脚本的符号链接，在这里可以取消一些程序的开机启动，或者关闭它自己利用`nice`命令和开机启动脚本开启服务。
`crontabs`里面包含了所有用户的cron任务规划配置，当然一般情况下我们可以使用`crontab -e`直接进行编辑。

## 参考博文及文献

[Linux系统添加crontab任务无效的问题解决方案](http://blog.csdn.net/zhubin215130/article/details/43271835)
[linux目录结构详细介绍](https://my.oschina.net/u/1429171/blog/507965)
[USB挂载& U盘启动](http://www.tuicool.com/articles/IJ32maI)
[openwrt挂载USB存储设备](http://www.360doc.com/content/14/1012/17/4171006_416337800.shtml)
[openwrt 安装PPTP VPN服务](http://www.openwrt.org.cn/bbs/forum.php?mod=viewthread&tid=1081)
[路由mini安装OpenWRT源的Transmission插件](http://www.miui.com/forum.php?mod=viewthread&tid=2093928)
[详细教程，添加迅雷固件Xware实现远程下载 ](http://www.right.com.cn/forum/thread-135843-1-1.html)
[OpenWrt 进程启动过程分析及添加自启动脚本](http://blog.csdn.net/rudyn/article/details/40455413)







