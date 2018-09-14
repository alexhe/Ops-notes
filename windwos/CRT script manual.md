# CRT脚本命令

## 二级对象之Dialog

### Dialog语法

```python
crt.Dialog.Method([arglist])
```

### 方法(Method)

#### FileOpenDialog

* 弹出一个对话框，用于选择单个文件，如果选择了具体文件则返回该文件的绝对路径，如果选择了弹窗的"取消"，则返回""
    ```python
    crt.Dialog.FileOpenDialog(title, buttonLabel, defaultFilename, filter)
    filePath = crt.Dialog.FileOpenDialog("Please select a text file", "Open", "a.log", "Log Files (*.log)|*.log")
    ```
    参数：
  * title:弹窗最上面的标题文字，见运行结果中窗口最上面的"Please select a text file"。
  * buttonLabel:使用"Open"即可。
  * defaultFilename:默认文件名，如下，在弹窗的"文件名"中默认有"a.log"。
  * filter:用于过滤文件类型,见脚本举例中的格式，"Log Files" (*.log)|*.log会显示在运行结果中的"文件类型"中，并且会过滤以.log结尾的文件。
  * 所有参数都是可选参数，可以自己试试无参的情况。

#### MessageBox

* 弹出一个消息框，可以定义按钮，使用按钮和文本消息来实现和用户的简单对话。
    ```python
    crt.Dialog.MessageBox(message , title,icon|buttons)
    crt.Dialog.MessageBox("这里是消息框正文","这里是标题",16|0)
    ```
    参数：
  * message:消息文字,必选参数，见运行结果中的消息正文。
  * title:弹窗的标题描述，见运行结果中的标题处。
  * icon:警示图标，见结果中的图1到图4。icon的取值有：16(叉号，表示错误)，32(问号，表示确认)，48(叹号，表示警告)，64()
  * buttons:按钮类型，定义不同的类型，可以有不同的选项，同时鼠标点击不同的选项时也有不同的返回值。button取值范围为0到6,
    button值 | 返回值
    --- | ---
    0 | 点击后返回值为1；
    1 | 点击'确定'时，返回1，点击'取消'时返回2；
    2 | 点击'终止'时，返回3，点击'重试'时返回4，点击'忽略'时返回5；
    3 | 点击'是'时，返回6，点击'否'时，返回7，点击'取消'时返回2；
    4 | 点击'是'时，返回6，点击'否'时，返回7；
    5 | 点击'重试'时，返回4，点击'取消'时返回2；
    6 | 点击'取消'时，返回2，点击'重试'时，返回10，点击'继续'，返回11；

#### Prompt

* 弹出一个输入框，用户可以填写文字，比如填写文件名，填写路径，填写IP地址等,运行结果如果点击'ok'，返回输入的字符串，否则返回""
    ```python
    crt.Dialog.Prompt(message [, title [, default [, isPassword ]]])
    password = crt.Dialog.Prompt("这里是正文","这里是弹窗标题","这是默认值",True)
    ```
    参数：
  * message:消息文字,必选参数，见运行结果中的消息正文。
  * title:弹窗的标题描述，见运行结果中的标题处。
  * default:输入框中的默认值，如果为""，则没有默认值。
  * isPassword:是否要隐藏输入的文字，类似于日常输入密码时显示****
  * 运行结果如下图1，如果点击'ok'，返回输入的字符串，否则返回""

#### 备注

> 以上就是Dialog这个二级属性的所有方法了，对于有和用户有交互需求的地方就可以使用以上几个方法，不过也要注意，虽然这个方法很炫很好看，但是如果过多的使用这些方法，只会适得其反。最后祝大家都能够学会这些方法，其实Dialog这个方法也可以更多的用于调试代码，就和JS中的console.log的功能是一样的，工具很好，学会了运用就能产生很好的效果。

## 二级对象之Screen

### Screen属性和方法

属性 | 方法
--- | ---
CurrentColumn | Clear
CurrentRow | Get
Columns | Get2
Rows | IgnoreCase
IgnoreEscape | Send
MatchIndex | SendKeys
Synchronous | SendSpecial
.  | WaitForCursor
.  | WaitForKey
.  | WaitForString
.  | WaitForStrings
.  | ReadString

### Screen属性

#### CurrentColumn

