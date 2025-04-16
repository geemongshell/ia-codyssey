import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone 스타일 계산기')
        self.setFixedSize(320, 480)
        self.init_ui()
        self.reset()

    def init_ui(self):
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

        grid = QGridLayout()
        buttons = [
            ('AC', 0, 0, 'gray'), ('±', 0, 1, 'gray'), ('%', 0, 2, 'gray'), ('÷', 0, 3, 'orange'),
            ('7', 1, 0, 'dark'), ('8', 1, 1, 'dark'), ('9', 1, 2, 'dark'), ('×', 1, 3, 'orange'),
            ('4', 2, 0, 'dark'), ('5', 2, 1, 'dark'), ('6', 2, 2, 'dark'), ('−', 2, 3, 'orange'),
            ('1', 3, 0, 'dark'), ('2', 3, 1, 'dark'), ('3', 3, 2, 'dark'), ('+', 3, 3, 'orange'),
            ('0', 4, 0, 'dark', 1, 2), ('.', 4, 2, 'dark'), ('=', 4, 3, 'orange')
        ]

        for btn in buttons:
            text, row, col, color = btn[:4]
            rowspan = btn[4] if len(btn) > 4 else 1
            colspan = btn[5] if len(btn) > 5 else 1

            button = QPushButton(text)
            button.setFixedSize(70 * colspan, 70 * rowspan)
            button.setStyleSheet(self.btn_style(color))
            button.clicked.connect(self.on_click)
            grid.addWidget(button, row, col, rowspan, colspan)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def btn_style(self, color):
        base = 'border-radius: 35px; font-size: 20px;'
        if color == 'gray':
            return f'{base} background-color: #a5a5a5; color: black;'
        elif color == 'orange':
            return f'{base} background-color: #ff9500; color: white;'
        elif color == 'dark':
            return f'{base} background-color: #333333; color: white;'
        return base

    def reset(self):
        self.current_input = ''
        self.previous_value = ''
        self.operator = ''
        self.display.setText('')
        self.history.setText('')

    def format_number(self, text):
        try:
            if '.' in text:
                i, d = text.split('.')
                return '{:,}'.format(int(i)) + '.' + d
            return '{:,}'.format(int(text))
        except:
            return text

    def on_click(self):
        btn_text = self.sender().text()

        if btn_text == 'AC':
            self.reset()
        elif btn_text == '=':
            if self.operator and self.previous_value and self.current_input:
                try:
                    expression = self.previous_value + self.operator + self.current_input
                    result = str(eval(expression.replace('÷', '/').replace('×', '*').replace('−', '-')))
                    self.display.setText(self.format_number(result))
                    self.history.setText('')
                    self.current_input = result
                    self.previous_value = ''
                    self.operator = ''
                except:
                    self.display.setText('Error')
                    self.reset()
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
    win = Calculator()
    win.show()
    sys.exit(app.exec_())
