import json
import os
import random
import sys
# os.chdir(os.getcwd()+'/UI')
# print(os.getcwd())
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QLabel
if 'UI' in os.getcwd():
    # sys.path.append('..')
    from last import *
    from creat_task import Ui_Dialog as CT_Dialog
    from all_tasks import Ui_Dialog as AT_Dialog
    from all_models import Ui_Dialog as AM_Dialog
    from dev_mana import Ui_Dialog as DM_Dialog
    from settings import Ui_Dialog as ST_Dialog
    from picture_preview import Ui_Dialog as PV_Dialog
    from utils import DataBase
    from UI.utils import ModelThread as Thread

    tasks_path = 'tasks/'
    data_path = 'data/'
    models_path = 'models/'

    icon_path = 'software_img/bitbug.ico'
else:
    from UI.last import *
    from UI.creat_task import Ui_Dialog as CT_Dialog
    from UI.all_tasks import Ui_Dialog as AT_Dialog
    from UI.all_models import Ui_Dialog as AM_Dialog
    from UI.dev_mana import Ui_Dialog as DM_Dialog
    from UI.settings import Ui_Dialog as ST_Dialog
    from UI.picture_preview import Ui_Dialog as PV_Dialog
    from UI.utils import DataBase
    from UI.utils import ModelThread as Thread

    tasks_path = 'UI/tasks/'
    data_path = 'UI/data/'
    models_path = 'UI/models/'

    icon_path = 'UI/software_img/bitbug.ico'
# global info
# dict_task存当前任务的参数
dict_task = {"task": "",  # 任务名
             "batch": -1,  # 是否为批处理
             "name": '',  # 产品编号
             "batch_name": [],   # 批处理时，文件名列表
             "model": ""}  # 模型名称

input_path = data_path + 'input/'
out_path = data_path + 'output/'
camera1_path = input_path + 'camera1/'
camera2_path = input_path + 'camera2/'
camera3_path = input_path + 'camera3/'
camera4_path = input_path + 'camera4/'
camera5_path = input_path + 'camera5/'
camera6_path = input_path + 'camera6/'
camera7_path = input_path + 'camera7/'
camera8_path = input_path + 'camera8/'


# 读取任务列表
def load_json_from_file(filename) -> dict:
    json_file = open(filename, 'r', encoding='utf-8')
    json_str = json.load(json_file)
    json_file.close()
    return json_str


# 存任务列表
def save_task():
    tasks_file = open(tasks_path + 'all_tasks.json', 'r', encoding='utf-8')
    try:
        all_tasks = json.load(tasks_file)
        tasks_file.close()
        num = all_tasks.values()[-1].split('task').split('.json')
        num = int(num)
        while f'task{num + 1}.json' in all_tasks.values():
            num += 1
        all_tasks[dict_task["task"]] = f'task{num + 1}.json'
    except:
        all_tasks = {}
        num = 0
        all_tasks[dict_task["task"]] = f'task{num + 1}.json'
    tasks_file = open(tasks_path + 'all_tasks.json', 'w', encoding='utf-8')
    json.dump(all_tasks, tasks_file, ensure_ascii=False)
    tasks_file.close()
    json.dump(dict_task, open(tasks_path + f'task{num + 1}.json', 'w', encoding='utf-8'), ensure_ascii=False)


