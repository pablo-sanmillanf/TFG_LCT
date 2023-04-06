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
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuFont = QtWidgets.QMenu(self.menuEdit)
        self.menuFont.setObjectName("menuFont")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
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
        self.actionText_size = QtWidgets.QAction(MainWindow)
        self.actionText_size.setObjectName("actionText_size")
        self.actionRects_colors = QtWidgets.QAction(MainWindow)
        self.actionRects_colors.setObjectName("actionRects_colors")
        self.monkey.addAction(self.actionNew)
        self.monkey.addAction(self.actionOpen)
        self.monkey.addAction(self.actionSave)
        self.monkey.addAction(self.actionSave_as)
        self.menuFont.addAction(self.actionText_size)
        self.menuFont.addAction(self.actionRects_colors)
        self.menuEdit.addAction(self.menuFont.menuAction())
        self.menuEdit.addAction(self.actionSubmenu2)
        self.menubar.addAction(self.monkey.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.monkey.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuFont.setTitle(_translate("MainWindow", "Change Font"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSubmenu2.setText(_translate("MainWindow", "Submenu2"))
        self.actionNew.setText(_translate("MainWindow", "New..."))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionSeve.setText(_translate("MainWindow", "Seve"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as..."))
        self.actionText_size.setText(_translate("MainWindow", "Text size"))
        self.actionRects_colors.setText(_translate("MainWindow", "Rects colors"))
from text_handler import TextHandler
