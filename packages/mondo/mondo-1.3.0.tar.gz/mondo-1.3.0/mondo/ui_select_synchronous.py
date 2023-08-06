# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_synchronous.ui',
# licensing of 'select_synchronous.ui' applies.
#
# Created: Tue Apr  2 19:36:21 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SelectSynchronousDialog(object):
    def setupUi(self, SelectSynchronousDialog):
        SelectSynchronousDialog.setObjectName("SelectSynchronousDialog")
        SelectSynchronousDialog.resize(400, 49)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SelectSynchronousDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(SelectSynchronousDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(SelectSynchronousDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SelectSynchronousDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SelectSynchronousDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectSynchronousDialog)

    def retranslateUi(self, SelectSynchronousDialog):
        SelectSynchronousDialog.setWindowTitle(QtWidgets.QApplication.translate("SelectSynchronousDialog", "Select Synchronous Channels", None, -1))

