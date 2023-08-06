# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_subchannels.ui',
# licensing of 'select_subchannels.ui' applies.
#
# Created: Tue Apr  2 19:36:21 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SelectSubchannelsDialog(object):
    def setupUi(self, SelectSubchannelsDialog):
        SelectSubchannelsDialog.setObjectName("SelectSubchannelsDialog")
        SelectSubchannelsDialog.resize(400, 49)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SelectSubchannelsDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(SelectSubchannelsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(SelectSubchannelsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SelectSubchannelsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SelectSubchannelsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectSubchannelsDialog)

    def retranslateUi(self, SelectSubchannelsDialog):
        SelectSubchannelsDialog.setWindowTitle(QtWidgets.QApplication.translate("SelectSubchannelsDialog", "Select Subchannels Channels", None, -1))

