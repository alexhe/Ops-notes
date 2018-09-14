# 通过yum软件库安装Mysql

> 以下命令对于启用了dnf的系统，用dnf替换命令中的 yum
>
> 发布软件包安装在系统上，yum update 命令（或dnf-enabled系统的dnf升级）进行的任何系统范围的更新都会自动升级系统上的MySQL软件包，并且还会替换任何本地的第三方软件包在MySQL Yum存储库中找到替代者
>
> 默认配置文件路径：</br>
配置文件：/etc/my.cnf </br>
日志文件：/var/log//var/log/mysqld.log </br>
服务启动脚本：/usr/lib/systemd/system/mysqld.service </br>
socket文件：/var/run/mysqld/mysqld.pid</br>

## 一、安装MySQL RPM

Yum存储库添加到系统的存储库列表中

* 到MySQL存储库下载适用linux版本的发行包，[点我下载](http://dev.mysql.com/downloads/repo/yum/.)</br>
* 使用以下命令安装下载的发行包</br>

    ```mysql
    rpm -Uvh 发行包名称
    ```

## 二、选择一个mysql安装版本

> 当使用MySQL Yum存储库时，默认选择安装MySQL的最新GA版本进行安装。如果这是你想要的，你可以跳到下一步， 用Yum安装MySQL

* 查看MySQL Yum存储库中的所有子存储库，并查看其中哪些被启用或禁用

```sh
yum repolist all | grep mysql
# 查看MySQL Yum存储库中的所有子存储库，并查看其中哪些被启用或禁用
sudo yum-config-manager --disable mysql**-community
# 禁用最新的GA系列的子库
sudo yum-config-manager --enable mysql**-community
# 启用特定GA系列的子库
```

* 如若不支持yum-config-manager命令，可以通过修改etc/yum.repos.d/mysql-community.repo来解决，

```sh
vim etc/yum.repos.d/mysql-community.repo
# 打开文件,找到要配置的子库的条目，然后编辑该enabled选项,指定 enabled=0禁用子库，或 enabled=1启用子库
yum repolist enabled | grep mysql
# 验证是否已启用和禁用了正确的子库
```

> 为一个发行版系列启用子库。当启用多个版本系列的子库时，Yum将使用最新的系列

## 三、安装mysql

```sh
yum install mysql-community-server
# 安装MySQL，装MySQL服务器的软件包以及其他必需的软件包
```

## 四、启动MySQL服务器

```sh
service mysqld start
# 启动MySQL服务
systemctl start mysqld.service
# EL7的启动命令，首选
service mysqld status
# 查看MySQL服务的状态
```

## 五、开机启动mysql

```sh
systemctl enable mysqld
systemctl daemon-reload
```

## 六、MySQL服务器初始化（仅适用于MySQL 5.7)

* mysql安装完成之后，在/var/log/mysqld.log文件中给root生成了一个默认密码（初始化）。通过下面的方式找到root默认密码，然后登录mysql进行修改
    ```sql
    grep 'temporary password' /var/log/mysqld.log
    //显示初始的超级用户的密码
    mysql_secure_installation
    //初始mysql，后边可以不用操作
    mysql -uroot -p
    //使用初始密码登陆
    mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';
    mysql> set password for 'root'@'localhost'=password('MyNewPass4!');
    //更改密码，两条命令选择一条即可
    ```
* mysql5.7默认安装了密码安全检查插件（validate_password），默认密码检查策略要求密码必须包含：大小写字母、数字和特殊符号，并且长度不能少于8位。否则会提示ERROR 1819
    ```sql
    show variables like '%password%';
    //通过msyql环境变量可以查看密码策略的相关信息
    >  validate_password_policy:
    // 密码策略，默认为MEDIUM策略
    validate_password_dictionary_file：
    //密码策略文件，策略为STRONG才需要
    validate_password_length：
    //密码最少长度
    validate_password_mixed_case_count：
    //大小写字符长度，至少1个
    validate_password_number_count:
    //数字至少1个
    validate_password_special_char_count：
    //特殊字符至少1个
    ```

    共有以下几种密码策略：

    策略 | 检查规则
    ---|---
    0 or LOW | Length
    1 or MEDIUM | Length; numeric, lowercase/uppercase, and special characters
    or STRONG | Length; numeric, lowercase/uppercase, and special characters; dictionary file
    MySQL官网密码策略详细说明：[点击查看](http://dev.mysql.com/doc/refman/5.7/en/validate-password-options-variables.html#sysvar_validate_password_policy)</br>
    </br>
    修改密码策略
    ```vim
    vim /etc/my.cnf
    //打开mysql的配置文件
    validate_password_policy=0
    //添加一种密码策略，选择0（LOW），1（MEDIUM），2（STRONG）其中一种，选择2需要提供密码字典文件
    validate_password = off
    //如果不需要密码策略，添加my.cnf文件中添加这一行的配置禁用即可
    systemctl restart mysqld
    //重新启动mysql服务使配置生效：
    ```

## 七、配置默认编码为utf8

* 修改/etc/my.cnf配置文件，在[mysqld]下添加编码配置，如下所示：
    ```ini
    [mysqld]
    character_set_server=utf8
    init_connect='SET NAMES utf8'
    ```
* 重新启动mysql服务，查看数据库默认
    ```sql
    systemctl restart mysqld
    mysql -uroot -p
    //登陆sql
    show variables like 'char%';
    //查看默认数据库编码
    ```
* 更改之前创建的数据库的编码
    ```sql
    use db_name;
    //db_name改成数据库名称
    show databases;
    //查看数据库表名称
    alter database db_name CHARACTER SET utf8;
    //db_name改成数据库名称
    ```

## 远程连接设置

* 把在所有数据库的所有表的所有权限赋值给位于所有IP地址的root用户。

    ```sql
    mysql> grant all privileges on *.* to root@'%'identified by 'password';
    ```

* 如果是新用户而不是root，则要先新建用户

    ```sql
    mysql>create user 'username'@'%' identified by 'password';
    ```