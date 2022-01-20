from pywinauto import application
from pywinauto import mouse, keyboard
import time
import psutil
import os
import pyperclip


def proc_exist(process_name):
    p1 = psutil.pids()
    for pid in p1:
        if psutil.Process(pid).name() == process_name:
            return pid


def get_app():
    if isinstance(proc_exist('Exchanger.exe'), int):
        # 如果正在运行
        app = application.Application(backend='uia').connect(path='C:/Program Files/CAD Exchanger/bin/exchanger')
    else:
        # 如果没有运行，就重复打开
        os.system("start C:\\\"Program Files\"\\\"CAD Exchanger\"\\bin\\Exchanger.exe")
        time.sleep(2)
        app = application.Application(backend='uia').connect(path='C:/Program Files/CAD Exchanger/bin/exchanger')
        n = 0
        while not app.is_process_running():
            app = application.Application(backend='uia').connect(path='C:/Program Files/CAD Exchanger/bin/exchanger')
            time.sleep(1)
            n += 1
            # 20秒后若仍然无法连接到进程，就退出
            if n > 20:
                print("进程连接失败")
                break
    # 加入对于是否存在的判断，如果不存在就进入等待
    if app.is_process_running():
        return app
    else:
        print("无法打开进程")


# 判断文件列表中是否存在某个文件
def document_is_exist(window, name):
    element = window.descendants(control_type="ListItem", title=name)
    return len(element) != 0


# 判断是否有重命名弹窗
# 如果有弹窗，就把原有的文件覆盖
def controlwindow_is_exist(window):
    element = window.child_window(title="确认另存为", control_type="Window")
    if element.exists():
        win_control = window.child_window(title="确认另存为", control_type="Window")
        btn_yes = win_control.child_window(title="是(Y)", control_type="Button")
        btn_yes.click_input()


# 功能：导出obj文件
# window是处理的窗口
# filename是转换之前的文件名字
# out_path是输出的路径
# 返回值：如果导出成功就返回文件的新名字，如果导出失败就返回-1
def export_obj(window, filename, out_path):
    oldname = filename
    newname = oldname.split(".")[0]
    time.sleep(1)
    # 获取菜单中导出文件的按钮
    btn_export = window.child_window(title="Export", control_type="Button")
    btn_export.click_input()
    # 获取弹出菜单
    stackview = window.child_window(class_name="QQuickStackView")
    # 当前菜单框中没有所需要的格式框的问题
    box = stackview.rectangle()
    x = box.right - 3
    y = int(box.top + (box.bottom - box.top) / 3)
    mouse.click(button='left', coords=(x, y))

    box_obj = stackview.child_window(title="OBJ", control_type="Text")
    box_obj.click_input()
    # 获取并点击最后的导出文件按钮
    btn_export1 = stackview.child_window(title="Export", control_type="Button")
    btn_export1.click_input()
    # 获取弹出的窗口
    win_brow = window.child_window(title="Please choose a file", control_type="Window")
    # 修改文件夹浏览的路径
    rect = win_brow.child_window(auto_id="1001", control_type="ToolBar").rectangle()
    w = rect.right - int((rect.right - rect.left) / 4)
    h = int((rect.bottom + rect.top) / 2)
    mouse.click(button='left', coords=(w, h))
    keyboard.send_keys(out_path)
    # keyboard.send_keys("C:\\Users\\aster\\Desktop")
    keyboard.send_keys("{VK_RETURN}")
    # 修改文件文件名进行保存
    win_brow.child_window(title="文件名:", auto_id="1001", control_type="Edit").type_keys('^a')
    pyperclip.copy(newname)
    window.child_window(title="文件名:", auto_id="1001", control_type="Edit").type_keys('^v')
    keyboard.send_keys("{VK_RETURN}")

    # 如果有弹窗就替换掉已经存在的转换后格式文件
    controlwindow_is_exist(win_brow)
    # 处理文件崩溃的情况：如果当前的窗口不存在，则文件进入了崩溃的状态，此时返回false
    if not window.exists():
        print("文件发生崩溃")
        return -1
    else:
        # 添加对于文件导出成功与否的判断
        exported = window.child_window(title="Export completed.", control_type="Edit")
        for i in range(2):
            while not exported.exists():
                time.sleep(0.5)
                exported = window.child_window(title="Export completed.", control_type="Edit")
            print("文件导出成功！")
            return newname + ".obj"
        else:
            print("文件导出失败！")
        return -1


