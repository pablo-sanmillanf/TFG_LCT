# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'colorsdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ColorsDialog(object):
    def setupUi(self, ColorsDialog):
        ColorsDialog.setObjectName("ColorsDialog")
        ColorsDialog.resize(480, 480)
        self.verticalLayout = QtWidgets.QVBoxLayout(ColorsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(ColorsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.aloneTab = QtWidgets.QWidget()
        self.aloneTab.setObjectName("aloneTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.aloneTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.alone_default_label = QtWidgets.QLabel(self.aloneTab)
        self.alone_default_label.setObjectName("alone_default_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.alone_default_label)
        self.alone_default_button = QtWidgets.QPushButton(self.aloneTab)
        self.alone_default_button.setText("")
        self.alone_default_button.setObjectName("alone_default_button")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.alone_default_button)
        self.alone_d_plusplus_label = QtWidgets.QLabel(self.aloneTab)
        self.alone_d_plusplus_label.setObjectName("alone_d_plusplus_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.alone_d_plusplus_label)
        self.alone_d_plusplus_button = QtWidgets.QPushButton(self.aloneTab)
        self.alone_d_plusplus_button.setText("")
        self.alone_d_plusplus_button.setObjectName("alone_d_plusplus_button")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.alone_d_plusplus_button)
        self.alone_d_plus_label = QtWidgets.QLabel(self.aloneTab)
        self.alone_d_plus_label.setObjectName("alone_d_plus_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.alone_d_plus_label)
        self.alone_d_plus_button = QtWidgets.QPushButton(self.aloneTab)
        self.alone_d_plus_button.setText("")
        self.alone_d_plus_button.setObjectName("alone_d_plus_button")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.alone_d_plus_button)
        self.alone_d_minus_label = QtWidgets.QLabel(self.aloneTab)
        self.alone_d_minus_label.setObjectName("alone_d_minus_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.alone_d_minus_label)
        self.alone_d_minus_button = QtWidgets.QPushButton(self.aloneTab)
        self.alone_d_minus_button.setText("")
        self.alone_d_minus_button.setObjectName("alone_d_minus_button")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.alone_d_minus_button)
        self.alone_d_minusminus_label = QtWidgets.QLabel(self.aloneTab)
        self.alone_d_minusminus_label.setObjectName("alone_d_minusminus_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.alone_d_minusminus_label)
        self.alone_d_minusminus_button = QtWidgets.QPushButton(self.aloneTab)
        self.alone_d_minusminus_button.setText("")
        self.alone_d_minusminus_button.setObjectName("alone_d_minusminus_button")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.alone_d_minusminus_button)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.tabWidget.addTab(self.aloneTab, "")
        self.togetherTab = QtWidgets.QWidget()
        self.togetherTab.setObjectName("togetherTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.togetherTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.together_default_label = QtWidgets.QLabel(self.togetherTab)
        self.together_default_label.setObjectName("together_default_label")
        self.gridLayout_2.addWidget(self.together_default_label, 1, 0, 1, 1)
        self.together_default_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_default_button.setText("")
        self.together_default_button.setObjectName("together_default_button")
        self.gridLayout_2.addWidget(self.together_default_button, 1, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.together_d_plusplus_g_minusminus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_plusplus_g_minusminus_label.setObjectName("together_d_plusplus_g_minusminus_label")
        self.gridLayout.addWidget(self.together_d_plusplus_g_minusminus_label, 0, 0, 1, 1)
        self.together_d_plusplus_g_minusminus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_plusplus_g_minusminus_button.setText("")
        self.together_d_plusplus_g_minusminus_button.setObjectName("together_d_plusplus_g_minusminus_button")
        self.gridLayout.addWidget(self.together_d_plusplus_g_minusminus_button, 0, 1, 1, 1)
        self.together_d_minus_g_minusminus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_minus_g_minusminus_label.setObjectName("together_d_minus_g_minusminus_label")
        self.gridLayout.addWidget(self.together_d_minus_g_minusminus_label, 0, 2, 1, 1)
        self.together_d_minus_g_minusminus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_minus_g_minusminus_button.setText("")
        self.together_d_minus_g_minusminus_button.setObjectName("together_d_minus_g_minusminus_button")
        self.gridLayout.addWidget(self.together_d_minus_g_minusminus_button, 0, 3, 1, 1)
        self.together_d_plusplus_g_minus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_plusplus_g_minus_label.setObjectName("together_d_plusplus_g_minus_label")
        self.gridLayout.addWidget(self.together_d_plusplus_g_minus_label, 1, 0, 1, 1)
        self.together_d_plusplus_g_minus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_plusplus_g_minus_button.setText("")
        self.together_d_plusplus_g_minus_button.setObjectName("together_d_plusplus_g_minus_button")
        self.gridLayout.addWidget(self.together_d_plusplus_g_minus_button, 1, 1, 1, 1)
        self.together_d_minus_g_minus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_minus_g_minus_label.setObjectName("together_d_minus_g_minus_label")
        self.gridLayout.addWidget(self.together_d_minus_g_minus_label, 1, 2, 1, 1)
        self.together_d_minus_g_minus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_minus_g_minus_button.setText("")
        self.together_d_minus_g_minus_button.setObjectName("together_d_minus_g_minus_button")
        self.gridLayout.addWidget(self.together_d_minus_g_minus_button, 1, 3, 1, 1)
        self.together_d_plusplus_g_plus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_plusplus_g_plus_label.setObjectName("together_d_plusplus_g_plus_label")
        self.gridLayout.addWidget(self.together_d_plusplus_g_plus_label, 2, 0, 1, 1)
        self.together_d_plusplus_g_plus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_plusplus_g_plus_button.setText("")
        self.together_d_plusplus_g_plus_button.setObjectName("together_d_plusplus_g_plus_button")
        self.gridLayout.addWidget(self.together_d_plusplus_g_plus_button, 2, 1, 1, 1)
        self.together_d_minus_g_plus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_minus_g_plus_label.setObjectName("together_d_minus_g_plus_label")
        self.gridLayout.addWidget(self.together_d_minus_g_plus_label, 2, 2, 1, 1)
        self.together_d_minus_g_plus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_minus_g_plus_button.setText("")
        self.together_d_minus_g_plus_button.setObjectName("together_d_minus_g_plus_button")
        self.gridLayout.addWidget(self.together_d_minus_g_plus_button, 2, 3, 1, 1)
        self.together_d_plusplus_g_plusplus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_plusplus_g_plusplus_label.setObjectName("together_d_plusplus_g_plusplus_label")
        self.gridLayout.addWidget(self.together_d_plusplus_g_plusplus_label, 3, 0, 1, 1)
        self.together_d_plusplus_g_plusplus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_plusplus_g_plusplus_button.setText("")
        self.together_d_plusplus_g_plusplus_button.setObjectName("together_d_plusplus_g_plusplus_button")
        self.gridLayout.addWidget(self.together_d_plusplus_g_plusplus_button, 3, 1, 1, 1)
        self.together_d_minus_g_plusplus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_minus_g_plusplus_label.setObjectName("together_d_minus_g_plusplus_label")
        self.gridLayout.addWidget(self.together_d_minus_g_plusplus_label, 3, 2, 1, 1)
        self.together_d_minus_g_plusplus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_minus_g_plusplus_button.setText("")
        self.together_d_minus_g_plusplus_button.setObjectName("together_d_minus_g_plusplus_button")
        self.gridLayout.addWidget(self.together_d_minus_g_plusplus_button, 3, 3, 1, 1)
        self.together_d_plus_g_minusminus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_plus_g_minusminus_label.setObjectName("together_d_plus_g_minusminus_label")
        self.gridLayout.addWidget(self.together_d_plus_g_minusminus_label, 4, 0, 1, 1)
        self.together_d_plus_g_minusminus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_plus_g_minusminus_button.setText("")
        self.together_d_plus_g_minusminus_button.setObjectName("together_d_plus_g_minusminus_button")
        self.gridLayout.addWidget(self.together_d_plus_g_minusminus_button, 4, 1, 1, 1)
        self.together_d_minusminus_g_minusminus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_minusminus_g_minusminus_label.setObjectName("together_d_minusminus_g_minusminus_label")
        self.gridLayout.addWidget(self.together_d_minusminus_g_minusminus_label, 4, 2, 1, 1)
        self.together_d_minusminus_g_minusminus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_minusminus_g_minusminus_button.setText("")
        self.together_d_minusminus_g_minusminus_button.setObjectName("together_d_minusminus_g_minusminus_button")
        self.gridLayout.addWidget(self.together_d_minusminus_g_minusminus_button, 4, 3, 1, 1)
        self.together_d_plus_g_minus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_plus_g_minus_label.setObjectName("together_d_plus_g_minus_label")
        self.gridLayout.addWidget(self.together_d_plus_g_minus_label, 5, 0, 1, 1)
        self.together_d_plus_g_minus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_plus_g_minus_button.setText("")
        self.together_d_plus_g_minus_button.setObjectName("together_d_plus_g_minus_button")
        self.gridLayout.addWidget(self.together_d_plus_g_minus_button, 5, 1, 1, 1)
        self.together_d_minusminus_g_minus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_minusminus_g_minus_label.setObjectName("together_d_minusminus_g_minus_label")
        self.gridLayout.addWidget(self.together_d_minusminus_g_minus_label, 5, 2, 1, 1)
        self.together_d_minusminus_g_minus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_minusminus_g_minus_button.setText("")
        self.together_d_minusminus_g_minus_button.setObjectName("together_d_minusminus_g_minus_button")
        self.gridLayout.addWidget(self.together_d_minusminus_g_minus_button, 5, 3, 1, 1)
        self.together_d_plus_g_plus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_plus_g_plus_label.setObjectName("together_d_plus_g_plus_label")
        self.gridLayout.addWidget(self.together_d_plus_g_plus_label, 6, 0, 1, 1)
        self.together_d_plus_g_plus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_plus_g_plus_button.setText("")
        self.together_d_plus_g_plus_button.setObjectName("together_d_plus_g_plus_button")
        self.gridLayout.addWidget(self.together_d_plus_g_plus_button, 6, 1, 1, 1)
        self.together_d_minusminus_g_plus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_minusminus_g_plus_label.setObjectName("together_d_minusminus_g_plus_label")
        self.gridLayout.addWidget(self.together_d_minusminus_g_plus_label, 6, 2, 1, 1)
        self.together_d_minusminus_g_plus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_minusminus_g_plus_button.setText("")
        self.together_d_minusminus_g_plus_button.setObjectName("together_d_minusminus_g_plus_button")
        self.gridLayout.addWidget(self.together_d_minusminus_g_plus_button, 6, 3, 1, 1)
        self.together_d_plus_g_plusplus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_plus_g_plusplus_label.setObjectName("together_d_plus_g_plusplus_label")
        self.gridLayout.addWidget(self.together_d_plus_g_plusplus_label, 7, 0, 1, 1)
        self.together_d_plus_g_plusplus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_plus_g_plusplus_button.setText("")
        self.together_d_plus_g_plusplus_button.setObjectName("together_d_plus_g_plusplus_button")
        self.gridLayout.addWidget(self.together_d_plus_g_plusplus_button, 7, 1, 1, 1)
        self.together_d_minusminus_g_plusplus_label = QtWidgets.QLabel(self.togetherTab)
        self.together_d_minusminus_g_plusplus_label.setObjectName("together_d_minusminus_g_plusplus_label")
        self.gridLayout.addWidget(self.together_d_minusminus_g_plusplus_label, 7, 2, 1, 1)
        self.together_d_minusminus_g_plusplus_button = QtWidgets.QPushButton(self.togetherTab)
        self.together_d_minusminus_g_plusplus_button.setText("")
        self.together_d_minusminus_g_plusplus_button.setObjectName("together_d_minusminus_g_plusplus_button")
        self.gridLayout.addWidget(self.together_d_minusminus_g_plusplus_button, 7, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.tabWidget.addTab(self.togetherTab, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(ColorsDialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(ColorsDialog)
        ColorsDialog.setTabOrder(self.tabWidget, self.alone_default_button)
        ColorsDialog.setTabOrder(self.alone_default_button, self.alone_d_plusplus_button)
        ColorsDialog.setTabOrder(self.alone_d_plusplus_button, self.alone_d_plus_button)
        ColorsDialog.setTabOrder(self.alone_d_plus_button, self.alone_d_minus_button)
        ColorsDialog.setTabOrder(self.alone_d_minus_button, self.alone_d_minusminus_button)
        ColorsDialog.setTabOrder(self.alone_d_minusminus_button, self.together_d_plusplus_g_minusminus_button)
        ColorsDialog.setTabOrder(self.together_d_plusplus_g_minusminus_button, self.together_d_plusplus_g_minus_button)
        ColorsDialog.setTabOrder(self.together_d_plusplus_g_minus_button, self.together_d_plusplus_g_plus_button)
        ColorsDialog.setTabOrder(self.together_d_plusplus_g_plus_button, self.together_d_plusplus_g_plusplus_button)
        ColorsDialog.setTabOrder(self.together_d_plusplus_g_plusplus_button, self.together_d_plus_g_minusminus_button)
        ColorsDialog.setTabOrder(self.together_d_plus_g_minusminus_button, self.together_d_plus_g_minus_button)
        ColorsDialog.setTabOrder(self.together_d_plus_g_minus_button, self.together_d_plus_g_plus_button)
        ColorsDialog.setTabOrder(self.together_d_plus_g_plus_button, self.together_d_plus_g_plusplus_button)
        ColorsDialog.setTabOrder(self.together_d_plus_g_plusplus_button, self.together_d_minus_g_minusminus_button)
        ColorsDialog.setTabOrder(self.together_d_minus_g_minusminus_button, self.together_d_minus_g_minus_button)
        ColorsDialog.setTabOrder(self.together_d_minus_g_minus_button, self.together_d_minus_g_plus_button)
        ColorsDialog.setTabOrder(self.together_d_minus_g_plus_button, self.together_d_minus_g_plusplus_button)
        ColorsDialog.setTabOrder(self.together_d_minus_g_plusplus_button, self.together_d_minusminus_g_minusminus_button)
        ColorsDialog.setTabOrder(self.together_d_minusminus_g_minusminus_button, self.together_d_minusminus_g_minus_button)
        ColorsDialog.setTabOrder(self.together_d_minusminus_g_minus_button, self.together_d_minusminus_g_plus_button)
        ColorsDialog.setTabOrder(self.together_d_minusminus_g_plus_button, self.together_d_minusminus_g_plusplus_button)
        ColorsDialog.setTabOrder(self.together_d_minusminus_g_plusplus_button, self.together_default_button)

    def retranslateUi(self, ColorsDialog):
        _translate = QtCore.QCoreApplication.translate
        ColorsDialog.setWindowTitle(_translate("ColorsDialog", "Dialog"))
        self.alone_default_label.setText(_translate("ColorsDialog", "Default color:"))
        self.alone_d_plusplus_label.setText(_translate("ColorsDialog", "SD++ or SG--:"))
        self.alone_d_plus_label.setText(_translate("ColorsDialog", "SD+ or SG-:"))
        self.alone_d_minus_label.setText(_translate("ColorsDialog", "SD- or SG+:"))
        self.alone_d_minusminus_label.setText(_translate("ColorsDialog", "SD-- or SG++:  "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.aloneTab), _translate("ColorsDialog", "SG or SD alone"))
        self.together_default_label.setText(_translate("ColorsDialog", "Default color:"))
        self.together_d_plusplus_g_minusminus_label.setText(_translate("ColorsDialog", "SD++;SG--:"))
        self.together_d_minus_g_minusminus_label.setText(_translate("ColorsDialog", "SD-;SG--:"))
        self.together_d_plusplus_g_minus_label.setText(_translate("ColorsDialog", "SD++;SG-:"))
        self.together_d_minus_g_minus_label.setText(_translate("ColorsDialog", "SD-;SG-:"))
        self.together_d_plusplus_g_plus_label.setText(_translate("ColorsDialog", "SD++;SG+:"))
        self.together_d_minus_g_plus_label.setText(_translate("ColorsDialog", "SD-;SG+:"))
        self.together_d_plusplus_g_plusplus_label.setText(_translate("ColorsDialog", "SD++;SG++:  "))
        self.together_d_minus_g_plusplus_label.setText(_translate("ColorsDialog", "SD-;SG++:  "))
        self.together_d_plus_g_minusminus_label.setText(_translate("ColorsDialog", "SD+;SG--:"))
        self.together_d_minusminus_g_minusminus_label.setText(_translate("ColorsDialog", "SD--;SG--:"))
        self.together_d_plus_g_minus_label.setText(_translate("ColorsDialog", "SD+;SG-:"))
        self.together_d_minusminus_g_minus_label.setText(_translate("ColorsDialog", "SD--;SG-:"))
        self.together_d_plus_g_plus_label.setText(_translate("ColorsDialog", "SD+;SG+:"))
        self.together_d_minusminus_g_plus_label.setText(_translate("ColorsDialog", "SD--;SG+:"))
        self.together_d_plus_g_plusplus_label.setText(_translate("ColorsDialog", "SD+;SG++:  "))
        self.together_d_minusminus_g_plusplus_label.setText(_translate("ColorsDialog", "SD--;SG++:  "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.togetherTab), _translate("ColorsDialog", "SG and SD together"))