* 返回当前光标处的列坐标
    ```python
    Cur_Col = crt.Screen.CurrentColumn
    ```

#### CurrentRow

* 检测当前行坐标，但这个功能有个问题就是当满屏输出后这个值一直表示最大值，等同于底下要讲的子属性四：Rows的值。
    ```python
    Cur_Row = crt.Screen.CurrentRow
    ```

#### Columns

* 检测当前屏幕最大列宽
    ```python
    Cols = crt.Screen.Columns
    ```

#### Rows

* 返回当前屏幕的最大行宽，这个行宽指的是可见区的，并不是指缓冲区的行宽
    ```python
    Rows = crt.Screen.Rows
    ```

#### IgnoreEscape

* 定义当使用WaitForString、WaitForStrings 和 ReadString这三个方法时是否获取Escape字符(也就是特殊控制字符，如"\n")，默认是会获取的。
    ```python
    crt.Screen.IgnoreEscape [ = True | False ]
    ```
    参数：
  * true|false：当设置为true时不会获取特殊字符，为false时会获取，默认为false

#### MatchIndex

* 当使用WaitForStrings 和 ReadString这两个方法获取字符串时，会根据参数的位置获取返回值，而MatchIndex就是这个位置，从1开始计算，如果没有一个匹配到则返回0，可以根据下面的例子来看。
    ```python
    crt.Screen.MatchIndex
    ```
    例子
    ```python
    outPut = crt.Screen.WaitForStrings(["error","warning","#"],10)
    index = crt.Screen.MatchIndex
    if (index == 0):
        crt.Dialog.MessageBox("Timed out!")
    elif (index == 1):
        crt.Dialog.MessageBox("Found 'error'")
    elif (index == 2):
        crt.Dialog.MessageBox("Found 'warning'")
    elif (index == 3):
        crt.Dialog.MessageBox("Found '#'")
    ```

#### Synchronous

* 设置屏幕的同步属性，关于该属性需要谨慎对待，若设置为false，则在脚本中使用WaitForString、WaitForStrings或ReadString函数时可能存在丢失一部分数据的现象，而设置为true时不会，但是设置为true后可能会存在屏幕卡顿的情况，出现这两种现象的原因应该是和这几个函数以及打印字符到Screen的机制有关系，具体内部原因不明，就具体使用而言，如果是跑脚本的话最好还是不要设置为true，大量的卡顿看着就会蛋疼了，还可能会造成CRT卡死。
    ```python
    crt.Screen.Synchronous [ = True | False ]
    ```
    参数
  * true|false ：默认为false

### Screen方法

#### Clear()

* 清屏功能
    ```python
    crt.Screen.Clear()
    ```

#### get()

* 按照坐标取出一个矩形框内的屏幕上的字符(即从某行某列开始到其它行其它列)，不包含字符串中的回车换行符，所以这个多用于获取无格式的光标处字符串或某小段特定区域字符串。
    ```python
    crt.Screen.Get(row1, col1, row2, col2)
    getScr = crt.Screen.Get(31,50,31,56)
    ```
    > 可以结合CurrentColumn\CurrentRow使用

#### get2()

* 按照坐标取出一个矩形框内的屏幕上的字符(即从某行某列开始到其它行其它列)，包含字符串中的回车换行符，所以这个多用于获取大段带格式的字符串。
    ```python
    crt.Screen.Get2(row1, col1, row2, col2)
    getScr = crt.Screen.Get2(29,1,35,20)
    ```
    > 可以结合CurrentColumn\CurrentRow使用

#### IgnoreCase()

* 使用全局参数设置控制在使用WaitForString、WaitForStrings和ReadString这三个函数时是否对大小写敏感，默认为false指大小写敏感即大小写字符串都会检查，设置为true时则不会检测大小写。
    ```python
    crt.Screen.IgnoreCase
    crt.Screen.IgnoreCase = true
    ```
    > 请注意，语法中并没有带()，根据语法来看，这个不像是方法，但是在CRT的使用说明中标注为了方法而不是属性，且在python的脚本中是当做方法使用的，因此这里先归类为方法

#### Send()

