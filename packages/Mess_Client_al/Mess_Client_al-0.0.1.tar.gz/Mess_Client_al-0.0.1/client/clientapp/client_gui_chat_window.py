# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_gui_chat_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(675, 499)
        Dialog.setToolTip("")
        self.list_contacts = QtWidgets.QListWidget(Dialog)
        self.list_contacts.setGeometry(QtCore.QRect(10, 10, 251, 361))
        self.list_contacts.setObjectName("list_contacts")
        self.list_msgs = QtWidgets.QListWidget(Dialog)
        self.list_msgs.setGeometry(QtCore.QRect(270, 10, 391, 301))
        self.list_msgs.setObjectName("list_msgs")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(590, 330, 71, 71))
        self.pushButton.setObjectName("pushButton")
        self.text_new_msg = QtWidgets.QTextEdit(Dialog)
        self.text_new_msg.setGeometry(QtCore.QRect(270, 320, 311, 91))
        self.text_new_msg.setObjectName("text_new_msg")
        self.line_find_contact = QtWidgets.QLineEdit(Dialog)
        self.line_find_contact.setGeometry(QtCore.QRect(10, 380, 251, 31))
        self.line_find_contact.setText("")
        self.line_find_contact.setObjectName("line_find_contact")
        self.list_add_contact = QtWidgets.QListWidget(Dialog)
        self.list_add_contact.setGeometry(QtCore.QRect(10, 420, 251, 71))
        self.list_add_contact.setObjectName("list_add_contact")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Отправить"))
        self.line_find_contact.setPlaceholderText(_translate("Dialog", "Введите имя пользователя"))
        self.list_add_contact.setToolTip(_translate("Dialog", "Для добавления пользователя дважды кликните по его имени"))
