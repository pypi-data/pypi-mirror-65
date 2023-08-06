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
        Form.resize(578, 340)
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
        self.motives = QtWidgets.QWidget(Form)
        self.motives.setObjectName("motives")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.motives)
        self.verticalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.travail = QtWidgets.QPushButton(self.motives)
        self.travail.setObjectName("travail")
        self.verticalLayout_2.addWidget(self.travail)
        self.courses = QtWidgets.QPushButton(self.motives)
        self.courses.setAutoDefault(True)
        self.courses.setDefault(True)
        self.courses.setObjectName("courses")
        self.verticalLayout_2.addWidget(self.courses)
        self.sante = QtWidgets.QPushButton(self.motives)
        self.sante.setObjectName("sante")
        self.verticalLayout_2.addWidget(self.sante)
        self.famille = QtWidgets.QPushButton(self.motives)
        self.famille.setObjectName("famille")
        self.verticalLayout_2.addWidget(self.famille)
        self.sport = QtWidgets.QPushButton(self.motives)
        self.sport.setObjectName("sport")
        self.verticalLayout_2.addWidget(self.sport)
        self.judiciaire = QtWidgets.QPushButton(self.motives)
        self.judiciaire.setObjectName("judiciaire")
        self.verticalLayout_2.addWidget(self.judiciaire)
        self.missions = QtWidgets.QPushButton(self.motives)
        self.missions.setObjectName("missions")
        self.verticalLayout_2.addWidget(self.missions)
        self.verticalLayout.addWidget(self.motives)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.travail, self.courses)
        Form.setTabOrder(self.courses, self.sante)
        Form.setTabOrder(self.sante, self.famille)
        Form.setTabOrder(self.famille, self.sport)
        Form.setTabOrder(self.sport, self.judiciaire)
        Form.setTabOrder(self.judiciaire, self.missions)
        Form.setTabOrder(self.missions, self.peopleBox)
        Form.setTabOrder(self.peopleBox, self.addPeople)
        Form.setTabOrder(self.addPeople, self.delPeople)
        Form.setTabOrder(self.delPeople, self.confButton)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Attestation Covid-19"))
        self.addPeople.setText(_translate("Form", "+"))
        self.delPeople.setText(_translate("Form", "-"))
        self.confButton.setText(_translate("Form", "C"))
        self.travail.setText(_translate("Form", "Pour aller au travail"))
        self.courses.setText(_translate("Form", "Pour aller faire les courses"))
        self.sante.setText(_translate("Form", "Pour aller dans un établissement médical"))
        self.famille.setText(_translate("Form", "Pour aller voir la famille en difficulté"))
        self.sport.setText(_translate("Form", "Pour pratiquer une activité physique ou une promenade"))
        self.judiciaire.setText(_translate("Form", "Pour répondre à une convocation administrative ou judiciaire"))
        self.missions.setText(_translate("Form", "Pour une mission d\'intérêt général"))
