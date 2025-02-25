from PyQt6.QtWidgets        import QWidget, QFileDialog, QMessageBox, QLabel
from PyQt6.QtCore           import QProcess
from button_style           import DefaultButtonStyle
from qtextedit_style        import DefaultQTextEditStyle
from cryptography.fernet    import Fernet
from pathlib                import Path
import sys, os

class DecryptionScreen(QWidget):
    def __init__(self, parent_window):
        super().__init__()

        self.parent_window = parent_window  # reference to the main window
        self.setGeometry(0, 0, 500, 500)
        self.setFixedSize(500, 500)

        self.downloads_path = str(Path.home() / "Downloads")

        title = QLabel("Decrypt a File", self)
        title.setGeometry(200, 10, 200, 50)

        # Back Button
        back_button = DefaultButtonStyle("Back", parent=self)
        back_button.setGeometry(20, 20, 70, 30)
        back_button.clicked.connect(lambda: self.parent_window.mainScreen.setCurrentWidget(self.parent_window.main_menu))

        select_encrypted_file_button = DefaultButtonStyle(
            'Select Encrypted File', parent=self, command=self.select_encrypted_file)
        select_encrypted_file_button.setGeometry(20, 80, 180, 50)

        select_key_button = DefaultButtonStyle(
            'Select Key File', parent=self, command=self.select_key_file)
        select_key_button.setGeometry(215, 80, 150, 50)

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, command=self.decrypt_file)
        decrypt_button.setGeometry(380, 80, 100, 50)

        self.selected_file_label = DefaultQTextEditStyle(text=None, parent=self, geometry=(20, 150, 470, 100))
        self.set_selected_file_label(selected_file=None)

        self.selected_key_label = DefaultQTextEditStyle(text=None, parent=self, geometry=(20, 270, 470, 100))
        self.set_selected_key_label(selected_encryption_key=None)

        self.decrypted_path_label = DefaultQTextEditStyle(text=None, parent=self, geometry=(20, 390, 470, 100))
        self.set_decrypted_path_label(decrypted_file=None)

    def set_selected_file_label(self, selected_file):
        self.selected_file_label.setHtml(f"<b>Current selected encrypted file:</b><br>{selected_file}")

    def set_selected_key_label(self, selected_encryption_key):
        self.selected_key_label.setHtml(f"<b>Current selected encryption key:</b><br>{selected_encryption_key}")

    def set_decrypted_path_label(self, decrypted_file):
        self.decrypted_path_label.setHtml(f"<b>Decrypted file location: </b><br>{decrypted_file}")    

    def select_encrypted_file(self):
        file_dialog = QFileDialog()
        self.selected_file_path, _ = file_dialog.getOpenFileName(self, 'Select Encrypted File', filter="(*.encrypted)")
        try:
            if self.selected_file_path:
                QMessageBox.information(self, 'Encrypted file successfully selected', f'Selected encrypted file: {self.selected_file_path}')
                self.set_selected_file_label(selected_file=self.selected_file_path)
        except Exception as e:
                QMessageBox.critical(self, f'An error occured: {e}', 'Unsuccessful file selection')
        
    def select_key_file(self):
        file_dialog = QFileDialog()
        self.selected_key_file_path, _ = file_dialog.getOpenFileName(self, 'Select Key File', filter="Key files (*.key)")
        try:
            if self.selected_key_file_path:
                QMessageBox.information(self, 'Encryption key successfully selected', f'Selected key file: {self.selected_key_file_path}')
                self.set_selected_key_label(selected_encryption_key=self.selected_key_file_path)
        except Exception as e:
                QMessageBox.critical(self, f'An error occured: {e}', 'Unsuccessful key selection')

    def decrypt_file(self):
        if not hasattr(self, 'selected_file_path'):
            QMessageBox.warning(self, 'No Encrypted File', 'Please select an encrypted file first.')
        if not hasattr(self, 'selected_key_file_path'):
            QMessageBox.warning(self, 'No Key File', 'Please select the encryption key file first.')

        try:
            # Read the encryption key
            with open(self.selected_key_file_path, 'rb') as key_file:
                key = key_file.read()
            cipher = Fernet(key)

            # Read the encrypted file
            with open(self.selected_file_path, 'rb') as encrypted_file:
                encrypted_data = encrypted_file.read()
            
            # Decrypt the data
            decrypted_data = cipher.decrypt(encrypted_data)

            # Save the decrypted file
            original_file_name = os.path.basename(self.selected_file_path).replace('.encrypted', '')
            decrypted_file_path = os.path.join(self.downloads_path, f'decrypted_{original_file_name}')

            with open(decrypted_file_path, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Decryption Successful')
            msg_box.setText(f'File decrypted and saved at: {decrypted_file_path}')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
            msg_box.exec()
            self.set_decrypted_path_label(decrypted_file=decrypted_file_path)
            if msg_box.clickedButton() == open_folder_btn:
                self.open_downloads_folder()

        except Exception as e:
            QMessageBox.critical(self, 'Decryption Failed', f'An error occurred during decryption: {str(e)}')
    
    def open_downloads_folder(self):
        # Open the Downloads folder using the appropriate command for the OS
        if sys.platform == 'win32':
            os.startfile(self.downloads_path)
        elif sys.platform == 'darwin':  # macOS
            QProcess.execute('open', [self.downloads_path])
        else:  # Linux and other Unix-like systems
            QProcess.execute('xdg-open', [self.downloads_path])
