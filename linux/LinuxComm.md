# linux常用命令<!-- omit in toc -->

1. [rpm命令](#rpm命令)
2. [vim命令](#vim命令)
3. [yum命令](#yum命令)
    1. [el7更改yum源与更新系统](#el7更改yum源与更新系统)
4. [systemctl服务管理](#systemctl服务管理)
5. [文件操作命令](#文件操作命令)
6. [问题](#问题)

## rpm命令

命令 | 作用
-- | --
rpm -ivh filename.rpm | 安装软件的命令格式
rpm -Uvh filename.rpm | 升级软件的命令格式
rpm -e filename.rpm | 卸载软件的命令格式
rpm -qpi filename.rpm | 查询软件描述信息的命令格式
rpm -qf filename | 查询文件输入哪个RPM包的命令格式
rpm -qa | 查询已安装哪些软件
rpm -q filename.rpm | 查询指定软件是否安装

## vim命令

> vi和vim是centos自带的一个编辑器，但是要熟练使用它并不容易，vim和vi一样，只是vim支持颜色
>
> vi编辑时，有命令模式和编辑模式，进入文件时，自动在命令模式

* 命令模式进入编辑模式的六个命令：

    i  光标所在字前插入
    I  光标所在行前插入
    a  光标所在字后插入
    A  光标所在行后插入
    o  光标所在行下插入新行
    O  光标所在行上插入新行
    **按下Esc键进入命令模式**

* 常用命令：
    ```vim
    /搜索内容                       # 搜索文件中的关键字(按’n ‘键 下一个)
    :set ic                        # 忽略大小写
    :set noic                      # 取消大小写
    :%s  /(旧字符)/(新字符)/g       #  新字符替换旧字符     %s全文下 ，最后的 ‘g’为不询问是否替换，换成 ‘c’为询问是否替换
    :n1,n2s /(旧字符)/(新字符)/g    #  新字符替换旧字符     从n1到n2替换，最后的 ‘g’为不询问是否替换，换成 ‘c’为询问是否替换
    :w                             # 保存
    :wq                            # 保存退出
    ZZ                             # 快捷，保存退出
    :q!                            # 强制不保存退出
    :wq!                           # 强制保存退出(文件所有者，root用户)
    :w + 新名字                     # 另存为指定文件
    :set  nu                       # 设行
    :set  nonu                     # 取消行
    ```
* 常用编辑命令：
    ```vim
    gg                    # 跳到第一行
    G                     # 跳到最后一行
    nG                    # 到第几行    n为行数
    :n                    # 到第几行    n为行数
    $                     # 行尾
    0                     # 行首
    x                     # 删除光标处字
    nx                    # 删除光标后n个字
    dd                    # 删除光标行(也为剪切)
    ndd                   # 删除n行(也为剪切)
    dG                    # 删除光标处至文件末尾
    n1,n2d                # 删除n1至n2行
    yy                    # 复制行
    nyy                   # 复制行下n行
    p                     # 黏贴到光标行下
    P                     # 黏贴到光标行上
    r                     # 替换光标文字
    R                     # 从光标处开始一直替换，Esc结束
    u                     # 取消上一步操作
    ab  a_____    b_____  # 替换命令  输入a+空格/回车 就变为b
    ```
* 导入命令( 光标所在处 )：
    ```vim
    :r                   # 文件名(命令/路径)
    :!which              # 查看命令所在位置
    :!date               # 看时间，ps. :r !date  可以导入时间
    ```
* 连续行注释：
    ```vim
    :n1,n2s /^/#/g       # 连续注释#号
    :n1,n2s /^#//g       # 取消连续#号
    :n1,n2s /^/\/\//g    # 设置//号
    ```

* map定义：
    ```sh
    :map (ctrl+v) + 快捷键
    # 组合命令比如： :map  [ctrl+v]P,定义之后，命令模式下输入P，行前就会多个#号，ctrl+v组合键在vi编辑器里会生成一个类似 ^ 的符号
    vi /root/.vimrc
    # 永久改变命令的文件,在此文件里配置的命令，会默认在vi里自动生效，而以上编辑的命令，是退出编辑器后会失效的,
    # 比如添加：  :set nu 那么以后进入编辑器都会自动设置行号了
    ```

## yum命令

* yum下载文件保存目录
    ```sh
    /var/cache/yum/*/packages
    # 通常安装后删除，但亦可通过配置保留。配置yum.conf  keepcache选项 keepcache=1
    ```
* 常用的一些命令
    命令 | 作用
    ---|---
    yum search vim | 用Yum查找源中的VIM包，看是否已经安装VIM
    yum -y install vim* | 安装VIM,*代表版本号
    yum install epel-release -y | 安装epel源
    yum repolist all | 列出所有的仓库
    yum list all | 列出仓库中所有的软件包
    yum info 软件包名称 | 查询软件包信息
    yum reinstall 软件包名称 | 重新安装软件包
    yum update 软件包名称 | 升级软件包
    yum remove 软件包名称 | 移除软件包
    yum clean all | 清空给所有仓库缓存
    yum check-update | 检查可更新软件包的软件包
    yum grouplist | 查看系统中已经安装的软件包组
    yum groupinstall 软件包组 | 安装指定的软件包组
    yum groupremove 软件包组 | 移除指定的软件包组
    yum groupinfo 软件包组 | 查询指定的软件包组的信息
* 用yum只下载rpm包
    > 用yumdownloader就能下载rpm包了。简单快捷啊。
    ```sh
    yum -y install yum-utils
    yumdownloader filename.rpm
    ```
* 下载rpm包强制安装
    > 有时用yum自动安装会不成功时，就可以下载该rpm包后，再强制安装
    ```sh
    rpm -ivh ***.rpm --force --nodeps
    ```

* 源代码包的安装
    > .src.rpm结尾的文件由软件源代码文件组成，要安装此种 rpm包，需要用下面的命令。
    ```sh
    rpm　--recompile 文件名称
    # 编译源代码，然后安装它
    rpm　--rebuild 文件名称
    # 编译源代码，然后安装它，再把源代码包装成RPM软件包
    ```

### el7更改yum源与更新系统

1. 首先备份yum源
    ```sh
    cp /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
    ```
2. 进入yum源配置文件所在文件夹
    ```sh
    cd /etc/yum.repos.d/
    ```
3. 下载163的yum源配置文件，放入/etc/yum.repos.d/(操作前请做好相应备份)
    ```sh
    wget http://mirrors.163.com/.help/*        # 首先去163查看最新的源是哪个
    or
    curl -o http://mirrors.163.com/.help/*
    ```
4. 运行yum makecache生成缓存
    ```sh
    yum makecache
    ```
5. 更新系统(选择update,时间比较久,主要看个人网速)
    ```sh
    yum -y update
    # 升级所有包，改变软件设置和系统设置,系统版本内核都升级
    yum -y upgrade
    # 升级所有包，不改变软件设置和系统设置，系统版本升级，内核不改变
    yum –exclude=kernel* update -y
    # 有些主机的硬件并不支持最新内核，在不确定的情况下就不要升级内核了
    ```

## systemctl服务管理

System V init（REHL6) | systemctl (REHL7) | 作用
-- | -- | --
service foo start | systemctl start foo.service | 启动服务
service foo restart | systemctl restart foo.service | 重启服务
service foo stop | systemctl stop foo.service | 停止服务
service foo reload | systemctl reload foo.service | 重新加载配置文件（不终止服务）
servuce foo status | systemctl status foo.service | 查看服务状态
chkconfig foo on | systemctl enable foo.service | 开机自启动服务
chkconfig foo off | systemctl disable foo.service | 开机不自动启动服务
chkconfig foo | systemctl is-enable foo.service | 查看指定服务是否开机启动
chkconfig --list | systemctl list-unit-files fo.service | 查看各个级别下服务的启动和禁用情况

## 文件操作命令

* mkdir
    语法：
    > mkdir（选项）（参数）

    选项：
    > -Z：设置安全上下文，当使用SELinux时有效；</br>
    > -m<目标属性>或--mode<目标属性>建立目录的同时设置目录的权限；</br>
    > -p或--parents 若所要建立目录的上层目录目前尚未建立，则会一并建立上层目录；</br>
    > --version 显示版本信息。

    参数：
    > 目录：指定要创建的目录列表，多个目录之间用空格隔开。

    示例：
    > 在目录/usr/meng下建立子目录test，并且只有文件主有读、写和执行权限，其他人无权访问
    ```sh
    mkdir -m 700 /usr/meng/test
    ```
    > 在当前目录中建立bin和bin下的os_1目录，权限设置为文件主可读、写、执行，同组用户可读和执行，其他用户无权访问
    ```sh
    mkdir -p -m 750 bin/os_1
    ```

## 问题

* 不能自动补全
    情况：CentOS 7 Mini版的系统，需要使用Firewall-cmd的功能，但是在tab件补全时，发现tab不能显示命令。
    解决方法：
    1. 安装bash-completion.一般bash自带这个自动补齐的功能，但是只能自动补全命令名和文件名。而         为了大道更好的补全效果，我们需要安装bash-completion包。
        ```sh
        [root@xijia01 html]# yum -y install bash-completion
        ```
    2. 此时需要退出终端，再次连接，然后就可以使用tab键自动补全了
