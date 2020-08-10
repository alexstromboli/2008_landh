#!/usr/bin/python3

import sys

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox

import params_file_copy
import params_unzip
from tasklist_entry_widget import TaskListEntryWidget
import dummy_data

tasks_data = dummy_data.data
task_types = {'file_copy': params_file_copy, 'unzip': params_unzip}
argumentswidget = None
current_edited_task_id = None
global argumentspanel
global com_task_type
global bt_add_update_task
global tb_blk_no

def SButton(text):
    button = QPushButton(text)
    button.setFixedWidth (60)
    return button

def enable_edit_form(enable):
    if enable:
        bt_add_update_task.setEnabled(True)
        com_task_type.setEnabled(True)
        tb_blk_no.setEnabled(True)
    else:
        bt_add_update_task.setEnabled(False)
        com_task_type.setEnabled(False)
        tb_blk_no.setEnabled(False)

        global argumentswidget
        if argumentswidget != None:
            argumentswidget.setParent(None)
            argumentswidget = None

def get_task_index_by_id(id):
    index = 0
    for t in tasks_data['tasks']:
        if t['id'] == id:
            return index
        index = index + 1
    return -1

def edit_task(id):
    enable_edit_form(True)
    task_index = get_task_index_by_id(id)
    task = tasks_data['tasks'][task_index]

    bt_add_update_task.setText('Update')

    global com_task_type
    task_type = task['type']
    type_index = com_task_type.findData(task_type)
    com_task_type.setCurrentIndex(type_index)

    selected_param_proc = task_types[task_type].ParamsWidget()
    selected_param_proc.set_params(task['params'])

    global argumentswidget
    if argumentswidget != None:
        argumentswidget.setParent(None)
        argumentswidget = None

    argumentswidget = QWidget()
    argumentspanel.addWidget(argumentswidget)
    argumentswidget.setLayout(selected_param_proc.widget)

    global current_edited_task_id
    current_edited_task_id = id

def task_type_selected(type_index):
    if current_edited_task_id == None:
        return
    type_index = type_index

def enable_task(id, is_enabled):
    task_index = get_task_index_by_id(id)
    tasks_data['tasks'][task_index]['is_enabled'] = is_enabled

def commit_task():
    enable_edit_form(False)

def main():

    app = QApplication(sys.argv)

    w = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)
    w.setLayout(layout)

    topbar = QHBoxLayout()
    layout.addLayout(topbar)
    topbar.addWidget(QLabel('<file name>'))
    topbar.addWidget(SButton('Open'))
    topbar.addWidget(SButton('Save'))
    bt_exit = SButton('Exit')
    topbar.addWidget(bt_exit)
    bt_exit.clicked.connect(lambda: w.close())

    editpanel = QHBoxLayout()
    layout.addLayout(editpanel)

    blknopanel = QVBoxLayout()
    blknopanel.setAlignment(Qt.AlignTop)
    editpanel.addLayout(blknopanel)
    blknopanel.addWidget(QLabel('Blk No'))
    global tb_blk_no
    tb_blk_no = QLineEdit('---')
    tb_blk_no.setFixedWidth (50)
    blknopanel.addWidget(tb_blk_no)

    tasknamepanel = QVBoxLayout()
    tasknamepanel.setAlignment(Qt.AlignTop)
    editpanel.addLayout(tasknamepanel)
    tasknamepanel.addWidget(QLabel('Task Name'))

    global com_task_type
    com_task_type = QComboBox()
    com_task_type.setFixedWidth (150)
    tasknamepanel.addWidget(com_task_type)
    com_task_type.currentIndexChanged.connect(lambda ind: task_type_selected(ind))
    for tt in task_types:
        com_task_type.addItem(tt, tt)

    global argumentspanel
    argumentspanel = QVBoxLayout()
    argumentspanel.setAlignment(Qt.AlignTop)
    editpanel.addLayout(argumentspanel)
    argumentspanel.addWidget(QLabel('Arguments'))

    global bt_add_update_task
    bt_add_update_task = SButton('Add')
    layout.addWidget(bt_add_update_task)
    bt_add_update_task.clicked.connect(commit_task)
    enable_edit_form(False)

    layout.addWidget(QLabel('Task List'))
    tasklist = QVBoxLayout()
    tasklist.setAlignment(Qt.AlignTop)
    layout.addLayout(tasklist)
    last_id = 1
    for t in tasks_data['tasks']:
        t['id'] = last_id
        tw = TaskListEntryWidget(t)
        tasklist.addWidget(tw)
        tw.bt_edit.clicked.connect(lambda s, x = last_id: edit_task(x))
        tw.cb_enable.stateChanged.connect(lambda s, x = last_id: enable_task(x, s == 2))
        last_id = last_id + 1

    enable_edit_form(False)

    layout.addWidget(QLabel('Runtime Variables for Simulation'))
    variablespanel = QVBoxLayout()
    variablespanel.setAlignment(Qt.AlignTop)
    layout.addLayout(variablespanel)

    var_01_panel = QHBoxLayout()
    variablespanel.addLayout(var_01_panel)
    var_01_panel.addWidget(QLabel('var 1'))
    var_01_panel.addWidget(QLineEdit('---'))

    var_02_panel = QHBoxLayout()
    variablespanel.addLayout(var_02_panel)
    var_02_panel.addWidget(QLabel('var 2'))
    var_02_panel.addWidget(QLineEdit('---'))

    var_03_panel = QHBoxLayout()
    variablespanel.addLayout(var_03_panel)
    var_03_panel.addWidget(QLabel('var 3'))
    var_03_panel.addWidget(QLineEdit('---'))

    var_04_panel = QHBoxLayout()
    variablespanel.addLayout(var_04_panel)
    var_04_panel.addWidget(QLabel('var 4'))
    var_04_panel.addWidget(QLineEdit('---'))

    w.resize(700, 500)
    w.move(300, 300)
    w.setWindowTitle('Task Management')

    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
