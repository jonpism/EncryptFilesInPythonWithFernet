from PyQt6.QtWidgets        import QWidget, QFileDialog, QMessageBox, QLabel
from PyQt6.QtCore           import QProcess
from button_style           import DefaultButtonStyle
from qtextedit_style        import DefaultQTextEditStyle
from cryptography.fernet    import Fernet
from pathlib                import Path
import sys, os

class EncryptionScreen(QWidget):
    def __init__(self, parent_window):
        super().__init__()

        self.parent_window = parent_window  # Reference to the main window
        self.setGeometry(0, 0, 500, 500)
        self.setFixedSize(500, 500)

        self.downloads_path = str(Path.home() / "Downloads")

        title = QLabel("Encrypt a File", self)
        title.setGeometry(200, 10, 200, 50)

        # Back Button implementation
        back_button = DefaultButtonStyle("Back", parent=self)
        back_button.setGeometry(20, 20, 70, 30)
        back_button.clicked.connect(lambda: self.parent_window.mainScreen.setCurrentWidget(self.parent_window.main_menu))

        select_file_button = DefaultButtonStyle(
            'Select File for Encryption',
            parent=self,
            command=self.select_file)
        select_file_button.setGeometry(50, 100, 230, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.encrypt_file)
        encrypt_button.setGeometry(350, 100, 100, 50)

        self.selected_file_label = DefaultQTextEditStyle(text=None, parent=self, geometry=(50, 180, 400, 100))
        self.set_selected_file_label(selected_file=None)

        self.encrypted_path_label = DefaultQTextEditStyle(text=None, parent=self, geometry=(50, 300, 400, 160))
        self.set_encrypted_path_label(encrypted_file=None, encryption_key=None)
    
    def set_selected_file_label(self, selected_file):
        self.selected_file_label.setHtml(f"<b>Current selected file:</b><br><br>{selected_file}")

    def set_encrypted_path_label(self, encrypted_file, encryption_key):
        self.encrypted_path_label.setHtml(
            f"<b>Encrypted file location: </b><br>{encrypted_file} <br><br><br><b>Encryption key location:</b><br>{encryption_key}")
    
    def select_file(self):
        """Selects the specified file."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select a file')
        try:
            if file_path:
                self.selected_file = file_path
                QMessageBox.information(self, 'File Selected Successfully', f'Selected file: {file_path}')
                self.set_selected_file_label(selected_file=file_path)
        except Exception as e:
            QMessageBox.critical(self, f'An error occured: {e}', 'Unsuccessful file selection.')
            
    def encrypt_file(self):
        """Encrypts the selected file."""
        if hasattr(self, 'selected_file'):
            try:
                file_name = os.path.basename(self.selected_file)
                encrypted_file_path = os.path.join(self.downloads_path, f'{file_name}.encrypted')

                # Key generation
                self.key = Fernet.generate_key()
                self.cipher = Fernet(self.key)
                key_file_path = os.path.join(self.downloads_path, 'encryption_key.key')
                with open(key_file_path, 'wb') as key_file:
                    key_file.write(self.key)

                with open(self.selected_file, 'rb') as file:
                    file_data = file.read()
                encrypted_data = self.cipher.encrypt(file_data)

                # write the encrypted data to the specified path
                with open(encrypted_file_path, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_data)

                # custom message box with a button to open the Downloads folder
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle('Encryption Successful')
                msg_box.setText(
                    f'Encrypted file saved at:\n {encrypted_file_path}\n\n Encryption key saved at:\n {key_file_path}')
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                msg_box.exec()
                self.set_encrypted_path_label(encrypted_file=encrypted_file_path, encryption_key=key_file_path)

                if msg_box.clickedButton() == open_folder_btn:
                    self.open_downloads_folder()
            except Exception as e:
                QMessageBox.critical(self, 'Encryption failed', f'An error occured during encryption: {str(e)}')
        else:
            QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')

    def open_downloads_folder(self):
        # Open the Downloads folder using the appropriate command for the OS
        if sys.platform == 'win32':
            os.startfile(self.downloads_path)
        elif sys.platform == 'darwin':  # macOS
            QProcess.execute('open', [self.downloads_path])
        else:  # Linux and other Unix-like systems
            QProcess.execute('xdg-open', [self.downloads_path])
