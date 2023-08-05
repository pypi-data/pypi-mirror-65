# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(578, 328)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.peopleBox = QtWidgets.QComboBox(Form)
        self.peopleBox.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        self.peopleBox.setObjectName("peopleBox")
        self.horizontalLayout.addWidget(self.peopleBox)
        self.addPeople = QtWidgets.QToolButton(Form)
        self.addPeople.setObjectName("addPeople")
        self.horizontalLayout.addWidget(self.addPeople)
        self.delPeople = QtWidgets.QToolButton(Form)
        self.delPeople.setObjectName("delPeople")
        self.horizontalLayout.addWidget(self.delPeople)
        self.confButton = QtWidgets.QToolButton(Form)
        self.confButton.setObjectName("confButton")
        self.horizontalLayout.addWidget(self.confButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.work = QtWidgets.QPushButton(Form)
        self.work.setObjectName("work")
        self.verticalLayout.addWidget(self.work)
        self.shopping = QtWidgets.QPushButton(Form)
        self.shopping.setAutoDefault(True)
        self.shopping.setDefault(True)
        self.shopping.setObjectName("shopping")
        self.verticalLayout.addWidget(self.shopping)
        self.health = QtWidgets.QPushButton(Form)
        self.health.setObjectName("health")
        self.verticalLayout.addWidget(self.health)
        self.family = QtWidgets.QPushButton(Form)
        self.family.setObjectName("family")
        self.verticalLayout.addWidget(self.family)
        self.walk = QtWidgets.QPushButton(Form)
        self.walk.setObjectName("walk")
        self.verticalLayout.addWidget(self.walk)
        self.police = QtWidgets.QPushButton(Form)
        self.police.setObjectName("police")
        self.verticalLayout.addWidget(self.police)
        self.collective = QtWidgets.QPushButton(Form)
        self.collective.setObjectName("collective")
        self.verticalLayout.addWidget(self.collective)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.peopleBox, self.work)
        Form.setTabOrder(self.work, self.shopping)
        Form.setTabOrder(self.shopping, self.health)
        Form.setTabOrder(self.health, self.family)
        Form.setTabOrder(self.family, self.walk)
        Form.setTabOrder(self.walk, self.police)
        Form.setTabOrder(self.police, self.collective)
        Form.setTabOrder(self.collective, self.addPeople)
        Form.setTabOrder(self.addPeople, self.delPeople)
        Form.setTabOrder(self.delPeople, self.confButton)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Attestation Covid-19"))
        self.addPeople.setText(_translate("Form", "+"))
        self.delPeople.setText(_translate("Form", "-"))
        self.confButton.setText(_translate("Form", "C"))
        self.work.setText(_translate("Form", "Pour aller au travail"))
        self.shopping.setText(_translate("Form", "Pour aller faire les courses"))
        self.health.setText(_translate("Form", "Pour aller dans un établissement médical"))
        self.family.setText(_translate("Form", "Pour aller voir la famille en difficulté"))
        self.walk.setText(_translate("Form", "Pour pratiquer une activité physique ou une promenade"))
        self.police.setText(_translate("Form", "Pour répondre à une convocation administrative ou judiciaire"))
        self.collective.setText(_translate("Form", "Pour une mission d\'intérêt général"))
