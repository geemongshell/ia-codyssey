import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('계산기')
        self.setFixedSize(320, 480)
        self.create_ui()
        self.expression = ''
        self.current_input = ''
        self.previous_value = ''
        self.operator = ''

    def create_ui(self):
        main_layout = QVBoxLayout()

        self.history = QLabel()
        self.history.setAlignment(Qt.AlignRight)
        self.history.setStyleSheet('font-size: 14px; color: gray; padding: 0 10px;')
        main_layout.addWidget(self.history)

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(70)
        self.display.setStyleSheet('font-size: 32px; background-color: black; color: white; border: none; padding: 0 10px;')
        main_layout.addWidget(self.display)

        button_layout = QGridLayout()

        buttons = [
            ('AC', 0, 0, 'gray'), ('±', 0, 1, 'gray'), ('%', 0, 2, 'gray'), ('÷', 0, 3, 'orange'),
            ('7', 1, 0, 'dark'), ('8', 1, 1, 'dark'), ('9', 1, 2, 'dark'), ('×', 1, 3, 'orange'),
            ('4', 2, 0, 'dark'), ('5', 2, 1, 'dark'), ('6', 2, 2, 'dark'), ('−', 2, 3, 'orange'),
            ('1', 3, 0, 'dark'), ('2', 3, 1, 'dark'), ('3', 3, 2, 'dark'), ('+', 3, 3, 'orange'),
            ('0', 4, 0, 'dark', 1, 2), ('.', 4, 2, 'dark'), ('=', 4, 3, 'orange')
        ]

        for button in buttons:
            text = button[0]
            row = button[1]
            col = button[2]
            color = button[3]
            rowspan = button[4] if len(button) > 4 else 1
            colspan = button[5] if len(button) > 5 else 1

            btn = QPushButton(text)
            btn.setFixedSize(70 * colspan, 70 * rowspan)
            btn.setStyleSheet(self.button_style(color))
            btn.clicked.connect(self.on_button_clicked)
            button_layout.addWidget(btn, row, col, rowspan, colspan)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def button_style(self, color):
        base = 'border-radius: 35px; font-size: 20px;'
        if color == 'gray':
            return f'{base} background-color: #a5a5a5; color: black;'
        elif color == 'orange':
            return f'{base} background-color: #ff9500; color: white;'
        elif color == 'dark':
            return f'{base} background-color: #333333; color: white;'
        return base

    def format_number(self, num_str):
        try:
            if '.' in num_str:
                integer_part, decimal_part = num_str.split('.')
                return '{:,}'.format(int(integer_part)) + '.' + decimal_part
            else:
                return '{:,}'.format(int(num_str))
        except:
            return num_str

    def on_button_clicked(self):
        button = self.sender()
        btn_text = button.text()

        if btn_text == 'AC':
            self.expression = ''
            self.current_input = ''
            self.previous_value = ''
            self.operator = ''
            self.display.setText('')
            self.history.setText('')
        elif btn_text == '=':
            try:
                if self.operator and self.previous_value:
                    exp = self.previous_value + self.operator + self.current_input
                    exp = exp.replace('÷', '/').replace('×', '*').replace('−', '-')
                    result = eval(exp)
                    result_str = str(result)
                    self.display.setText(self.format_number(result_str))
                    self.history.setText('')
                    self.expression = result_str
                    self.current_input = result_str
                    self.previous_value = ''
                    self.operator = ''
            except Exception:
                self.display.setText('Error')
                self.expression = ''
                self.current_input = ''
                self.previous_value = ''
                self.operator = ''
        elif btn_text in ['+', '−', '×', '÷']:
            if self.current_input:
                self.previous_value = self.current_input
                self.operator = btn_text
                self.history.setText(f'{self.format_number(self.current_input)} {btn_text}')
                self.current_input = ''
        else:
            self.current_input += btn_text
            self.display.setText(self.format_number(self.current_input))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
