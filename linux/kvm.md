# kvm学习笔记 <!-- omit in toc -->

1. [查看是否支持kvm虚拟化](#查看是否支持kvm虚拟化)
2. [编译安装qemu和libvirt（未完成）](#编译安装qemu和libvirt未完成)
3. [YUM安装](#yum安装)
4. [libvirt配置文件](#libvirt配置文件)
   1. [主机xml配置文件](#主机xml配置文件)
5. [管理工具](#管理工具)
   1. [qemu-img](#qemu-img)
   2. [virsh](#virsh)
   3. [virt-manager](#virt-manager)
   4. [virt-install](#virt-install)
   5. [virt-viewer](#virt-viewer)
   6. [guestfish](#guestfish)
   7. [GNOME Boxes](#gnome-boxes)
   8. [其他工具](#其他工具)
6. [优化和介绍KVM](#优化和介绍kvm)
   1. [CPU优化](#cpu优化)
   2. [内存优化](#内存优化)
   3. [I/O等设备使用半虚拟化设备](#io等设备使用半虚拟化设备)
   4. [磁盘&存储](#磁盘存储)
   5. [KVM网络](#kvm网络)

## 查看是否支持kvm虚拟化

1. CPU必需支持虚拟化，可以在/proc/cpuinfo文件中想找flags，如果是inter的显示为vmx，amd的显示为svm
2. CPU必需支持64位操作系统，可以在上述文件中查找lm标记，如果有则支持
3. 系统必需为64为的RHEL，且系统版本为RHEL6.4及以上为最佳
4. 必需在BIOS里开启CPU的VT功能

## 编译安装qemu和libvirt（未完成）

* 下载文件
    ```sh
    # 可以去官网下载最新的
    wget https://download.qemu.org/qemu-3.0.0.tar.xz
    ````
  
* 安装需要用到的库文件
    ```sh
    yum install git glib2-devel libfdt-devel pixman-devel zlib-devel bzip2-devel libaio-devel spice-server-devel spice-protocol libusb-devel usbredir-devel
    ```
  
* 编译安装
    ```sh
    ./configure \
    --prefix=/opt/qemu-kvm \
    --datadir=/home/data/kvm \
    --target-list=i386-softmmu,x86_64-softmmu \
    --enable-system \
    --disable-debug-info \
    --enable-usb-redir \
    --enable-libusb \
    --enable-spice \
    --enable-uuid \
    --enable-kvm \
    --enable-bzip2 \
    --enable-linux-aio \
    --enable-tools

    make -j4
    make install
    ```

* 创建环境变量和添加sytemd服务

## YUM安装

> centos默认存储库的版本过低，添加virt存储库，然后通过yum安装

* 添加qemu扩展存储库

    ```sh
    yum install centos-release-qemu-ev
    ```
* 安装qemu和libvirt

    ```sh
    yum install qemu-kvm libvirt -y
    ```

## libvirt配置文件

> libvirt的默认配置文件在：`/etc/libvirt`
> libvirt的默认工作区在：`/var/cache/libvirt`

### 主机xml配置文件

> 验证xml文件`virt-xml-validate /path/to/XML/file`
> [官方文档](https://libvirt.org/drvqemu.html#xmlconfig)

1. 通用根配置文件

    ```xml
    <domain type='kvm' id='1'>
        <name>MyGuest</name>
        <uuid>4dea22b3-1d52-d8f3-2516-782e98ab3fa0</uuid>
        <genid>43dc0cf8-809b-4adb-9bea-a9abb5f3d90e</genid>
        <title>A short description - title - of the domain</title>
        <description>Some human readable description</description>
        <metadata>
            <app1:foo xmlns:app1="http://app1.org/app1/">..</app1:foo>
            <app2:bar xmlns:app2="http://app1.org/app2/">..</app2:bar>
        </metadata>
        ......
    <domain>
    ```
    * 根元素`domain`有两个属性，`type`代表虚拟机的管理程序，有`kvm`，`xen`,`qemu`,`lxc`和`kqemu`；`id`代表正在运行的虚拟机唯一整数标识符，非活动的虚拟机没有id
    * `name`
        虚拟机的名称，同一个物理机器唯一
    * `uuid`
        全局唯一标识符，格式必须符合RFC 4122，如果在定义/创建新guest时省略，则会生成随机UUID。也可以通过[sysinfo](https://libvirt.org/formatdomain.html#elementsSysinfo)规范提供uuid
    * `genid`
        和`uuid`元素一样。
    * `title`
        可选元素title为虚拟机的简短描述，不应包含任何换行符。
    * `description`
        description元素为虚拟机的详细描述，libvirt不以任何方式使用此数据，它可以包含用户想要的任何信息
    * `metadata`（没理解）
        The metadata node can be used by applications to store custom metadata in the form of XML nodes/trees. Applications must use custom namespaces on their XML nodes/trees, with only one top-level element per namespace (if the application needs structure, they should have sub-elements to their namespace element)

2. 虚拟机系统启动相关

    > 有许多不同的方法可以启动虚拟机，每种方法各有利弊。

    1. bios启动
        > 通过BIOS引导可用于支持完全虚拟化的虚拟机管理程序。在这种情况下，BIOS具有引导顺序优先级（软盘，硬盘，cdrom，网络），用于确定获取/查找引导映像的位置。
        ```xml
        ...........
        <os>
            <type arch='x86_64' machine='pc-q35-rhel7.5.0'>hvm</type>
            <loader readonly='no' secure='no' type='rom'>/usr/share/OVMF/OVMF_CODE.fd</loader>
            <nvram>/home/cc/.config/libvirt/qemu/nvram/windows_VARS.fd</nvram>
            <boot dev='hd'/>
            <boot dev='cdrom'/>
            <bootmenu enable='yes' timeout='3000'/>
            <smbios mode='sysinfo'/>
            <bios useserial='yes' rebootTimeout='0'/>
        </os>
        ...........
        ```

        * `type`
            `type`元素的内容指定要在虚拟机中引导的操作系统的类型, `hvm`为借助qemu-kvm完全虚拟化，`arch`属性指定虚拟化的CPU架构，`machine`属性指定虚拟化的机器类型；可以通过 [`virsh capabilities`](https://libvirt.org/formatcaps.html) 查看`type`元素支持的内容
        * `loader`
            `loader`可选元素的内容是指定虚拟机守护进程的绝对路径，用户辅助虚拟机的创建。有两个可选属性，`readonly`: 值有yes|no，标记镜像是可写或者只读；`type`: 值有rom|pflash，以什么方式引导镜像，pflash可以加载UEFI镜像，`secure`控制是否开启安全启动
        * `nvram`
            `nvram`可选元素的表示虚拟uefi固件的文件位置，在`qemu.conf`文件中定义了，`template`属性会覆盖掉`qemu.conf`中的关于nvram的相应配置
        * `boot`
            `boot`元素的值：`fd`,`hd`,`cdrom`或`network`中的一个，用于指定引导设备，可以重复多次来设置设备引导的优先级列表，在磁盘等设备的部分也可以控制引导顺序，并且优先级比这里的高，也是官方推荐的。
        * `bootmenu`
            `bootmenu`元素定义是否在guest启动时启用交互式启动菜单，如果未指定，将使用管理程序的默认值
        * `smbios`
            `smbios`元素定义如何填充guest虚拟机中可见的SMBIOS信息，必选属性`mode`的值:`emulate`(让虚拟机管理程序生成所有值)，`host`(从主机的SMBIOS值复制块0和块1中的所有块，除了UUID)或者`sysinfo`(使用[sysinfo](https://libvirt.org/formatdomain.html#elementsSysinfo)元素中的值)
        * `bios`
            `bios`元素定义bios启动的设置，uefi启动无效。`useserial`属性：启用或禁用串行图形适配器，允许用户在串行端口上查看BIOS消息，需要定义[串口](https://libvirt.org/formatdomain.html#elementCharSerial); `rebootTimeout`属性：引导失败后多久重新启动，毫秒为单位，最大65535，`-1`禁止启动

    2. 主机启动加载器
        使用其他的启动加载器来启动IOS文件，安装系统或者直接启动系统，例如 `pygrubXen`：

        ```xml
        <bootloader>/usr/bin/pygrub</bootloader>
        <bootloader_args>--append single</bootloader_args>
        ```

        * bootloader:
            bootloader元素的内容提供了主机OS​​中引导加载程序可执行文件的完全路径。将运行此引导加载程序以选择要引导的内核
        * bootloader_args:
            可选bootloader_args元素参数传递给引导加载程序

    3. 直接内核启动
        安装新的客户操作系统时，直接从存储在主机操作系统中的内核和initrd启动通常很有用，允许将命令行参数直接传递给安装程序。此功能通常适用于para和full虚拟客户端
        参考官网:<https://libvirt.org/formatdomain.html#elementsOSKernel>

    4. linux容器启动
        使用基于容器的虚拟化而不是内核/启动映像启动域
        参考官网:<https://libvirt.org/formatdomain.html#elementsOSContainer>

    5. SMBIOS系统信息
        一些管理程序允许控制向客户呈现的系统信息（例如，SMBIOS字段可以由管理程序填充并通过客户机中的dmidecode命令进行检查）。可选sysinfo元素涵盖所有此类信息。
        参照官网:<https://libvirt.org/formatdomain.html#elementsSysinfo>

3. CPU分配

    ```xml
    <domain>
    ......
        <vcpu placement='static' cpuset="1-4,^3,6" current="1">2</vcpu>
        <vcpus>
            <vcpu id='0' enabled='yes' hotpluggable='no' order='1'/>
            <vcpu id='1' enabled='no' hotpluggable='yes'/>
        </vcpus>
    ......
    </domain>
    ```

    * vcpu
        此元素的内容定义为guest虚拟机操作系统分配的最大虚拟CPU数，必须介于1和虚拟机管理程序支持的最大值之间。最好不要超过实际CPU数量
      * cpuset
        可选属性cpuset是以逗号分隔的物理CPU编号列表，默认情况下可以固定域进程和虚拟CPU。该列表中的每个元素可以是单个CPU编号，一系列CPU编号，`^`后跟要从先前范围中排除的CPU编号。
      * current
        是否应启用最少CPU数量
      * placement
        placement(分配模式):static|auto，如果通过`cpuset`来指定CPU个数，必须为`static`。如果`placement`为`static`，`cpuset`并没有指定，将固定所有可用物理CPU
    * vcpus
        控制各个vCPU的状态
        * `ID`属性指定libvirt使用的vcpu id,注意：某些情况下，guest中现实的`vcpu id`可能和`libvirt`不一样，有效范围从`0`到由`vcpu`定义的最大CPU减一
        * `enable`属性表示允许控制`vcpu`的状态，值：`yes|no`
        * `hotpluggable`属性控制在启动时启用CPU的情况下，是否可以对指定的vCPU进行热插拔。请注意，所有已禁用的vCPU必须是可热插拔的(即`enable`是`no`的`hotpluggable`必须为`yes`)。有效值为 `yes`和`no`
        * `order`属性允许指定添加在线vCPU的顺序 
4. IOThreads分配
5. CPU调整
6. 内存分配
7. 内存备份
8. 内存调整
9. NUMA节点调整
10. 阻止I / O调整
11. 资源分区
12. CPU模型和拓扑
13. 事件配置
14. 能源管理
15. 管理程序功能
16. 保持时间
17. 绩效监测事件
18. 设备
19. Vsock
20. 安全标签
21. 钥匙包裹
22. 启动安全性
23. 我的xml配置
    ```xml
    <domain type='kvm'>                     <!-- 如果是Xen，则type=‘xen’，还有qemu、lxc、kqemu等参数 -->
        <name>node1</name>                  <!-- 虚拟机名称，同一物理机唯一 -->
        <uuid>fd3535db-2558-43e9-b067-314f48211343</uuid>   <!-- 同一物理机唯一，可用uuidgen生成，如果不指定，启动的是后自动生成 -->
        <title>This is my first test kvm</title>            <!-- title参数提供一个对虚拟机简短的说明，它不能包含换行符。 -->
        <description>我是个描述</description>                 <!-- 描述，libvirt不会使用这个参数 -->
        <memory unit='KiB'>524288</memory>                  <!-- 最大内存，unit(内存单位，默认KiB)：K、KiB、M、MiB、G、GiB、T、TiB-->
        <currentMemory>524288</currentMemory>               <!-- 实际分给给客户端的内存她小于memory的定义，默认和memory一样 -->
        <vcpu placement='static' cpuset="1-4,^3,6" current="1">2</vcpu> <!-- 虚拟机可使用的cpu个数，可选参数有：
                                                                                placement(分配模式):static|auto；
                                                                                cpuset(使用那个物理CPU):逗号分割，^代表排除这个CPU；
                                                                                current：最少CPU个数。 -->
        <!-- 系统启动相关 -->
        <os>
            <type arch='x86_64' machine='pc-i440fx-vivid'>hvm</type>    <!-- arch指出系统架构类型，machine(机器类型)，查看机器类型：qemu-system-x86_64 -M ? -->
            <loader>/usr/bin/qemu-kvm</loader>                          <!-- 全虚拟化的守护进程所在的位置 -->
            <boot dev='hd'/>                <!-- 启动介质，第一次需要装系统可以选择cdrom光盘启动，dev参数：fd、hd、cdrom、network -->
            <bootmenu enable='yes'/>        <!-- 表示启动按F12进入启动菜单 -->
        </os>
        <!-- Hypervisor的特性 -->
        <features>
            <acpi/>                         <!-- Advanced Configuration and Power Interface,高级配置与电源接口 -->
            <apic/>                         <!-- Advanced Programmable Interrupt Controller,高级可编程中断控制器 -->
            <pae/>                          <!-- Physical Address Extension,物理地址扩展 -->
        </features>
        <!-- 虚拟机时钟设置，offset(时间格式)：
                UTC：同步到UTC时钟
                localtime：同步到主机时钟所在的时区
                timezone：The guest clock will be synchronized to the requested timezone using the timezone attribute. -->
        <clock offset='localtime'/>
        <!-- 控制周期，参数分别是：
                destory:domain终止并释放占用的资源；
                restart:domain终止并以相同配置启动；
                preserver:domain终止但不释放资源；
                rename-restart：domain终止并以一个新的名字重新启动 -->
        <on_poweroff>destroy</on_poweroff>  <!-- 当客户端请求poweroff时执行特定的动作 -->
        <on_reboot>restart</on_reboot>      <!-- 当客户端请求reboot时执行特定的动作 -->
        <on_crash>restart</on_crash>        <!-- 当客户端崩溃时执行的动作 -->
        <!-- 设备配置，所有的设备都是一个名为devices元素的子设备 -->
        <devices>
            <emulator>/usr/bin/qemu-kvm</emulator>                           <!-- 指定模拟设备二进制文件的全路径 -->
            <!-- disk、floppy(软盘)、cdrom或者一个 paravirtualized driver(半虚拟驱动程序)，
                他们通过一个disk元素指定 -->
            <disk type='file' device='disk'>
                <driver name='qemu' type='qcow2'/>
                <source file='/home/data/kvm/node1.0.qcow2'/>           <!-- source -->
                <target dev='vda' bus='virtio'/>
                <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/> <!-- 域、总线、槽、功能号，slot值同一虚拟机上唯一 -->
            </disk>
            <!-- 定义串口 -->
            <serial type='pty'>
                <target port='0'/>
            </serial>
            <!-- console用来代表交互性的控制台 -->
            <console type='pty'>
                <target port='0'/>
            </console>
            <!-- 利用Linux网桥连接网络 -->
            <interface type='bridge'>
                <mac address='fa:92:01:33:d4:fa'/>
                <source bridge='virbr0'/>       <!-- 配置的网桥网卡名称 -->
                <target dev='vnet0'/>           <!-- 同一网桥下相同 -->
                <alias name='net0'/>            <!-- 别名，同一网桥下相同 -->
                <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>     <!-- 注意slot值唯一 -->
            </interface>
            <!-- 利用ovs网桥连接网络 -->
            <interface type='bridge'>  
                <source bridge='br-ovs0'/>  
                <virtualport type='openvswitch'/>
                <target dev='tap0'/>
                <model type='virtio'/>  
            </interface>
            <!-- 配置成pci直通虚拟机连接网络，SR-IOV网卡的VF场景 -->
            <hostdev mode='subsystem' type='pci' managed='yes'>
                <source>
                    <address domain='0x0000' bus='0x03' slot='0x00' function='0x0'/>
                </source>
            </hostdev>
            <!-- 利用vhostuser连接ovs端口 -->
            <interface type='vhostuser'>
                <mac address='fa:92:01:33:d4:fa'/>
                <source type='unix' path='/var/run/vhost-user/tap0' mode='client'/>  
                <model type='virtio'/>
                <driver vringbuf='2048'/>
                <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>  
            </interface>
            <interface type='network'>              <!-- 基于虚拟局域网的网络 -->
                <mac address='52:54:4a:e1:1c:84'/>  <!-- 可用命令生成，见下面的补充 -->
                <source network='default'/>         <!-- 默认 -->
                <target dev='vnet1'/>               <!-- 同一虚拟局域网的值相同 -->
                <alias name='net1'/>
                <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>     <!-- 注意slot值 -->
            </interface>
            <graphics type='vnc' port='5900' autoport='yes' listen='0.0.0.0' keymap='en-us'/>   <!-- 配置vnc，windows下可以使用vncviewer登录，获取vnc端口号：virsh vncdisplay vm0 -->
                <listen type='address' address='0.0.0.0'/>
            </graphics>
        </devices>
    </domain>
    ```

## 管理工具

> 这里直接写命令的创建方式和介绍，涉及到的参数的意义，可从[优化和介绍kvm里](#优化和介绍KVM)详细查看
> 默认的KVM虚拟机工作目录为`/var/lib/libvirt`，配置文件目录`/etc/libvirt/qemu`,主机名称+xml结尾的文件即其相关虚拟机的配置文件，需要修改其配置，也可以直接修改xml文件实现（不建议）。其中autostart目录定义的配置文件会随主机一起启动，而network定义了虚拟机使用桥接网络时的网关网卡的相关配置。

### qemu-img

> 创建镜像文件，参考[磁盘存储](#磁盘存储)

```sh
qemu-img create -f qcow2 node1.qcow2 10G  # 创建大小为10G，qcow2格式的镜像文件
qemu-img info node1.qcow2                 # 查看镜像信息
qemu-img convert -f raw -o qcow2 node1.img node1.qcow2     # 更改镜像格式
```

### virsh

> virsh 是一个用于监控系统程序和客户机虚拟机器的命令行接口（CLI）工具。virsh 命令行工具建立在 libvirt 管理 API，并作为可选择的一个运行方式来替代 qemu-kvm 命令和图形界面的 virt-manager 应用。无特权的用户以只读的方式使用 virsh 命令；有根用户权限的用户可以使用该命令的所有功能。virsh 是一个对虚拟环境的管理任务进行脚本化的理想工具。另外，virsh 工具是 guest 操作系统 域的一个主要管理接口，可以用于创造、暂停和关闭“域”，或罗列现有域。这一工具作为 libvirt-client 软件包中的一部分被安装。
>
> KVM虚拟机依靠两个主要文件来启动，一个是img文件，一个是xml配置文件

* 安装

    ```sh
    dnf install libvirt-client
    or
    yum install libvirt-client
    ```

* 命令常用方式

    ```sh
    virsh define node1.xml          # 导入虚拟机配置（xml格式）（这个虚拟机还不是活动的)
    virsh create node1.xml          # 创建虚拟机（创建后，虚拟机立即执行，成为活动主机）
    virsh start node1               # 开启node1虚拟机
    virsh suspend node1             # 暂停虚拟机（不释放资源）
    virsh resume node1              # 启动暂停的虚拟机
    virsh shutdown node1            # 正常关闭虚拟机
    virsh destroy node1             # 强制关闭虚拟机
    virsh dominfo node1             # 查看虚拟机的基本信息
    virsh domname 2                 # 查看序号为2的虚拟机别名
    virsh domid node1               # 查看虚拟机的序号
    virsh domstate node1            # 查看虚拟机的当前状态
    virsh list --all                # 查看所有虚拟机
    virsh domstate node1            # 查看虚拟机的xml配置（可能和定义虚拟机时的配置不同，因为当虚拟机启动时，需要给虚拟机分配id号、uuid、vnc端口号等等）
    virsh setmem node1 512000       # 给不活动的虚拟机设置内存大小
    virsh setvcpus node1 4          # 给不活动的虚拟机设置CPU个数
    virsh destroy node1             # 销毁虚拟机，不删除虚拟机配置
    virsh undefine node1            # 删除虚拟机配置
    virsh dumpxml node1             # 显示虚拟机的xml配置
    virsh edit node1                # 编辑xml配置文件
    virsh vncdisplay node1          # 获取虚拟机的vnc连接端口
    ```

* 存储池来管理存储

    ```sh
    virsh pool-define-as kvm_images dir - - - - "/home/data/kvm/pool" # 定义存储池
    virsh pool-build kvm_images     # 建立基于文件夹的存储池
    virsh pool-start kvm_images     # 使存储池生效
    virsh pool-info kvm_images      # 查看存储池详情
    virsh pool-list --all           # 查看所有存储池

    # 创建完存储池后，就可以通过创建卷的方法来创建虚拟机的磁盘
    virsh vol-create-as kvm_images node1.qcow2 10G --format qcow2   # 创建卷
    virsh pool-refresh kvm_images   # 刷新存储池
    virsh vol-info kvm_images       # 查看存储池里边的存储卷信息
    virsh vol-info node1.qcow2 kvm_images       # 查看存储池里边单独一个卷的信息
    virsh vol-dumpxml node1.qcow2 kvm_images    # 查看存储池里边的一个卷的详细信息
    ```

* 虚拟机备份
    ```sh
    virsh save --bypass-cache node1 /var/lib/libvirt/save/node1_1.save --running    # 备份
    virsh restore /var/lib/libvirt/save/node1_1.save --bypass-cache --running       # 还原
    ```

* 虚拟机快照

    > 如果要使用kvm的快照功能，就必须使用qcow2的磁盘格式，而raw只支持内存快照，如果不是，请修改

    ```sh
    virsh snapshot-create node1 node1.snap1 # 创建快照
    virsh snapshot-revert node1 node1.snap1 # 恢复快照
    virsh snapshot-list node1               # 查看快照
    virsh snapshot-delete node1 node1.snap1 # 删除快照
    ```

* 虚拟机迁移

    > KVM虚拟机依靠两个主要文件来启动，一个是img文件，一个是xml配置文件,因此迁移的时候，可以直接迁移这两个文件就能实现静态迁移。如果img文件存放在共享存储，则更为方便，只用迁移xml配置文件，就可以实现静态迁移。
    > 当然，virsh命令也可以迁移虚拟机，不过要求目标主机与当前主机的应用环境须保持一致，其命令格式如下：

    ```sh
    virsh migrate --live node1 qemu+tcp//destnationip/system tcp://destnationip
    ```

* 通过xml创建虚拟机，xml写法请参考[xml](#libvirt配置文件)

### virt-manager

> virt-manager 是一个用于管理虚拟机器的简单的图形工具。它所提供的功能用以控制现有机器寿命周期、储备新机器、管理虚拟网络、访问虚拟机器的图形控制台并查看性能数据。

* 安装

    ```sh
    dnf install virt-manager
    or
    yum install virt-manager
    ```

### virt-install

> virt-install 是一个用来配置新的虚拟机器的命令行工具。它通过使用连续的控制台、SPICE 或 VNC 客户/服务器成对图形，支持基于文本和图形的安装。安装介质可以是本地的，或已有的远程 NFS、HTTP 或 FTP 服务器。考虑到便捷的自动化安装，还可以通过配置此工具实现在无需人工参与的情况下运行，并在安装完成时快速启动客机。此工具以 python-virtinst 软件包的一部分进行安装。

* 安装

    ```sh
    dnf install virt-install
    or
    yum install virt-install
    ```

* 常用参数

    ```sh
    virt-install --connect qemu:///system \ # 如果使用kvm安装，并且使用的root，默认为此，基于xen或者其它，可参考man virt-install
    --n test1 \                             # 指定虚拟机的显示名称
    --c /mnt/centos6.4-x86_64.iso \         # 指定安装镜像，也可以指定cdrom直接安装，如:-c /dev/sr0
    --r 2048 \                              # 指定内存，默认为MB
    --arch=x86_64 \                         # 指定arch模型
    --vcpus=2 --check-cpu --cpuset=0-1 \    # 指定cpu0,1作为虚拟机的CPU，此处绑定了CPU
    --os-type=linux --os-variant=rhel6 \    # 指定系统类型和版本
    --disk path=/var/lib/libvirt/images/node.qcow2,device=disk,bus=virtio,spare=true -s 10 \ # 指定磁盘信息，使用virtio驱动加载
    --network bridge=br0 \                  # 指定桥接模式，并指定通过br0网卡进行桥接
    --noautoconsol --autostart \            # 不自动开启控制台，并且随主机自启动
    --vnc \                                 # 提供vnc端口访问，在这里可以设置密码，也可以不设置
    --force
    ```

### virt-viewer

### guestfish

> guestfish 是一个命令行工具，用来检验和修改客机的文件系统。此工具使用 libguestfs，并显示所有 guestfs API 所提供的功能。这个工具包括在同名的软件包中，称为 guestfish。
> **在运行中的虚拟机上使用 guestfish 会引起磁盘镜像损坏。若一个正在运行中的虚拟机正在使用磁盘镜像，则需搭配 --ro（只读）共同使用 guestfish 命令。**

### GNOME Boxes

> Boxes 是一个简单的图形桌面虚拟化工具，用来查看和访问虚拟机和远程系统。Boxes 提供了一种方法，即以最小的配置来测试桌面上的不同操作系统和应用。虚拟系统可以手动也可使用快速安装功能，快速安装功能可以通过优化设置来自动预配置虚拟机。这个工具包括在同名的软件包中，被称作 gnome-boxes。
> 需要gnome桌面环境

* 安装

    ```sh
    dnf install gnome-boxes
    or
    yum install gnome-boxes
    ```

### 其他工具

请查看redhat官方介绍[其他工具](https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/7/html/virtualization_getting_started_guide/sect-virtualization_getting_started-tools-other)

## 优化和介绍KVM

### CPU优化

* 要考虑CPU的数量问题，所有guest cpu的总数目不要超过物理机CPU总数目，如果超过，则将对性能带来严重影响，建议选择复制主机CPU配置。

* “CPU 型号 ”（CPU model）规定了哪些主机 CPU 功能对客机操作系统有效。 qemu-kvm 和 libvirt 包含了几种当前处理器型号的定义，允许用户启用仅在新型 CPU 型号中可用的 CPU 功能。 对客机有效的的 CPU 功能取决于主机 CPU 的支持、内核以及 qemu-kvm 代码。

* 为了使虚拟机可以在具有不同 CPU 功能集的主机间安全地进行迁移，qemu-kvm 在默认状态下不会把主机 CPU 的所有功能都提供给客机操作系统，而是根据所选的 CPU 型号来为虚拟机提供相关的 CPU 功能。如果虚拟机启用了某个 CPU 功能，则此虚拟机无法迁移到不支持向客机提供此功能的主机上。

### 内存优化

1. KSM（kernel Samepage Merging）相同页合并

    > 内存分配的最小单位是page（页面），默认大小是4KB，可以将host主机内容相同的内存合并，以节省内存的使用。
    >
    > 当KVM上运行许多相同系统的客户机时，客户机之间将有很多内存页是完全相同的，特别是只读的内核代码页完全可以在客户机之间共享，从而减少客户机占用的内存资源，也能同时运行更多的客户机。
    >
    > 使用KSM存在性能损失，在一般的环境中，性能损失大概是10%，这也是在某些环境中关闭KSM的原因。
    >
    > 建议开启KSM的同时不要使用memory balloon，两种内存优化方案会降低系统的性能;
  
    * 在什么时候开启KSM？

      * 如果目标是运行尽可能多的虚拟机，而且性能不是问题，应该保持KSM处于运行状态。例如KSM允许运行30个虚拟机的主机上运行40个虚拟机，这意味着最大化硬件使用效率。

      * 如果服务器在运行相对较少的虚拟机并且性能是个问题时，那么应该关闭KSM。

      * 如果CPU是整个宿主机的资源瓶颈则不建议使用KSM，因为KSM会带来相应的CPU开销
  
    * KSM文件目录：
        ```bash
        ls /sys/kernel/mm/ksm/
        总用量 0
        -r--r--r--. 1 root root 4096 11月 30 17:05 full_scans           # 对可合并的内存区域扫描过的次数
        -rw-r--r--. 1 root root 4096 11月 30 17:05 max_page_sharing
        -rw-r--r--. 1 root root 4096 11月 30 17:05 merge_across_nodes   # 是否可以合并来自不同NUMA节点的页面。参数更改0,避免跨NUMA节点合并页面
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
        -rw-r--磁盘r--. 1 root root 4096 11月 30 17:05 use_zero_pages
        ```
  
    * KSM管理
     ksm可以直接配置/sys/kernel/mm/ksm/目录下的文件
  
    * ksmtuned管理
        > ksmtuned会一直保持循环执行，以调节ksm服务运行。

        * 安装ksmtuned管理工具
            ```sh
            yum install ksmtuned
            ```

        * 编辑ksmtuned配置文件
            ```ini
            # ksm每次内存扫描的时间;
            KSM_MONITOR_INTERVAL = 60

            # 表示每次扫描休息的间隔时间(最小值为10)，KSM扫描会占用一些CPU的开销，所以当KVM虚拟机数量或者应用软件较少时可以调整KSM_SLEEP_MSEC至一个较大的值，反之则设置较小的值;同时当Hypervisor里面的虚拟机的内存调优到达一个稳定状态，也可以根据情况把这个参数调小节省CPU的开销;
            KSM_SLEEP_MSEC = 10

            # 内存页合并增加数量;
            KSM_NPAGES_BOOST = 300

            # 内存页合并减少数量;
            KSM_NPAGES_DECAY = -50

            # 内存页合并最小值;
            KSM_NPAGES_MIN = 64

            # 内存页合并最大值
            KSM_NPAGES_MAX = 1250

            # 临界值系数，越大合并的越多
            KSM_THRES_COEF = 20

            # 临界值常量
            KSM_THRES_CONST = 2048

            # 取消注释以下内容以启用ksmtuned调试信息
            LOGFILE = /var/log/ksmtuned
            # DEBUG = 1
            ```

        * ksmtuned工作方法：
            * ksm先取得到宿主机的总内存“total”， thres = total * KSM_THRES_COEF / 100。然后与临界值常量KSM_THRES_CONST进行比较，如果thres 小于 KSM_THRES_CONST，那么thres就 等于 KSM_THRES_CONST;

            * 计算qemu进程使用的内存总和：committed; 当且仅当committed + thres > total时，才开始操作内存页合并。所以调整临界值常量与临界值系数可以确定临界值thres, 从而有效地调整ksm工作方式。

            * 判断剩余内存量free与thres的大小，如果free < thres，ksm每次扫描后内存页合并数会增加 KSM_NPAGES_BOOST，该参数上限为KSM_NPAGES_MAX;反之如果free>thres内存页合并数量会 减少 KSM_NPAGES_DECAY，下限为KSM_NPAGES_MIN。
  
2. 对内存设置限制
    > 如果我们有多个虚拟机，为了防止某个虚拟机无节制的使用内存资源，导致其他虚拟机无法正常使用，就需要对使用的内存进行限制。
    >
    > 不同的管理工具不同的配置方法，以virs为例

    * 查看当前虚拟机的内存限制，单位为KB
    ```sh
    virsh memtune c7-1

    hard_limit     : 无限制       # 强制最大内存
    soft_limit     : 无限制       # 可用最大内存
    swap_hard_limit: 无限制       # 强制最大swap使用大小
    ```
    * 设置强制最大内存为100MB，在线生效。
    ```sh
    virsh memtune c7-1 --hard-limit 1024000 --live

    virsh memtune c7-1          # 查看
    hard_limit     : 1024000
    soft_limit     : 无限制
    swap_hard_limit: 无限制
    ```

3. 大页后端内存

    > 在逻辑地址想物理地址转换时，CPU保持一个翻译后备缓冲器TLB，用来缓冲转换结果，而TLB容量很小，所以如果page很小，TLB很容易就充满，这样就容易导致cache miss，相反page变大，TLB需要保存的缓存项就变少，就会减少cache miss，通过为客户端提供大页后端内存，就能减少客户机消耗的内存并提高TLB命中率，从而提高KVM性能。
    >
    > 在RHEL里，大页的大小可以是2M,1G.默认情况下，已经开启了透明大页功能
    >
    > 配置大页面后，系统在开机启动时会首选尝试在内存中找到并预留连续的大小为 HugePages_Total * Hugepagesize 的内存空间。如果内存空间不满足，则启动会报错 Kernel Panic, Out of Memory 等错误。
    > 如只配置了一个大小的大页面，可以通过 /proc/meminfo 中的 Hugepagesize 和 HugePages_Total 计算出大页面所在内存空间的大小。这部分空间会被算到已用的内存空间里，即使还未真正被使用
  
    * 查看内存信息，无可用大页
        ```sh
        cat /proc/meminfo | grep Huge
        HugePages_Total:       0        # 大叶面的数量
        HugePages_Free:        0        # 未使用的大叶面数量
        HugePages_Rsvd:        0
        HugePages_Surp:        0
        Hugepagesize:       2048 kB     # 每个大页面的大小
        ```
  
    * 查看设置的大页面的数目
        ```bash
        cat /proc/sys/vm/nr_hugepages
        ```
  
    * 指定大页需要的内存页面数量,页面大小一般不更改，
        ```bash
        echo 25000 > /proc/sys/vm/nr_hugepages  # 临时生效
        sysctl -w vm.nr_hugepages=25000         # 永久生效
        或者
        vim /etc/sysctl.conf
        vm.nr_hugepages=25000
        sysctl -p                               # 重新加载配置
        ```
    * kvm虚拟机需要手动开启大页内存的
     根据不同的管理工具开启方法不同，具体请百度下

### I/O等设备使用半虚拟化设备

1. 采用virtio磁盘控制器

    > kvm设计了virtio类型的磁盘控制器，是针对磁盘和网络的一个半虚拟化接口，以提高效率为目的。
    > guest 系统需要安装半虚拟化驱动，Linux内核中已经集成进去了，window平台的话，必须手动安装

    * virtio-scsi
        半虚拟化 SCSI 控制器设备是一种更为灵活且可扩展的 virtio-blk 替代品，irtio-scsi 客机能继承目标设备的各种特征，并且能操作几百个设备，相比之下，virtio-blk 仅能处理 28 台设备。使用大量磁盘或高级储功能（如 TRIM）的客机推荐使用的半虚拟化设备。

    * virtio-blk
        适用于向客机提供镜像文件的半虚拟化储存设备。virtio-blk 可以为虚拟机提供最好的磁盘 I/O 性能，但比 virtio-scsi 的功能少。

2. 其的半虚拟化设备

    * virtio-net
        半虚拟化网络设备是虚拟化网络设备，它为虚拟机提供了网络访问能力，并可以提供网络性能及减少网络延迟。

    * 半虚拟化时钟
        使用时间戳计数器（TSC，Time Stamp Counter）作为时钟源的客机可能会出现与时间相关的问题。KVM 在主机外围工作，这些主机在向客机提供半虚拟化时间时没有固定的 TSC。此外，半虚拟化时钟会在客机运行 S3 或挂起 RAM 时帮助调整所需时间。半虚拟化时钟不支持 Windows guest。

    * virtio-serial
        半虚拟化串口设备是面向比特流的字符流设备，它为主机用户空间与客机用户空间之间提供了一个简单的交流接口。

    * virtio-balloon
        > 建议开启KSM的同时不要使用memory balloon，两种内存优化方案会降低系统的性能;
        > 个人理解，动态使用内存，虚拟机使用多少就占用多少内存，但是也不可以超过限定值

        气球（ballon）设备可以指定虚拟机的部分内存为没有被使用（这个过程被称为气球“充气 ” — inflation），从而使这部分内存可以被主机（或主机上的其它虚拟机）使用。当虚拟机需要这部分内存时，气球可以进行“放气 ”（deflated），主机就会把这部分内存重新分配给虚拟机。

    * virtio-rng
        半虚拟化随机数字生成器使虚拟机可以直接从主机收集熵或随意值来使用，以进行数据加密和安全。因为典型的输入数据（如硬件使用情况）不可用，虚拟机常常急需熵。取得熵很耗时；virtio-rng 通过直接把熵从主机注入客机虚拟机从而使这个过程加快 。
    * QXL
        半虚拟化图形卡与 QXL 驱动一同提供了一个有效地显示来自远程主机的虚拟机图形界面。SPICE 需要 QXL 驱动。

3. 直接使用物理主机设备

    > 特定硬件平台允许虚拟机直接访问多种硬件设备及组件。在虚拟化中，此操作被称为 “设备分配 ”（device assignment）。设备分配又被称作 “传递 ”（passthrough）。
    > 需要物理设备支持 device assignment

    * VFIO 设备分配

        虚拟功能 I/O（VFIO）把主机系统上的 PCI 设备与虚拟机直接相连，允许客机在执行特定任务时有独自访问 PCI 设备的权限。这就象 PCI 设备物理地连接到客机虚拟机上一样。通过把设备分配从 KVM 虚拟机监控系统中(半虚拟化和全虚拟化)移出，并在内核级中强制进行不同guest之间进行设备隔离，VFIO 安全性更高且与安全启动兼容。在 Red Hat Enterprise Linux 7 中，它是默认的设备分配机制。VFIO 可以分配的设备数量为32个， 并且支持对 NVIDIA GPU 的分配。

    * USB传递

        > USB 设备分配允许客机拥有在执行特定任务时有专有访问 USB 设备的权利。这就象 USB 设备物理地连接到虚拟机上一样。

    * SR-IOV

        > 支持 SR-IOV 的 PCI-e 设备提供一个单一根功能（如单一以太网接口），并把多个各自分离的虚拟设备作为独特 PCI 设备功能。每个虚拟化设备都可能有自身独特的 PCI 配置空间、内存映射的寄存器以及单独的基于 MSI 的中断系统。

        SR-IOV （Single Root I/O Virtualization）是一个 PCI 快捷标准，把单一物理 PCI 功能扩展到同分散的虚拟化功能（VF）一样共享 PCI 资源。通过 PCI 设备分配，每个功能可以被不同虚拟机使用。

    * NPIV

        > NPIV 可以提供带有企业级存储解决方案的高密度虚拟环境。

        N_Port ID Virtualization（NPIV）是对光纤通道设备有效的功能。NPIV 共享单一物理 N_Port 作为多个 N_Port ID。NPIV 为 HBA（光纤通道主机总线适配器，Fibre Channel Host Bus Adapter）提供和 SR-IOV 为 PCIe 接口提供的功能相似的功能。有了 NPIV，可以为 SAN（存储区域网络，Storage Area Network）提供带有虚拟光纤通道发起程序的虚拟机。

### 磁盘&存储

1. 存储池和储存卷

    > “存储池 ”（storage pool）即一个由 “libvirt” 管理的文件、目录或储存设备，其目的是为虚拟机提供储存空间。存储池被分隔为存储 “卷 ”（volume），可以用来存储虚拟机镜像或附加到虚拟机作为额外额存储。多个客机可共享同一储存池，允许储存资源得到更好分配
    >
    >储存池进一步划分为“储存卷 ”（storage volume）。储存卷是物理分区、LVM 逻辑卷、基于文件的磁盘镜像及其它由 libvirt 控制的储存形式的抽象层。不论基于何种硬件，储存卷会作为本地储存设备呈现给虚拟机。
    >
    > 个人理解为，存储池就是从本地硬盘或网络硬盘划分出来一个区域给虚拟机 guest 系统使用的存储空间，每个卷相对guest系统来说就是一块硬盘

    * 本地存储池

        > 本地储存池直接连接到主机服务器。它们包括本地目录、直接连接的磁盘、物理分区和本地设备上的 LVM 卷组，因为本地存储池不支持实时迁移，所以它可能不适用于某些生产环境。

    * 网络存储池

        > 网络储存池包括在网络上使用标准协议共享的储存设备。使用 virt-manager 在主机间进行虚拟机的迁移需要网络储存，但是当使用 virsh 迁移时，它是可选的。网络储存池由 libvirt 进行管理。

2. 主机存储

    > 磁盘镜像可以储存在一系列和主机相连的本地或远程存储中。(可以存储在本地或者网络磁盘中)
    > KVM虚拟机的磁盘镜像从存储方式来看分为两种：存储于文件系统，直接使用使用裸设备。

    * 镜像文件(存储在文件系统中)
        > 镜像文件储存在主机文件系统中。它可以储存在本地文件系统中，如 ext4 或 xfs；或网络文件系统中，如 NFS
        > 创建一个镜像文件给 guest 系统当作磁盘使用

        例如 libguestfs 这样的工具，能管理、备份及监控文件。

        KVM 上的磁盘镜像格式包括：
        * raw

            > 当对磁盘 I/O 性能要求非常高，而且通常不需要通过网络传输镜像文件时，可以使用 raw 文件。**不推荐使用**

            raw 镜像文件指不包含附加元数据的磁盘内容。

            假如主机文件系统允许，raw 文件可以是预分配（pre-allocated）或稀疏（sparse）。稀疏文件根据需求分配主机磁盘空间（动态存储)，因此它是一种精简配置形式（thin provisioning）。预分配文件的所有空间需要被预先分配，但它比稀疏文件性能好。

        * qcow2

            > Red Hat Enterprise Linux 7.0 及更新版本支持 qcow2 v3 镜像文件格式。
            > 动态存储，用多少就实际占用多少物理存储空间

            qcow2 镜像文件提供许多高级磁盘镜像特征，如快照、压缩及加密。它们可以用来代表通过模板镜像创建的虚拟机。因为只有虚拟机写入的扇区部分才会分配在镜像中，所以 qcow2 文件的网络传输效率较高。

    * lvm卷(直接使用裸设备)

        > LVM 精简配置为 LVM 卷提供快照和高效的空间使用，它可以作为 qcow2 的一种替代选择。
        > 创建一个lvm卷给 guest 系统当作硬盘使用

        逻辑卷可用于磁盘镜像，并使用系统的 LVM 工具进行管理。 由于它使用更简单的块储存模式，LVM 比文件系统的性能更高。

    * 主机设备(直接使用裸设备)

        > 在 SAN 而不是主机上进行储存管理时，可以使用主机设备

        主机设备如物理 CD-ROM、原始磁盘或 LUN 都可以提供给客机。这使得 SAN 或 iSCSI LUN 还有本地 CD-ROM 都可以提供给客机所用。

    * 分布式存储系统(直接使用裸设备)

        > Gluster 卷可用作磁盘镜像。它提供了高效的、使用网络的集群存储。

        Red Hat Enterprise Linux 7 包括在 GlusterFS 上对磁盘镜像的原生支援。这使 KVM 主机可以直接从 GlusterFS 卷引导虚拟机镜像，并使用 GlusterFS 卷中的镜像作为虚拟机的数据磁盘。与 GlusterFS FUSE 相比，KVM 原生支持性能更好。

### KVM网络