class MyCTDialog(CT_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(MyCTDialog, self).__init__(parent=None)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.pushButton.clicked.connect(self.upload_file)
        self.pushButton_2.clicked.connect(self.create_task)
        self.pushButton_3.clicked.connect(self.cancel)
        self.radioButton.clicked.connect(self.update_config)
        self.lineEdit.setEnabled(True)
        self.pushButton.setEnabled(False)
        self.lineEdit_2.setEnabled(False)

    def update_config(self):
        if self.radioButton.isChecked():
            self.lineEdit.setEnabled(False)
            self.pushButton.setEnabled(True)
            self.lineEdit_2.setEnabled(True)
        else:
            self.lineEdit.setEnabled(True)
            self.pushButton.setEnabled(False)
            self.lineEdit_2.setEnabled(False)

    def upload_file(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, '上传批处理文件', '', '*.txt')
        self.lineEdit_2.setText(fileName)

    def create_task(self):
        dict_task['task'] = self.lineEdit_3.text()
        dict_task["batch"] = 1 if self.radioButton.isChecked() else 0

        dict_task['name'] = self.lineEdit.text()
        if self.lineEdit_2.text() and os.path.exists(self.lineEdit_2.text()):
            with open(self.lineEdit_2.text(), 'r', encoding='utf-8') as f:
                dict_task['batch_name'] = f.read().split('\n')
        dict_task['model'] = self.comboBox.itemText(self.comboBox.currentIndex())
        print(dict_task)
        save_task()
        self.setVisible(False)

    def cancel(self):
        self.setVisible(False)


class MyATDialog(AT_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(MyATDialog, self).__init__(parent=None)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        # 原来有东西的话先删除
        # while self.listWidget.count() > 0:
        #     self.listWidget.takeItem(0)
        self.tasks = load_json_from_file(tasks_path + 'all_tasks.json')
        self.load_all_tasks()
        self.pushButton.clicked.connect(self.creat_new_task)
        self.pushButton_2.clicked.connect(self.delete_task)
        self.pushButton_3.clicked.connect(self.use_task)
        self.pushButton_4.clicked.connect(self.edit_task)

    def load_all_tasks(self):
        for task in self.tasks.keys():
            item = QtWidgets.QListWidgetItem(task)
            self.listWidget.addItem(item)

    def creat_new_task(self):
        self.ct_dialog = MyCTDialog()
        self.ct_dialog.setVisible(True)

    def delete_task(self):
        pass

    def edit_task(self):
        pass

    def use_task(self):
        task_name = self.listWidget.currentItem().text()
        task_filename = self.tasks[task_name]
        global dict_task
        dict_task = load_json_from_file(tasks_path + task_filename)
        self.setVisible(False)


class MyAMDialog(AM_Dialog, QtWidgets.QDialog):
    def __init__(self, my_parent):
        super(MyAMDialog, self).__init__(parent=None)
        self.setupUi(self)
        self.my_parent = my_parent
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.pushButton.clicked.connect(self.create_or_update_model)
        self.pushButton_2.clicked.connect(self.delete_model)
        self.pushButton_3.clicked.connect(self.select_model)

    def create_or_update_model(self):
        self.my_parent.showNewModel()
        self.setVisible(False)

    def delete_model(self):
        pass

    def select_model(self):
        dict_task['model'] = self.listWidget.currentItem().text()
        self.setVisible(False)


class MyDMDialog(DM_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(MyDMDialog, self).__init__(parent=None)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(icon_path))


class MySTDialog(ST_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(MySTDialog, self).__init__(parent=None)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(icon_path))


class MyPVDialog(PV_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(MyPVDialog, self).__init__(parent=None)
        self.setupUi(self)
        self.label.installEventFilter(self)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.isKeyPress = False

    def eventFilter(self, object, event):
        print('鼠标事件：', event.type())
        # 释放鼠标左键和释放空格时关闭窗口
        # QtCore.QEvent
        if event.type() == 3:
            self.setVisible(False)
            return True
        return False

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.isKeyPress = True

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if self.isVisible() and self.isKeyPress:
            if a0.key() == QtCore.Qt.Key_Space:
                self.setVisible(False)
        self.isKeyPress = False

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        if self.isVisible():
            if a0.angleDelta().y() > 0:
                self.resize(QtCore.QSize(self.width() + 10, self.height() + 10))
            else:
                self.resize(QtCore.QSize(self.width() - 10, self.height() - 10))


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__(parent=None)
        self.predict_result_list = None
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.statusBar().showMessage('正在初始化...', )
        self.showMainWindow()
        self.ct_dialog = MyCTDialog()
        self.at_dialog = MyATDialog()
        self.am_dialog = MyAMDialog(self)
        self.dm_dialog = MyDMDialog()
        self.st_dialog = MySTDialog()
        self.preview_dialog = MyPVDialog()
        self.database = DataBase()
        if self.database.search():
            self.database.cu.execute("select MAX(fault_id) from test")
            self.current_max_id = self.database.cu.fetchall()[0][0]
            self.database.cu.execute("select MAX(fault_id) from test")
            self.current_max_fault_id = self.database.cu.fetchall()[0][0]
        else:
            self.current_max_id = 0
            self.current_max_fault_id = 0

        self.action_10.triggered.connect(self.showMainWindow)
        self.action_17.triggered.connect(self.showHistory)
        self.action_18.triggered.connect(self.showTasks)
        self.action_13.triggered.connect(self.showNewModel)

        self.action.triggered.connect(self.dialog_create_task)
        self.action_3.triggered.connect(self.dialog_all_tasks)
        self.action_4.triggered.connect(self.dialog_all_models)
        self.action_15.triggered.connect(self.dialog_dev_mana)
        self.action_16.triggered.connect(self.dialog_settings)

        self.action_20.triggered.connect(self.blue_theme)
        self.action_21.triggered.connect(self.black_theme)
        self.action_22.triggered.connect(self.white_theme)
        self.action_23.triggered.connect(self.purple_theme)

        # self.pushButton_2.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(lambda: self.model_process())
        self.pushButton_15.clicked.connect(self.stop)

        # 异常图像显示区设置
        self.listWidget.setIconSize(QtCore.QSize(200, 253))
        self.listWidget.itemSelectionChanged.connect(self.show_bigPicture)
        # 异常图像路径列表
        self.fault_pictures = []
        # 当前图像索引值
        self.currentImgIdx = 0

        # 更新模型页面的模型单选框
        # 首先初始化，读取模型
        # self.comboBox_2.addItem()
        # 设置默认模型为当前任务模型或None
        # self.comboBox_2.setCurrentIndex()
        self.update_model_name = self.comboBox_2.currentText()

        # 模型更新的图片路径
        self.update_img_dir = ''
        # 选取图片路径
        self.pushButton_3.clicked.connect(self.open_update_img_dir)
        # 模型更新的标签文件路径
        self.update_label_file = ''
        # 选取标签文件路径
        self.pushButton_4.clicked.connect(self.open_update_label_file)
        # 更新模型的保存路径
        self.update_model_save_name = models_path + 'save.pt'
        # 获取保存路径
        self.pushButton_23.clicked.connect(self.save_new_model_path)

        self.pushButton_5.clicked.connect(self.update_model_start)
        self.pushButton_6.clicked.connect(self.update_model_pause)
        self.pushButton_7.clicked.connect(self.switch_CPU_GPU)
        self.pushButton_8.clicked.connect(self.save_update_model_result)

        # 每隔2秒检测任务栏状态
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_statusbar)
        self.timer.start(2000)
        self.count_fault = 0
        self.count_object = 1
        # start函数用
        self.max_i = 0
        self.i = 0
        self.timer_control = QTimer()
        self.timer_control.timeout.connect(self.setPhoto)

        # 更新模型日志的最后一行信息
        self.update_timer = QTimer()
        self.last_line =None
        self.is_last_line_read = False

        self.statusbar_message = '初始化完成'
        self.show_statusbar_message()

    def showMainWindow(self):
        self.stackedWidget.setCurrentIndex(0)

    def showHistory(self):
        self.stackedWidget.setCurrentIndex(1)

    def showTasks(self):
        self.stackedWidget.setCurrentIndex(2)

    def showNewModel(self):
        self.stackedWidget.setCurrentIndex(3)

    # 显示异常图片大图
    def show_bigPicture(self):
        # self.currentImgIdx = self.listWidget.currentIndex().row()
        self.currentImgIdx = self.listWidget.currentRow()
        print(self.currentImgIdx)
        self.listWidget.clearSelection()
        if self.currentImgIdx in range(len(self.fault_pictures)):
            currentImg = QPixmap(self.fault_pictures[self.currentImgIdx]).scaledToHeight(400)
            self.preview_dialog.label.setPixmap(currentImg)
            self.preview_dialog.label.setScaledContents(True)
            self.preview_dialog.setVisible(True)

    def show_statusbar_message(self):
        self.statusbar.showMessage(self.statusbar_message)

    def dialog_create_task(self):
        self.ct_dialog.setVisible(True)

    def dialog_all_tasks(self):
        self.at_dialog.setVisible(True)

    def dialog_all_models(self):
        self.am_dialog.setVisible(True)

    def dialog_dev_mana(self):
        self.dm_dialog.setVisible(True)

    def dialog_settings(self):
        self.st_dialog.setVisible(True)

    def blue_theme(self):
        self.setStyleSheet("background-color:rgb(26, 29, 37)")
        self.stackedWidget.setStyleSheet("background-color: rgb(30, 37, 48);\n"
                                         "color: rgb(255,255,255);\n"
                                         "border-color: rgb(125, 253, 255);\n"
                                         "border-style: solid;\n"
                                         "border-width: 2px;border-radius:5px;")
        self.page.setStyleSheet("background-color: rgb(30, 37, 48);\n")
        self.widget.setStyleSheet("background-color: rgb(30, 37, 48);border-width:0px")
        self.label_2.setStyleSheet("background-color: rgb(49, 58, 75);broder-width : 0px;border-radius:5px;")
        self.label.setStyleSheet("broder-width: 0px;")
        self.pushButton_2.setStyleSheet("background-color: rgb(65, 97, 136);\n"
                                        "border-radius:5px;")
        self.pushButton_15.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.groupBox_2.setStyleSheet("background-color: rgb(49, 58, 75);\n"
                                      "border-color: rgb(125, 253, 255);\n"
                                      "border-style: solid;\n"
                                      "border-width: 1px;border-radius:5px;")
        self.label_6.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.label_10.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.label_12.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.label_5.setStyleSheet("background-color: rgb(49, 58, 75);")
        self.label_9.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.label_11.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.label_8.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.label_7.setStyleSheet("border-color: rgb(125, 253, 255);")
        self.groupBox.setStyleSheet("background-color: rgb(49, 58, 75);\n"
                                    "border-color: rgb(125, 253, 255);\n"
                                    "border-style: solid;\n"
                                    "border-width: 1px;border-radius:5px;")
        self.listWidget.setStyleSheet("background-color: rgb(30, 37, 48);")
        self.page_2.setStyleSheet("border-color: rgb(129, 242, 255);border-width: 0px;border-radius:5px;")
        self.page_3.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_4.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.statusbar.setStyleSheet("background-color: rgb(220, 220, 220)")
        self.dockWidget_3.setStyleSheet("background-color:rgb(26, 29, 37);\n"
                                        "color: rgb(255, 255, 255);")
        self.dockWidgetContents_3.setStyleSheet("background-color: rgb(30, 37, 48);")
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);border-radius:3px;")
        self.pushButton_18.setStyleSheet("background-color: rgb(155, 183, 220);border-radius:5px;")
        self.textBrowser.setStyleSheet("background-color: rgba(68, 70, 74, 150);color: rgb(255,255,"
                                       "255);border-radius:5px;border-style:solid;border-width:2px;border-color: rgb("
                                       "125, 253, 255);")
        self.pushButton_19.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.textBrowser_2.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);color: rgb(255,255,"
            "255);border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(125, 253, 255);")
        self.pushButton_21.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.textBrowser_3.setStyleSheet("background-color: rgba(68, 70, 74, 150);color: rgb(255,255,"
                                         "255);border-radius:5px;border-style:solid;border-width:2px;border-color: "
                                         "rgb(125, 253, 255);")
        self.pushButton_20.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.dockWidget_4.setStyleSheet("background-color:rgb(26, 29, 37);\n"
                                        "color:rgb(255,255,255);")
        self.dockWidgetContents_4.setStyleSheet("background-color: rgb(30, 37, 48);")
        self.widget_3.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);border-radius:5px;border-color: rgb(125, 253, "
            "255);border-width:2px;border-style:solid;color:rgb(255, 255, 255);")
        self.label_18.setStyleSheet("border-width:1px;")
        self.label_19.setStyleSheet("border-width:1px;")
        # self.line.setStyleSheet("background-color: rgb(105, 137, 187);")
        self.widget_4.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);border-radius:5px;border-color: rgb(125, 253, "
            "255);border-width:2px;border-style:solid;color:rgb(255, 255, 255);")
        self.label_24.setStyleSheet("border-width:1px;")
        self.label_25.setStyleSheet("border-width:1px;")
        # self.line_4.setStyleSheet("background-color: rgb(105, 137, 187);")
        self.widget_5.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);border-radius:5px;border-color: rgb(125, 253, "
            "255);border-width:2px;border-style:solid;color:rgb(255, 255, 255);")
        self.label_26.setStyleSheet("border-width:1px;")
        self.label_27.setStyleSheet("border-width:1px;")
        self.pushButton.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")

    def black_theme(self):
        self.setStyleSheet("background-color:rgb(36, 36, 36)")
        self.stackedWidget.setStyleSheet("background-color: rgb(68, 70, 74);\n"
                                         "color: rgb(255,255,255);\n"
                                         "border-color: rgb(134, 89, 52);\n"
                                         "border-style: solid;\n"
                                         "border-width: 3px;border-radius:5px;")
        self.page.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                "border-width: 0px;border-radius:5px;")
        self.widget.setStyleSheet("background-color:rgb(59, 61, 65);")
        self.label_2.setStyleSheet("background-color: rgb(68, 70, 74);\n"
                                   "broder-width : 0px;border-radius:5px;")
        self.label.setStyleSheet("broder-width: 0px;")
        self.pushButton_2.setStyleSheet("background-color: rgb(68, 70, 74);\n"
                                        "border-radius:5px;")
        self.pushButton_15.setStyleSheet("background-color: rgb(68, 70, 74);border-radius:5px;")
        self.groupBox_2.setStyleSheet("background-color: rgb(59, 61, 65);\n"
                                      "border-color: rgb(134, 89, 52);\n"
                                      "border-style: solid;\n"
                                      "border-width: 1px;border-radius:5px;")
        self.label_6.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_10.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_12.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_5.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_9.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_11.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_8.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.label_7.setStyleSheet("background-color: rgb(68, 70, 74);")
        self.groupBox.setStyleSheet("background-color: rgb(68, 70, 74);\n"
                                    "border-color: rgb(134, 89, 52);\n"
                                    "border-style: solid;\n"
                                    "border-width: 1px;border-radius:5px;")
        self.listWidget.setStyleSheet("background-color:rgb(59, 61, 65);")
        self.page_2.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_3.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_4.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.menubar.setStyleSheet("color: rgb(0, 0, 0);\n"
                                   "background-color: rgb(255, 255, 255);")
        self.menu.setStyleSheet("")
        self.statusbar.setStyleSheet("background-color: rgb(220, 220, 220)")
        self.dockWidget_3.setStyleSheet("background-color: rgb(36, 36, 36);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "")
        self.dockWidgetContents_3.setStyleSheet("background-color: rgb(59, 61, 65)")
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);border-radius:3px;")
        self.pushButton_18.setStyleSheet("background-color: rgb(155, 183, 220);border-radius:5px;")
        self.textBrowser.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);color: rgb(255,255,255);border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(134, 89, 52)\n"
            "")
        self.pushButton_19.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.textBrowser_2.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);color: rgb(255,255,255);border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(134, 89, 52)\n"
            "")
        self.pushButton_21.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.textBrowser_3.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);color: rgb(255,255,255);border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(134, 89, 52)\n"
            "")
        self.pushButton_20.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.dockWidget_4.setStyleSheet("background-color: rgb(36, 36, 36);color: rgb(255,255,255);")
        self.dockWidgetContents_4.setStyleSheet("background-color: rgb(59, 61, 65);")
        self.widget_3.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);border-radius:5px;border-color: rgb(134, 89, 52);border-width:3px;border-style:solid;color:rgb(255, 255, 255);")
        self.label_18.setStyleSheet("border-width:2px;")
        self.label_19.setStyleSheet("border-width:2px;")
        self.widget_4.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);border-radius:5px;border-color: rgb(134, 89, 52);border-width:3px;border-style:solid;color:rgb(255, 255, 255);")
        self.label_24.setStyleSheet("border-width:2px;")
        self.label_25.setStyleSheet("border-width:2px;")
        self.widget_5.setStyleSheet(
            "background-color: rgba(68, 70, 74, 150);border-radius:5px;border-color: rgb(134, 89, 52);border-width:3px;border-style:solid;color:rgb(255, 255, 255);")
        self.label_26.setStyleSheet("border-width:2px;")
        self.label_27.setStyleSheet("border-width:2px;")
        self.pushButton.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")

    def white_theme(self):
        self.setStyleSheet("background-color:rgb(240, 240, 240)")
        self.stackedWidget.setStyleSheet("background-color: rgb(240, 240, 240);\n"
                                         "/*color: rgb(255,255,255);*/\n"
                                         "border-color: rgb(113, 120, 126);\n"
                                         "border-style: solid;\n"
                                         "border-width: 2px;border-radius:5px;")
        self.page.setStyleSheet("background-color: rgb(240, 240, 240);\n"
                                "border-width: 0px;border-radius:5px;")
        self.widget.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_2.setStyleSheet("background-color: rgb(230, 230, 230);\n"
                                   "broder-width : 0px;border-radius:5px;")
        self.label.setStyleSheet("broder-width: 0px;")
        self.pushButton_2.setStyleSheet("background-color: rgb(220, 220, 220);\n"
                                        "border-radius:5px;")
        self.pushButton_15.setStyleSheet("background-color: rgb(220, 220, 220);border-radius:5px;")
        self.groupBox_2.setStyleSheet("background-color: rgb(240, 240, 240);\n"
                                      "border-color: rgb(113, 120, 126);;\n"
                                      "border-style: solid;\n"
                                      "border-width: 1px;border-radius:5px;")
        self.label_6.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_10.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_12.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_5.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_9.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_11.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_8.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.label_7.setStyleSheet("border-color: rgb(113, 120, 126);")
        self.groupBox.setStyleSheet("background-color: rgb(240, 240, 240);\n"
                                    "border-color: rgb(113, 120, 126);\n"
                                    "border-style: solid;\n"
                                    "border-width: 1px;border-radius:5px;")
        self.listWidget.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.page_2.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_3.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_4.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.menubar.setStyleSheet("color: rgb(0, 0, 0);\n"
                                   "background-color: rgb(255, 255, 255);")
        self.menu.setStyleSheet("")
        self.statusbar.setStyleSheet("background-color: rgb(220, 220, 220)")
        self.dockWidget_3.setStyleSheet("background-color:rgba(240, 240, 240,0);\n"
                                        "/*color: rgb(255, 255, 255);*/\n"
                                        "")
        self.dockWidgetContents_3.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);border-radius:3px;")
        self.pushButton_18.setStyleSheet("background-color: rgb(230, 230, 230);border-radius:5px;")
        self.textBrowser.setStyleSheet(
            "background-color: rgba(220, 220, 220, 150);/*color: rgb(255,255,255);*/border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(113, 120, 126);\n"
            "")
        self.pushButton_19.setStyleSheet("background-color: rgb(220, 220, 220);border-radius:5px;")
        self.textBrowser_2.setStyleSheet(
            "background-color: rgba(220, 220, 220, 150);/*color: rgb(255,255,255);*/border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(113, 120, 126);\n"
            "")
        self.pushButton_21.setStyleSheet("background-color: rgb(220, 220, 220);border-radius:5px;")
        self.textBrowser_3.setStyleSheet(
            "background-color: rgba(220, 220, 220, 150);/*color: rgb(255,255,255);*/border-radius:5px;border-style:solid;border-width:2px;border-color: rgb(113, 120, 126);\n"
            "")
        self.pushButton_20.setStyleSheet("background-color: rgb(220, 220, 220);border-radius:5px;")
        self.dockWidget_4.setStyleSheet("background-color:rgba(240, 240, 240, 0);\n"
                                        "/*color:rgb(255,255,255);*/")
        self.dockWidgetContents_4.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.widget_3.setStyleSheet(
            "background-color: rgba(220, 220, 220, 150);border-radius:5px;border-color: rgb(113, 120, 126);border-width:2px;border-style:solid;/*color:rgb(255, 255, 255);*/")
        self.label_18.setStyleSheet("border-width:1px;")
        self.label_19.setStyleSheet("border-width:1px;")
        self.widget_4.setStyleSheet(
            "background-color: rgba(220, 220, 220, 150);border-radius:5px;border-color: rgb(113, 120, 126);border-width:2px;border-style:solid;/*color:rgb(255, 255, 255);*/")
        self.label_24.setStyleSheet("border-width:1px;")
        self.label_25.setStyleSheet("border-width:1px;")
        self.widget_5.setStyleSheet(
            "background-color: rgba(220, 220, 220, 150);border-radius:5px;border-color: rgb(113, 120, 126);border-width:2px;border-style:solid;/*color:rgb(255, 255, 255);*/")
        self.label_26.setStyleSheet("border-width:1px;")
        self.label_27.setStyleSheet("border-width:1px;")
        self.pushButton.setStyleSheet("background-color: rgb(220, 220, 220);border-radius:5px;")

    def purple_theme(self):
        self.setStyleSheet("background-color:rgb(105, 105, 157)")
        self.stackedWidget.setStyleSheet("background-color: rgb(103, 139, 183);\n"
                                         "color: rgb(255,255,255);\n"
                                         "border-color: rgb(129, 242, 255);\n"
                                         "border-style: solid;\n"
                                         "border-width: 3px;border-radius:5px;")
        self.page.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                "border-width: 0px;border-radius:5px;")
        self.widget.setStyleSheet("background-color:rgb(94, 125, 165);")
        self.label_2.setStyleSheet("background-color: rgb(103, 140, 184);\n"
                                   "broder-width : 0px;border-radius:5px;")
        self.label.setStyleSheet("broder-width: 0px;")
        self.pushButton_2.setStyleSheet("background-color: rgb(163, 201, 214);\n"
                                        "border-radius:5px;")
        self.pushButton_15.setStyleSheet("background-color: rgb(163, 201, 214);border-radius:5px;")
        self.groupBox_2.setStyleSheet("background-color: rgb(103, 140, 184);\n"
                                      "border-color: rgb(129, 242, 255);\n"
                                      "border-style: solid;\n"
                                      "border-width: 1px;border-radius:5px;")
        self.label_6.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                   "border-color: rgb(134, 150, 199);")
        self.label_10.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                    "border-color: rgb(134, 150, 199);")
        self.label_12.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                    "border-color: rgb(134, 150, 199);")
        self.label_5.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                   "border-color: rgb(134, 150, 199);")
        self.label_9.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                   "border-color: rgb(134, 150, 199);")
        self.label_11.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                    "border-color: rgb(134, 150, 199);")
        self.label_8.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                   "border-color: rgb(134, 150, 199);")
        self.label_7.setStyleSheet("background-color: rgb(157, 183, 220);color: rgb(0,0,0);border-width: 2px;\n"
                                   "border-color: rgb(134, 150, 199);")
        self.groupBox.setStyleSheet("background-color: rgb(157, 183, 220);\n"
                                    "border-color: rgb(129, 242, 255);\n"
                                    "border-style: solid;\n"
                                    "border-width: 1px;border-radius:5px;")
        self.listWidget.setStyleSheet("background-color: rgb(157, 183, 220);")
        self.page_2.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_3.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.page_4.setStyleSheet("border-color: rgb(129, 242, 255);\n"
                                  "border-width: 0px;border-radius:5px;")
        self.menubar.setStyleSheet("color: rgb(0, 0, 0);\n"
                                   "background-color: rgb(255, 255, 255);")
        self.menu.setStyleSheet("")
        self.statusbar.setStyleSheet("background-color: rgb(220, 220, 220)")
        self.dockWidget_3.setStyleSheet("background-color: rgb(61, 98, 136);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "")
        self.dockWidgetContents_3.setStyleSheet("background-color: rgb(105, 105, 157)")
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);border-radius:3px;")
        self.pushButton_18.setStyleSheet("background-color: rgb(155, 183, 220);border-radius:5px;")
        self.textBrowser.setStyleSheet(
            "background-color: rgba(163, 201, 214, 150);color: rgb(0,0,0);border-radius:5px;")
        self.pushButton_19.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.textBrowser_2.setStyleSheet("background-color: rgb(163, 201, 214, 150);\n"
                                         "border-color: rgb(123, 180, 232);color: rgb(0,0,0);border-radius:5px;")
        self.pushButton_21.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.textBrowser_3.setStyleSheet(
            "background-color: rgba(163, 201, 214, 150);color: rgb(0,0,0);border-radius:5px;")
        self.pushButton_20.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")
        self.dockWidget_4.setStyleSheet("background-color: rgb(61, 98, 136);color: rgb(255,255,255);")
        self.dockWidgetContents_4.setStyleSheet("background-color: rgb(105, 105, 157);\n"
                                                "border-color: rgb(123, 180, 232);")
        self.widget_3.setStyleSheet(
            "background-color: rgba(162, 202, 212, 150);border-radius:5px;border-color:rgb(109, 169, 223);border-width:3px;border-style:solid;color:rgb(0, 0, 0);")
        self.label_18.setStyleSheet("border-width:2px;")
        self.label_19.setStyleSheet("border-width:2px;")
        self.widget_4.setStyleSheet(
            "background-color: rgba(162, 202, 212, 150);border-radius:5px;border-color:rgb(109, 169, 223);border-width:3px;border-style:solid;color:rgb(0, 0, 0);")
        self.label_24.setStyleSheet("border-width:2px;")
        self.label_25.setStyleSheet("border-width:2px;")
        self.widget_5.setStyleSheet(
            "background-color: rgba(162, 202, 212, 150);border-radius:5px;border-color:rgb(109, 169, 223);border-width:3px;border-style:solid;color:rgb(0, 0, 0);")
        self.label_26.setStyleSheet("border-width:2px;")
        self.label_27.setStyleSheet("border-width:2px;")
        self.pushButton.setStyleSheet("background-color: rgb(65, 97, 136);border-radius:5px;")

    # 开始
    def start(self):
        self.camera1 = self.join_path(self.all_photos(camera1_path))
        self.camera2 = self.join_path(self.all_photos(camera2_path))
        self.camera3 = self.join_path(self.all_photos(camera3_path))
        self.camera4 = self.join_path(self.all_photos(camera4_path))
        self.camera5 = self.join_path(self.all_photos(camera5_path))
        self.camera6 = self.join_path(self.all_photos(camera6_path))
        self.camera7 = self.join_path(self.all_photos(camera7_path))
        self.camera8 = self.join_path(self.all_photos(camera8_path))

        self.max_i = len(self.camera8)
        # 每隔一秒换一张图片
        self.timer_control.start(1000)
        self.find_fault()
        # self.new_fault = []

    def join_path(self, tur):
        root, files = tur
        full_path = []
        for file in files:
            file = root + file
            full_path.append(file)
        return full_path

    # 在视频显示区显示图片（视频）
    def setPhoto(self):
        if self.i == self.max_i:
            self.timer_control.stop()
            self.statusbar.showMessage('任务：' + dict_task['task'] + ' 检测完成！')
            self.i = 0
            return
        print('设置图片', self.i)
        self.label_5.setPixmap(QPixmap(self.camera1[self.i]))
        if os.path.getsize(self.camera1_outpath[self.i].split('.')[0] + '.txt') != 0:
            self.show_fault(self.camera1_outpath[self.i].split('.')[0])

        self.label_6.setPixmap(QPixmap(self.camera2[self.i]))
        if os.path.getsize(self.camera2_outpath[self.i].split('.')[0] + '.txt') != 0:
            self.show_fault(self.camera2_outpath[self.i].split('.')[0])

        self.label_7.setPixmap(QPixmap(self.camera3[self.i]))
        if os.path.getsize(self.camera3_outpath[self.i].split('.')[0] + '.txt') != 0:
            self.show_fault(self.camera3_outpath[self.i].split('.')[0])

        self.label_8.setPixmap(QPixmap(self.camera4[self.i]))
        if os.path.getsize(self.camera4_outpath[self.i].split('.')[0] + '.txt') != 0:
            self.show_fault(self.camera4_outpath[self.i].split('.')[0])

        self.label_9.setPixmap(QPixmap(self.camera5[self.i]))
        if os.path.getsize(self.camera5_outpath[self.i].split('.')[0] + '.txt') != 0:
            self.show_fault(self.camera5_outpath[self.i].split('.')[0])

        self.label_10.setPixmap(QPixmap(self.camera6[self.i]))
        if os.path.getsize(self.camera6_outpath[self.i].split('.')[0] + '.txt') != 0:
            self.show_fault(self.camera6_outpath[self.i].split('.')[0])

        self.label_11.setPixmap(QPixmap(self.camera7[self.i]))
        if os.path.getsize(self.camera7_outpath[self.i].split('.')[0] + '.txt') != 0:
            self.show_fault(self.camera7_outpath[self.i].split('.')[0])

        self.label_12.setPixmap(QPixmap(self.camera8[self.i]))
        if os.path.getsize(self.camera8_outpath[self.i].split('.')[0] + '.txt') != 0:
            self.show_fault(self.camera8_outpath[self.i].split('.')[0])

        self.i += 1

    def all_photos(self, path):
        for root, dirs, files in os.walk(path):
            print('读取', path, '成功', root, files)
            return root, files

    # 暂停
    def stop(self):
        self.timer_control.stop()

    # 确定输入图像（视频）和输出图像路径
    def find_fault(self):
        _, self.camera1_out = self.all_photos(camera1_path)
        _, self.camera2_out = self.all_photos(camera2_path)
        _, self.camera3_out = self.all_photos(camera3_path)
        _, self.camera4_out = self.all_photos(camera4_path)
        _, self.camera5_out = self.all_photos(camera5_path)
        _, self.camera6_out = self.all_photos(camera6_path)
        _, self.camera7_out = self.all_photos(camera7_path)
        _, self.camera8_out = self.all_photos(camera8_path)
        self.camera1_outpath = self.join_path((out_path, self.camera1_out))
        self.camera2_outpath = self.join_path((out_path, self.camera2_out))
        self.camera3_outpath = self.join_path((out_path, self.camera3_out))
        self.camera4_outpath = self.join_path((out_path, self.camera4_out))
        self.camera5_outpath = self.join_path((out_path, self.camera5_out))
        self.camera6_outpath = self.join_path((out_path, self.camera6_out))
        self.camera7_outpath = self.join_path((out_path, self.camera7_out))
        self.camera8_outpath = self.join_path((out_path, self.camera8_out))

    # 显示异常图像区
    def show_fault(self, filename):
        self.fault_pictures.append(filename + '.jpg')
        item = QtWidgets.QListWidgetItem(QtGui.QIcon(filename + '.jpg'), '')
        self.listWidget.addItem(item)
        self.count_fault += 1
        if self.count_fault < 4:
            index_fault_tasks = [self.textBrowser, self.textBrowser_2, self.textBrowser_3]
            index_fault_tasks_button = [self.pushButton_19, self.pushButton_21, self.pushButton_20]
            index_fault_warn = [self.label_18, self.label_24, self.label_26]
            index_fault_percent = [self.label_19, self.label_25, self.label_27]

            with open(filename + '.txt', 'r', encoding='utf-8') as f:
                info_list = f.read().split()
            current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
            print(current_time)

            index_fault_tasks[self.count_fault - 1].setHtml(
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">铸件编号：{}</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">异常编号：{}</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">异常类别：{}</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">检测时间：{}</p></body></html>".format(
                    dict_task['name'], self.count_fault, info_list[0], current_time))
            index_fault_tasks_button[self.count_fault - 1].setText('待处理')
            index_fault_warn[self.count_fault - 1].setText(f'异常{self.count_fault}')
            index_fault_percent[self.count_fault - 1].setText(f'{int(float(info_list[1]) * 10000) / 100.0}%')
        self.label_14.setText(f'已检测 产品{self.count_object}件 异常{self.count_fault}处')
        print('有缺陷', filename)

    # # 调用模型, 返回预测结果
    # def use_model(self, infer_img, config_path="configs/yolov3/yolov3_darknet53_270e_voc_defect.yml",
    #               model_weights="output/yolov3_darknet53_270e_voc_defect/best_model.pdparams"):
    #     from tools.inference import predict
    #     return predict(infer_img, config_path, model_weights)
    #     # return [['hole', '0.5608304142951965', '787.90478515625', '257.6526794433594', '53.2989501953125', '60.5352783203125']]

    # 调用模型, 返回预测结果
    def generate_info(self, infer_img, config_path="configs/yolov3/yolov3_darknet53_270e_voc_defect.yml",
                  model_weights="output/yolov3_darknet53_270e_voc_defect/best_model.pdparams"):
        from tools.inference import predict
        return_list = []
        try:
            predict_result = predict(infer_img, config_path, model_weights)
            for result in predict_result:
                items = result.split()
                return_list.append(items)
        except:
            print('模型运行异常')
            self.statusbar_message = '模型运行异常'
            self.show_statusbar_message()
        self.predict_result_list = return_list


    def model_process(self, image="dataset/merge_dataset_fake/valid_image/IMG_20220117_101624_3.jpg"):
        predict_result = self.generate_info(image)
        # thread = Thread(self.generate_info, image, "configs/yolov3/yolov3_darknet53_270e_voc_defect.yml", "output/yolov3_darknet53_270e_voc_defect/best_model.pdparams")
        # thread.start()

        self.label_5.setPixmap(QPixmap(image))
        # thread.join()
        if self.predict_result_list:
            fault_temp = 'output/'+image.split('/')[-1]
            self.fault_pictures.append(fault_temp)
            item = QtWidgets.QListWidgetItem(QtGui.QIcon(fault_temp), '')
            self.listWidget.addItem(item)
            index_fault_tasks = [self.textBrowser, self.textBrowser_2, self.textBrowser_3]
            index_fault_tasks_button = [self.pushButton_19, self.pushButton_21, self.pushButton_20]
            index_fault_warn = [self.label_18, self.label_24, self.label_26]
            index_fault_percent = [self.label_19, self.label_25, self.label_27]
            for result in self.predict_result_list:
                self.count_fault += 1
                current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
                print(current_time)
                if self.count_fault < 4:
                    index_fault_tasks[self.count_fault - 1].setHtml(
                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                        "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">铸件编号：{}</p>\n"
                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">异常编号：{}</p>\n"
                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">异常类别：{}</p>\n"
                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">检测时间：{}</p></body></html>".format(
                            dict_task['name'], self.count_fault, result[0], current_time))
                    index_fault_tasks_button[self.count_fault - 1].setText('待处理')
                    index_fault_warn[self.count_fault - 1].setText(f'异常{self.count_fault}')
                    index_fault_percent[self.count_fault - 1].setText(f'{int(float(result[1]) * 10000) / 100.0}%')
                self.label_14.setText(f'已检测 产品{self.count_object}件 异常{self.count_fault}处')
                print('有缺陷', image)
                # 写入数据库
                info = [self.current_max_id+1, os.path.join(os.getcwd(), image).replace('\\', '/'),
                        os.path.join(os.getcwd(), fault_temp).replace('\\', '/'),
                        self.count_fault+self.current_max_fault_id, result[0], current_time,
                        result[1], result[2], result[3], result[4], result[5]]
                self.current_max_id+=1
                self.database.insert(info)

    # def thread_model_process(self, img = "dataset/merge_dataset_fake/valid_image/IMG_20220117_101624_3.jpg"):
    #     thread = Thread(self.model_process, img)
    #     thread.start()
        # thread.join() # 等待线程结束

    # 状态改变时，更新状态栏
    def update_statusbar(self):
        if dict_task['batch'] == -1:
            self.statusbar_message = '请选择或创建一个任务以运行'
            self.show_statusbar_message()
        else:
            self.statusbar_message = '当前任务：' + dict_task['task'] + '\t模型：'+dict_task['model']
            self.show_statusbar_message()

    # 模型更新图片目录,
    def open_update_img_dir(self):
        # 选择文件，最后一个参数，一个分号是都可以选，两个分号是分割开，各选各的，若有描述，则把后缀名放在()内
        # fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取图片所在文件夹", os.getcwd(),
        #                                                            "*.jpeg;*.jpg;*.png;;All Files(*)")
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选取图片所在文件夹", os.getcwd())
        self.update_img_dir = dir_path
        self.lineEdit.setText(dir_path)

    # 模型更新的标签文件
    def open_update_label_file(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取标签文件", os.getcwd(),
                                                                   "Txt Files(*.txt);;All Files(*)")
        self.update_label_file = fileName
        self.lineEdit_2.setText(fileName)

    # 更新模型的保存路径
    def save_new_model_path(self):
        filename, filetype = QtWidgets.QFileDialog.getSaveFileName(self, "选择模型保存位置", os.getcwd() + '/' + models_path,
                                                                   "pdparams files (*.pdparams);;all files(*.*)")
        self.update_model_save_name = filename
        self.lineEdit_5.setText(filename)

    # 模型更新
    def update_model_start(self):
        self.update_img_dir = self.lineEdit.text()
        self.update_label_file = self.lineEdit_2.text()
        self.update_model_save_name = self.lineEdit_5.text()
        # if self.update_img_dir and self.update_label_file and self.update_model_save_name:
        sys.path.append("..")
        from tasks import retrain_task
        # self.move_files(self.update_img_dir, self.update_label_file)  # TODO
        exp_name = '1'
        # pretrain_weights = self.map_model_name_weights(dict_task['model'])  # TODO
        self.task = retrain_task(exp_name)  #, 'dataset/dataset', pretrain_weights)
        print('开始训练模型')
        self.task.run()
        self.update_timer.timeout.connect(lambda: self.set_end_line(f"output/yolov3_darknet53_270e_{exp_name}/log.txt"))
        self.update_timer.start(2000)
        # else:
        #     print('请输入正确的路径')

    def set_end_line(self, filename):
        self.last_line = read_end_line(filename)
        if self.last_line is not None:
            self.is_last_line_read = True
            line_list = self.last_line.split()
            print(line_list[4], line_list[5], line_list[6], line_list[7])
        if self.is_last_line_read and self.last_line is None:
            self.update_timer.stop()
            print('模型训练结束')

    # 暂停模型更新
    def update_model_pause(self):
        self.task.stop()

    # 切换CPU/GPU(先写成停止tmux会话)
    def switch_CPU_GPU(self):
        self.task.close()
        pass

    # 保存训练结果
    def save_update_model_result(self):
        pass

    # 关闭事件
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ct_dialog.setVisible(False)
        self.at_dialog.setVisible(False)
        self.am_dialog.setVisible(False)
        self.dm_dialog.setVisible(False)
        self.st_dialog.setVisible(False)


