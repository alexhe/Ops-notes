[toc]

> 采用yum源安装，方便，也可以二进制安装，编译的话不建议了，浪费时间，如果你要研究代码的话可以编译看下

# 通过yum安装docker-ce

> 参考下这里:<https://yq.aliyun.com/articles/110806>

```sh
# step 1: 安装必要的一些系统工具
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
# Step 2: 添加软件源信息
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# Step 3: 更新并安装 Docker-CE
sudo yum makecache fast
sudo yum -y install docker-ce
# Step 4: 开启Docker服务
sudo service docker start

# 注意：
# 官方软件源默认启用了最新的软件，您可以通过编辑软件源的方式获取各个版本的软件包。例如官方并没有将测试版本的软件源置为可用，你可以通过以下方式开启。同理可以开启各种测试版本等。
# vim /etc/yum.repos.d/docker-ce.repo
# 将 [docker-ce-test] 下方的 enabled=0 修改为 enabled=1
#
# 安装指定版本的Docker-CE:
# Step 1: 查找Docker-CE的版本:
# yum list docker-ce.x86_64 --showduplicates | sort -r
#   Loading mirror speeds from cached hostfile
#   Loaded plugins: branch, fastestmirror, langpacks
#   docker-ce.x86_64            17.03.1.ce-1.el7.centos            docker-ce-stable
#   docker-ce.x86_64            17.03.1.ce-1.el7.centos            @docker-ce-stable
#   docker-ce.x86_64            17.03.0.ce-1.el7.centos            docker-ce-stable
#   Available Packages
# Step2 : 安装指定版本的Docker-CE: (VERSION 例如上面的 17.03.0.ce.1-1.el7.centos)
# sudo yum -y install docker-ce-[VERSION]
```

# 配置docker网络

* 如果要docker内容器要固定ip地址，需要创建一个network
    ```sh
    # 把ip改为相应的即可
    docker network create --attachable --driver bridge --gateway 192.168.243.1 --subnet 192.168.243.1/24 --ipam-driver default mybridge
    ```

* 不同主机之间的docker相互访问，首先要确定主机与主机之间是否互联，不能经过nat，然后在主机配置到docker网段的路由即可
    ```sh
    # linux配置路由，注意替换ip地址
    # centos7
    firewall-cmd --add-masquerade --permanent --zone=public
    firewall-cmd --reload
    ip route add 192.168.240.0/20 via 192.168.250.4
    ip route del 192.168.240.0/20 via 192.168.250.4 # 删除路由
    # centos 6
    sysctl -w net.ipv4.ip_forward=1
    route add -net 10.20.30.48 netmask 255.255.255.248 gw 10.20.30.41
    or
    route add -net 192.168.1.0/24 eth1
    route del -net 10.20.30.40 netmask 255.255.255.248 eth0 # 删除路由

    # windows配置路由
    route -p add 157.0.0.0 MASK 255.0.0.0 157.55.80.1 METRIC 3 IF 2
    # 修改删除路由
    route CHANGE 157.0.0.0 MASK 255.0.0.0 157.55.80.5 METRIC 2 IF 2 # 修改
    route delete 157.0.0.0 # 删除
    ```

# docker配置镜像加速

> docker加速网址可以去阿里云搞一个，地址是：<https://yq.aliyun.com/>

    ```sh
    mkdir -p /etc/docker
    vim /etc/docker/daemon.json
    # 添加一下内容
    {
        "registry-mirrors":["docker加速网址"]
    }
    ```

# docker daemon.json配置文件格式

官方的完整配置样式，需要根据你的需要修改

```json
{
    "authorization-plugins":h[],
    "data-root": "",
    "dns": [],
    "dns-opts": [],
    "dns-search": [],
    "exec-opts": [],
    "exec-root": "",
    "experimental": false,
    "storage-driver": "",
    "storage-opts": [],
    "labels": [],
    "live-restore": true,
    "log-driver": "",
    "log-opts": {},
    "mtu": 0,
    "pidfile": "",
    "cluster-store": "",
    "cluster-store-opts": {},
    "cluster-advertise": "",
    "max-concurrent-downloads": 3,
    "max-concurrent-uploads": 5,
    "default-shm-size": "64M",
    "shutdown-timeout": 15,
    "debug": true,
    "hosts": [],
    "log-level": "",
    "tls": true,
    "tlsverify": true,
    "tlscacert": "",
    "tlscert": "",
    "tlskey": "",
    "swarm-default-advertise-addr": "",
    "api-cors-header": "",
    "selinux-enabled": false,
    "userns-remap": "",
    "group": "",
    "cgroup-parent": "",
    "default-ulimits": {},
    "init": false,
    "init-path": "/usr/libexec/docker-init",
    "ipv6": false,
    "iptables": false,
    "ip-forward": false,
    "ip-masq": false,
    "userland-proxy": false,
    "userland-proxy-path": "/usr/libexec/docker-proxy",
    "ip": "0.0.0.0",
    "bridge": "",
    "bip": "",
    "fixed-cidr": "",
    "fixed-cidr-v6": "",
    "default-gateway": "",
    "default-gateway-v6": "",
    "icc": false,
    "raw-logs": false,
    "allow-nondistributable-artifacts": [],
    "registry-mirrors": [],
    "seccomp-profile": "",
    "insecure-registries": [],
    "no-new-privileges": false,
    "default-runtime": "runc",
    "oom-score-adjust": -500,
    "node-generic-resources": ["NVIDIA-GPU=UUID1", "NVIDIA-GPU=UUID2"],
    "runtimes": {
        "cc-runtime": {
            "path": "/usr/bin/cc-runtime"
        },
        "custom": {
            "path": "/usr/local/bin/my-runc-replacement",
            "runtimeArgs": [
                "--debug"
            ]
        }
    }
}
```