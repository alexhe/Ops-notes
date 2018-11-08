[toc]

# kubernetes所需端口

> 标有*的任何端口号都是可覆盖的，因此您需要确保您提供的任何自定义端口也是打开
> 尽管主节点中包含etcd端口，但您也可以在外部或自定义端口上托管您自己的etcd集群

* Master node

|  协议  |  方向    |   港口范围      |             目的          |             使用           |
|-------|----------|---------------|---------------------------|---------------------------|
|   TCP |   入站    |   6443*       |   Kubernetes API server   |           所有            |
|   TCP |   入站    |   2379-2380   |   etcd server client API  |   kube-apiserver，etcd    |
|   TCP |   入站    |   10250       |   Kubelet API             |     本机，Control plan    |
|   TCP |   入站    |   10251       |   kube-scheduler          |           本机            |
|   TCP |   入站    |   10252       |   kube-controller-manager |           本机            |

* Worker node

|  协议  |  方向    |   港口范围      |           目的         |             使用       |
|-------|----------|---------------|------------------------|-----------------------|
|   TCP |   入站    |   10250       |   Kubelet API          |   本机，Control plan   |
|   TCP |   入站    |  30000-32767  |   NodePort Services**  |          所有          |

# 在线安装

## 配置yum源

* centos的yum源
    ```shell
    cat <<EOF > /etc/yum.repos.d/kubernetes.repo
    [kubernetes]
    name=Kubernetes
    baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
    enabled=1
    gpgcheck=1
    repo_gpgcheck=1
    gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
    EOF
    ```
* ubuntu的apt源
    ```shell
    apt-get update && apt-get install -y apt-transport-https
    curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add - 
    cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
    deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
    EOF
    ```

## 安装

* centos
    ```shell
    setenforce 0
    sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config # 设置selinux为透明模式
    yum install -y kubelet kubeadm kubectl
    systemctl enable kubelet && systemctl start kubelet # 启动kubelet
    ```
* ubuntu
    ```shell
    apt-get update
    apt-get install -y kubelet kubeadm kubectl
    apt-mark hold kubelet kubeadm kubectl  # 对软件进行安装标记
    ```

## 配置
