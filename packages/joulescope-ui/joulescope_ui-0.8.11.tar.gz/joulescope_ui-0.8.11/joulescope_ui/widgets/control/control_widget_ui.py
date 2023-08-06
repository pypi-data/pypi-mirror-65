# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\repos\Jetperch\pyjoulescope_ui\joulescope_ui\widgets\control\control_widget_ui.ui',
# licensing of 'C:\repos\Jetperch\pyjoulescope_ui\joulescope_ui\widgets\control\control_widget_ui.ui' applies.
#
# Created: Fri Apr 10 12:51:37 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ControlWidget(object):
    def setupUi(self, ControlWidget):
        ControlWidget.setObjectName("ControlWidget")
        ControlWidget.resize(754, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ControlWidget.sizePolicy().hasHeightForWidth())
        ControlWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ControlWidget)
        self.horizontalLayout.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.playButton = QtWidgets.QPushButton(ControlWidget)
        self.playButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/joulescope/resources/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playButton.setIcon(icon)
        self.playButton.setCheckable(True)
        self.playButton.setFlat(True)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout.addWidget(self.playButton)
        self.recordButton = QtWidgets.QPushButton(ControlWidget)
        self.recordButton.setEnabled(True)
        self.recordButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/joulescope/resources/record.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.recordButton.setIcon(icon1)
        self.recordButton.setCheckable(True)
        self.recordButton.setFlat(True)
        self.recordButton.setObjectName("recordButton")
        self.horizontalLayout.addWidget(self.recordButton)
        self.iRangeLabel = QtWidgets.QLabel(ControlWidget)
        self.iRangeLabel.setObjectName("iRangeLabel")
        self.horizontalLayout.addWidget(self.iRangeLabel)
        self.iRangeComboBox = QtWidgets.QComboBox(ControlWidget)
        self.iRangeComboBox.setObjectName("iRangeComboBox")
        self.horizontalLayout.addWidget(self.iRangeComboBox)
        self.vRangeLabel = QtWidgets.QLabel(ControlWidget)
        self.vRangeLabel.setObjectName("vRangeLabel")
        self.horizontalLayout.addWidget(self.vRangeLabel)
        self.vRangeComboBox = QtWidgets.QComboBox(ControlWidget)
        self.vRangeComboBox.setObjectName("vRangeComboBox")
        self.horizontalLayout.addWidget(self.vRangeComboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.energyNameLabel = QtWidgets.QLabel(ControlWidget)
        self.energyNameLabel.setObjectName("energyNameLabel")
        self.horizontalLayout.addWidget(self.energyNameLabel)
        self.energyValueLabel = QtWidgets.QLabel(ControlWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.energyValueLabel.setFont(font)
        self.energyValueLabel.setObjectName("energyValueLabel")
        self.horizontalLayout.addWidget(self.energyValueLabel)

        self.retranslateUi(ControlWidget)
        QtCore.QMetaObject.connectSlotsByName(ControlWidget)

    def retranslateUi(self, ControlWidget):
        self.playButton.setToolTip(QtWidgets.QApplication.translate("ControlWidget", "Enable to capture data from the selected Joulescope.  Disable to stop/pause capture.", None, -1))
        self.recordButton.setToolTip(QtWidgets.QApplication.translate("ControlWidget", "Click once to start recording capture Joulescope data to a file.  Click again to stop the capture.  Only new data is recorded.", None, -1))
        self.iRangeLabel.setText(QtWidgets.QApplication.translate("ControlWidget", "Current Range", None, -1))
        self.iRangeComboBox.setToolTip(QtWidgets.QApplication.translate("ControlWidget", "Select the Joulescope current range.  \"Auto\" allows Joulescope to dynamical adjust the current range.", None, -1))
        self.vRangeLabel.setText(QtWidgets.QApplication.translate("ControlWidget", "Voltage Range", None, -1))
        self.vRangeComboBox.setToolTip(QtWidgets.QApplication.translate("ControlWidget", "The voltage range.  No autoranging option exists.", None, -1))
        self.energyNameLabel.setText(QtWidgets.QApplication.translate("ControlWidget", "Energy", None, -1))
        self.energyValueLabel.setText(QtWidgets.QApplication.translate("ControlWidget", "0 J", None, -1))

from joulescope_ui import joulescope_rc