* 向远端设备或者向屏幕(向屏幕发送的功能是CRT7.2以后版本才提供的)发送字符串。如语法中所表示的，string是待发送的字符串，这个字符串可以包含转码字符比如"\r","\n","\03"(ctrl+c)，当向屏幕上发送字符串时需要指定第二个参数为true。有了向屏幕发送字符串的功能，我们就可以很方便的和用户进行交互了。可以打印出一些我们需要的报错信息之类的。
    ```python
    crt.Screen.Send(string, [, bSendToScreenOnly])
    crt.Screen.Send("show memory\r\n") # 向远程设备发送英文命令"show memory
    ```
    > 可以发送变量的值，发送后最好加一个延迟

#### SendKeys()

* 向当前窗口发送按键，包含组合按键，
    ```python
    crt.Screen.SendKeys(string)
    crt.screen.sendkeys("^%c") #发送类似"CTRL+ALT+C"等这样的组合键
    ```
    > 这个功能需要语言本身支持，目前只有VBS和JS脚本可以使用，Python和Perl都不可以。
    >
    具体可以有哪些按键，参照下表,可以根据需要自由组合：
    Key(按键) | Argument(参数)
    --- | ---
    SHIFT | +
    CTRL | ^
    ALT | %
    BACKSPACE | {BACKSPACE}, {BS}, or {BKSP}
    BREAK | {BREAK}
    CAPS LOCK | {CAPSLOCK}
    DEL or DELETE | {DELETE} or {DEL}
    DOWN ARROW | {DOWN}
    END | {END}
    ENTER | {ENTER} or ~
    ESC | {ESC}
    HELP | {HELP}
    HOME | {HOME}
    INS or INSERT | {INSERT} or {INS}
    LEFT ARROW | {LEFT}
    NUM LOCK | {NUMLOCK}
    PAGE DOWN | {PGDN}
    PAGE UP | {PGUP}
    PRINT SCREEN | {PRTSC}
    RIGHT ARROW | {RIGHT}
    SCROLL LOCK | {SCROLLLOCK}
    TAB | {TAB}
    UP ARROW | {UP}
    F1, F2, ... F16 | {F1}, {F2}, ... {F16}
    0, 1, ... 9 on number pad | {NUM_0}, {NUM_1}, ... {NUM_9}
    . on number pad | {NUM_.}
    / on number pad | {NUM_/}
    * on number pad | {NUM_*}
    - on number pad | {NUM_-}
    + on number pad | {NUM_+}
    ENTER on number pad | {NUM_ENTER}
    HOME on number pad | {NUM_HOME}
    PAGE UP on number pad | {NUM_PGUP}
    END on number pad | {NUM_END}
    PAGE DOWN on number pad | {NUM_PGDN}
    UP ARROW on number pad | {NUM_UP}
    DOWN ARROW on number pad | {NUM_DOWN}
    LEFT ARROW on number pad | {NUM_LEFT}
    RIGHT ARROW on number pad | {NUM_RIGHT}

#### SendSpecial()

* 可以发送特殊控制码，这个控制码是Crt内置的功能，具体可以包含的有Menu、Telnet、VT functions功能列表中提供的所有功能，
    ```python
    crt.Screen.SendSpecial(string)
    # 以下是Crt文档中举的例子，具体还有什么我也没有不知道
    crt.screen.SendSpecial("MENU_PASTE")
    crt.screen.SendSpecial("TN_BREAK")
    crt.screen.SendSpecial("VT_PF1")
    ```

#### WaitForCursor()

* 等待光标移动，当移动时返回值为true，当有超时时间参数且超时时返回false，否则会一直等待光标移动。利用这个功能可以用来判断一个命令的输出是否结束，只不过超时时间是以秒为单位的，对于脚本当中，这个时间还是略显久了。
    ```python
    crt.Screen.WaitForCursor([timeout])
    # 每5秒内光标有移动时即发送一个命令
    while True:
    if (crt.Screen.WaitForCursor(5)):
        crt.Screen.Send("show version\r\n")
    ```

#### WaitForKey()

* 检测有键盘按键时返回true，当有超时时间参数且超时时返回false，否则会一直等待按键。只可惜这个函数不知道输入的键是什么，否则就可以针对性的判断了，它只能检测到有输入而已。
    ```python
    crt.Screen.WaitForKey([timeout])
    # 每5秒内有输入时发送一个命令
    while True:
        if (crt.Screen.WaitForKey(5)):
            crt.Screen.Send("show version\r\n")

    ```

#### WaitForString()

