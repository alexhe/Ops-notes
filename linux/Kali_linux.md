# Kali 学习笔记<!-- omit in toc -->

1. [常用设置](#常用设置)
    1. [更新apt源](#更新apt源)
2. [常用命令](#常用命令)
3. [软件使用](#软件使用)

## 常用设置

### 更新apt源

1. 备份sources.list，查看版本
    ```shell
    cp /etc/apt/sources.list /etc/apt/sources.list.bak
    lsb_release -a
    leafpad /etc/apt/sources.list
    ```
2. 阿里云源
    在sources.list文件末尾添加以下源，sana版本：把kali-rolling更改成sana
    ```shell
    deb http://mirrors.aliyun.com/kali kali-rolling main non-free contrib
    deb-src http://mirrors.aliyun.com/kali kali-rolling main non-free contrib
    ```

## 常用命令

## 软件使用