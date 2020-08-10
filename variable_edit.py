from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit

name_width = 120
value_width = 170

class VariableEditWidget(QWidget):
    def __init__(self, Name = None, Value = None):
        QWidget.__init__(self)

        panel = QHBoxLayout()
        panel.setAlignment(Qt.AlignLeft)
        self.setLayout(panel)

        self.tb_name = QLineEdit(Name)
        self.tb_name.setFixedWidth(name_width)
        panel.addWidget(self.tb_name)

        lb_eq = QLabel('=')
        panel.addWidget(lb_eq)
        lb_eq.setFixedWidth(10)

        self.tb_value = QLineEdit(Value)
        self.tb_value.setFixedWidth(value_width)
        panel.addWidget(self.tb_value)
