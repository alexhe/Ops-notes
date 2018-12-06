# CentOS 7 静态IP配置

## 打开网卡配置ifcfg-***

```shell
vim /etc/sysconfig/network-scripts/ifcfg-***
# 编辑 ifcfg-*** 文件，vim 最小化安装时没有被安装，需要自行安装不描述。
```

## 修改如下内容

```ini
BOOTPROTO="static"
# dhcp改为static
ONBOOT="yes"
# 开机启用本配置
IPADDR=192.168.7.106
# 静态IP
GATEWAY=192.168.7.1
# 默认网关
NETMASK=255.255.255.0
# 子网掩码
DNS1=192.168.7.1
# DNS 配置
```

## 重启下网络服务

```sh
service network restart
# 重启下网络服务
systemctl restart network
# EL7首选
ifconfig
# 查看改动后的效果
```