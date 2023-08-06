# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\repos\Jetperch\pyjoulescope_ui\joulescope_ui\widgets\gpio\gpio_widget_ui.ui',
# licensing of 'C:\repos\Jetperch\pyjoulescope_ui\joulescope_ui\widgets\gpio\gpio_widget_ui.ui' applies.
#
# Created: Fri Apr 10 12:51:37 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_GpioWidget(object):
    def setupUi(self, GpioWidget):
        GpioWidget.setObjectName("GpioWidget")
        GpioWidget.resize(659, 22)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GpioWidget.sizePolicy().hasHeightForWidth())
        GpioWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(GpioWidget)
        self.horizontalLayout.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input1CheckBox = QtWidgets.QCheckBox(GpioWidget)
        self.input1CheckBox.setObjectName("input1CheckBox")
        self.horizontalLayout.addWidget(self.input1CheckBox)
        self.input1Label = QtWidgets.QLabel(GpioWidget)
        self.input1Label.setToolTip("")
        self.input1Label.setObjectName("input1Label")
        self.horizontalLayout.addWidget(self.input1Label)
        self.label = QtWidgets.QLabel(GpioWidget)
        self.label.setMinimumSize(QtCore.QSize(10, 0))
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.input0CheckBox = QtWidgets.QCheckBox(GpioWidget)
        self.input0CheckBox.setObjectName("input0CheckBox")
        self.horizontalLayout.addWidget(self.input0CheckBox)
        self.input0Label = QtWidgets.QLabel(GpioWidget)
        self.input0Label.setObjectName("input0Label")
        self.horizontalLayout.addWidget(self.input0Label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.output1Button = QtWidgets.QPushButton(GpioWidget)
        self.output1Button.setStyleSheet("QPushButton {padding-left: 10px; padding-right: 10px;}")
        self.output1Button.setCheckable(True)
        self.output1Button.setObjectName("output1Button")
        self.horizontalLayout.addWidget(self.output1Button)
        self.output0Button = QtWidgets.QPushButton(GpioWidget)
        self.output0Button.setStyleSheet("QPushButton {padding-left: 10px; padding-right: 10px;}")
        self.output0Button.setCheckable(True)
        self.output0Button.setObjectName("output0Button")
        self.horizontalLayout.addWidget(self.output0Button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.voltageLabel = QtWidgets.QLabel(GpioWidget)
        self.voltageLabel.setObjectName("voltageLabel")
        self.horizontalLayout.addWidget(self.voltageLabel)
        self.voltageComboBox = QtWidgets.QComboBox(GpioWidget)
        self.voltageComboBox.setObjectName("voltageComboBox")
        self.horizontalLayout.addWidget(self.voltageComboBox)

        self.retranslateUi(GpioWidget)
        QtCore.QMetaObject.connectSlotsByName(GpioWidget)

    def retranslateUi(self, GpioWidget):
        GpioWidget.setWindowTitle(QtWidgets.QApplication.translate("GpioWidget", "Form", None, -1))
        self.input1CheckBox.setToolTip(QtWidgets.QApplication.translate("GpioWidget", "<html><head/><body><p>Check to enable general purpose input 1 (IN1).</p><p>When IN1 is enabled, the data overwrites the voltage least-significant bit, which reduces the resolution from 14 bits to 13 bits.</p></body></html>", None, -1))
        self.input1CheckBox.setText(QtWidgets.QApplication.translate("GpioWidget", "IN1", None, -1))
        self.input1Label.setText(QtWidgets.QApplication.translate("GpioWidget", "_", None, -1))
        self.label.setToolTip(QtWidgets.QApplication.translate("GpioWidget", "The IN1 signal value.", None, -1))
        self.input0CheckBox.setToolTip(QtWidgets.QApplication.translate("GpioWidget", "<html><head/><body><p>Check to enable general purpose input 0 (IN1).</p><p>When IN0 is enabled, the data overwrites the current least-significant bit, which reduces the resolution from 14 bits to 13 bits.</p></body></html>", None, -1))
        self.input0CheckBox.setText(QtWidgets.QApplication.translate("GpioWidget", "IN0", None, -1))
        self.input0Label.setToolTip(QtWidgets.QApplication.translate("GpioWidget", "The IN0 signal value.", None, -1))
        self.input0Label.setText(QtWidgets.QApplication.translate("GpioWidget", "_", None, -1))
        self.output1Button.setToolTip(QtWidgets.QApplication.translate("GpioWidget", "<html><head/><body><p>Toggle the output 1 (OUT1) value.</p><p>When inactive the output will be 0 V (digital low).  When pressed, the output will be the configured voltage, (digital high).</p></body></html>", None, -1))
        self.output1Button.setText(QtWidgets.QApplication.translate("GpioWidget", "OUT1", None, -1))
        self.output0Button.setToolTip(QtWidgets.QApplication.translate("GpioWidget", "<html><head/><body><p>Toggle the output 0 (OUT0) value.</p><p>When inactive the output will be 0 V (digital low).  When pressed, the output will be the configured voltage, (digital high).</p></body></html>", None, -1))
        self.output0Button.setText(QtWidgets.QApplication.translate("GpioWidget", "OUT0", None, -1))
        self.voltageLabel.setToolTip(QtWidgets.QApplication.translate("GpioWidget", "<html><head/><body><p>Select the general purpose input/output reference voltage.</p><p>The reference voltage determines the output signal voltage,  the logic level thresholds for the inputs, and the maximum voltage the inputs can tolerate.  </p></body></html>", None, -1))
        self.voltageLabel.setText(QtWidgets.QApplication.translate("GpioWidget", "Voltage", None, -1))
        self.voltageComboBox.setToolTip(QtWidgets.QApplication.translate("GpioWidget", "<html><head/><body><p>Select the general purpose input/output reference voltage.</p><p>The reference voltage determines the output signal voltage,  the logic level thresholds for the inputs, and the maximum voltage the inputs can tolerate.  </p></body></html>", None, -1))

