# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unit_preferences_widget.ui',
# licensing of 'unit_preferences_widget.ui' applies.
#
# Created: Fri Mar 27 10:07:05 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_UnitPreferencesWidget(object):
    def setupUi(self, UnitPreferencesWidget):
        UnitPreferencesWidget.setObjectName("UnitPreferencesWidget")
        UnitPreferencesWidget.resize(207, 17)
        self.unitGridLayout = QtWidgets.QGridLayout(UnitPreferencesWidget)
        self.unitGridLayout.setContentsMargins(0, 0, 0, 0)
        self.unitGridLayout.setObjectName("unitGridLayout")
        self.metricUnits = QtWidgets.QRadioButton(UnitPreferencesWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.metricUnits.setFont(font)
        self.metricUnits.setObjectName("metricUnits")
        self.unitGridLayout.addWidget(self.metricUnits, 0, 0, 1, 1)
        self.usUnits = QtWidgets.QRadioButton(UnitPreferencesWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.usUnits.setFont(font)
        self.usUnits.setObjectName("usUnits")
        self.unitGridLayout.addWidget(self.usUnits, 0, 1, 1, 1)
        self.mixedUnits = QtWidgets.QRadioButton(UnitPreferencesWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.mixedUnits.setFont(font)
        self.mixedUnits.setObjectName("mixedUnits")
        self.unitGridLayout.addWidget(self.mixedUnits, 0, 2, 1, 1)

        self.retranslateUi(UnitPreferencesWidget)
        QtCore.QMetaObject.connectSlotsByName(UnitPreferencesWidget)

    def retranslateUi(self, UnitPreferencesWidget):
        self.metricUnits.setText(QtWidgets.QApplication.translate("UnitPreferencesWidget", "SI", None, -1))
        self.usUnits.setText(QtWidgets.QApplication.translate("UnitPreferencesWidget", "US Customary", None, -1))
        self.mixedUnits.setText(QtWidgets.QApplication.translate("UnitPreferencesWidget", "Mixed", None, -1))

