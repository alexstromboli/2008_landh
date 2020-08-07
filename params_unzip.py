from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QLineEdit

label_width = 50
value_width = 200

class ParamsWidget:
    def __init__(self):

        argumentspanel = QHBoxLayout()
        argumentspanel.setAlignment(Qt.AlignLeft)

        column01 = QVBoxLayout()
        column01.setAlignment(Qt.AlignTop)
        argumentspanel.addLayout(column01)

        column02 = QVBoxLayout()
        column02.setAlignment(Qt.AlignTop)
        argumentspanel.addLayout(column02)

        lb_source = QLabel('file path')
        lb_source.setFixedWidth (label_width)
        ed_source = QLineEdit()
        ed_source.setFixedWidth (value_width)
        st_source = QHBoxLayout()
        st_source.setAlignment(Qt.AlignLeft)
        st_source.addWidget(lb_source)
        st_source.addWidget(ed_source)
        column01.addLayout(st_source)

        lb_target = QLabel('to dir')
        lb_target.setFixedWidth(label_width)
        ed_target = QLineEdit()
        ed_target.setFixedWidth(value_width)
        st_target = QHBoxLayout()
        st_target.setAlignment(Qt.AlignLeft)
        st_target.addWidget(lb_target)
        st_target.addWidget(ed_target)
        column01.addLayout(st_target)

        self.widget = argumentspanel
        self.ed_source = ed_source
        self.ed_target = ed_target
