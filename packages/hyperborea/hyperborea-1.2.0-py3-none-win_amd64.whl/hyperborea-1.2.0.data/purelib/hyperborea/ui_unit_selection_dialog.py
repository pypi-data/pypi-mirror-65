# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unit_selection_dialog.ui',
# licensing of 'unit_selection_dialog.ui' applies.
#
# Created: Fri Oct 25 09:11:22 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_UnitSelectionDialog(object):
    def setupUi(self, UnitSelectionDialog):
        UnitSelectionDialog.setObjectName("UnitSelectionDialog")
        UnitSelectionDialog.resize(184, 68)
        self.verticalLayout = QtWidgets.QVBoxLayout(UnitSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.unitGridLayout = QtWidgets.QGridLayout()
        self.unitGridLayout.setHorizontalSpacing(20)
        self.unitGridLayout.setObjectName("unitGridLayout")
        self.metricLabel = QtWidgets.QLabel(UnitSelectionDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.metricLabel.setFont(font)
        self.metricLabel.setObjectName("metricLabel")
        self.unitGridLayout.addWidget(self.metricLabel, 0, 0, 1, 1)
        self.usLabel = QtWidgets.QLabel(UnitSelectionDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.usLabel.setFont(font)
        self.usLabel.setObjectName("usLabel")
        self.unitGridLayout.addWidget(self.usLabel, 0, 1, 1, 1)
        self.otherLabel = QtWidgets.QLabel(UnitSelectionDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.otherLabel.setFont(font)
        self.otherLabel.setObjectName("otherLabel")
        self.unitGridLayout.addWidget(self.otherLabel, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.unitGridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(UnitSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(UnitSelectionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), UnitSelectionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), UnitSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UnitSelectionDialog)

    def retranslateUi(self, UnitSelectionDialog):
        UnitSelectionDialog.setWindowTitle(QtWidgets.QApplication.translate("UnitSelectionDialog", "Select Unit", None, -1))
        self.metricLabel.setText(QtWidgets.QApplication.translate("UnitSelectionDialog", "SI", None, -1))
        self.usLabel.setText(QtWidgets.QApplication.translate("UnitSelectionDialog", "US Customary", None, -1))
        self.otherLabel.setText(QtWidgets.QApplication.translate("UnitSelectionDialog", "Other", None, -1))

