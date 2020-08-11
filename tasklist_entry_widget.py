from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QCheckBox, QSpacerItem, QSizePolicy

from PyQt5.QtGui import QFont

description_width = 550
label_width = 50
value_width = 180

def SIconButton(text, font, tooltip = None):
    button = QPushButton(text)
    button.setFixedWidth(20)
    button.setStyleSheet("padding: 0px")
    button.setFont(font)
    button.setToolTip(tooltip)
    return button

class TaskListEntryWidget(QWidget):
    def __init__(self, task):
        QWidget.__init__(self)

        panel = QHBoxLayout()
        self.setLayout(panel)
        panel.setContentsMargins(2, 2, 2, 2)

        self.lb_description = QLabel()
        panel.addWidget(self.lb_description)
        self.lb_description.setMaximumWidth(description_width)
        panel.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.MinimumExpanding))
        self.update(task)

        font = QFont()
        font.setBold(True)
        font.setPointSize(14)

        buttons = QHBoxLayout()
        buttons.setAlignment(Qt.AlignLeft)
        self.bt_up = SIconButton('↑', font, 'Move up')
        self.bt_edit = SIconButton('✎', font, 'Edit')
        self.bt_delete = SIconButton('♻', font, 'Delete')
        self.bt_add = SIconButton('+', font, 'Add new')
        self.cb_enable = QCheckBox()
        self.cb_enable.setChecked(task['is_enabled'])
        buttons.addWidget(self.bt_up)
        buttons.addWidget(self.bt_edit)
        buttons.addWidget(self.bt_delete)
        buttons.addWidget(self.bt_add)
        buttons.addWidget(self.cb_enable)
        panel.addLayout(buttons)

        self.setLayout(panel)

    def update(self, task):
        description = task['type'];
        params = task['params']
        for p in params:
            description = description + ", " + p + "=" + params[p]
        self.lb_description.setText(description)
        self.lb_description.setToolTip(description)
