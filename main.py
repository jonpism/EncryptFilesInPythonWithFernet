from PyQt6.QtWidgets    import QWidget, QLabel, QApplication, QStackedWidget
from button_style       import DefaultButtonStyle
from qtextedit_style    import DefaultQTextEditStyle
from encryption         import EncryptionScreen
from decryption         import DecryptionScreen
import sys

class EncryptAndDecryptFiles(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Encrypt and Decrypt Files in Python using Fernet')

        self.mainScreen = QStackedWidget(self)
        self.mainScreen.setGeometry(0, 0, 500, 500)
        self.setFixedSize(500, 500)

        # Create screens
        self.main_menu = self.create_main_menu()
        self.encryption_screen = EncryptionScreen(self)
        self.decryption_screen = DecryptionScreen(self)

        # add screens
        self.mainScreen.addWidget(self.main_menu)
        self.mainScreen.addWidget(self.encryption_screen)
        self.mainScreen.addWidget(self.decryption_screen)

        # Show the main menu first
        self.mainScreen.setCurrentWidget(self.main_menu)
        
    def create_main_menu(self):
        """Creates the main menu with buttons to navigate."""
        widget = QWidget()

        title = QLabel("Main Menu", widget)
        title.setGeometry(200, 10, 200, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=widget)
        encrypt_button.setGeometry(140, 80, 200, 50)
        encrypt_button.clicked.connect(lambda: self.mainScreen.setCurrentWidget(self.encryption_screen))

        decrypt_button = DefaultButtonStyle("Decrypt", parent=widget)
        decrypt_button.setGeometry(140, 180, 200, 50)
        decrypt_button.clicked.connect(lambda: self.mainScreen.setCurrentWidget(self.decryption_screen))

        about_tool = DefaultQTextEditStyle(text=None, parent=widget, geometry=(20, 280, 470, 200))
        about_tool.setHtml(
            f"<b>About Fernet File Encryption in Python:</b><br><br>"
            "Fernet is a symmetric encryption method in Python's <i>cryptography</i> library. "
            "It ensures data confidentiality and integrity using AES encryption with HMAC authentication.<br><br>"
            "Fernet uses the same key for both encryption and decryption, meaning the sender and receiver "
            "must share the key securely and keep it private to prevent unauthorized access.")

        return widget

    def create_encryption_screen(self):
        self.mainScreen.setCurrentWidget(self.encryption_screen)

    def create_decryption_screen(self):
        self.mainScreen.setCurrentWidget(self.decryption_screen)

try:
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = EncryptAndDecryptFiles()
        window.show()
        sys.exit(app.exec())
except Exception as e:
    raise ValueError(f'An error occured: {e}')
