# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting_viewer.ui',
# licensing of 'setting_viewer.ui' applies.
#
# Created: Tue Mar  3 14:52:37 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SettingViewerDialog(object):
    def setupUi(self, SettingViewerDialog):
        SettingViewerDialog.setObjectName("SettingViewerDialog")
        SettingViewerDialog.resize(400, 53)
        self.verticalLayout = QtWidgets.QVBoxLayout(SettingViewerDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(SettingViewerDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingViewerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SettingViewerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SettingViewerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SettingViewerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingViewerDialog)

    def retranslateUi(self, SettingViewerDialog):
        SettingViewerDialog.setWindowTitle(QtWidgets.QApplication.translate("SettingViewerDialog", "Device Settings", None, -1))

