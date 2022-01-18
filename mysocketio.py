import socketio
import zlib
import exchange
import os
import time

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
    # fp是一个step格式的文件，存到指定的路径下
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

    # --------------------文件转换
    try:
        # 成功转换
        result = exchange.autoexchange(in_path, filename, out_path)

        if result == -1:
            exchange.kill_process('Exchanger')
            time.sleep(2)
        else:  #文件转换成功
            print("文件转换完成")
            # 从指定的路径中获取格式转换完成的文件
            fp2 = open(out_path + filename.split(".")[0] + '.ifc', 'rb');
            content = fp2.read();
            print(len(content));
            zippedContent = zlib.compress(content);
            print(len(zippedContent));
    except Exception as e:
        # if repr(e).split("\'")[1] == "timed out":
        #     print("程序崩溃")
        #     kill_process('Exchanger')
        # else:
        #     print(repr(e))
        print(repr(e))
        exchange.kill_process('Exchanger')
    else:
        exchange.kill_process('Exchanger')

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