* 一般用于发送命令后等待某字符串，这个字符串只要是屏幕上出现的即可，哪怕是粘贴上去的命令也会同样被检测到，也可以用于等待屏幕的输出打印，不需要先发送命令。不过一般我们使用它来检测的都是发送命令后出现的标识符。
    ```python
    crt.Screen.WaitForString(string,[timeout],[bCaseInsensitive])
    # 发送命令，并在5秒内获取到对应的字符串后发送一条命令
    crt.Screen.Send("\r\n")
    if (crt.Screen.WaitForString("#",5)):
        crt.Screen.Send("ifconfig\r\n")
    crt.Screen.Send(chr(3))
    if (crt.Screen.WaitForString(">",5)):
        crt.Screen.Send("who\r\n")
    ```
    参数：
  * string，必选参数，等待的字符串，可以是特殊字符比如:\r\n；
  * timeout，可选参数，超时时间，当检测不到对应字符串时会返回false，没有此参数时会一直等待；
  * bCaseInsensitive，可选参数，大小写不敏感，默认值是false，表示将检测字符串的大小写，当为true时不检测大小写

#### WaitForStrings()

* 和WaitForString是同样的功能，只不过可以等待多个字符串，如果有匹配到某个字符串，则返回值该字符串在这些字符串中的位置，位置值从1开始。若在超时时间内没有匹配到则返回false，没有超时时间时会一直等待。
    ```python
    crt.Screen.WaitForStrings([string1,string2..],[timeout],[bCaseInsensitive])
    # 参考例子
    outPut = crt.Screen.WaitForStrings(["error","warning","#"],10)
    index = crt.Screen.MatchIndex
    if (index == 0):
        crt.Dialog.MessageBox("Timed out!")
    elif (index == 1):
        crt.Dialog.MessageBox("Found 'error'")
    elif (index == 2):
        crt.Dialog.MessageBox("Found 'warning'")
    elif (index == 3):
        crt.Dialog.MessageBox("Found '#'")
    ```
    > 也用到了crt.Screen.MatchIndex功能

    参数：
  * string，必选参数，等待的字符串，可以是特殊字符比如:\r\n；
  * timeout，可选参数，超时时间，当检测不到对应字符串时会返回false，没有此参数时会一直等待；
  * bCaseInsensitive，可选参数，大小写不敏感，默认值是false，表示将检测字符串的大小写，当为true时不检测大小写

#### ReadString()

* 这个功能和上面的WaitForStrings函数有些类似，都是等待某几个字符串出现，不过不同的是，ReadString函数还会读取字符串之前的所有出现的字符，这个功能可以很方便的用于发送一个命令后获取这个命令的输出结果，不过这个函数也不是特别稳定，因为很可能存在命令的输出结果很快，而屏幕又没有捕捉到时，要么会由于超时而返回false，要么会一直等待，最终返回的都是空值，因此完全依靠该函数获取命令的输出的话并不是很把稳(如果程序对于稳定性要求很高的话，那么最好还是不要依赖这个函数。)
    ```python
    crt.Screen.ReadString([string1,string2..],[timeout],[bCaseInsensitive])
    # 发送命令并根据提示符获取命令的输出
    crt.Screen.Send("show version\r\n")
    crt.Screen.WaitForString("show version",2)
    outPut = crt.Screen.ReadString(["error","warning","#"],10)
    index = crt.Screen.MatchIndex
    if (index == 0):
        crt.Dialog.MessageBox("Timed out!")
    elif (index == 1):
        crt.Dialog.MessageBox("Found 'error'")
    elif (index == 2):
        crt.Dialog.MessageBox("Found 'warning'")
    elif (index == 3):
        crt.Dialog.MessageBox("Found '#'")
    ```
    > 在这个举例中可以看到还使用了WaitForString，为什么要使用这个，有两个方面原因，一是确定命令已经被发送到了远端设备，二是确保命令的输出结果中没有改命令，而仅仅是该命令的输出结果

    参数：
  * string，必选参数，等待的字符串，最少有一个，可以是特殊字符比如:\r\n；
  * timeout，可选参数，超时时间，当检测不到对应字符串时会返回false，没有此参数时会一直等待；
  * bCaseInsensitive，可选参数，大小写不敏感，默认值是false，表示将检测字符串的大小写，当为true时不检测大小写。

