# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/builds/clients/python/sakia/src/sakia/gui/dialogs/startup.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StartupDialog(object):
    def setupUi(self, StartupDialog):
        StartupDialog.setObjectName("StartupDialog")
        StartupDialog.resize(362, 95)
        self.horizontalLayoutWidget = QtWidgets.QWidget(StartupDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 341, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(50, 50))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/icons/sakia_logo"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.cancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setAutoDefault(True)
        self.cancelButton.setObjectName("cancelButton")
        self.verticalLayout.addWidget(self.cancelButton, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(StartupDialog)
        QtCore.QMetaObject.connectSlotsByName(StartupDialog)

    def retranslateUi(self, StartupDialog):
        _translate = QtCore.QCoreApplication.translate
        StartupDialog.setWindowTitle(_translate("StartupDialog", "Sakia"))
        self.label.setText(_translate("StartupDialog", "Connecting to the network\n"
"please wait..."))
        self.cancelButton.setText(_translate("StartupDialog", "Cancel"))

import sakia.icons_rc
