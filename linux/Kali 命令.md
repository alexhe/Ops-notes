# Kali 常用设置、命令和软件使用笔记

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