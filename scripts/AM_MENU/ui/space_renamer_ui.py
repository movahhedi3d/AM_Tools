from AM_MENU.extensions.Qt  import QtWidgets , QtGui , QtCore

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(188, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.renamerTable = QtWidgets.QTableWidget(Dialog)
        self.renamerTable.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.renamerTable.setGridStyle(QtCore.Qt.SolidLine)
        self.renamerTable.setRowCount(1)
        self.renamerTable.setColumnCount(1)
        self.renamerTable.setObjectName("renamerTable")
        self.renamerTable.setColumnCount(1)
        self.renamerTable.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.renamerTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.renamerTable.setItem(0, 0, item)
        self.renamerTable.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.renamerTable)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.renamerTable.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("Dialog", "space name", None, -1))
        __sortingEnabled = self.renamerTable.isSortingEnabled()
        self.renamerTable.setSortingEnabled(False)
        self.renamerTable.item(0, 0).setText(QtWidgets.QApplication.translate("Dialog", "None", None, -1))
        self.renamerTable.setSortingEnabled(__sortingEnabled)

