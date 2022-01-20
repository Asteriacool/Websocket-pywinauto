import socketio
import zlib
import exchange
import os
import time
from threading import Timer
import psutil
import datetime



count = 0
def restart_process(name):
    formattime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pids = psutil.pids()
    name_list = []
    for pid in pids:
        p = psutil.Process(pid)
        process_name = p.name()
        name_list.append(process_name)
    # 如果当前进程中已经没有了此应用
    if name not in name_list:
        # 声明变量的全局性
        global count
        count += 1
        print(formattime + "第" + str(count) + "次发现异常重连")
        os.system("start C:\\\"Program Files\"\\\"CAD Exchanger\"\\bin\\Exchanger.exe")
    global timer
    timer = Timer(8, restart_process, ("Exchanger.exe",))
    timer.start()


sio = socketio.Client();


# 客户端注册
@sio.event
def connect():
    print("I'm connected!")
    sio.emit('CONV_REGISTER', {
        'clientKey': 'a56cb044285e017a329401182ec58578',
        'fileType': ['stp', 'step', 'sldprt', 'sldasm']
    });


@sio.on('CONV_REGISTER')
def on_message(data):
    if data['registerOk']:
        return;
    print('register failed');


@sio.event
def connect_error(data):
    print("The connection failed!")


# 客户端注销
@sio.event
def disconnect():
    print("I'm disconnected!")
    sio.emit('CONV_DEREGISTER', {
        'clientKey': 123,
        'fileType': ['stp', 'step']
    });


# 转码请求
@sio.on('CONV_REQUEST')
def on_message(data):
    print('I received a message!')
    # 将获取到的文件存到指定的路径下
    in_path = "C:\\Users\\aster\\Desktop\\分布式转码\\input\\"
    # 判断是否存在导入文件的存放目录，如果不存在该目录，则创建
    if not os.path.exists(in_path):
        os.mkdir(in_path)
    fp = open(in_path + data['fileName'], 'wb');
    if data['zipped']:
        fp.write(zlib.decompress(data['data']));
    else:
        fp.write(data['data']);
    fp.close();
    print('create file ' + data['fileName']);

    filename = data['fileName']
    out_path = "C:\\Users\\aster\\Desktop\\分布式转码\\output\\"

    # 创建并初始化计时器线程
    timer = Timer(8, restart_process, ("Exchanger.exe",))
    timer.start()
    # --------------------文件转换
    try:
        # 成功转换正常进行的流程
        result = exchange.autoexchange(in_path, filename, out_path)
        if result == -1:
            exchange.kill_process('Exchanger')
            time.sleep(2)
        else:  # 文件转换成功
            print("文件转换完成")
            # 从指定的路径中获取格式转换完成的文件
            fp2 = open(out_path + filename.split(".")[0] + '.ifc', 'rb');
            content = fp2.read();
            print(len(content));
            zippedContent = zlib.compress(content);
            print(len(zippedContent));
    except Exception as e:
        print(repr(e))
        exchange.kill_process('Exchanger')
    finally:
        timer.cancel()

    # fp2 = open(out_path + filename.split(".")[0] + '.ifc', 'rb');
    # content = fp2.read();
    # print(len(content));
    # zippedContent = zlib.compress(content);
    # print(len(zippedContent));

    sio.emit('CONV_RESPONSE', {
        'fileName': data['fi'] + '.ifc',
        'socketId': data['socketId'],
        'uuid': data['uuid'],
        'fi': data['fi'],
        'convSucess': True,
        'zipped': True,
        'data': zippedContent
    });


# sio.connect('http://localhost:8092');
sio.connect('http://47.92.115.234:8090');
sio.wait();
