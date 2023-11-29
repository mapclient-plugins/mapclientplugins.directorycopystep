# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuredialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_ConfigureDialog(object):
    def setupUi(self, ConfigureDialog):
        if not ConfigureDialog.objectName():
            ConfigureDialog.setObjectName(u"ConfigureDialog")
        ConfigureDialog.resize(418, 303)
        self.gridLayout = QGridLayout(ConfigureDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.configGroupBox = QGroupBox(ConfigureDialog)
        self.configGroupBox.setObjectName(u"configGroupBox")
        self.formLayout = QFormLayout(self.configGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.labelIdentifier = QLabel(self.configGroupBox)
        self.labelIdentifier.setObjectName(u"labelIdentifier")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelIdentifier)

        self.lineEditIdentifier = QLineEdit(self.configGroupBox)
        self.lineEditIdentifier.setObjectName(u"lineEditIdentifier")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEditIdentifier)

        self.labelDirectory = QLabel(self.configGroupBox)
        self.labelDirectory.setObjectName(u"labelDirectory")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelDirectory)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditDirectoryLocation = QLineEdit(self.configGroupBox)
        self.lineEditDirectoryLocation.setObjectName(u"lineEditDirectoryLocation")

        self.horizontalLayout.addWidget(self.lineEditDirectoryLocation)

        self.pushButtonDirectoryChooser = QPushButton(self.configGroupBox)
        self.pushButtonDirectoryChooser.setObjectName(u"pushButtonDirectoryChooser")

        self.horizontalLayout.addWidget(self.pushButtonDirectoryChooser)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)

        self.checkBoxRecurse = QCheckBox(self.configGroupBox)
        self.checkBoxRecurse.setObjectName(u"checkBoxRecurse")
        self.checkBoxRecurse.setChecked(True)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.checkBoxRecurse)


        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(ConfigureDialog)
        self.buttonBox.accepted.connect(ConfigureDialog.accept)
        self.buttonBox.rejected.connect(ConfigureDialog.reject)

        QMetaObject.connectSlotsByName(ConfigureDialog)
    # setupUi

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QCoreApplication.translate("ConfigureDialog", u"Configure Directory Copy", None))
        self.configGroupBox.setTitle("")
        self.labelIdentifier.setText(QCoreApplication.translate("ConfigureDialog", u"Identifier:", None))
        self.labelDirectory.setText(QCoreApplication.translate("ConfigureDialog", u"Output directory:", None))
        self.pushButtonDirectoryChooser.setText(QCoreApplication.translate("ConfigureDialog", u"...", None))
        self.checkBoxRecurse.setText(QCoreApplication.translate("ConfigureDialog", u"Recursively copy directory", None))
    # retranslateUi

