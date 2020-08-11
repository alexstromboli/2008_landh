#!/usr/bin/python3

import sys

from PyQt5.QtGui import QFont
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QSpacerItem, QScrollArea, QFrame, QSizePolicy

from tasklist_entry_widget import TaskListEntryWidget
from variable_edit import VariableEditWidget
from task_arguments_edit import TaskArgumentsEditWidget
import task_definitions
import dummy_data

tasks_data = dummy_data.data
global task_types

global application
global app_widget

tasklist = None
task_entry_widgets_dict = None

# None for non-editing mode
# -1 for new task
# >0 for editing existing task
current_edited_task_id = None
last_selected_type = None
entered_params = None
task_last_id = 0
task_insert_before_index = -1

arguments_panel_height = 80
arguments_panel_margin = 6
# placeholder used when no arguments widget is in place
arguments_panel_spacer = None
# current arguments form
current_arguments_widget = None

global argumentspanel
# dropbox with task types
global com_task_type
global bt_add_update_task
global tb_blk_no

#
global variablespanel
global variable_widgets

def SButton(text):
    button = QPushButton(text)
    button.setFixedWidth (60)
    return button

def SHeaderLabel(text):
    lb = QLabel(text)
    font = QFont()
    font.setBold(True)
    lb.setFont(font)
    return lb

def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

def put_arguments_layout(new_arguments_widget = None):
    global current_arguments_widget
    if current_arguments_widget != None:
        current_arguments_widget.deleteLater()
        current_arguments_widget = None

    global arguments_panel_spacer
    global argumentspanel
    if arguments_panel_spacer != None:
        argumentspanel.removeItem(arguments_panel_spacer)
        arguments_panel_spacer = None

    if new_arguments_widget == None:
        arguments_panel_spacer = QSpacerItem(10, arguments_panel_height + arguments_panel_margin)
        argumentspanel.addSpacerItem(arguments_panel_spacer)
    else:
        current_arguments_widget = new_arguments_widget
        argumentspanel.addWidget(current_arguments_widget)

        current_height = current_arguments_widget.sizeHint().height()
        if current_height < arguments_panel_height:
            current_arguments_widget.setFixedHeight(arguments_panel_height)

def enable_edit_form(enable):
    if enable:
        bt_add_update_task.setEnabled(True)
        com_task_type.setEnabled(True)
        tb_blk_no.setEnabled(True)
    else:
        bt_add_update_task.setEnabled(False)
        com_task_type.setCurrentIndex(-1)
        com_task_type.setEnabled(False)
        tb_blk_no.setEnabled(False)
        tb_blk_no.setText('')
        put_arguments_layout(None)
        global task_insert_before_index
        task_insert_before_index = -1

def get_task_index_by_id(id):
    index = 0
    for t in tasks_data['tasks']:
        if t['id'] == id:
            return index
        index = index + 1
    return -1

def set_task_params(task_type, params = None):
    if task_type == None:
        return

    new_arguments_widget = TaskArgumentsEditWidget(task_types[task_type], params)
    put_arguments_layout(new_arguments_widget)

def add_task(before_id):
    global current_edited_task_id
    if current_edited_task_id != None:
        return

    global task_insert_before_index
    task_insert_before_index = get_task_index_by_id(before_id)
    current_edited_task_id = -1

    enable_edit_form(True)
    bt_add_update_task.setText('Add')

    global entered_params
    entered_params = {}
    com_task_type.setCurrentIndex(0)

def edit_task(id):
    global current_edited_task_id
    if current_edited_task_id != None:
        return

    enable_edit_form(True)
    task_index = get_task_index_by_id(id)
    task = tasks_data['tasks'][task_index]

    global tb_blk_no
    tb_blk_no.setText(f'{task["blk_no"]}')
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
    if current_arguments_widget != None:
        entered_params[last_selected_type] = current_arguments_widget.read_input()

    last_selected_type = com_task_type.itemData(type_index)

    params = None
    if last_selected_type in entered_params:
        params = entered_params[last_selected_type]

    set_task_params(last_selected_type, params)

def enable_task(id, is_enabled):
    task_index = get_task_index_by_id(id)
    tasks_data['tasks'][task_index]['is_enabled'] = is_enabled

def append_task_to_list(task, insert_before_index = -1):
    global task_last_id
    task_last_id = task_last_id + 1
    task['id'] = task_last_id
    tw = TaskListEntryWidget(task)
    task_entry_widgets_dict[task['id']] = tw
    if insert_before_index < 0:
        tasklist.addWidget(tw)
    else:
        tasklist.insertWidget(insert_before_index, tw)
    tw.bt_add.clicked.connect(lambda s, x=task_last_id: add_task(x))
    tw.bt_up.clicked.connect(lambda s, x=task_last_id: up_task(x))
    tw.bt_edit.clicked.connect(lambda s, x=task_last_id: edit_task(x))
    tw.cb_enable.stateChanged.connect(lambda s, x=task_last_id: enable_task(x, s == 2))
    tw.bt_delete.clicked.connect(lambda s, x=task_last_id: delete_task(x))

