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
global argumentspanel

def SButton(text):
    button = QPushButton(text)
    button.setFixedWidth (60)
    return button

def get_task_index_by_id(id):
    index = 0
    for t in tasks_data['tasks']:
        if t['id'] == id:
            return index
        index = index + 1
    return -1

def edit_task(id):
    task_index = get_task_index_by_id(id)
    task = tasks_data['tasks'][task_index]
    selected_param_proc = task_types[task['type']].ParamsWidget()
    selected_param_proc.set_params(task['params'])

    global argumentswidget
    if argumentswidget != None:
        argumentswidget.setParent(None)
        argumentswidget = None

    argumentswidget = QWidget()
    argumentspanel.addWidget(argumentswidget)
    argumentswidget.setLayout(selected_param_proc.widget)

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
    topbar.addWidget(SButton('Exit'))

    editpanel = QHBoxLayout()
    layout.addLayout(editpanel)

    blknopanel = QVBoxLayout()
    blknopanel.setAlignment(Qt.AlignTop)
    editpanel.addLayout(blknopanel)
    blknopanel.addWidget(QLabel('Blk No'))
    blk_line_edit = QLineEdit('---')
    blk_line_edit.setFixedWidth (50)
    blknopanel.addWidget(blk_line_edit)

    tasknamepanel = QVBoxLayout()
    tasknamepanel.setAlignment(Qt.AlignTop)
    editpanel.addLayout(tasknamepanel)
    tasknamepanel.addWidget(QLabel('Task Name'))
    tasknamepanel.addWidget(QComboBox())

    global argumentspanel
    argumentspanel = QVBoxLayout()
    argumentspanel.setAlignment(Qt.AlignTop)
    editpanel.addLayout(argumentspanel)
    argumentspanel.addWidget(QLabel('Arguments'))

    layout.addWidget(SButton('Add'))

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
        last_id = last_id + 1

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
