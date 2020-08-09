from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton

label_width = 50
value_width = 180

class TaskListEntryWidget(QWidget):
    def __init__(self, task):
        QWidget.__init__(self)

        panel = QHBoxLayout()
        self.setLayout(panel)

        description = task['type'];
        params = task['params']
        for p in params:
            description = description + ", " + p + "=" + params[p]

        lb_description = QLabel(description)
        panel.addWidget(lb_description)

        buttons = QHBoxLayout()
        buttons.setAlignment(Qt.AlignLeft)
        self.bt_up = QPushButton('up')
        self.bt_edit = QPushButton('edit')
        self.bt_delete = QPushButton('delete')
        self.bt_add = QPushButton('add')
        self.bt_enable = QPushButton('enable')
        buttons.addWidget(self.bt_up)
        buttons.addWidget(self.bt_edit)
        buttons.addWidget(self.bt_delete)
        buttons.addWidget(self.bt_add)
        buttons.addWidget(self.bt_enable)
        panel.addLayout(buttons)

        self.setLayout(panel)
