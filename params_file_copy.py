from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QLineEdit

label_width = 50
value_width = 180

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

        lb_source = QLabel('source')
        lb_source.setFixedWidth (label_width)
        ed_source = QLineEdit()
        ed_source.setFixedWidth (value_width)
        st_source = QHBoxLayout()
        st_source.setAlignment(Qt.AlignLeft)
        st_source.addWidget(lb_source)
        st_source.addWidget(ed_source)
        column01.addLayout(st_source)

        lb_target = QLabel('target')
        lb_target.setFixedWidth(label_width)
        ed_target = QLineEdit()
        ed_target.setFixedWidth(value_width)
        st_target = QHBoxLayout()
        st_target.setAlignment(Qt.AlignLeft)
        st_target.addWidget(lb_target)
        st_target.addWidget(ed_target)
        column01.addLayout(st_target)

        lb_buffer_size = QLabel('buffer')
        lb_buffer_size.setFixedWidth(label_width)
        ed_buffer_size = QLineEdit()
        ed_buffer_size.setFixedWidth(value_width)
        st_buffer_size = QHBoxLayout()
        st_buffer_size.setAlignment(Qt.AlignLeft)
        st_buffer_size.addWidget(lb_buffer_size)
        st_buffer_size.addWidget(ed_buffer_size)
        column02.addLayout(st_buffer_size)

        self.widget = argumentspanel
        self.ed_source = ed_source
        self.ed_target = ed_target
        self.ed_buffer_size = ed_buffer_size

    def set_params(self, data):
        self.ed_source.setText(data['source'])
        self.ed_target.setText(data['target'])
        self.ed_buffer_size.setText(data['buffer_size'])

    def get_params(self, data):
        data['source'] = self.ed_source.text()
        data['target'] = self.ed_target.text()
        data['buffer_size'] = self.ed_buffer_size.text()
