from PySide2 import QtCore, QtWidgets

from .ui_preferences import Ui_PreferencesDialog


class PreferencesDialog(QtWidgets.QDialog, Ui_PreferencesDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QtCore.QSettings()

        self.setupUi(self)

        # this is easily forgotten in Qt Designer
        self.tabWidget.setCurrentIndex(0)

        self.accepted.connect(self.write_settings)

        self.read_settings()

    def read_settings(self):
        self.unitPreferences.read_settings()

    def write_settings(self):
        self.unitPreferences.write_settings()