def read_end_line(filename):
    with open(filename, 'rb') as f:  # 打开文件
        offset = -500  # 设置偏移量
        while True:
            """
                 file.seek(off, whence=0)：从文件中移动off个操作标记（文件指针），正往结束方向移动，负往开始方向移动。
                 如果设定了whence参数，就以whence设定的起始位为准，0代表从头开始，1代表当前位置，2代表文件最末尾位置。 
            """
            try:
                f.seek(offset, 2)  # seek(offset, 2)表示文件指针：从文件末尾(2)开始向前300个字符
                lines = f.readlines()  # 读取文件指针范围内所有行
                last_line = None
                # if len(lines) >= 4:  # 判断是否最后至少有3行，这样保证了最后两行是完整的
                #     if is_needed_line(lines[-1].decode()):
                #         last_line = lines[-1].decode()
                #     elif is_needed_line(lines[-2].decode()):
                #         last_line = lines[-2].decode()
                #     elif is_needed_line(lines[-3].decode()):
                #         last_line = lines[-3].decode()
                #     print('文件' + filename + '最后一行信息为：' + last_line)
                #     break
                # 如果off为300时得到的readlines只有一行内容，那么不能保证最后一行是完整的
                # 所以off翻倍重新运行，直到readlines不止一行
                if len(lines) >= 2:  # 判断是否最后至少有3行，这样保证了最后两行是完整的
                    if is_needed_line(lines[-1].decode()):
                        last_line = lines[-1].decode()
                    print(last_line)
                    break
                offset *= 2
            except Exception as e:
                last_line = None
                print(e)
                break
        return last_line


def is_needed_line(line: str):
    line_list = line.split()
    if len(line_list) < 20:
        return False
    elif 'engine' in line_list[2]:
        return True
    else:
        return False


def main():
    try:
        app = QApplication(sys.argv)
        myWin = MyWindow()
        myWin.show()
    except:
        print('app.aboutQt()', app.aboutQt())
        print('app.aboutToQuit()', app.aboutToQuit())
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
