# VPN

## 加密技术

### 加密算法

> 加密算法多种多样，加密算法分为加密和解密两个过程：
加密是对明文数据按照一定的算法换算成看不懂的密文数据，算法的规则为密钥； 解密是对加密的反运算，将密文数据按照加密时用的算法和算法规则换算为明文数据。

#### 对称加密算法（私钥算法）

> 加密和解密使用相同的密钥，此密钥称为私钥;
由于密钥交换时交换私钥，容易被截取私钥，解密用户数据，

* DES
    > DES是一种经典的数据加密算法

    DES加密共有三种形式:
    DES（40-bit长度加密）
    DES（56-bit长度加密）
    3DES（168-bit长度加密）
    3DES加密长度够长，安全性高，推荐使用3DES。

* AES
    > 高级加密算法

    AES加密共有三种形式：
    AES 128（128-bit长度加密）
    AES 192（192-bit长度加密）
    AES 256（256-bit长度加密）
    AES 256加密长度够长，安全性高，推荐使用AES 256

#### 非对称加密算法（公钥算法）

> 使用公钥加密，私钥解密；

    由于密钥交换时交换公钥，公钥不能解密数据，安全性高

* RSA

    该算法的长度位数不定，由人手工定义。

<font color=red size=3> 注： 在硬件上公钥算法的速度明显慢于私钥算法，一般使用公钥算法完成私钥算法的私钥交换，使用私钥算法来加密数据。</font><br/>

### HMAC (Hashed Message Authentication Code)

概要

* HMAC是密钥相关的哈希运算消息认证码（Hash-based Message Authentication Code）,HMAC运算利用哈希算法，“以一个密钥和一个消息为输入，生成一个消息摘要作为输出”

* Hash算法的特征：

    任何大小的数据计算出的Hash值的长度都是一样的，所以仅仅是根据Hash值，是无法推算出数据

* 基于Hash的特征，所以Hash多用于认证，认证对等体双方在相互认证时，只需要交换密码的Hash值即可，而无需交换密码，从而防止了密码被窃取，但仅仅是窃取Hash值，也无法推算出密码是多少。但可以伪造Hash值，掩耳盗铃。

Hash算法

* MD5（Message Digest 5）

    将任何数据通过计算后输出128-bit 长度的Hash值。

* SHA-1（Secure Hash Algorithm 1）

    将任何数据通过计算后输出160-bit 长度的Hash值。

<font color=red size=3>注： SHA-1拥有着比MD5更高的安全性。</font>

## IPsec（IP Security）

概述

* IPsec最突出，也是最主要的功能就是保证VPN数据的安全传输。
* IPsec定义了使用什么样的方法来管理相互之间的认证，以及使用什么样的方法来保护数据，IPsec只是定义了一些方法，本身并不是一个协议

IPsec的协议有：IKE、ESP、AH，总共三个协议，分为两类：

* IKE（ISAKMP/Oakley）:针对密钥安全的，是用来保证密钥的安全传输、交换以及存储，主要是对密钥进行操作，并不对用户的实际数据进行操作
    **注：其中包含部分Oakley协议以及内置在ISAKMP（Internet Security Association and Key Management Protocol协议中的部分SKEME协议，所以IKE也可写为ISAKMP/Oakley。**

* ESP和AH：主要工作是如何保护数据安全，也就是如何加密数据，是直接对用户数据进行操作的。

IPSec框架
框架 | 可选择的算法
-- | ---
IPSec安全协议 | ESP AH
加密 | DES 3DES AES
数据摘要 | SHA MD5
密钥交换算法 | DH1 DH2 (Diffie-Hellman)

IPsec能够起到的功能有：

* **数据源认证（Data origin authentication）**

    保证数据是从真正的发送者发来的，而不是来自于第三方攻击者。
* **保护数据完整性（Data integrity）**

    保证数据不会被攻击者改动。
* **保证数据私密性（Data confidentiality)**

    保证数据不会被攻击者读取。
* **防止中间人攻击（Man-in-the-Middle)**

    防止数据被中间人截获。

* **防止数据被重放（Anti-Replay）**

    也可以认为是防止数据被读取和改动。

> IPsec除了能够为隧道提供数据保护来实现VPN之外，IPsec还可以自己单独作为隧道协议来提供隧道的建立,如果IPsec自己单独作为隧道协议来使用，那么IPsec就不需要借助任何其它隧道协议就能独立实现VPN功能
>
> IPSec目前只支持IPv4 Unicast（IPv4 单播），不支持其它任何协议。

## IPsec协议

### IKE

IPsec在保护数据时使用私钥加密算法（私钥加密速度快），私钥加密算法的重点就是要保证密钥的安全传递与交换；即使使用公钥加密算法来保证私钥算法的密钥安全传递与交换，仍然存在以下问题：

```sequence
A->>中间人C: B，你用“公钥A”加密
中间人C-->>B: B，你用“公钥C"加密
B->>中间人C: OK，A，你用“公钥B”加密
中间人C-->>A: OK，A，你用“公钥C"加密
A->>中间人C: 使用“公钥C”加密的私钥
B->>中间人C: 使用“公钥C”加密的私钥
```

* C作为中间人截获数据获取到A和B的私钥算法的私钥，数据不安全。
* 由于以上普通的密钥交换方式存在着许多问题与弱点，所以IKE（Internet Key Exchange）将努力构架一个完善的方案体系，以保证VPN之间的密钥与数据的安全。

#### 认证

IKE会在VPN对等体之间采用认证机制（Authentication），可以有效确保会话是来自于真正的对等体而不是攻击者，IKE的认证方式有三种：

* Pre-Shared Keys (PSK)

    使用由管理员事先在双方定义好的密码，认证时，只有双方密码匹配之后，后续的工作才能继续；配置时通常可以包含IP地址，子网以及掩码，也可以指定为任意地址来代替固定地址，适用于IP地址不固定的环境。
* Public Key Infrastructure (PKI) using X.509 Digital Certificates

    使用第三方证书做认证，叫做Certificate Authority (CA),，里面包含名字、序列号，有效期以及其它可以用来确认身份的参数；证书也可以被取消。
* RSA encrypted nonce

    待深入了解

#### 密钥算法（Diffie-Hellman）

Diffie-Hellman是一种密钥交换算法

#### SA（Security Association）

#### IPsec Mode

### ESP（Encapsulating Security Protocol）

### AH（Authentication Header）
