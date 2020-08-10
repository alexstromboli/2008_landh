from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QCheckBox

label_width = 50
value_width = 180

class TaskListEntryWidget(QWidget):
    def __init__(self, task):
        QWidget.__init__(self)

        panel = QHBoxLayout()
        self.setLayout(panel)

        self.lb_description = QLabel()
        panel.addWidget(self.lb_description)
        self.update(task)

        buttons = QHBoxLayout()
        buttons.setAlignment(Qt.AlignLeft)
        self.bt_up = QPushButton('up')
        self.bt_edit = QPushButton('edit')
        self.bt_delete = QPushButton('delete')
        self.bt_add = QPushButton('add')
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
