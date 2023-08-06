# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientapp\client_gui_login.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_login(object):
    def setupUi(self, Dialog_login):
        Dialog_login.setObjectName("Dialog_login")
        Dialog_login.resize(342, 255)
        self.label_login = QtWidgets.QLabel(Dialog_login)
        self.label_login.setGeometry(QtCore.QRect(26, 50, 71, 31))
        self.label_login.setObjectName("label_login")
        self.line_login = QtWidgets.QLineEdit(Dialog_login)
        self.line_login.setGeometry(QtCore.QRect(110, 50, 191, 31))
        self.line_login.setObjectName("line_login")
        self.label_password = QtWidgets.QLabel(Dialog_login)
        self.label_password.setGeometry(QtCore.QRect(26, 100, 71, 31))
        self.label_password.setObjectName("label_password")
        self.line_password = QtWidgets.QLineEdit(Dialog_login)
        self.line_password.setGeometry(QtCore.QRect(110, 100, 191, 31))
        self.line_password.setObjectName("line_password")
        self.button_ok_login = QtWidgets.QPushButton(Dialog_login)
        self.button_ok_login.setGeometry(QtCore.QRect(170, 190, 131, 51))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.button_ok_login.setFont(font)
        self.button_ok_login.setAccessibleName("")
        self.button_ok_login.setObjectName("button_ok_login")
        self.label_error = QtWidgets.QLabel(Dialog_login)
        self.label_error.setGeometry(QtCore.QRect(36, 10, 261, 21))
        self.label_error.setText("")
        self.label_error.setObjectName("label_error")
        self.button_registration = QtWidgets.QPushButton(Dialog_login)
        self.button_registration.setGeometry(QtCore.QRect(30, 190, 131, 51))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.button_registration.setFont(font)
        self.button_registration.setAccessibleName("")
        self.button_registration.setObjectName("button_registration")
        self.line_password_2 = QtWidgets.QLineEdit(Dialog_login)
        self.line_password_2.setGeometry(QtCore.QRect(110, 150, 191, 31))
        self.line_password_2.setObjectName("line_password_2")

        self.retranslateUi(Dialog_login)
        QtCore.QMetaObject.connectSlotsByName(Dialog_login)

    def retranslateUi(self, Dialog_login):
        _translate = QtCore.QCoreApplication.translate
        Dialog_login.setWindowTitle(_translate("Dialog_login", "Dialog"))
        self.label_login.setText(_translate("Dialog_login", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Логин</span></p></body></html>"))
        self.label_password.setText(_translate("Dialog_login", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Пароль</span></p></body></html>"))
        self.button_ok_login.setText(_translate("Dialog_login", "Подключиться"))
        self.button_registration.setText(_translate("Dialog_login", "Зарегистрироваться"))
