# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:/maya/CODE/PERSONAL/AmPakage/scripts/AM_Tools/scripts/AM_MENU/ui/space_initializer_ui.ui',
# licensing of 'F:/maya/CODE/PERSONAL/AmPakage/scripts/AM_Tools/scripts/AM_MENU/ui/space_initializer_ui.ui' applies.
#
# Created: Sun Jan 16 14:01:31 2022
#      by: pyside2-uic  running on PySide2 5.12.5
#
# WARNING! All changes made in this file will be lost!

from AM_MENU.extensions.Qt  import QtWidgets , QtGui , QtCore

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(327, 185)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.by_constraint_rb = QtWidgets.QRadioButton(self.groupBox)
        self.by_constraint_rb.setChecked(True)
        self.by_constraint_rb.setObjectName("by_constraint_rb")
        self.verticalLayout_2.addWidget(self.by_constraint_rb)
        self.by_blnd_rb = QtWidgets.QRadioButton(self.groupBox)
        self.by_blnd_rb.setObjectName("by_blnd_rb")
        self.verticalLayout_2.addWidget(self.by_blnd_rb)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.useTrans_chb = QtWidgets.QCheckBox(Dialog)
        self.useTrans_chb.setChecked(True)
        self.useTrans_chb.setObjectName("useTrans_chb")
        self.verticalLayout.addWidget(self.useTrans_chb)
        self.useRotate_chb = QtWidgets.QCheckBox(Dialog)
        self.useRotate_chb.setChecked(True)
        self.useRotate_chb.setObjectName("useRotate_chb")
        self.verticalLayout.addWidget(self.useRotate_chb)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("Dialog", "Driver Node", None, -1))
        self.by_constraint_rb.setText(QtWidgets.QApplication.translate("Dialog", "Parent Constraint", None, -1))
        self.by_blnd_rb.setText(QtWidgets.QApplication.translate("Dialog", "Blend Matrix [ just available for maya 2020 and higher ]", None, -1))
        self.useTrans_chb.setText(QtWidgets.QApplication.translate("Dialog", "Use Translate", None, -1))
        self.useRotate_chb.setText(QtWidgets.QApplication.translate("Dialog", "Use Rotation", None, -1))

