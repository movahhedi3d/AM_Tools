from AM_MENU.extensions.Qt  import QtWidgets , QtGui , QtCore

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(261, 224)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.current_key_label = QtWidgets.QLabel(Dialog)
        self.current_key_label.setMinimumSize(QtCore.QSize(70, 0))
        self.current_key_label.setText("")
        self.current_key_label.setObjectName("current_key_label")
        self.horizontalLayout_3.addWidget(self.current_key_label)
        self.remove_btn = QtWidgets.QPushButton(Dialog)
        self.remove_btn.setObjectName("remove_btn")
        self.horizontalLayout_3.addWidget(self.remove_btn)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.hotKey_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.hotKey_lineEdit.setObjectName("hotKey_lineEdit")
        self.verticalLayout_2.addWidget(self.hotKey_lineEdit)
        self.shift_chb = QtWidgets.QCheckBox(Dialog)
        self.shift_chb.setObjectName("shift_chb")
        self.verticalLayout_2.addWidget(self.shift_chb)
        self.ctrl_chb = QtWidgets.QCheckBox(Dialog)
        self.ctrl_chb.setObjectName("ctrl_chb")
        self.verticalLayout_2.addWidget(self.ctrl_chb)
        self.alt_chb = QtWidgets.QCheckBox(Dialog)
        self.alt_chb.setObjectName("alt_chb")
        self.verticalLayout_2.addWidget(self.alt_chb)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.ok_btn = QtWidgets.QPushButton(Dialog)
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout.addWidget(self.ok_btn)
        self.close_btn = QtWidgets.QPushButton(Dialog)
        self.close_btn.setObjectName("close_btn")
        self.horizontalLayout.addWidget(self.close_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "Current Hotkey : ", None, -1))
        self.remove_btn.setText(QtWidgets.QApplication.translate("Dialog", "Remove", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Enter the hotkey for the marking menu", None, -1))
        self.shift_chb.setText(QtWidgets.QApplication.translate("Dialog", "Shift", None, -1))
        self.ctrl_chb.setText(QtWidgets.QApplication.translate("Dialog", "Ctrl", None, -1))
        self.alt_chb.setText(QtWidgets.QApplication.translate("Dialog", "Alt", None, -1))
        self.ok_btn.setText(QtWidgets.QApplication.translate("Dialog", "OK", None, -1))
        self.close_btn.setText(QtWidgets.QApplication.translate("Dialog", "Close", None, -1))

