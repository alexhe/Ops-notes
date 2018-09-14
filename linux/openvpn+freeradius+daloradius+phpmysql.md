# openvpn+freeradius+daloradius+phpmysql

[toc]

>此文档为做实验的实验笔记，在阿里云买了个低配服务器，通过openvpn在家里电脑上安装mysql和freeradius，并通过freeradius控制openvpn账号

## 编译安装openvpn

* 安装编译依赖库
    ```shell
    yum -y install gcc gcc-c++ make autoconf openssl-devel lzo-devel pam-devel
    ```

* 下载并配置编译环境
    ```shell
    cd /usr/local/src/

    # 需要翻墙，我是翻墙下载过来上传上去的
    wget https://swupdate.openvpn.org/community/releases/openvpn-2.4.6.tar.gz

    # 解压并进入目录
    tar -zxf openvpn-2.4.6.tar.gz
    cd openvpn-2.4.6

    # 配置编译选项，--prefix控制安装目录
    ./configure \
    --prefix=/opt/openvpn \
    --enable-selinux \
    --enable-systemd \
    --enable-server \
    --enable-plugins \
    --enable-management \
    --enable-multihome \
    --enable-port-share \
    --disable-debug \
    --enable-iproute2 \
    --enable-plugin-auth-pam \
    --enable-pam-dlopen \
    --enable-async-push
    ```

* 安装openvpn到/opt/openvpn目录中
    ```shell
    make && make install
    ```

* 配置环境变量
    ```shell
    vim /etc/profile   # 编辑profile
    export PATH=$PATH:/opt/openvpn/sbin/  # 在最后一行添加，然后就可以直接使用 openvpn命令了
    ```

* 添加man手册
    这步可有可无，无伤大雅
    ```shell
    vim /etc/man_db.conf  # 编辑man配置文件

    # 在MANDATORY_MANPATH文件位置添加以下字符串
    MANDATORY_MANPATH                       /opt/openvpn/share/man
    ```

* 加载内核模块
    ```shell
    lsmod | grep tun    # 查看模块是否有tunnel4和tun模块

    # 安装缺少的模块
    modprobe tunnel4
    modprobe tun

* 添加service服务
    ```shell
    cd /opt/openvpn  # 进入openvpn的安装目录目录
    cp ./lib/systemd/system/openvpn-server@.service /usr/lib/systemd/system/openvpn-server.service  # 拷贝服务文件到系统服务目录
    mkdir /etc/openvpn/server/ # 创建配置文件目录
    cp sample/sample-config-files/server.conf /etc/openvpn/server/openvpn.conf # 拷贝配置文件
