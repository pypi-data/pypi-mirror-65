# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferences.ui',
# licensing of 'preferences.ui' applies.
#
# Created: Fri Mar 27 12:26:29 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        PreferencesDialog.setObjectName("PreferencesDialog")
        PreferencesDialog.resize(414, 379)
        self.verticalLayout = QtWidgets.QVBoxLayout(PreferencesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(PreferencesDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.unitTab = QtWidgets.QWidget()
        self.unitTab.setObjectName("unitTab")
        self.gridLayout = QtWidgets.QGridLayout(self.unitTab)
        self.gridLayout.setObjectName("gridLayout")
        self.unitsLabel = QtWidgets.QLabel(self.unitTab)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.unitsLabel.setFont(font)
        self.unitsLabel.setObjectName("unitsLabel")
        self.gridLayout.addWidget(self.unitsLabel, 0, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 2)
        self.unitPreferences = UnitPreferencesWidget(self.unitTab)
        self.unitPreferences.setObjectName("unitPreferences")
        self.gridLayout.addWidget(self.unitPreferences, 1, 1, 1, 1)
        self.tabWidget.addTab(self.unitTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(PreferencesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PreferencesDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), PreferencesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), PreferencesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDialog)
        PreferencesDialog.setTabOrder(self.tabWidget, self.buttonBox)

    def retranslateUi(self, PreferencesDialog):
        PreferencesDialog.setWindowTitle(QtWidgets.QApplication.translate("PreferencesDialog", "Preferences", None, -1))
        self.unitsLabel.setText(QtWidgets.QApplication.translate("PreferencesDialog", "Display Units", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.unitTab), QtWidgets.QApplication.translate("PreferencesDialog", "Units", None, -1))

from hyperborea.unit_preferences import UnitPreferencesWidget
