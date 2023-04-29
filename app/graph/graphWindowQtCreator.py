# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GraphWindow(object):
    def setupUi(self, GraphWindow):
        GraphWindow.setObjectName("GraphWindow")
        GraphWindow.resize(1150, 550)
        self.centralwidget = QtWidgets.QWidget(GraphWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(350, 0))
        self.scrollArea.setMaximumSize(QtCore.QSize(350, 16777215))
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 348, 508))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text = TextLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text.sizePolicy().hasHeightForWidth())
        self.text.setSizePolicy(sizePolicy)
        self.text.setAutoFillBackground(True)
        self.text.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.text.setWordWrap(True)
        self.text.setObjectName("text")
        self.verticalLayout_2.addWidget(self.text)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.mplWidget = MplWidget(self.centralwidget)
        self.mplWidget.setMinimumSize(QtCore.QSize(200, 200))
        self.mplWidget.setObjectName("mplWidget")
        self.verticalLayout.addWidget(self.mplWidget)
        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.verticalLayout.addWidget(self.slider)
        self.horizontalLayout.addLayout(self.verticalLayout)
        GraphWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(GraphWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1150, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuTarget = QtWidgets.QMenu(self.menuEdit)
        self.menuTarget.setObjectName("menuTarget")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuVisibility = QtWidgets.QMenu(self.menuView)
        self.menuVisibility.setObjectName("menuVisibility")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        GraphWindow.setMenuBar(self.menubar)
        self.actionSave_Visibe_Chart_as_Image = QtWidgets.QAction(GraphWindow)
        self.actionSave_Visibe_Chart_as_Image.setObjectName("actionSave_Visibe_Chart_as_Image")
        self.actionSD = QtWidgets.QAction(GraphWindow)
        self.actionSD.setCheckable(True)
        self.actionSD.setChecked(True)
        self.actionSD.setObjectName("actionSD")
        self.actionSG = QtWidgets.QAction(GraphWindow)
        self.actionSG.setCheckable(True)
        self.actionSG.setChecked(True)
        self.actionSG.setObjectName("actionSG")
        self.actionVisible_points = QtWidgets.QAction(GraphWindow)
        self.actionVisible_points.setObjectName("actionVisible_points")
        self.actiongroupTarget = QtWidgets.QActionGroup(GraphWindow)
        self.actiongroupTarget.setObjectName("actiongroupTarget")
        self.actionClauses = QtWidgets.QAction(self.actiongroupTarget)
        self.actionClauses.setCheckable(True)
        self.actionClauses.setChecked(True)
        self.actionClauses.setObjectName("actionClauses")
        self.actionSuperClauses = QtWidgets.QAction(self.actiongroupTarget)
        self.actionSuperClauses.setCheckable(True)
        self.actionSuperClauses.setObjectName("actionSuperClauses")
        self.menuFile.addAction(self.actionSave_Visibe_Chart_as_Image)
        self.menuTarget.addAction(self.actionClauses)
        self.menuTarget.addAction(self.actionSuperClauses)
        self.menuEdit.addAction(self.actionVisible_points)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.menuTarget.menuAction())
        self.menuVisibility.addAction(self.actionSD)
        self.menuVisibility.addAction(self.actionSG)
        self.menuView.addAction(self.menuVisibility.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(GraphWindow)
        QtCore.QMetaObject.connectSlotsByName(GraphWindow)

    def retranslateUi(self, GraphWindow):
        _translate = QtCore.QCoreApplication.translate
        GraphWindow.setWindowTitle(_translate("GraphWindow", "MainWindow"))
        self.text.setText(_translate("GraphWindow", "Text Label"))
        self.menuFile.setTitle(_translate("GraphWindow", "File"))
        self.menuEdit.setTitle(_translate("GraphWindow", "Edit"))
        self.menuTarget.setTitle(_translate("GraphWindow", "Target"))
        self.menuView.setTitle(_translate("GraphWindow", "View"))
        self.menuVisibility.setTitle(_translate("GraphWindow", "Visibility"))
        self.menuHelp.setTitle(_translate("GraphWindow", "Help"))
        self.actionSave_Visibe_Chart_as_Image.setText(_translate("GraphWindow", "Save Visibe Chart as Image"))
        self.actionSD.setText(_translate("GraphWindow", "SD"))
        self.actionSG.setText(_translate("GraphWindow", "SG"))
        self.actionVisible_points.setText(_translate("GraphWindow", "Visible points"))
        self.actionClauses.setText(_translate("GraphWindow", "Clauses"))
        self.actionSuperClauses.setText(_translate("GraphWindow", "Super clauses"))
from .mpl_canvas import MplWidget
from .text_label import TextLabel
