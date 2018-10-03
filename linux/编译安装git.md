[toc]

# 配置编译环境

## 下载源代码包

```shell
mkdir ~/src
cd ~/src
wget https://github.com/git/git/archive/v2.19.0.tar.gz
```

## 安装依赖库文件

```shell
yum install curl-devel expat-devel openssl-devel zlib-devel asciidoc
```

# 编译配置

## 编译

```shell
mkdir /opt/git
make prefix=/opt/git/ all
```

## 设置环境变量

```shell
mkdir /opt/bin
ln -s /opt/git/bin/* /opt/bin
echo "export PATH=$PATH:/opt/bin/" > /etc/profile
source /etc/profile
```

## 测试

```shell
git --version

# 初始化
git config --global user.email "alex_zjf@163.com"
git config --global user.name "cc"
git config --global user.editor "vim"
```