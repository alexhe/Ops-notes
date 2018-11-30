# kvm学习笔记

1. [kvm学习笔记](#kvm学习笔记)
    1. [编译安装qemu](#编译安装qemu)
    2. [配置环境变量](#配置环境变量)
    3. [创建虚拟机](#创建虚拟机)
    4. [优化KVM](#优化kvm)
        1. [CPU优化](#cpu优化)
        2. [内存优化](#内存优化)

## 编译安装qemu

- 下载文件
    ```sh
    # 可以去官网下载最新的
    wget https://download.qemu.org/qemu-3.0.0.tar.xz
    ```
  
- 安装需要用到的库文件
    ```sh
    sudo apt install libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev libpixman-1-dev
    or
    yum install git glib2-devel libfdt-devel pixman-devel zlib-devel
    ```
  
- 配置
    ```sh
    ./configure \
    --prefix=/opt/qemu-kvm \
    --datadir=/home/cc/data/kvm

## 配置环境变量

## 创建虚拟机

## 优化KVM

### CPU优化

1. 要考虑CPU的数量问题，所有guestcpu的总数目不要超过物理机CPU总数目，如果超过，则将对性能带来严重影响，建议选择复制主机CPU配置。

### 内存优化

1. KSM（kernel Samepage Merging）相同页合并
    - 内存分配的最小单位是page（页面），默认大小是4KB，可以将host主机内容相同的内存合并，以节省内存的使用。
  
    - 当KVM上运行许多相同系统的客户机时，客户机之间将有很多内存页是完全相同的，特别是只读的内核代码页完全可以在客户机之间共享，从而减少客户机占用的内存资源，也能同时运行更多的客户机。
  
    - 使用KSM存在性能损失，在一般的环境中，性能损失大概是10%，这也是在某些环境中关闭KSM的原因。在什么时候开启KSM？
        - 如果目标是运行尽可能多的虚拟机，而且性能不是问题，应该保持KSM处于运行状态。例如KSM允许运行30个虚拟机的主机上运行40个虚拟机，这意味着最大化硬件使用效率。
        - 如果服务器在运行相对较少的虚拟机并且性能是个问题时，那么应该关闭KSM。
  
    - KSM文件目录：
        ```bash
        ls /sys/kernel/mm/ksm/
        总用量 0
        -r--r--r--. 1 root root 4096 11月 30 17:05 full_scans           # 对可合并的内存区域扫描过的次数
        -rw-r--r--. 1 root root 4096 11月 30 17:05 max_page_sharing
        -rw-r--r--. 1 root root 4096 11月 30 17:05 merge_across_nodes
        -r--r--r--. 1 root root 4096 11月 30 17:05 pages_shared         # 记录合并后共有多少内存页
        -r--r--r--. 1 root root 4096 11月 30 17:05 pages_sharing        # 记录有多少内存页正在使用被合并的共享页，不包括合并的内存页本身
        -rw-r--r--. 1 root root 4096 11月 30 17:05 pages_to_scan        # 决定每次扫描多少个页面默认是100，越大越好，超过2000无效，需要开启两个服务ksmtuned和tuned,支持更多页面
        -r--r--r--. 1 root root 4096 11月 30 17:05 pages_unshared       # 因为没有重复内容而不能被合并的内存页数量
        -r--r--r--. 1 root root 4096 11月 30 17:05 pages_volatile       # 因为内容很容易变化而不能被合并的内存页数量
        -rw-r--r--. 1 root root 4096 11月 30 17:05 run                  # 查看是否开启KSM，0为关闭，1为开启,临时开启 echo 1 > run 2为停止ksmd并分离已合并的内存页
        -rw-r--r--. 1 root root 4096 11月 30 17:05 sleep_millisecs      # 决定多长时间扫描一次
        -r--r--r--. 1 root root 4096 11月 30 17:05 stable_node_chains
        -rw-r--r--. 1 root root 4096 11月 30 17:05 stable_node_chains_prune_millisecs
        -r--r--r--. 1 root root 4096 11月 30 17:05 stable_node_dups
        -rw-r--r--. 1 root root 4096 11月 30 17:05 use_zero_pages
        ```
  
    - 开启KSM

2. 对内存设置限制