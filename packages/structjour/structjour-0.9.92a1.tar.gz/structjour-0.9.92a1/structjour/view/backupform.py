# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\backupform.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(866, 332)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(33, 34, 713, 233))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.backup = QtWidgets.QPushButton(self.widget)
        self.backup.setObjectName("backup")
        self.horizontalLayout_4.addWidget(self.backup)
        spacerItem = QtWidgets.QSpacerItem(588, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.restore = QtWidgets.QPushButton(self.widget)
        self.restore.setObjectName("restore")
        self.horizontalLayout_3.addWidget(self.restore)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.select_recent = QtWidgets.QPushButton(self.widget)
        self.select_recent.setObjectName("select_recent")
        self.horizontalLayout.addWidget(self.select_recent)
        spacerItem1 = QtWidgets.QSpacerItem(138, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.avail_backups = QtWidgets.QComboBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(255)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.avail_backups.sizePolicy().hasHeightForWidth())
        self.avail_backups.setSizePolicy(sizePolicy)
        self.avail_backups.setMinimumSize(QtCore.QSize(300, 0))
        self.avail_backups.setObjectName("avail_backups")
        self.verticalLayout.addWidget(self.avail_backups)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.backup_files = QtWidgets.QListWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(255)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backup_files.sizePolicy().hasHeightForWidth())
        self.backup_files.setSizePolicy(sizePolicy)
        self.backup_files.setMinimumSize(QtCore.QSize(300, 0))
        self.backup_files.setMaximumSize(QtCore.QSize(16777215, 100))
        self.backup_files.setObjectName("backup_files")
        self.horizontalLayout_3.addWidget(self.backup_files)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 48, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.init_settings = QtWidgets.QPushButton(self.widget)
        self.init_settings.setObjectName("init_settings")
        self.horizontalLayout_2.addWidget(self.init_settings)
        self.label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.backup.setToolTip(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt; color:#0633c6;\">Backup setting and database</span></p></body></html>"))
        self.backup.setText(_translate("Dialog", "Backup"))
        self.restore.setToolTip(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt; color:#0633c6;\">Restore settings and database from a previous backup</span></p></body></html>"))
        self.restore.setText(_translate("Dialog", "Restore"))
        self.select_recent.setText(_translate("Dialog", "Select most recent"))
        self.avail_backups.setToolTip(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt; color:#0633c6;\">Available backups to restore from.</span></p></body></html>"))
        self.backup_files.setToolTip(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt; color:#0633c6;\">The backup files for the selected backup.</span></p></body></html>"))
        self.init_settings.setText(_translate("Dialog", "Initialize Settings"))
        self.label.setText(_translate("Dialog", "This will clear all settings except for the setting of the journal directory."))
