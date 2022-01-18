### 基于WebSocket实现网页端的文件转换

#### 【SocketIO背景知识】

客户端和服务器端可以双向主动通信、实现真正的双向平等对话

* 完成握手动作之后，浏览器和服务器端之间形成了一条快速通道
* 相互沟通的header很小
* 服务器不再被动接收到浏览器的请求之后才返回数据，有新的数据时就主动推送给浏览器

##### WebSocket协议

服务器端可以主动直接将产生的数据推送给浏览器端

* 浏览器向服务器发送一个HTTP请求（包含附加头信息）

* 服务器端解析头信息

* 服务器端产生应答信息

* 服务器端和客户端建立握手连接

--------------

① Web应用端调用new WebSocket（url接口）

② 浏览器与服务器通过三次TCP握手建立连接如果失败，Web会受到错误消息通知

③ 在TCP建立连接成功后，浏览器通过HTTP协议传送WebSocket支持的版本号、原始地址、主机地址等给服务器端

④ 服务器接收到来自浏览器的握手请求后，如果数据包和格式正确，协议版本匹配等，就接受本次的握手连接，并给出相应的HTTP数据回复

⑤ 浏览器在回复数据包后，如果数据包的内容和格式都没有问题，几句表示本次连接成功，触发onopen消息如果握手失败，就浏览器端会收到onerror消息

⑥ 此时开发者可以通过send接口向服务器发送数据

##### HTTP协议

通信协议的头部数据量很大

* 浏览器端向服务器端发出请求资源

* 服务器端返回对应的数据

______________________________________

Polling轮询的方式

浏览器端定时向服务器端发送请求

服务器端得到请求之后将最新的数据返回给浏览器

问题：如果没有服务器没有更新数据，在响应请求结果的时候，是将老数据传送过去改进后的LongPolling 轮询的方式

* 浏览器端发送请求
* 如果服务器端有新的数据需要传送，就立即传送
* 如果服务器端没有新的数据需要传送，就暂时不响应请求，等有新的数据来到的时候，再去响应这个请求
  * 如果服务器的数据长期没有更新，浏览器端发送的HTTP请求就会超时，超时候会立即发一个新的请求给服务器

#### 【WebSoket和TCP、HTTP的关系】

Web开发者调用的WebSocket的send函数在Browser的实现中最终都是通过TCP的系统接口进行传输的。WebSocket和HTTP协议样都属于应用层协议，那么它们之间有没有什么关系呢？答案是肯定的，WebSocket在建立握手连接时，数据是通过HTTP协议传输的。但在建立连接之后，真正的数据传输阶段是不需要HTTP参与的。

![Image](C:\Users\aster\Desktop\分布式转码\Image.png)

#### **【实现功能】**

一、上传源文件

1.用户通过浏览器上传文件（这里用另外一个文件夹扮演用户的位置）

2.浏览器在接收到文件数据之后，在本地的文件夹中创建一个路径，用来所有需要处理的文件

二、文件格式转换

1.服务器将文件的名字和存放路径和输出的路径都提供给后台程序

2.本地的CAD转换应用通过路径和文件名得到存放在本地的待处理文件，并进行处理

3.本地应用程序根据指定的文件路径将完成转换后的文件保存

三、上传源文件

1.服务器根据预先规定好的文件路径去相应的位置拿到完成文件

2.浏览器对源文件进行展示

细节问题：

* 问题：当应用程序处于最小化的时候，如何弹出
  * 思路：加入restore函数

```python
win_main = app.window(class_name='ExchangerGui_MainWindow_QMLTYPE_259')
win_main.restore()
```

* 问题：将从另外一个文件夹中上传的文件写到指定路径下
  * 思路，fp.open的第一个参数前面加上想要的路径

* 文件的路径
  * 在项目的目录文件中新建input文件夹，用来存放用户从浏览器上传后存放在本地的内容
  * 在项目的目录文件中新建output文件夹，用来存放文件格式转换完成之后的文件
    * 通过此文件夹上传到浏览器中进行呈现
  * 修改导入文件的方式，用输入名字（路径）的方式
    * 点击上方的空白位置
    * 引入keyborad库，修改文件所在的路径为input文件夹的路径

```python
rect = win_brow.child_window(auto_id="1001", control_type="ToolBar").rectangle()
print(rect.top, rect.bottom, rect.left, rect.right)
w = rect.right - int((rect.right - rect.left) / 4)
h = int((rect.bottom + rect.top) / 2)
print(w, h)
mouse.click(button='left', coords=(w, h))
# keyboard.send_keys("C:\\Users\\aster\Desktop")
keyboard.send_keys(path)
keyboard.send_keys("{VK_RETURN}")
```

* 根据文件的名字在此路径下寻找指定的文件
  * 点击文件名后面的框格
  * 全选
  * 输入文件的名字
  * 点击打开，或者提示文件存在

* 修改文件的导出方式
  * 寻找指定名字的文件夹
  * 导入的时候文件的名字前半部分与导入的时候的后缀之前的部分相同
  * 导出的时候点选不到ifc块
    * 思路：在选中相关块之前首先点击滑动块的某个位置，使得ifc按钮和obj按钮同时出现在目标范围之中

* 导出的时候名字相关的框会挡住保存按钮的问题
  * 思路：更改点击保存为空格

* 问题：由于新进程的打开时间比较长，在后面的程序需要拿到程序窗口中的某些元素的时候出现拿不到的问题
  * 解决思路：对于新运行起来的程序，需要等待一段时间，再执行后面的操作，同时添加当前进程存在与否的判断

```python
def get_app():
    if isinstance(proc_exist('Exchanger.exe'), int):
        # 如果正在运行
        app = application.Application(backend='uia').connect(path='C:/Program Files/CAD Exchanger/bin/exchanger')
    else:
        # 如果没有运行
        app = application.Application(backend='uia').start('C:/Program Files/CAD Exchanger/bin/exchanger')
        time.sleep(2)
    # 加入对于是否存在的判断，如果不存在就进入等待
    if app.is_process_running():
        return app
    else:
        print("无法打开进程")
```