# 功能：导出ifc文件
# window是处理的窗口
# filename是转换之前的文件名字
# out_path是输出的路径
def export_ifc(window, filename, out_path):
    oldname = filename
    newname = ".".join(oldname.split(".")[:-1])
    time.sleep(1)
    # 获取菜单中导出文件的按钮
    btn_export = window.child_window(title="Export", control_type="Button")
    btn_export.click_input()
    # 获取弹出菜单
    stackview = window.child_window(class_name="QQuickStackView")
    # 当前菜单框中没有所需要的格式框的问题
    box = stackview.rectangle()
    x = box.right - 3
    y = int(box.top + (box.bottom - box.top) / 3)
    mouse.click(button='left', coords=(x, y))

    box_obj = stackview.child_window(title="IFC", control_type="Text")
    box_obj.click_input()
    # 获取并点击最后的导出文件按钮
    btn_export1 = stackview.child_window(title="Export", control_type="Button")
    btn_export1.click_input()
    # 获取弹出的窗口
    win_brow = window.child_window(title="Please choose a file", control_type="Window")

    # 修改文件夹浏览的路径
    rect = win_brow.child_window(auto_id="1001", control_type="ToolBar").rectangle()
    w = rect.right - int((rect.right - rect.left) / 4)
    h = int((rect.bottom + rect.top) / 2)
    mouse.click(button='left', coords=(w, h))
    keyboard.send_keys(out_path)
    # keyboard.send_keys("C:\\Users\\aster\\Desktop")
    keyboard.send_keys("{VK_RETURN}")
    # 修改文件文件名进行保存
    win_brow.child_window(title="文件名:", auto_id="1001", control_type="Edit").type_keys('^a')
    pyperclip.copy(newname)
    window.child_window(title="文件名:", auto_id="1001", control_type="Edit").type_keys('^v')
    keyboard.send_keys("{VK_RETURN}")
    # 如果有弹窗就替换掉已经存在的转换后格式文件
    controlwindow_is_exist(win_brow)
    # 处理文件崩溃的情况：如果当前的窗口不存在，则文件进入了崩溃的状态，此时返回false
    if not window.exists():
        print("文件发生崩溃")
        return -1
    else:
        # 添加对于文件导出成功与否的判断
        exported = window.child_window(title="Export completed.", control_type="Edit")
        for i in range(2):
            while not exported.exists():
                time.sleep(0.5)
                exported = window.child_window(title="Export completed.", control_type="Edit")
            print("文件导出成功！")
            return newname + ".ifc"
        else:
            print("文件导出失败！")
        return -1


# 功能：导入文件：修改窗口中的文件路径,查找文件并打开
def get_item(in_path, filename, window):
    try:
        # 修改文件夹浏览的路径
        rect = window.child_window(auto_id="1001", control_type="ToolBar").rectangle()
        w = rect.right - int((rect.right - rect.left) / 4)
        h = int((rect.bottom + rect.top) / 2)
        mouse.click(button='left', coords=(w, h))
        keyboard.send_keys(in_path)
        # keyboard.send_keys("C:\\Users\\aster\\Desktop")
        keyboard.send_keys("{VK_RETURN}")
        # 修改文件文件名进行搜索的方式(type_keys)无法键入符号
        window.child_window(title="文件名(N):", auto_id="1148", control_type="Edit").type_keys('^a')
        pyperclip.copy(filename)
        window.child_window(title="文件名(N):", auto_id="1148", control_type="Edit").type_keys('^v')
        window.child_window(title="打开(O)", auto_id="1", control_type="Button").click_input()
    except:
        print("文件不存在")
        return -1


