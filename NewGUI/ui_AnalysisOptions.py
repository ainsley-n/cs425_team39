# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AnalysisOptions.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(781, 620)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.CircuitImage = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CircuitImage.sizePolicy().hasHeightForWidth())
        self.CircuitImage.setSizePolicy(sizePolicy)
        self.CircuitImage.setObjectName("CircuitImage")
        self.verticalLayout.addWidget(self.CircuitImage)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_4 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_4.sizePolicy().hasHeightForWidth())
        self.page_4.setSizePolicy(sizePolicy)
        self.page_4.setObjectName("page_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.RequestProperty = QtWidgets.QPushButton(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RequestProperty.sizePolicy().hasHeightForWidth())
        self.RequestProperty.setSizePolicy(sizePolicy)
        self.RequestProperty.setObjectName("RequestProperty")
        self.gridLayout.addWidget(self.RequestProperty, 5, 1, 1, 1)
        self.NodeAnalysis = QtWidgets.QPushButton(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NodeAnalysis.sizePolicy().hasHeightForWidth())
        self.NodeAnalysis.setSizePolicy(sizePolicy)
        self.NodeAnalysis.setObjectName("NodeAnalysis")
        self.gridLayout.addWidget(self.NodeAnalysis, 3, 1, 1, 1)
        self.MeshAnalysis = QtWidgets.QPushButton(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MeshAnalysis.sizePolicy().hasHeightForWidth())
        self.MeshAnalysis.setSizePolicy(sizePolicy)
        self.MeshAnalysis.setObjectName("MeshAnalysis")
        self.gridLayout.addWidget(self.MeshAnalysis, 3, 0, 1, 1)
        self.TheveninAnalysis = QtWidgets.QPushButton(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TheveninAnalysis.sizePolicy().hasHeightForWidth())
        self.TheveninAnalysis.setSizePolicy(sizePolicy)
        self.TheveninAnalysis.setObjectName("TheveninAnalysis")
        self.gridLayout.addWidget(self.TheveninAnalysis, 4, 0, 1, 1)
        self.StateSpaceAnalysis = QtWidgets.QPushButton(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StateSpaceAnalysis.sizePolicy().hasHeightForWidth())
        self.StateSpaceAnalysis.setSizePolicy(sizePolicy)
        self.StateSpaceAnalysis.setObjectName("StateSpaceAnalysis")
        self.gridLayout.addWidget(self.StateSpaceAnalysis, 5, 0, 1, 1)
        self.NortonAnalysis = QtWidgets.QPushButton(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NortonAnalysis.sizePolicy().hasHeightForWidth())
        self.NortonAnalysis.setSizePolicy(sizePolicy)
        self.NortonAnalysis.setObjectName("NortonAnalysis")
        self.gridLayout.addWidget(self.NortonAnalysis, 4, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.stackedWidget.addWidget(self.page_4)
        self.page_3 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_3.sizePolicy().hasHeightForWidth())
        self.page_3.setSizePolicy(sizePolicy)
        self.page_3.setObjectName("page_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget = QtWidgets.QWidget(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.SolutionImage = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SolutionImage.sizePolicy().hasHeightForWidth())
        self.SolutionImage.setSizePolicy(sizePolicy)
        self.SolutionImage.setObjectName("SolutionImage")
        self.verticalLayout_3.addWidget(self.SolutionImage)
        self.verticalLayout_4.addWidget(self.widget)
        self.stackedWidget.addWidget(self.page_3)
        self.verticalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 781, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAnalysis = QtWidgets.QMenu(self.menubar)
        self.menuAnalysis.setObjectName("menuAnalysis")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setEnabled(True)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionNodal = QtWidgets.QAction(MainWindow)
        self.actionNodal.setObjectName("actionNodal")
        self.actionMesh = QtWidgets.QAction(MainWindow)
        self.actionMesh.setObjectName("actionMesh")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuAnalysis.addAction(self.actionNodal)
        self.menuAnalysis.addAction(self.actionMesh)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.CircuitImage.setText(_translate("MainWindow", "CircuitImage"))
        self.RequestProperty.setText(_translate("MainWindow", "Component and Node Properties"))
        self.NodeAnalysis.setText(_translate("MainWindow", "Nodal Analysis"))
        self.MeshAnalysis.setText(_translate("MainWindow", "Mesh Analysis"))
        self.TheveninAnalysis.setText(_translate("MainWindow", "Thevenin Analysis"))
        self.StateSpaceAnalysis.setText(_translate("MainWindow", "State-Space Analysis"))
        self.NortonAnalysis.setText(_translate("MainWindow", "Norton Analysis"))
        self.SolutionImage.setText(_translate("MainWindow", "SolutionImage"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAnalysis.setTitle(_translate("MainWindow", "Analysis"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionNodal.setText(_translate("MainWindow", "Nodal"))
        self.actionMesh.setText(_translate("MainWindow", "Mesh"))