def commit_task():
    global current_edited_task_id
    if current_edited_task_id == None:
        return

    global current_arguments_widget
    if current_edited_task_id > 0:
        task_index = get_task_index_by_id(current_edited_task_id)
        task = tasks_data['tasks'][task_index]
    else:
        task = { 'is_enabled': True }
        if task_insert_before_index < 0:
            tasks_data['tasks'].append(task)
        else:
            tasks_data['tasks'].insert(task_insert_before_index, task)

    global entered_params
    global last_selected_type
    params = None
    if current_arguments_widget != None:
        params = current_arguments_widget.read_input(True)

    if params == None:
        return

    task['type'] = last_selected_type
    task['params'] = params
    task['blk_no'] = tb_blk_no.text()

    if current_edited_task_id > 0:
        global task_entry_widgets_dict
        task_entry_widgets_dict[current_edited_task_id].update(task)
    else:
        append_task_to_list(task, task_insert_before_index)

    #
    enable_edit_form(False)

    current_edited_task_id = None
    global entered_params
    entered_params = None
    last_selected_type = None

def delete_task(id):
    global current_edited_task_id
    if current_edited_task_id != None:
        return

    task_index = get_task_index_by_id(id)
    tasks_data['tasks'].pop(task_index)

    task_entry_widgets_dict[id].deleteLater()
    del task_entry_widgets_dict[id]

def up_task(id):
    global current_edited_task_id
    if current_edited_task_id != None:
        return

    task_index = get_task_index_by_id(id)
    if task_index == 0:
        return

    task = tasks_data['tasks'][task_index]
    tasks_data['tasks'].pop(task_index)
    tasks_data['tasks'].insert(task_index - 1, task)

    tw = task_entry_widgets_dict[id]
    tasklist.removeWidget(tw)
    tasklist.insertWidget(task_index - 1, tw)

def arrange_var_editing():
    global variablespanel
    have_empty = False

    global variable_widgets
    if len(variable_widgets) > 0:
        var_widget_last = variable_widgets[-1]
        if var_widget_last.tb_name.text().strip() == '' and var_widget_last.tb_value.text().strip() == '':
            have_empty = True

    if not have_empty:
        var_widget = VariableEditWidget()
        variablespanel.addWidget(var_widget)
        hook_up_var_widget(var_widget)

def hook_up_var_widget(var_widget):
    global variable_widgets
    variable_widgets.append(var_widget)
    var_widget.tb_name.textChanged.connect(arrange_var_editing)
    var_widget.tb_value.textChanged.connect(arrange_var_editing)

def primary_form_init():
    global task_types
    task_types = {}
    for tt in task_definitions.definitions:
        task_types[tt['name']] = tt

    global app_widget
    app_widget = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)
    app_widget.setLayout(layout)

    topbar = QHBoxLayout()
    layout.addLayout(topbar)
    topbar.addWidget(QLabel('<file name>'))
    topbar.addWidget(SButton('Open'))
    topbar.addWidget(SButton('Save'))
    bt_exit = SButton('Exit')
    topbar.addWidget(bt_exit)
    bt_exit.clicked.connect(lambda: app_widget.close())

    editpanel = QHBoxLayout()
    layout.addLayout(editpanel)

    blknopanel = QVBoxLayout()
    blknopanel.setAlignment(Qt.AlignTop)
    editpanel.addLayout(blknopanel)
    blknopanel.addWidget(SHeaderLabel('Blk No'))
    global tb_blk_no
    tb_blk_no = QLineEdit()
    tb_blk_no.setFixedWidth (50)
    blknopanel.addWidget(tb_blk_no)

    tasknamepanel = QVBoxLayout()
    tasknamepanel.setAlignment(Qt.AlignTop)
    editpanel.addLayout(tasknamepanel)
    tasknamepanel.addWidget(SHeaderLabel('Task Name'))

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
    editpanel.addSpacerItem(QSpacerItem(30, 1, QSizePolicy.Fixed))
    editpanel.addLayout(argumentspanel)
    argumentspanel.addWidget(SHeaderLabel('Arguments'))

    global bt_add_update_task
    bt_add_update_task = SButton('Add')
    layout.addWidget(bt_add_update_task)
    bt_add_update_task.clicked.connect(commit_task)
    enable_edit_form(False)

    #
    layout.addWidget(SHeaderLabel('Task List'))
    task_scroll = QScrollArea()
    task_scroll.setFixedHeight(200)
    task_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    task_scroll.setWidgetResizable(True)

    global tasklist
    tasklist = QVBoxLayout()
    tasklist.setAlignment(Qt.AlignTop)

    task_frame = QFrame(task_scroll)
    task_frame.setLayout(tasklist)

    layout.addWidget(task_scroll)
    task_scroll.setWidget(task_frame)

    layout.addWidget(SHeaderLabel('Runtime Variables for Simulation'))
    global variablespanel
    variablespanel = QVBoxLayout()
    variablespanel.setAlignment(Qt.AlignTop)
    layout.addLayout(variablespanel)

    app_widget.resize(770, 500)
    app_widget.move(300, 300)
    app_widget.setWindowTitle('TaskList Management')

def load_data(tasks_data):
    global task_last_id
    task_last_id = 0

    global tasklist
    tasklist.addWidget(QWidget())
    tasklist.addLayout(QHBoxLayout())
    clear_layout(tasklist)

    global task_entry_widgets_dict
    task_entry_widgets_dict = {}
    for t in tasks_data['tasks']:
        append_task_to_list(t)

    enable_edit_form(False)

    #
    global variablespanel
    clear_layout(variablespanel)

    global variable_widgets
    variable_widgets = []
    vars = tasks_data['variables']
    for var_name in vars:
        var_widget = VariableEditWidget(var_name, vars[var_name])
        variablespanel.addWidget(var_widget)
        hook_up_var_widget(var_widget)
    arrange_var_editing()

def main():
    global application
    application = QApplication(sys.argv)

    primary_form_init()

    load_data(tasks_data)

    #
    global app_widget
    app_widget.show()
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
