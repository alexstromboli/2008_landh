#!/usr/bin/python3

import sys

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox

import params_file_copy
import params_unzip
from tasklist_entry_widget import TaskListEntryWidget
import dummy_data

tasks_data = dummy_data.data

def SButton(text):
    button = QPushButton(text)
    button.setFixedWidth (60)
    return button

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

    argumentspanel = QVBoxLayout()
    argumentspanel.setAlignment(Qt.AlignTop)
    editpanel.addLayout(argumentspanel)
    argumentspanel.addWidget(QLabel('Arguments'))
    argumentswidget = QWidget()
    argumentspanel.addWidget(argumentswidget)

    layout.addWidget(SButton('Add'))

    layout.addWidget(QLabel('Task List'))
    tasklist = QVBoxLayout()
    tasklist.setAlignment(Qt.AlignTop)
    layout.addLayout(tasklist)
    for t in tasks_data['tasks']:
        tasklist.addWidget(TaskListEntryWidget(t))

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

    #
    task_types = {'file_copy': params_file_copy, 'unzip': params_unzip}

    #
    task_index = 0
    task = tasks_data['tasks'][task_index]
    selected_param_proc = task_types[task['type']].ParamsWidget()
    selected_param_proc.set_params(task['params'])
    argumentswidget.setLayout(selected_param_proc.widget)

    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
