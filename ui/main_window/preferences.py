from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QCheckBox, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QIcon

class Preferences(QDialog):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("sources/voider_icon.ico"))

        layout = QVBoxLayout()
        self.setLayout(layout)

        show_numbers = QHBoxLayout()
        self.line_numbers = QLabel("Show line nubmer") 
        self.line_checkbox = QCheckBox()
        self.line_checkbox.setChecked(self.config.row_numbers)
        show_numbers.addWidget(self.line_numbers)
        show_numbers.addWidget(self.line_checkbox)

        carret_type = QHBoxLayout() 
        self.what_carret = QLabel("Choose carret type: ")
        self.combobox = QComboBox()
        self.combobox.addItem("Thin")
        self.combobox.addItem("Box")
        self.combobox.setCurrentIndex(self.config.cursor_style - 1)
        carret_type.addWidget(self.what_carret)
        carret_type.addWidget(self.combobox)
        
        layout.addLayout(show_numbers)
        layout.addLayout(carret_type)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close|
                                           QDialogButtonBox.StandardButton.Apply)
        
        apply_button = self.button_box.button(QDialogButtonBox.StandardButton.Apply)
        self.button_box.addButton(apply_button, QDialogButtonBox.ButtonRole.AcceptRole)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
    
        self._center_of_monitor()
    
    def accept(self):
        self.save_config()
        super().accept()

    def reject(self):
        super().reject()
    
    def save_config(self):
        self.config.row_numbers = self.line_checkbox.isChecked()
        self.config.cursor_style = self.combobox.currentIndex() + 1

    def _center_of_monitor(self):
        screen_geometry = self.screen().availableGeometry()
        window_geometry = self.frameGeometry()

        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)

        self.move(window_geometry.topLeft())


