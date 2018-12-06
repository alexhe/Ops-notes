# TCP-IP路由协议 <!-- omit in toc -->

1. [TCP/IP回顾](#tcpip回顾)
    1. [IP包头](#ip包头)

## TCP/IP回顾

### IP包头

1. TCP/IP协议层
    * TCP/IP和OSI参考模型对比
        TCP/IP | OSI
        ---|---
        应用层</br>表示层</br>会话层 | 应用层
        传输层 | 主机到主机层
        网络层 | Internet层
        数据链路层</br>物理层 | 网络接口层
    * IP包头
        |一行32bit|||||
        ---|---|---|---|---|---|---|---
        版本(4bit)|头部长度(4bit)|服务类型(8bit)|总长度(16bit)
        标识符(16bit)|---|---|标记(3bit)|分片偏移(13bit)
        生存时间(8bit)|---|协议(8bit)|头部校验(16bit)
        |源地址(32bit)|
        |目的地址(32bit)|
        可选项|||填充项
2. 图片

    ![avatar](./image/2.jpg)
    @import "./image/2.jpg"