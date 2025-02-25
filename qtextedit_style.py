from PyQt6.QtWidgets    import QTextEdit
from PyQt6              import QtCore

class DefaultQTextEditStyle(QTextEdit):

    def __init__(self, text, parent=None, object_name=None, geometry=None):
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(object_name if object_name else text)

        self.setReadOnly(True)
        self.setGeometry(QtCore.QRect(*geometry))
        self.setStyleSheet(self.get_qtextedit_style())

    def get_qtextedit_style(self):
        return """
        QTextEdit {
            border: 2px solid #5D6D7E;
            border-radius: 15px;
            padding: 10px;}"""
