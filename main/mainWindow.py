# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(490, 420)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textHandler = TextHandler(self.centralwidget)
        self.textHandler.setObjectName("textHandler")
        self.horizontalLayout.addWidget(self.textHandler)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 490, 22))
        self.menubar.setObjectName("menubar")
        self.monkey = QtWidgets.QMenu(self.menubar)
        self.monkey.setObjectName("monkey")
        self.menupenguin = QtWidgets.QMenu(self.menubar)
        self.menupenguin.setObjectName("menupenguin")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionSubmenu1 = QtWidgets.QAction(MainWindow)
        self.actionSubmenu1.setObjectName("actionSubmenu1")
        self.actionSubmenu2 = QtWidgets.QAction(MainWindow)
        self.actionSubmenu2.setObjectName("actionSubmenu2")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSeve = QtWidgets.QAction(MainWindow)
        self.actionSeve.setObjectName("actionSeve")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.monkey.addAction(self.actionNew)
        self.monkey.addAction(self.actionOpen)
        self.monkey.addAction(self.actionSave)
        self.monkey.addAction(self.actionSave_as)
        self.menupenguin.addAction(self.actionSubmenu1)
        self.menupenguin.addAction(self.actionSubmenu2)
        self.menubar.addAction(self.monkey.menuAction())
        self.menubar.addAction(self.menupenguin.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.monkey.setTitle(_translate("MainWindow", "File"))
        self.menupenguin.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSubmenu1.setText(_translate("MainWindow", "Submenu1"))
        self.actionSubmenu2.setText(_translate("MainWindow", "Submenu2"))
        self.actionNew.setText(_translate("MainWindow", "New..."))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionSeve.setText(_translate("MainWindow", "Seve"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as..."))
from text_handler import TextHandler