## python脚本编写学习指南

 > 在测试网络设备中，通常使用脚本对设备端进行配置和测试以及维护；对于PE设备的测试维护人员来说使用较多是SecureCRT工具；SecureCRT支持VB、JavaScript、Python等多种脚本语言，为了实现脚本在CRT中更加丰富稳定地执行，掌握CRT的常用函数是非常有用的。接下来的时间我将对SecureCRT脚本编写的常用函数展开学习应用。

## 使用python语言实现SecureCRT中的Dialog功能

```python
# $language = "Python"
# $interface = "1.0"

#crt.Dialog.FileOpenDialog([title,[buttonLabel,[defaultFilename,[filter]]]])
#弹出一个对话框，用于选择单个文件;如果选择了具体文件则返回该文件的绝对路径，如果选择了弹窗的“取消”，则返回空。
filePath =  crt.Dialog.FileOpenDialog("please open a file","open","a.log","(*.log)|*.log")
#filePath =  crt.Dialog.FileOpenDialog("","","a.log","")
#crt.Dialog.MessageBox(message, [title, [icon|buttons]]) 警告、按钮类型弹出一个消息框，可以定义按钮，使用按钮和文本消息来实现和用户的简单对话；
crt.Dialog.MessageBox(filePath,"",64|0)
crt.Dialog.MessageBox("会话已断开","session",64|2)
crt.Dialog.MessageBox("确认是否退出","session",32|1)
crt.Dialog.MessageBox("确认是否退出","session",32|3)
crt.Dialog.MessageBox("是否继续安装","session",32|4)
crt.Dialog.MessageBox("此会话已打开","session",48|5)
crt.Dialog.MessageBox("无法连接此窗口","session",16|6)

#crt.Dialog.Prompt(message [, title [,default [,isPassword ]]])
#弹出一个输入框，用户可以填写文字，比如填写文件名，填写路径，填写IP地址等,运行结果如果点击'ok'，返回输入的字符串，否则返回""
password = crt.Dialog.Prompt("password","session","admin",False)
crt.Dialog.MessageBox(password,"password",64|0)
password = crt.Dialog.Prompt("password","session","",True)
crt.Dialog.MessageBox(password,"password",64|0)
```

## 使用python语言实现SecureCRT中的Screen功能

