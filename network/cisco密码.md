# CIsco密码破解

## 设置登陆/enbale密码

```cisco
sername fashion password 0 *******   /设置登录密码 （0的意思是明文存储）
enable password *********            /设置enable密码
```

## 重置/查询密码

重启长按CTRL+Pause Break键，进入rommon

```Cisco
rommon >confreg 0x2142  /修改寄存器
rommon 〉reset          /重启

Router(config)#show startup-config /通过存储配置查看密码
Router(config)#show startup-config /通过存储配置查看密码,如若加密执行下边的
Router(config)#copy startup-config run /加载存储配置
Router(config)#sername fashion password 0 *******   /设置登录密码 （0的意思是明文存储）
Router(config)#enable password *********            /设置enable密码
Router(config)#copy run startup-config /保存存储配置
Router(config)#conf t
Router(config)#config-register 0x2102 /寄存器修改为原来的
```

> 如果密码加密存储，不要忘记备份之前的配置