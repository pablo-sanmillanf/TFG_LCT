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
        ColorsDialog.resize(480, 340)
        self.verticalLayout = QtWidgets.QVBoxLayout(ColorsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self._tabWidget = QtWidgets.QTabWidget(ColorsDialog)
        self._tabWidget.setObjectName("_tabWidget")
        self._aloneTab = QtWidgets.QWidget()
        self._aloneTab.setObjectName("_aloneTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self._aloneTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self._formLayout = QtWidgets.QFormLayout()
        self._formLayout.setObjectName("_formLayout")
        self._alone_default_label = QtWidgets.QLabel(self._aloneTab)
        self._alone_default_label.setObjectName("_alone_default_label")
        self._formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._alone_default_label)
        self._alone_default_button = QtWidgets.QPushButton(self._aloneTab)
        self._alone_default_button.setText("")
        self._alone_default_button.setObjectName("_alone_default_button")
        self._formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self._alone_default_button)
        self._alone_d_plusplus_label = QtWidgets.QLabel(self._aloneTab)
        self._alone_d_plusplus_label.setObjectName("_alone_d_plusplus_label")
        self._formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._alone_d_plusplus_label)
        self._alone_d_plusplus_button = QtWidgets.QPushButton(self._aloneTab)
        self._alone_d_plusplus_button.setText("")
        self._alone_d_plusplus_button.setObjectName("_alone_d_plusplus_button")
        self._formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self._alone_d_plusplus_button)
        self._alone_d_plus_label = QtWidgets.QLabel(self._aloneTab)
        self._alone_d_plus_label.setObjectName("_alone_d_plus_label")
        self._formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._alone_d_plus_label)
        self._alone_d_plus_button = QtWidgets.QPushButton(self._aloneTab)
        self._alone_d_plus_button.setText("")
        self._alone_d_plus_button.setObjectName("_alone_d_plus_button")
        self._formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self._alone_d_plus_button)
        self._alone_d_minus_label = QtWidgets.QLabel(self._aloneTab)
        self._alone_d_minus_label.setObjectName("_alone_d_minus_label")
        self._formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self._alone_d_minus_label)
        self._alone_d_minus_button = QtWidgets.QPushButton(self._aloneTab)
        self._alone_d_minus_button.setText("")
        self._alone_d_minus_button.setObjectName("_alone_d_minus_button")
        self._formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self._alone_d_minus_button)
        self._alone_d_minusminus_label = QtWidgets.QLabel(self._aloneTab)
        self._alone_d_minusminus_label.setObjectName("_alone_d_minusminus_label")
        self._formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self._alone_d_minusminus_label)
        self._alone_d_minusminus_button = QtWidgets.QPushButton(self._aloneTab)
        self._alone_d_minusminus_button.setText("")
        self._alone_d_minusminus_button.setObjectName("_alone_d_minusminus_button")
        self._formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self._alone_d_minusminus_button)
        self.verticalLayout_2.addLayout(self._formLayout)
        self._tabWidget.addTab(self._aloneTab, "")
        self._togetherTab = QtWidgets.QWidget()
        self._togetherTab.setObjectName("_togetherTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self._togetherTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self._gridLayout_2 = QtWidgets.QGridLayout()
        self._gridLayout_2.setObjectName("_gridLayout_2")
        self._together_default_label = QtWidgets.QLabel(self._togetherTab)
        self._together_default_label.setObjectName("_together_default_label")
        self._gridLayout_2.addWidget(self._together_default_label, 1, 0, 1, 1)
        self._together_default_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_default_button.setText("")
        self._together_default_button.setObjectName("_together_default_button")
        self._gridLayout_2.addWidget(self._together_default_button, 1, 1, 1, 1)
        self._gridLayout = QtWidgets.QGridLayout()
        self._gridLayout.setObjectName("_gridLayout")
        self._together_d_plusplus_g_minusminus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_plusplus_g_minusminus_label.setObjectName("_together_d_plusplus_g_minusminus_label")
        self._gridLayout.addWidget(self._together_d_plusplus_g_minusminus_label, 0, 0, 1, 1)
        self._together_d_plusplus_g_minusminus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_plusplus_g_minusminus_button.setText("")
        self._together_d_plusplus_g_minusminus_button.setObjectName("_together_d_plusplus_g_minusminus_button")
        self._gridLayout.addWidget(self._together_d_plusplus_g_minusminus_button, 0, 1, 1, 1)
        self._together_d_minus_g_minusminus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_minus_g_minusminus_label.setObjectName("_together_d_minus_g_minusminus_label")
        self._gridLayout.addWidget(self._together_d_minus_g_minusminus_label, 0, 2, 1, 1)
        self._together_d_minus_g_minusminus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_minus_g_minusminus_button.setText("")
        self._together_d_minus_g_minusminus_button.setObjectName("_together_d_minus_g_minusminus_button")
        self._gridLayout.addWidget(self._together_d_minus_g_minusminus_button, 0, 3, 1, 1)
        self._together_d_plusplus_g_minus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_plusplus_g_minus_label.setObjectName("_together_d_plusplus_g_minus_label")
        self._gridLayout.addWidget(self._together_d_plusplus_g_minus_label, 1, 0, 1, 1)
        self._together_d_plusplus_g_minus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_plusplus_g_minus_button.setText("")
        self._together_d_plusplus_g_minus_button.setObjectName("_together_d_plusplus_g_minus_button")
        self._gridLayout.addWidget(self._together_d_plusplus_g_minus_button, 1, 1, 1, 1)
        self._together_d_minus_g_minus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_minus_g_minus_label.setObjectName("_together_d_minus_g_minus_label")
        self._gridLayout.addWidget(self._together_d_minus_g_minus_label, 1, 2, 1, 1)
        self._together_d_minus_g_minus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_minus_g_minus_button.setText("")
        self._together_d_minus_g_minus_button.setObjectName("_together_d_minus_g_minus_button")
        self._gridLayout.addWidget(self._together_d_minus_g_minus_button, 1, 3, 1, 1)
        self._together_d_plusplus_g_plus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_plusplus_g_plus_label.setObjectName("_together_d_plusplus_g_plus_label")
        self._gridLayout.addWidget(self._together_d_plusplus_g_plus_label, 2, 0, 1, 1)
        self._together_d_plusplus_g_plus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_plusplus_g_plus_button.setText("")
        self._together_d_plusplus_g_plus_button.setObjectName("_together_d_plusplus_g_plus_button")
        self._gridLayout.addWidget(self._together_d_plusplus_g_plus_button, 2, 1, 1, 1)
        self._together_d_minus_g_plus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_minus_g_plus_label.setObjectName("_together_d_minus_g_plus_label")
        self._gridLayout.addWidget(self._together_d_minus_g_plus_label, 2, 2, 1, 1)
        self._together_d_minus_g_plus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_minus_g_plus_button.setText("")
        self._together_d_minus_g_plus_button.setObjectName("_together_d_minus_g_plus_button")
        self._gridLayout.addWidget(self._together_d_minus_g_plus_button, 2, 3, 1, 1)
        self._together_d_plusplus_g_plusplus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_plusplus_g_plusplus_label.setObjectName("_together_d_plusplus_g_plusplus_label")
        self._gridLayout.addWidget(self._together_d_plusplus_g_plusplus_label, 3, 0, 1, 1)
        self._together_d_plusplus_g_plusplus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_plusplus_g_plusplus_button.setText("")
        self._together_d_plusplus_g_plusplus_button.setObjectName("_together_d_plusplus_g_plusplus_button")
        self._gridLayout.addWidget(self._together_d_plusplus_g_plusplus_button, 3, 1, 1, 1)
        self._together_d_minus_g_plusplus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_minus_g_plusplus_label.setObjectName("_together_d_minus_g_plusplus_label")
        self._gridLayout.addWidget(self._together_d_minus_g_plusplus_label, 3, 2, 1, 1)
        self._together_d_minus_g_plusplus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_minus_g_plusplus_button.setText("")
        self._together_d_minus_g_plusplus_button.setObjectName("_together_d_minus_g_plusplus_button")
        self._gridLayout.addWidget(self._together_d_minus_g_plusplus_button, 3, 3, 1, 1)
        self._together_d_plus_g_minusminus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_plus_g_minusminus_label.setObjectName("_together_d_plus_g_minusminus_label")
        self._gridLayout.addWidget(self._together_d_plus_g_minusminus_label, 4, 0, 1, 1)
        self._together_d_plus_g_minusminus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_plus_g_minusminus_button.setText("")
        self._together_d_plus_g_minusminus_button.setObjectName("_together_d_plus_g_minusminus_button")
        self._gridLayout.addWidget(self._together_d_plus_g_minusminus_button, 4, 1, 1, 1)
        self._together_d_minusminus_g_minusminus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_minusminus_g_minusminus_label.setObjectName("_together_d_minusminus_g_minusminus_label")
        self._gridLayout.addWidget(self._together_d_minusminus_g_minusminus_label, 4, 2, 1, 1)
        self._together_d_minusminus_g_minusminus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_minusminus_g_minusminus_button.setText("")
        self._together_d_minusminus_g_minusminus_button.setObjectName("_together_d_minusminus_g_minusminus_button")
        self._gridLayout.addWidget(self._together_d_minusminus_g_minusminus_button, 4, 3, 1, 1)
        self._together_d_plus_g_minus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_plus_g_minus_label.setObjectName("_together_d_plus_g_minus_label")
        self._gridLayout.addWidget(self._together_d_plus_g_minus_label, 5, 0, 1, 1)
        self._together_d_plus_g_minus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_plus_g_minus_button.setText("")
        self._together_d_plus_g_minus_button.setObjectName("_together_d_plus_g_minus_button")
        self._gridLayout.addWidget(self._together_d_plus_g_minus_button, 5, 1, 1, 1)
        self._together_d_minusminus_g_minus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_minusminus_g_minus_label.setObjectName("_together_d_minusminus_g_minus_label")
        self._gridLayout.addWidget(self._together_d_minusminus_g_minus_label, 5, 2, 1, 1)
        self._together_d_minusminus_g_minus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_minusminus_g_minus_button.setText("")
        self._together_d_minusminus_g_minus_button.setObjectName("_together_d_minusminus_g_minus_button")
        self._gridLayout.addWidget(self._together_d_minusminus_g_minus_button, 5, 3, 1, 1)
        self._together_d_plus_g_plus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_plus_g_plus_label.setObjectName("_together_d_plus_g_plus_label")
        self._gridLayout.addWidget(self._together_d_plus_g_plus_label, 6, 0, 1, 1)
        self._together_d_plus_g_plus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_plus_g_plus_button.setText("")
        self._together_d_plus_g_plus_button.setObjectName("_together_d_plus_g_plus_button")
        self._gridLayout.addWidget(self._together_d_plus_g_plus_button, 6, 1, 1, 1)
        self._together_d_minusminus_g_plus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_minusminus_g_plus_label.setObjectName("_together_d_minusminus_g_plus_label")
        self._gridLayout.addWidget(self._together_d_minusminus_g_plus_label, 6, 2, 1, 1)
        self._together_d_minusminus_g_plus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_minusminus_g_plus_button.setText("")
        self._together_d_minusminus_g_plus_button.setObjectName("_together_d_minusminus_g_plus_button")
        self._gridLayout.addWidget(self._together_d_minusminus_g_plus_button, 6, 3, 1, 1)
        self._together_d_plus_g_plusplus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_plus_g_plusplus_label.setObjectName("_together_d_plus_g_plusplus_label")
        self._gridLayout.addWidget(self._together_d_plus_g_plusplus_label, 7, 0, 1, 1)
        self._together_d_plus_g_plusplus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_plus_g_plusplus_button.setText("")
        self._together_d_plus_g_plusplus_button.setObjectName("_together_d_plus_g_plusplus_button")
        self._gridLayout.addWidget(self._together_d_plus_g_plusplus_button, 7, 1, 1, 1)
        self._together_d_minusminus_g_plusplus_label = QtWidgets.QLabel(self._togetherTab)
        self._together_d_minusminus_g_plusplus_label.setObjectName("_together_d_minusminus_g_plusplus_label")
        self._gridLayout.addWidget(self._together_d_minusminus_g_plusplus_label, 7, 2, 1, 1)
        self._together_d_minusminus_g_plusplus_button = QtWidgets.QPushButton(self._togetherTab)
        self._together_d_minusminus_g_plusplus_button.setText("")
        self._together_d_minusminus_g_plusplus_button.setObjectName("_together_d_minusminus_g_plusplus_button")
        self._gridLayout.addWidget(self._together_d_minusminus_g_plusplus_button, 7, 3, 1, 1)
        self._gridLayout_2.addLayout(self._gridLayout, 0, 0, 1, 2)
        self.verticalLayout_3.addLayout(self._gridLayout_2)
        self._tabWidget.addTab(self._togetherTab, "")
        self.verticalLayout.addWidget(self._tabWidget)

        self.retranslateUi(ColorsDialog)
        self._tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(ColorsDialog)
        ColorsDialog.setTabOrder(self._tabWidget, self._alone_default_button)
        ColorsDialog.setTabOrder(self._alone_default_button, self._alone_d_plusplus_button)
        ColorsDialog.setTabOrder(self._alone_d_plusplus_button, self._alone_d_plus_button)
        ColorsDialog.setTabOrder(self._alone_d_plus_button, self._alone_d_minus_button)
        ColorsDialog.setTabOrder(self._alone_d_minus_button, self._alone_d_minusminus_button)
        ColorsDialog.setTabOrder(self._alone_d_minusminus_button, self._together_d_plusplus_g_minusminus_button)
        ColorsDialog.setTabOrder(self._together_d_plusplus_g_minusminus_button, self._together_d_plusplus_g_minus_button)
        ColorsDialog.setTabOrder(self._together_d_plusplus_g_minus_button, self._together_d_plusplus_g_plus_button)
        ColorsDialog.setTabOrder(self._together_d_plusplus_g_plus_button, self._together_d_plusplus_g_plusplus_button)
        ColorsDialog.setTabOrder(self._together_d_plusplus_g_plusplus_button, self._together_d_plus_g_minusminus_button)
        ColorsDialog.setTabOrder(self._together_d_plus_g_minusminus_button, self._together_d_plus_g_minus_button)
        ColorsDialog.setTabOrder(self._together_d_plus_g_minus_button, self._together_d_plus_g_plus_button)
        ColorsDialog.setTabOrder(self._together_d_plus_g_plus_button, self._together_d_plus_g_plusplus_button)
        ColorsDialog.setTabOrder(self._together_d_plus_g_plusplus_button, self._together_d_minus_g_minusminus_button)
        ColorsDialog.setTabOrder(self._together_d_minus_g_minusminus_button, self._together_d_minus_g_minus_button)
        ColorsDialog.setTabOrder(self._together_d_minus_g_minus_button, self._together_d_minus_g_plus_button)
        ColorsDialog.setTabOrder(self._together_d_minus_g_plus_button, self._together_d_minus_g_plusplus_button)
        ColorsDialog.setTabOrder(self._together_d_minus_g_plusplus_button, self._together_d_minusminus_g_minusminus_button)
        ColorsDialog.setTabOrder(self._together_d_minusminus_g_minusminus_button, self._together_d_minusminus_g_minus_button)
        ColorsDialog.setTabOrder(self._together_d_minusminus_g_minus_button, self._together_d_minusminus_g_plus_button)
        ColorsDialog.setTabOrder(self._together_d_minusminus_g_plus_button, self._together_d_minusminus_g_plusplus_button)
        ColorsDialog.setTabOrder(self._together_d_minusminus_g_plusplus_button, self._together_default_button)

    def retranslateUi(self, ColorsDialog):
        _translate = QtCore.QCoreApplication.translate
        ColorsDialog.setWindowTitle(_translate("ColorsDialog", "Rectangles Colors"))
        self._alone_default_label.setText(_translate("ColorsDialog", "Default color:"))
        self._alone_d_plusplus_label.setText(_translate("ColorsDialog", "SD++ or SG--:"))
        self._alone_d_plus_label.setText(_translate("ColorsDialog", "SD+ or SG-:"))
        self._alone_d_minus_label.setText(_translate("ColorsDialog", "SD- or SG+:"))
        self._alone_d_minusminus_label.setText(_translate("ColorsDialog", "SD-- or SG++:  "))
        self._tabWidget.setTabText(self._tabWidget.indexOf(self._aloneTab), _translate("ColorsDialog", "SG or SD alone"))
        self._together_default_label.setText(_translate("ColorsDialog", "Default color:"))
        self._together_d_plusplus_g_minusminus_label.setText(_translate("ColorsDialog", "SD++;SG--:"))
        self._together_d_minus_g_minusminus_label.setText(_translate("ColorsDialog", "SD-;SG--:"))
        self._together_d_plusplus_g_minus_label.setText(_translate("ColorsDialog", "SD++;SG-:"))
        self._together_d_minus_g_minus_label.setText(_translate("ColorsDialog", "SD-;SG-:"))
        self._together_d_plusplus_g_plus_label.setText(_translate("ColorsDialog", "SD++;SG+:"))
        self._together_d_minus_g_plus_label.setText(_translate("ColorsDialog", "SD-;SG+:"))
        self._together_d_plusplus_g_plusplus_label.setText(_translate("ColorsDialog", "SD++;SG++:  "))
        self._together_d_minus_g_plusplus_label.setText(_translate("ColorsDialog", "SD-;SG++:  "))
        self._together_d_plus_g_minusminus_label.setText(_translate("ColorsDialog", "SD+;SG--:"))
        self._together_d_minusminus_g_minusminus_label.setText(_translate("ColorsDialog", "SD--;SG--:"))
        self._together_d_plus_g_minus_label.setText(_translate("ColorsDialog", "SD+;SG-:"))
        self._together_d_minusminus_g_minus_label.setText(_translate("ColorsDialog", "SD--;SG-:"))
        self._together_d_plus_g_plus_label.setText(_translate("ColorsDialog", "SD+;SG+:"))
        self._together_d_minusminus_g_plus_label.setText(_translate("ColorsDialog", "SD--;SG+:"))
        self._together_d_plus_g_plusplus_label.setText(_translate("ColorsDialog", "SD+;SG++:  "))
        self._together_d_minusminus_g_plusplus_label.setText(_translate("ColorsDialog", "SD--;SG++:  "))
        self._tabWidget.setTabText(self._tabWidget.indexOf(self._togetherTab), _translate("ColorsDialog", "SG and SD together"))
