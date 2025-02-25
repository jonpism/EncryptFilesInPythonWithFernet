from PyQt6.QtWidgets    import QPushButton, QSizePolicy

class DefaultButtonStyle(QPushButton):

    def __init__(self, text, parent=None, object_name=None, command=None):
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(object_name if object_name else text)

        self.setStyleSheet(self.get_style())
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        if command:
            self.clicked.connect(command)

    def get_style(self):
        return """
        QPushButton {
            border-radius: 15px;
            border: 2px solid #5D6D7E;
            padding: 10px;
            min-width: 16px;
            min-height: 16px;
        }
        QPushButton:hover {
            background-color: grey;
        }
        QPushButton:pressed {
            background-color: #839192;
        }"""
