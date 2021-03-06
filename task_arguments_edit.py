from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QSpacerItem, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QSizePolicy

name_width = 80
value_width = 130
gap_width = 40
items_per_row = 2

class Entry:
    def __init__(self, argument):
        self.name = argument[0]
        self.default_value = argument[1]
        self.is_mandatory = argument[2] == 'M'
        self.tooltip = argument[3]
        self.textbox = QLineEdit(self.default_value)
        self.textbox.setToolTip(self.tooltip)
        self.normal_style = self.textbox.styleSheet()
        self.error_style = "border: 1px solid red;"

    def input(self):
        return self.textbox.text().strip()

    def validate(self):
        if self.is_mandatory and self.input() == '':
            self.textbox.setStyleSheet(self.error_style)
            return False

        self.textbox.setStyleSheet(self.normal_style)
        return True

class TaskArgumentsEditWidget(QWidget):
    def __init__(self, arguments_definition, values = None):
        QWidget.__init__(self)

        panel = QVBoxLayout()
        panel.setAlignment(Qt.AlignTop)
        self.setLayout(panel)

        self.map = {}

        added = 0
        row = None
        args = arguments_definition['arguments']
        for arg in args:
            if added % items_per_row == 0:
                row = QHBoxLayout()
                row.setAlignment(Qt.AlignLeft)
                panel.addLayout(row)
            else:
                row.addSpacerItem(QSpacerItem(gap_width, 1, QSizePolicy.Fixed))

            entry = Entry(arg)
            self.map[entry.name] = entry

            lb_name = QLabel(f"{entry.name}{' *' if entry.is_mandatory else ''}:")
            lb_name.setFixedWidth(name_width)
            lb_name.setToolTip(entry.tooltip)
            row.addWidget(lb_name)

            entry.textbox.setFixedWidth(value_width)
            row.addWidget(entry.textbox)

            if values != None:
                entry.textbox.setText(values[entry.name])

            added = added + 1

    def read_input(self, validate = False):
        result = {}
        valid = True
        for name in self.map:
            tb = self.map[name]
            input = tb.input()
            result[name] = input
            if validate and not tb.validate():
                valid = False

        if not valid:
            return None

        return result
