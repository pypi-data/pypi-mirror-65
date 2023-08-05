# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plover_vcs/ui/vcs_settings.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VcsSettings(object):
    def setupUi(self, VcsSettings):
        VcsSettings.setObjectName("VcsSettings")
        VcsSettings.resize(396, 281)
        VcsSettings.setSizeGripEnabled(False)
        self.buttonBox = QtWidgets.QDialogButtonBox(VcsSettings)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(VcsSettings)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 377, 231))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.settingsForm = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.settingsForm.setContentsMargins(0, 0, 0, 0)
        self.settingsForm.setObjectName("settingsForm")
        self.versionControlSystemLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.versionControlSystemLabel.setObjectName("versionControlSystemLabel")
        self.settingsForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.versionControlSystemLabel)
        self.versionControlSystemComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.versionControlSystemComboBox.setObjectName("versionControlSystemComboBox")
        self.versionControlSystemComboBox.addItem("")
        self.settingsForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.versionControlSystemComboBox)
        self.dictionariesLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.dictionariesLabel.setObjectName("dictionariesLabel")
        self.settingsForm.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.dictionariesLabel)
        self.dictionaryListLayout = QtWidgets.QVBoxLayout()
        self.dictionaryListLayout.setObjectName("dictionaryListLayout")
        self.dictionariesListWidget = QtWidgets.QListWidget(self.formLayoutWidget)
        self.dictionariesListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.dictionariesListWidget.setObjectName("dictionariesListWidget")
        self.dictionaryListLayout.addWidget(self.dictionariesListWidget)
        self.dictionaryListControlsLayout = QtWidgets.QHBoxLayout()
        self.dictionaryListControlsLayout.setObjectName("dictionaryListControlsLayout")
        self.addDictionaryButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.addDictionaryButton.setObjectName("addDictionaryButton")
        self.dictionaryListControlsLayout.addWidget(self.addDictionaryButton)
        self.removeDictionaryButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.removeDictionaryButton.setObjectName("removeDictionaryButton")
        self.dictionaryListControlsLayout.addWidget(self.removeDictionaryButton)
        self.dictionaryListLayout.addLayout(self.dictionaryListControlsLayout)
        self.settingsForm.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.dictionaryListLayout)

        self.retranslateUi(VcsSettings)
        self.addDictionaryButton.clicked.connect(VcsSettings.add_dictionary)
        self.removeDictionaryButton.clicked.connect(VcsSettings.remove_dictionary)
        self.buttonBox.accepted.connect(VcsSettings.accept)
        self.buttonBox.rejected.connect(VcsSettings.reject)
        self.dictionariesListWidget.itemDoubleClicked['QListWidgetItem*'].connect(VcsSettings.edit_dictionary)
        QtCore.QMetaObject.connectSlotsByName(VcsSettings)

    def retranslateUi(self, VcsSettings):
        _translate = QtCore.QCoreApplication.translate
        VcsSettings.setWindowTitle(_translate("VcsSettings", "VCS Settings"))
        self.versionControlSystemLabel.setText(_translate("VcsSettings", "Version Control System"))
        self.versionControlSystemComboBox.setItemText(0, _translate("VcsSettings", "Git"))
        self.dictionariesLabel.setText(_translate("VcsSettings", "Dictionaries"))
        self.addDictionaryButton.setText(_translate("VcsSettings", "Add Dictionary"))
        self.removeDictionaryButton.setText(_translate("VcsSettings", "Remove Selected"))
