# FTP&SFTP常用命令<!-- omit in toc -->

1. [SFTP](#sftp)
2. [FTP命令](#ftp命令)

## SFTP

```sh
cd 路径                     # 更改远程目录到“路径”
lcd 路径                    # 更改本地目录到“路径”
chgrp group path            # 将文件“path”的组更改为“group”
chmod mode path             # 将文件“path”的权限更改为“mode”
chown owner path            # 将文件“path”的属主更改为“owner”
get 远程路径                 # 下载文件
ln existingpath linkpath    # 符号链接远程文件
ls [选项] [路径]             # 显示远程目录列表
lls [选项] [路径]            # 显示本地目录列表
mkdir 路径                   # 创建远程目录
lmkdir 路径                  # 创建本地目录
mv oldpath newpath           # 移动远程文件
open [用户@]主机[:端口]       # 连接到远程主机
put 本地路径                  # 上传文件
pwd                          # 显示远程工作目录
lpwd                         # 打印本地工作目录
quit                         # 退出 sftp
rmdir 路径                    # 移除远程目录
lrmdir 路径                   # 移除本地目录
rm 路径                       # 删除远程文件
lrm 路径                      # 删除本地文件
symlink existingpath linkpath # 符号链接远程文件
version                       # 显示协议版本
```

## FTP命令

```sh

```