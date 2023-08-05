import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .node_scene import Scene, InvalidFile
from .node_node import Node
from .node_edge import Edge, EDGE_TYPE_BEZIER,EDGE_TYPE_DIRECT, EDGE_TYPE_POLYGONAL
from .node_graphics_view import QDMGraphicsView


class NodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.filename = None


        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # crate graphics scene
        self.scene = Scene()

        # 添加部分样例
        self.addSampleNodes()

        # create graphics view
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        # 创建一个文本框,用来显示提示信息
        self.label = QLabel(self.view)

        # self.layout.addWidget(self.label)
        # self.label.move(self.scene.scene_width, self.scene.scene_height)
        self.label.setStyleSheet(
            "font: 18pt '微软雅黑';"
            # "border-bottom-color: rgb(0,0,0);"
            # "background-color: rgba(255, 228, 23, 0%);"
            # "color: rgba(189, 189, 189, 50%); "
            "border-radius: 4px"
        )
        self.label.setAlignment(Qt.AlignCenter)
        
        


    def showTips(self, message):


         # 下面是透明度动画
        self.label.move(self.width()/3, self.height()* 0.95)
        pxWdith = self.label.fontMetrics().width(message)             # 获取字符串的像素宽度
        self.label.setFixedWidth(pxWdith)              # 宽度
        self.label.setText(message)

         
        opEffect = QGraphicsOpacityEffect(self)
        # opEffect.setOpacity(0.5)
        self.label.setGraphicsEffect(opEffect)
        # 1. 创建动画对象
        animation = QPropertyAnimation(self)
        animation.setTargetObject(opEffect)
        animation.setPropertyName(b"opacity")
        # 2.设置动画的属性，插值，结束
        animation.setStartValue(0)
  
   
        animation.setKeyValueAt(0.5, 1)
        animation.setEndValue(0)

        # 3.设置动画时长
        animation.setEasingCurve(QEasingCurve.OutInQuint)
        animation.setDuration(2000) # ms 动画时长
        animation.start()




    def isModified(self):
        return self.scene.has_been_modified

    def isFilenameSet(self):
        return self.filename is not None

    def getUserFriendlyFilename(self):
        name = os.path.basename(self.filename) if self.isFilenameSet() else "New Graph"
        return name + ("*" if self.isModified() else "")

    def fileNew(self):
        self.scene.clear()
        self.filename = None

    def fileLoad(self, filename):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.scene.loadFromFile(filename)
            self.filename = filename
            # clear history
            return True
        except InvalidFile as e:
            print(e)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, "Error loading %s" % os.path.basename(filename), str(e))
            return False
        finally:
            QApplication.restoreOverrideCursor()


    def fileSave(self, filename=None):
        # when called with empty parameter, we won't store the filename
        if filename is not None: self.filename = filename
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.scene.saveToFile(self.filename)
        QApplication.restoreOverrideCursor()
        return True

    # 添加node到scene
    def addnode(self, node_name):
        return Node(self.scene, node_name)

    # 添加样例node到scene
    def addSampleNodes(self):
        # node1 = Node(self.scene, "pressure sensor")
        node2 = Node(self.scene, "tank")
        node3 = Node(self.scene, "flow meter")
        # node4 = Node(self.scene, "gauge")
        # node5 = Node(self.scene, "servo valve")
        # node6 = Node(self.scene,  "piston right")
        # node6.grNode.value = -100
        # node7 = Node(self.scene, "simple tank")

        # node1.rotate(90)
        #
        # node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)
        # node4.setPos(-200, -150)
        # node6.setPos(-300, -250)
        # print(type(node1.sockets[0]))
        edge1 = Edge(self.scene, node3.sockets[0], node2.sockets[0], edge_type= EDGE_TYPE_POLYGONAL)
        # edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)


    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)


        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText("This is my Awesome _text!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))


        widget1 = QPushButton("Hello World")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)


        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)


        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)

    def getObjectByID(self, id):
        for object in self.scene.nodes + self.scene.edges:
            if object.id == id:
                return object
        return None


    def getObjectByName(self, name):
        for object in self.scene.nodes + self.scene.edges:
            if object.name == name:
                return object
        return None


    # 选中所有的元素
    def selectAll(self):
        for item in self.scene.nodes + self.scene.edges:
            item.grItem.setSelected(True)
        # for edge in  self.scene.edges:
        #     edge.grEdge.setSelected(True)



