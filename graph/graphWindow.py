# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GraphWindow(object):
    def setupUi(self, GraphWindow):
        GraphWindow.setObjectName("GraphWindow")
        GraphWindow.resize(489, 358)
        self.centralwidget = QtWidgets.QWidget(GraphWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.scrollArea = QtWidgets.QScrollArea(self.splitter)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 205, 316))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.text.setObjectName("text")
        self.verticalLayout_2.addWidget(self.text)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mplWidget = MplWidget(self.layoutWidget)
        self.mplWidget.setObjectName("mplWidget")
        self.verticalLayout.addWidget(self.mplWidget)
        self.slider = QtWidgets.QSlider(self.layoutWidget)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.verticalLayout.addWidget(self.slider)
        self.horizontalLayout.addWidget(self.splitter)
        GraphWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(GraphWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 489, 22))
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
        GraphWindow.setMenuBar(self.menubar)
        self.actionSubmenu1 = QtWidgets.QAction(GraphWindow)
        self.actionSubmenu1.setObjectName("actionSubmenu1")
        self.actionSubmenu2 = QtWidgets.QAction(GraphWindow)
        self.actionSubmenu2.setObjectName("actionSubmenu2")
        self.menupenguin.addSeparator()
        self.menupenguin.addAction(self.actionSubmenu1)
        self.menupenguin.addAction(self.actionSubmenu2)
        self.menubar.addAction(self.monkey.menuAction())
        self.menubar.addAction(self.menupenguin.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(GraphWindow)
        QtCore.QMetaObject.connectSlotsByName(GraphWindow)

    def retranslateUi(self, GraphWindow):
        _translate = QtCore.QCoreApplication.translate
        GraphWindow.setWindowTitle(_translate("GraphWindow", "GraphWindow"))
        self.text.setText(_translate("GraphWindow", "TextLabel"))
        self.monkey.setTitle(_translate("GraphWindow", "File"))
        self.menupenguin.setTitle(_translate("GraphWindow", "Edit"))
        self.menuView.setTitle(_translate("GraphWindow", "View"))
        self.menuWindow.setTitle(_translate("GraphWindow", "Window"))
        self.menuHelp.setTitle(_translate("GraphWindow", "Help"))
        self.actionSubmenu1.setText(_translate("GraphWindow", "Submenu1"))
        self.actionSubmenu2.setText(_translate("GraphWindow", "Submenu2"))
from mpl_canvas import MplWidget
