# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1032, 730)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pics/images/APPIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        MainWindow.setIconSize(QtCore.QSize(36, 36))
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.nodeEditor = NodeEditorWidget(self.centralwidget)
        self.nodeEditor.setAcceptDrops(False)
        self.nodeEditor.setStyleSheet("")
        self.nodeEditor.setObjectName("nodeEditor")
        self.horizontalLayout.addWidget(self.nodeEditor)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1032, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dock_toolBox = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_toolBox.sizePolicy().hasHeightForWidth())
        self.dock_toolBox.setSizePolicy(sizePolicy)
        self.dock_toolBox.setMinimumSize(QtCore.QSize(250, 213))
        self.dock_toolBox.setMaximumSize(QtCore.QSize(250, 524287))
        self.dock_toolBox.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.dock_toolBox.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dock_toolBox.setObjectName("dock_toolBox")
        self.dock_toolBox_layout = QtWidgets.QWidget()
        self.dock_toolBox_layout.setObjectName("dock_toolBox_layout")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dock_toolBox_layout)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBoxLib = QtWidgets.QToolBox(self.dock_toolBox_layout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBoxLib.sizePolicy().hasHeightForWidth())
        self.toolBoxLib.setSizePolicy(sizePolicy)
        self.toolBoxLib.setMinimumSize(QtCore.QSize(240, 0))
        self.toolBoxLib.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.toolBoxLib.setObjectName("toolBoxLib")
        self.dynamic = QtWidgets.QWidget()
        self.dynamic.setGeometry(QtCore.QRect(0, 0, 240, 516))
        self.dynamic.setObjectName("dynamic")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dynamic)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidgetDynamic = QtWidgets.QListWidget(self.dynamic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetDynamic.sizePolicy().hasHeightForWidth())
        self.listWidgetDynamic.setSizePolicy(sizePolicy)
        self.listWidgetDynamic.setMinimumSize(QtCore.QSize(200, 0))
        self.listWidgetDynamic.setMaximumSize(QtCore.QSize(300, 16777215))
        self.listWidgetDynamic.setAutoScrollMargin(0)
        self.listWidgetDynamic.setProperty("showDropIndicator", False)
        self.listWidgetDynamic.setDragEnabled(False)
        self.listWidgetDynamic.setDragDropOverwriteMode(False)
        self.listWidgetDynamic.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.listWidgetDynamic.setItemAlignment(QtCore.Qt.AlignCenter)
        self.listWidgetDynamic.setObjectName("listWidgetDynamic")
        self.verticalLayout_2.addWidget(self.listWidgetDynamic)
        self.toolBoxLib.addItem(self.dynamic, "")
        self.executive = QtWidgets.QWidget()
        self.executive.setGeometry(QtCore.QRect(0, 0, 240, 516))
        self.executive.setObjectName("executive")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.executive)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.listWidgetExecutive = QtWidgets.QListWidget(self.executive)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetExecutive.sizePolicy().hasHeightForWidth())
        self.listWidgetExecutive.setSizePolicy(sizePolicy)
        self.listWidgetExecutive.setMinimumSize(QtCore.QSize(200, 0))
        self.listWidgetExecutive.setMaximumSize(QtCore.QSize(300, 16777215))
        self.listWidgetExecutive.setAutoScrollMargin(0)
        self.listWidgetExecutive.setProperty("showDropIndicator", False)
        self.listWidgetExecutive.setDragEnabled(False)
        self.listWidgetExecutive.setDragDropOverwriteMode(False)
        self.listWidgetExecutive.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.listWidgetExecutive.setItemAlignment(QtCore.Qt.AlignCenter)
        self.listWidgetExecutive.setObjectName("listWidgetExecutive")
        self.verticalLayout_3.addWidget(self.listWidgetExecutive)
        self.toolBoxLib.addItem(self.executive, "")
        self.control = QtWidgets.QWidget()
        self.control.setGeometry(QtCore.QRect(0, 0, 240, 516))
        self.control.setObjectName("control")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.control)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.listWidgetControl = QtWidgets.QListWidget(self.control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetControl.sizePolicy().hasHeightForWidth())
        self.listWidgetControl.setSizePolicy(sizePolicy)
        self.listWidgetControl.setMinimumSize(QtCore.QSize(200, 0))
        self.listWidgetControl.setMaximumSize(QtCore.QSize(300, 16777215))
        self.listWidgetControl.setAutoScrollMargin(0)
        self.listWidgetControl.setProperty("showDropIndicator", False)
        self.listWidgetControl.setDragEnabled(False)
        self.listWidgetControl.setDragDropOverwriteMode(False)
        self.listWidgetControl.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.listWidgetControl.setItemAlignment(QtCore.Qt.AlignCenter)
        self.listWidgetControl.setObjectName("listWidgetControl")
        self.verticalLayout_4.addWidget(self.listWidgetControl)
        self.toolBoxLib.addItem(self.control, "")
        self.auxiliary = QtWidgets.QWidget()
        self.auxiliary.setGeometry(QtCore.QRect(0, 0, 240, 516))
        self.auxiliary.setObjectName("auxiliary")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.auxiliary)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.listWidgetAuxiliary = QtWidgets.QListWidget(self.auxiliary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetAuxiliary.sizePolicy().hasHeightForWidth())
        self.listWidgetAuxiliary.setSizePolicy(sizePolicy)
        self.listWidgetAuxiliary.setMinimumSize(QtCore.QSize(200, 0))
        self.listWidgetAuxiliary.setMaximumSize(QtCore.QSize(300, 16777215))
        self.listWidgetAuxiliary.setAutoScrollMargin(0)
        self.listWidgetAuxiliary.setProperty("showDropIndicator", False)
        self.listWidgetAuxiliary.setDragEnabled(False)
        self.listWidgetAuxiliary.setDragDropOverwriteMode(False)
        self.listWidgetAuxiliary.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.listWidgetAuxiliary.setItemAlignment(QtCore.Qt.AlignCenter)
        self.listWidgetAuxiliary.setObjectName("listWidgetAuxiliary")
        self.verticalLayout_6.addWidget(self.listWidgetAuxiliary)
        self.toolBoxLib.addItem(self.auxiliary, "")
        self.verticalLayout.addWidget(self.toolBoxLib)
        self.dock_toolBox.setWidget(self.dock_toolBox_layout)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dock_toolBox)
        self.dock_propertyTable = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_propertyTable.sizePolicy().hasHeightForWidth())
        self.dock_propertyTable.setSizePolicy(sizePolicy)
        self.dock_propertyTable.setMinimumSize(QtCore.QSize(120, 119))
        self.dock_propertyTable.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dock_propertyTable.setObjectName("dock_propertyTable")
        self.dock_propertyTable_layout = QtWidgets.QWidget()
        self.dock_propertyTable_layout.setObjectName("dock_propertyTable_layout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.dock_propertyTable_layout)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tableWidget = QtWidgets.QTableWidget(self.dock_propertyTable_layout)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.verticalLayout_5.addWidget(self.tableWidget)
        self.dock_propertyTable.setWidget(self.dock_propertyTable_layout)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dock_propertyTable)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setMaximumSize(QtCore.QSize(16777215, 25))
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setIconSize(QtCore.QSize(15, 15))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionFileOpen = QtWidgets.QAction(MainWindow)
        self.actionFileOpen.setObjectName("actionFileOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.actionRotate_P90 = QtWidgets.QAction(MainWindow)
        self.actionRotate_P90.setObjectName("actionRotate_P90")
        self.actionRotate_N90 = QtWidgets.QAction(MainWindow)
        self.actionRotate_N90.setObjectName("actionRotate_N90")
        self.actionscalePlus = QtWidgets.QAction(MainWindow)
        self.actionscalePlus.setObjectName("actionscalePlus")
        self.actionScaleMinus = QtWidgets.QAction(MainWindow)
        self.actionScaleMinus.setObjectName("actionScaleMinus")
        self.actionHS_help = QtWidgets.QAction(MainWindow)
        self.actionHS_help.setObjectName("actionHS_help")
        self.actionAbout_HS = QtWidgets.QAction(MainWindow)
        self.actionAbout_HS.setObjectName("actionAbout_HS")
        self.actionselectAll = QtWidgets.QAction(MainWindow)
        self.actionselectAll.setObjectName("actionselectAll")
        self.actionData_interface = QtWidgets.QAction(MainWindow)
        self.actionData_interface.setObjectName("actionData_interface")
        self.actionstart = QtWidgets.QAction(MainWindow)
        self.actionstart.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pics/images/icons/start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionstart.setIcon(icon1)
        self.actionstart.setObjectName("actionstart")
        self.actionLibrary = QtWidgets.QAction(MainWindow)
        self.actionLibrary.setObjectName("actionLibrary")
        self.actionProperty = QtWidgets.QAction(MainWindow)
        self.actionProperty.setObjectName("actionProperty")
        self.actionWater_mark = QtWidgets.QAction(MainWindow)
        self.actionWater_mark.setCheckable(True)
        self.actionWater_mark.setObjectName("actionWater_mark")
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionFileOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addAction(self.actionRotate_P90)
        self.menuEdit.addAction(self.actionRotate_N90)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionscalePlus)
        self.menuEdit.addAction(self.actionScaleMinus)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionselectAll)
        self.menuHelp.addAction(self.actionHS_help)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_HS)
        self.menuSettings.addAction(self.actionData_interface)
        self.menuView.addAction(self.actionLibrary)
        self.menuView.addAction(self.actionProperty)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionWater_mark)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionstart)

        self.retranslateUi(MainWindow)
        self.toolBoxLib.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "hydraulic Sketcher"))
        self.menuFile.setTitle(_translate("MainWindow", "FIle"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.dock_toolBox.setWindowTitle(_translate("MainWindow", "Library"))
        self.toolBoxLib.setItemText(self.toolBoxLib.indexOf(self.dynamic), _translate("MainWindow", "dynamic"))
        self.toolBoxLib.setItemText(self.toolBoxLib.indexOf(self.executive), _translate("MainWindow", "executive"))
        self.toolBoxLib.setItemText(self.toolBoxLib.indexOf(self.control), _translate("MainWindow", "control"))
        self.toolBoxLib.setItemText(self.toolBoxLib.indexOf(self.auxiliary), _translate("MainWindow", "auxiliary"))
        self.dock_propertyTable.setWindowTitle(_translate("MainWindow", "Property"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionFileOpen.setText(_translate("MainWindow", "Open"))
        self.actionFileOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as..."))
        self.actionSave_as.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionRedo.setText(_translate("MainWindow", "Redo"))
        self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Shift+Z"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionDelete.setShortcut(_translate("MainWindow", "Del"))
        self.actionRotate_P90.setText(_translate("MainWindow", "Rotate 90+"))
        self.actionRotate_P90.setShortcut(_translate("MainWindow", "Space"))
        self.actionRotate_N90.setText(_translate("MainWindow", "Rotate 90-"))
        self.actionRotate_N90.setShortcut(_translate("MainWindow", "Ctrl+Space"))
        self.actionscalePlus.setText(_translate("MainWindow", "Scale +"))
        self.actionscalePlus.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionScaleMinus.setText(_translate("MainWindow", "Scale-"))
        self.actionScaleMinus.setShortcut(_translate("MainWindow", "Ctrl+M"))
        self.actionHS_help.setText(_translate("MainWindow", "HS help"))
        self.actionHS_help.setToolTip(_translate("MainWindow", "actionHydraulic_sketcher_help"))
        self.actionHS_help.setShortcut(_translate("MainWindow", "F1"))
        self.actionAbout_HS.setText(_translate("MainWindow", "About HS"))
        self.actionAbout_HS.setShortcut(_translate("MainWindow", "F2"))
        self.actionselectAll.setText(_translate("MainWindow", "selectAll"))
        self.actionselectAll.setToolTip(_translate("MainWindow", "actionselectAll"))
        self.actionselectAll.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionData_interface.setText(_translate("MainWindow", "Data interface"))
        self.actionData_interface.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionstart.setText(_translate("MainWindow", "start"))
        self.actionstart.setToolTip(_translate("MainWindow", "start receiving data from clients"))
        self.actionstart.setShortcut(_translate("MainWindow", "Shift+S"))
        self.actionLibrary.setText(_translate("MainWindow", "Library"))
        self.actionProperty.setText(_translate("MainWindow", "Property"))
        self.actionWater_mark.setText(_translate("MainWindow", "Water mark"))
from pyHydraulic.node_editor_widget import NodeEditorWidget
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
