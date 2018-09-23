# firewall防火墙配置

> 启用服务的时候，可以通过 /usr/lib/firewalld/services/ 目录查看相应服务配置， 在 /etc/firewalld/services/ 这个目录中也有配置文件,这个要优先之前的那个

## 常用

* 启动|关闭|重新启动|查看防火墙

    ```sh
    systemctl [start|stop|restart|status] firewalld.service
    ```

* 更新防火墙规则

    ```sh
    firewall-cmd --reload
    firewall-cmd --complete-reload
    # 两者的区别就是第一个无需断开连接，就是firewalld特性之一动态添加规则，第二个需要断开连接，类似重启服务
    ```

## 自定义开启/关闭/查看端口

* 开启端口

    ```sh
    firewall-cmd --zone=public --permanent --add-port=8080/tcp
    1、firwall-cmd：   # 是Linux提供的操作firewall的一个工具；
    2、--permanent：   # 永久生效，没有此参数重启后失效；
    3、--add-port：    # 添加端口，格式为：端口/通讯协议；
    4、--zone=public： # 作用域
    ```

* 关闭端口

    ```sh
    firewall-cmd --permanent --zone=public --remove-port=8080/tcp
    ```

* 查看端口
    > 查看8080端口是否开启
     ```sh
    firewall-cmd --query-port=8080/tcp
    ```
    > 通过配置文件查看端口配置
    ```sh
    vim /etc/firewalld/zones/public.xml
    # 查看public区的配置
    ```