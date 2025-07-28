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

        auto_save = QHBoxLayout()
        self.should_save = QLabel("Save file on close") 
        self.save = QCheckBox()
        self.save.setChecked(self.config.auto_save)
        auto_save.addWidget(self.should_save)
        auto_save.addWidget(self.save)

        wrap_mode = QHBoxLayout() 
        self.what_mode = QLabel("Choose carret type: ")
        self.cb_mode = QComboBox()
        self.cb_mode.addItem("No Wrap")
        self.cb_mode.addItem("Wrap")
        self.cb_mode.setCurrentIndex(self.config.wrap_mode)
        wrap_mode.addWidget(self.what_mode)
        wrap_mode.addWidget(self.cb_mode)

        carret_type = QHBoxLayout() 
        self.what_carret = QLabel("Choose carret type: ")
        self.cb_carret = QComboBox()
        self.cb_carret.addItem("Thin")
        self.cb_carret.addItem("Box")
        self.cb_carret.setCurrentIndex(self.config.cursor_style - 1)
        carret_type.addWidget(self.what_carret)
        carret_type.addWidget(self.cb_carret)
        
        layout.addLayout(auto_save)
        layout.addLayout(show_numbers)
        layout.addLayout(wrap_mode)
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
        self.config.auto_save = self.save.isChecked()
        self.config.row_numbers = self.line_checkbox.isChecked()
        self.config.wrap_mode = self.cb_mode.currentIndex()
        self.config.cursor_style = self.cb_carret.currentIndex() + 1

    def _center_of_monitor(self):
        screen_geometry = self.screen().availableGeometry()
        window_geometry = self.frameGeometry()

        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)

        self.move(window_geometry.topLeft())


