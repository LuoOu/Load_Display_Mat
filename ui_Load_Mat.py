# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Load_Mat.ui'
#
# Created: Wed Nov 18 16:04:19 2020
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Ui_LoadMatWindow(object):
    def setupUi(self, LoadMatWindow):
        LoadMatWindow.setObjectName("LoadMatWindow")
        LoadMatWindow.resize(399, 90)
        LoadMatWindow.setMaximumSize(QtCore.QSize(400, 600))
        self.centralWidget = QWidget(LoadMatWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.allWidget = QWidget(self.centralWidget)
        self.allWidget.setGeometry(QtCore.QRect(0, 0, 400, 90))
        self.allWidget.setMinimumSize(QtCore.QSize(400, 90))
        self.allWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.allWidget.setObjectName("allWidget")
        self.allLayout = QVBoxLayout(self.allWidget)
        self.allLayout.setContentsMargins(0, 0, 0, 0)
        self.allLayout.setObjectName("allLayout")
        self.aWidget = QWidget(self.allWidget)
        self.aWidget.setMaximumSize(QtCore.QSize(400, 50))
        self.aWidget.setObjectName("aWidget")
        self.aLayout = QHBoxLayout(self.aWidget)
        self.aLayout.setSpacing(3)
        self.aLayout.setContentsMargins(3, 3, 3, 3)
        self.aLayout.setObjectName("aLayout")
        self.outlabel = QLabel(self.aWidget)
        self.outlabel.setObjectName("outlabel")
        self.aLayout.addWidget(self.outlabel)
        self.pathlineEdit = QLineEdit(self.aWidget)
        self.pathlineEdit.setObjectName("pathlineEdit")
        self.aLayout.addWidget(self.pathlineEdit)
        self.lookpushButton = QPushButton(self.aWidget)
        self.lookpushButton.setObjectName("lookpushButton")
        self.aLayout.addWidget(self.lookpushButton)
        self.allLayout.addWidget(self.aWidget)
        self.bWidget = QWidget(self.allWidget)
        self.bWidget.setMaximumSize(QtCore.QSize(400, 40))
        self.bWidget.setObjectName("bWidget")
        self.bLayout = QHBoxLayout(self.bWidget)
        self.bLayout.setSpacing(3)
        self.bLayout.setContentsMargins(3, 3, 3, 3)
        self.bLayout.setObjectName("bLayout")
        self.filelabel = QLabel(self.bWidget)
        self.filelabel.setObjectName("filelabel")
        self.bLayout.addWidget(self.filelabel)
        self.cleanpushButton = QPushButton(self.bWidget)
        self.cleanpushButton.setObjectName("cleanpushButton")
        self.bLayout.addWidget(self.cleanpushButton)
        self.allLayout.addWidget(self.bWidget)
        LoadMatWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(LoadMatWindow)
        QtCore.QMetaObject.connectSlotsByName(LoadMatWindow)

    def retranslateUi(self, LoadMatWindow):
        _translate = QtCore.QCoreApplication.translate
        LoadMatWindow.setWindowTitle(_translate("LoadMatWindow", "加载材质"))
        self.outlabel.setText(_translate("LoadMatWindow", "材质链接文件"))
        self.lookpushButton.setText(_translate("LoadMatWindow", "浏览"))
        self.filelabel.setText(_translate("LoadMatWindow", ""))
        self.cleanpushButton.setText(_translate("LoadMatWindow", "加载材质"))

