#!/usr/bin/python3

import sys

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QSpacerItem

import params_file_copy
import params_unzip
from tasklist_entry_widget import TaskListEntryWidget
import dummy_data

tasks_data = dummy_data.data
task_types = {'file_copy': params_file_copy, 'unzip': params_unzip}

task_entry_widgets_dict = None

# None for non-editing mode
# -1 for new task
# >0 for editing existing task
current_edited_task_id = None
last_selected_type = None
entered_params = None
selected_param_proc = None

arguments_panel_height = 80
arguments_panel_margin = 6
arguments_panel_spacer = None
argumentswidget = None

global argumentspanel
global com_task_type
global bt_add_update_task
global tb_blk_no

def SButton(text):
    button = QPushButton(text)
    button.setFixedWidth (60)
    return button

def put_arguments_widget(widget = None):
    global argumentswidget
    if argumentswidget != None:
        argumentswidget.setParent(None)
        argumentswidget = None

    global arguments_panel_spacer
    global argumentspanel
    if arguments_panel_spacer != None:
        argumentspanel.removeItem(arguments_panel_spacer)
        arguments_panel_spacer = None

    if widget == None:
        arguments_panel_spacer = QSpacerItem(10, arguments_panel_height + arguments_panel_margin)
        argumentspanel.addSpacerItem(arguments_panel_spacer)
    else:
        argumentswidget = QWidget()
        argumentspanel.addWidget(argumentswidget)
        argumentswidget.setLayout(widget)
        argumentswidget.setFixedHeight(arguments_panel_height)

def enable_edit_form(enable):
    if enable:
        bt_add_update_task.setEnabled(True)
        com_task_type.setEnabled(True)
        tb_blk_no.setEnabled(True)
    else:
        bt_add_update_task.setEnabled(False)
        com_task_type.setEnabled(False)
        tb_blk_no.setEnabled(False)
        put_arguments_widget(None)

def get_task_index_by_id(id):
    index = 0
    for t in tasks_data['tasks']:
        if t['id'] == id:
            return index
        index = index + 1
    return -1

def set_task_params(task_type, params = None):
    global selected_param_proc
    selected_param_proc = task_types[task_type].ParamsWidget()

    if params != None:
        selected_param_proc.set_params(params)

    put_arguments_widget(selected_param_proc.widget)

def edit_task(id):
    global current_edited_task_id
    if current_edited_task_id != None:
        return

    enable_edit_form(True)
    task_index = get_task_index_by_id(id)
    task = tasks_data['tasks'][task_index]

    bt_add_update_task.setText('Update')

    global com_task_type
    task_type = task['type']
    params = task['params']
    type_index = com_task_type.findData(task_type)
    com_task_type.setCurrentIndex(type_index)
    set_task_params(task_type, params)

    global last_selected_type
    last_selected_type = task_type
    global entered_params
    entered_params = { task_type: params }

    current_edited_task_id = id

def task_type_selected(type_index):
    global current_edited_task_id
    if current_edited_task_id == None:
        return

    global entered_params
    global last_selected_type
    if selected_param_proc != None:
        data = {}
        selected_param_proc.get_params(data)
        entered_params[last_selected_type] = data

    last_selected_type = com_task_type.itemData(type_index)

    params = None
    if last_selected_type in entered_params:
        params = entered_params[last_selected_type]

    set_task_params(last_selected_type, params)

def enable_task(id, is_enabled):
    task_index = get_task_index_by_id(id)
    tasks_data['tasks'][task_index]['is_enabled'] = is_enabled

def commit_task():
    global current_edited_task_id
    global selected_param_proc
    global last_selected_type

    if current_edited_task_id > 0:
        task_index = get_task_index_by_id(current_edited_task_id)
        task = tasks_data['tasks'][task_index]

        global entered_params
        global last_selected_type
        if selected_param_proc != None:
            params = {}
            selected_param_proc.get_params(params)
            task['type'] = last_selected_type
            task['params'] = params

        global task_entry_widgets_dict
        task_entry_widgets_dict[current_edited_task_id].update(task)

    enable_edit_form(False)

    current_edited_task_id = None
    selected_param_proc = None
    global entered_params
    entered_params = None
    last_selected_type = None

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
    global task_entry_widgets_dict
    task_entry_widgets_dict = {}
    for t in tasks_data['tasks']:
        t['id'] = last_id
        tw = TaskListEntryWidget(t)
        task_entry_widgets_dict[t['id']] = tw
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