```python
# $language = "Python"
# $interface = "1.0"

# CurrentColumn返回当前光标的列坐标。
curCol =  crt.Screen.CurrentColumn
crt.Dialog.MessageBox(str(curCol))

# CurrentRow返回当前光标的行坐标。
curRow = crt.Screen.CurrentRow
crt.Dialog.MessageBox(str(curRow))

# Columns 返回当前屏幕的最大列宽
cols = crt.Screen.Columns
crt.Dialog.MessageBox(str(cols))

# Rows 返回当前屏幕的最大行宽
rows = crt.Screen.Rows
crt.Dialog.MessageBox(str(rows))

#IgnoreEscape 定义当使用WaitForString、WaitForStrings和ReadString这三个方法时是否获取Escape字符（特殊字符如回车）默认是会获取的
crt.Screen.IgnoreEscape = False
crt.Dialog.MessageBox(crt.Screen.ReadString(["\03"],5)) #获取ctrl+c

crt.Screen.IgnoreEscape = True
crt.Dialog.MessageBox(crt.Screen.ReadString(["\03"],2)) #不获取ctrl+c

# MatchIndex 定义当使用WaitForStrings和ReadString这三个方法时会根据参数的位置 获取返回值，从1开始计算，如果没有一个匹配则返回0.
outPut = crt.Screen.ReadString(["error","warning","#"],10)
index = crt.Screen.MatchIndex
if (index == 0):
    crt.Dialog.MessageBox("Timed out!")
elif (index == 1):
    crt.Dialog.MessageBox("Found 'error'")
elif (index == 2):
    crt.Dialog.MessageBox("Found 'warning'")
elif (index == 3):
    crt.Dialog.MessageBox("Found '#'")

# Synchronous 设置屏幕的同步属性。若设置为false，则在脚本中使用WaitForString、WaitForStrings、ReadString函数时可能存在丢失一部分数据的现象，设置为true后可能会存在屏幕卡顿的情况，默认为false
crt.Screen.Synchronous = True
crt.Screen.Send("\r\n")
crt.Screen.ReadString("#")
crt.Screen.Send("\r\n")
crt.Screen.WaitForString("#")
crt.Screen.Send("\r\n")
crt.Screen.WaitForStrings(["#",">"])
crt.Screen.Send("conf t\r\n")

# 方法
# Clear()清屏功能
# crt.Screen.Clear()

# get()按照坐标取出一个矩形框内的屏幕上的字符(即从某行某列开始到其它行其它列)，不包含字符串中的回车换行符，所以这个多用于获取无格式的光标处字符串或某小段特定区域字符串。
out = crt.Screen.Get(row1, col1, row2, col2)
crt.Dialog.MessageBox(out)

# get2()解释按照坐标取出一个矩形框内的屏幕上的字符(即从某行某列开始到其它行其它列)，包含字符串中的回车换行符，所以这个多用于获取大段带格式的字符串。
crt.Screen.Get2(row1, col1, row2, col2)

# IgnoreCase 使用全局参数设置控制在使用WaitForString、WaitForStrings和ReadString这三个函数时是否对大小写敏感，默认为false大小写字符串都会检查，设置为true时则不会检测大小写。
crt.Screen.IgnoreCase = True
crt.Screen.Send("show memory\r\n")
crt.Screen.WaitForString("more")
crt.Screen.Send("\r\n")
crt.Screen.WaitForStrings("more","#")
crt.Screen.Send("\r\n")
crt.Screen.ReadString("more","#")

# Send() 向远端设备或者屏幕发送字符串，当向屏幕发送字符串时需要指定第二个参数为Ture
crt.Screen.Send("show version\r\n")
crt.Screen.Send("\r\nhello,world!\r\n",True)
crt.Screen.IgnoreCase = True
while (crt.Screen.WaitForString("more",10)):
    crt.Screen.Send("\r\n")

# SendKeys()向当前窗口发送按键，包含组合按键，比如可以发送类似"CTRL+ALT+C"等这样的组合键，这样写即可：crt.screen.sendkeys("^%c");这个功能需要语言本身支持，目前只有VBS和JS脚本可以使用。

# SendSpecial()可以发送特殊控制码，这个控制码是Crt内置的功能，具体可以包含的有Menu、Telnet、VT functions功能列表中提供的所有功能，
crt.Screen.SendSpecial("vT_HOLD_SCREEN")

# WaitForCursor()等待光标移动，当移动时返回值为true，当有超时时间参数且超时时返回false，否则会一直等待光标移动。利用这个功能可以用来判断一个命令的输出是否结束，
crt.Screen.WaitForCursor(5)
crt.Screen.Send("\r\nhello,world!\r\n",True)
if ( crt.Screen.WaitForCursor(5)):
    crt.Screen.Send("show version\r\n")

# WaitForKey()检测有键盘按键时返回true，当有超时时间参数且超时时返回false，否则会一直等待按键
if (crt.Screen.WaitForKey(5)):
    crt.Screen.Send("show version\r\n")

# WaitForString()一般用于发送命令后等待某字符串
# crt.Screen.WaitForString(string,[timeout],[bCaseInsensitive])
crt.Screen.WaitForString("#",10)

# WaitForStrings()与WaitForString是同样的功能，可以等待多个字符串
outPut = crt.Screen.WaitForStrings(["error","warning","#"],10)
index = crt.Screen.MatchIndex
if (index == 0):
    crt.Dialog.MessageBox("Timed out!")
elif (index == 1):
    crt.Dialog.MessageBox("Found 'error'")
elif (index == 2):
    crt.Dialog.MessageBox("Found 'warning'")
elif (index == 3):
    crt.Dialog.MessageBox("Found '#'")

# ReadString()与WaitForStrings功能类似，都是等待某几个字符出现，不同的是它还会读取字符串之前出现的所有字符。
crt.Screen.ReadString([string1,string2..],[timeout],[bCaseInsensitive])
1、string，必选参数，等待的字符串，最少有一个，可以是特殊字符比如:\r\n；
2、timeout，可选参数，超时时间，当检测不到对应字符串时会返回false，没有此参数时会一直等待；
3、bCaseInsensitive，可选参数，大小写不敏感，默认值是false，表示将检测字符串的大小写，当为true时不检测大小写。
```
