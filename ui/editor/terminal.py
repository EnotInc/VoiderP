import subprocess

from PyQt6.QtWidgets import QWidget, QTextEdit, QLineEdit, QVBoxLayout
from PyQt6.QtGui import QShortcut, QKeySequence

class Terminal(QWidget):
    def __init__(self):
        super().__init__()

        self.script_edit = QLineEdit()
        self.text = QTextEdit()
        self.text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.script_edit)
        layout.setContentsMargins(0, 0, 0, 0)

        self.script_edit.setStyleSheet(
            """QLineEdit {
               border-radius: none;
               padding: 5px;
               background-color: #000000;
               color: #21FC0D;
            }"""
        )
        self.text.setStyleSheet("QTextEdit {background-color: #000000;color: white; border:none;}")

        self.setLayout(layout)

        self.quitSc = QShortcut(QKeySequence("Return"), self)
        self.quitSc.activated.connect(self.run_script)

    def run_script(self):
        script = self.script_edit.text()
        try:
            if self.script_edit.text() == "clear" or self.script_edit.text() == "cls":
                self.text.setText("")
            else:
                result = subprocess.run(["powershell", script], capture_output=True, text=True)
                output = result.stdout.encode('cp1251').decode('cp866')
                output = output.replace("\n\r", "\n").replace("\r", "\n")
                self.text.append(output)
            self.script_edit.setText("")
        except Exception as ex:
            print(ex)