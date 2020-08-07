from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit

label_width = 50
value_width = 180

class TaskListEntryWidget(QWidget):
    def __init__(self, task):
        QWidget.__init__(self)

        panel = QHBoxLayout()
        self.setLayout(panel)

        description = QLabel(f'{task["type"]}')
        panel.addWidget(description)