def kill_process(name):
    # 获取当前所有应用的pids
    pids = psutil.pids()
    for pid in pids:
        # 根据pid 获取进程对象
        p = psutil.Process(pid)
        # 获取每个pid的应用对应的文件名字
        process_name = p.name()
        # print(process_name)
        # 判断形参是否是应用名字的子串来判断进程是否存在
        if name in process_name:
            # print("Process name is: %s, pid is: %s" % (process_name, pid))  # 1,33664
            try:
                # 如果存在，就删掉
                import subprocess
                subprocess.Popen("cmd.exe /k taskkill /F /T /PID %i" % pid, shell=True)
            except OSError:
                print('没有此进程!!!')


# 正常情况下发生转换框架函数
# 返回值：如果正常为0，不正常为-1
def autoexchange(in_path, filename, out_path):
    # 获取应用
    app = get_app()
    # 获取主窗口
    time.sleep(1)
    win_main = app.window(class_name='ExchangerGui_MainWindow_QMLTYPE_259')
    win_main.restore()
    btn_browse = win_main.child_window(title="Browse", control_type="Button")
    if btn_browse.exists():
        # 点击浏览的按钮
        btn_browse.click_input()
        # 获取弹出的文件选择窗口
        win_brow = win_main.child_window(title="Please choose a file", control_type="Window")
        get_item(in_path, filename, win_brow)
        # 导入成功的判断：判断5秒之内是否有成功标签出现
        for i in range(0, 5):
            if win_main.child_window(title="Import completed.", control_type="Edit").exists():
                print("文件导入成功！")
                # 设置等待完成标签提示出现的时间，最大等待时间为5
                win_main.child_window(title="Display completed.", control_type="Edit").wait('exists', timeout=5)
                new_file = export_ifc(win_main, filename, out_path)
                if new_file != -1:
                    return 0
                else:
                    return -1
            else:
                time.sleep(1)
        else:
            print("文件导入失败！")
            return -1
    else:
        # 如果没有，就通过侧栏的菜单选择import按钮后再浏览目标文件
        btn_import = win_main.child_window(title="Import", control_type="Button")
        btn_import.click_input()
        # 获取弹出菜单
        stackview = win_main.child_window(class_name="QQuickStackView")
        btn_browse = stackview.child_window(title="Browse", control_type="Button")
        btn_browse.click_input()
        # 获取弹出的文件选择窗口
        win_brow = win_main.child_window(title="Please choose a file", control_type="Window")
        # 修改文件夹浏览的路径
        get_item(in_path, filename, win_brow)
        # 获取并点击下方的导入文件按钮
        btn_import1 = stackview.child_window(title="Import", control_type="Button")
        btn_import1.click_input()
        # 对导入成功的判断
        if win_main.child_window(title="Import completed.", control_type="Edit").exists():
            win_main.child_window(title="Display completed.", control_type="Edit").wait('exists', timeout=3)
            print("文件导入成功")
            # 导出文件
            new_file = export_ifc(win_main, filename, out_path)
            if new_file != -1:
                return 0
            else:
                return -1
        else:
            print("文件导入失败！")
            return -1

# # 包括异常处理
# def myexchange(in_path, filename, out_path):
#     # 如果出现异常就再执行一次
#     try:
#         # 成功转换
#         result = autoexchange(in_path, filename, out_path)
#         print("文件转换已经完成")
#         if result == -1:
#             kill_process('Exchanger')
#             time.sleep(2)
#     except Exception as e:
#         # if repr(e).split("\'")[1] == "timed out":
#         #     print("程序崩溃")
#         #     kill_process('Exchanger')
#         # else:
#         #     print(repr(e))
#         print(repr(e))
#         kill_process('Exchanger')
#     else:
#         kill_process('Exchanger')


# main函数中的内容是要出现在socket中的内容
# if __name__ == "__main__":
#     in_path = "C:\\Users\\aster\\Desktop\\分布式转码\\input"
#     filename = "kk35-7.step"
#     out_path = "C:\\Users\\aster\\Desktop\\分布式转码\\output"
#
#     myexchange(in_path, filename, out_path)
