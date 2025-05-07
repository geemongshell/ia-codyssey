import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone 계산기')
        self.setFixedSize(320, 480)
        self.setStyleSheet('background-color: black;')
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
            button.setStyleSheet(self.button_style(color))
            button.clicked.connect(self.on_click)
            grid.addWidget(button, row, col, rowspan, colspan)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def button_style(self, color):
        base = 'border-radius: 35px; font-size: 20px; font-weight: bold;'
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
        self.display.setText('0')
        self.history.setText('')
        self.adjust_font_size('0')

    def negative_positive(self):
        if self.current_input:
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.display.setText(self.current_input)

    def percent(self):
        if self.current_input:
            try:
                value = float(self.current_input) / 100
                self.current_input = str(value)
                self.display.setText(self.current_input)
            except ValueError:
                self.display.setText('Error')

    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ZeroDivisionError
        return x / y

    def on_click(self):
        btn_text = self.sender().text()
        if btn_text == 'AC':
            self.reset()
        elif btn_text == '±':
            self.negative_positive()
        elif btn_text == '%':
            self.percent()
        elif btn_text == '=':
            self.equal()
        elif btn_text in ['+', '−', '×', '÷']:
            self.operator = btn_text
            self.previous_value = self.current_input
            self.current_input = ''
            self.history.setText(f'{self.previous_value} {btn_text}')
        else:
            if btn_text == '.' and '.' in self.current_input:
                return
            self.current_input += btn_text
            self.display.setText(self.current_input)

    def equal(self):
        try:
            x = float(self.previous_value)
            y = float(self.current_input)
            if self.operator == '+':
                result = self.add(x, y)
            elif self.operator == '−':
                result = self.subtract(x, y)
            elif self.operator == '×':
                result = self.multiply(x, y)
            elif self.operator == '÷':
                result = self.divide(x, y)

            # 반올림 후 계산된 값 표시
            formatted_result = self.format_number(str(result))
            self.display.setText(formatted_result)
            self.history.setText('')

            self.current_input = str(result)
            self.previous_value = ''
            self.operator = ''

            # 결과에 맞게 폰트 크기 조정
            self.adjust_font_size(formatted_result)

        except ZeroDivisionError:
            self.display.setText('Error')
            self.reset()

    def format_number(self, number_str):
        try:
            number = float(number_str)
            # 계산된 결과만 소수점 6자리로 반올림하고, 나머지 0은 없애기
            return '{:,.6f}'.format(round(number, 6)).rstrip('0').rstrip('.')
        except ValueError:
            return number_str

    def adjust_font_size(self, result):
        # 결과의 길이에 따라 폰트 크기 조정
        length = len(result)
        base_font_size = 32
        min_font_size = 20
        max_font_size = 40

        font_size = max(min_font_size, base_font_size - length * 2)
        font_size = min(font_size, max_font_size)  # 너무 작은 폰트 크기 방지

        self.display.setStyleSheet(f'font-size: {font_size}px; background-color: black; color: white; border: none; padding: 0 10px;')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec_())
