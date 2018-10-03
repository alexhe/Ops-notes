[toc]

# 编译安装

* 下载文件
    ```sh
    # 可以去官网下载最新的
    wget https://download.qemu.org/qemu-3.0.0.tar.xz
    ```
* 安装需要用到的库文件
    ```sh
    sudo apt install libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev libpixman-1-dev
    or
    yum install git glib2-devel libfdt-devel pixman-devel zlib-devel
    ```
* 配置
    ```sh
    ./configure \
    --prefix=/opt/qemu-kvm \
    --datadir=/home/cc/data/kvm

# 配置环境变量

# 创建虚拟机