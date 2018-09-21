# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'show_widget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_show_widget(object):
    def setupUi(self, show_widget):
        show_widget.setObjectName("show_widget")
        show_widget.setWindowModality(QtCore.Qt.WindowModal)
        show_widget.resize(500, 400)
        show_widget.setMouseTracking(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(show_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(show_widget)
        self.frame.setMouseTracking(True)
        self.frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(show_widget)
        QtCore.QMetaObject.connectSlotsByName(show_widget)

    def retranslateUi(self, show_widget):
        _translate = QtCore.QCoreApplication.translate
        show_widget.setWindowTitle(_translate("show_widget", "Form"))

