from PyQt5.QtWidgets import QGraphicsView, QApplication, QGraphicsItem, QGraphicsScene
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from .node_graphics_socket import QDMGraphicsSocket
from .node_graphics_edge import QDMGraphicsEdge
from .node_edge import Edge, EDGE_TYPE_BEZIER, EDGE_TYPE_POLYGONAL
from .node_graphics_cutline import QDMCutLine
from .node_graphics_node import QAbstractGraphicsNode,MyIndicatorItem

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 15


DEBUG = False


class QDMGraphicsView(QGraphicsView):
    scenePosChanged = pyqtSignal(int, int)
    # sceneItemSelected = pyqtSignal(str, int)
    sceneItemSelected = pyqtSignal([QGraphicsItem], [str]) # overload型 信号

    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.parent =parent


        self.initUI()

        self.setScene(self.grScene)

        self.mode = MODE_NOOP
        self.editingFlag = False
        self.rubberBandDraggingRectangle = False

        self.zoomInFactor = 1.25  # 每次放大的因子
        self.zoomClamp = True  # 指示放大缩小是否有效标志位
        self.zoom = 0  # 初始的倍数值
        self.zoomStep = 0.5  # 每次滚轮，self.zoom的变化值
        self.zoomRange = [-6, 3]  # self.zoom的变化值的变化范围，超过范围，zoomInFactor为False

        # cutline
        self.cutline = QDMCutLine()
        self.grScene.addItem(self.cutline)

        # enable drops
        self.setAcceptDrops(True)



    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        # 全局刷新，一个item刷新，其他item也跟着刷新，全局刷新费CPU
        # self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # 单个item调用update的时候刷新，其他item并不刷新，除非两者相干涉
        self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        # self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        # 每次动item, scene 的drawBackGround()不会立即调用，仅缩放视图才调用drawbackground
        self.setCacheMode(QGraphicsView.CacheBackground)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)

        self.setDragMode(QGraphicsView.RubberBandDrag)



    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):


        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)


    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)



    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.RubberBandDrag)


    def leftMouseButtonPress(self, event):
        # get item which we clicked on
        item = self.getItemAtClick(event)

        # we store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        # if DEBUG: print("LMB Click on", item, self.debug_modifiers(event))

        # logic
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return


        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                QApplication.setOverrideCursor(Qt.CrossCursor)  # 拖动鼠标图标换成可编辑状态
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        if item is None: # 左键空
            # 如果按住ctrl键盘情况下，左键鼠标
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT  # 处于剪断连接线模式，方便在鼠标移动事件中添加鼠标移动的坐标到linePoints
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return
            else:
                self.rubberBandDraggingRectangle = True

        # item = self.getItemAtClick(event)

        if item is not None:
            if isinstance(item, MyIndicatorItem): # 如果选中的是标注,则发送其对应的液压元件item
                self.sceneItemSelected.emit(item.parent.grNode)  # 发送选中的元素grNode或者grEdge对象
            else:
                self.sceneItemSelected.emit(item)  # 发送选中的元素grNode或者grEdge对象

        else:
            # noneType = QGraphicsItem() #emit()不能发射None对象
            self.sceneItemSelected[str].emit("")

        #
        # if isinstance(item, QAbstractGraphicsNode):   # 如果选中的是node对象或者子对象
        #     QApplication.setOverrideCursor(Qt.ClosedHandCursor)  #选中后变成移动图标
        #     self.sceneItemSelected.emit(item)  # 发送选中的元素对象
        #
        # elif isinstance(item, QDMGraphicsEdge):  # 如果选中的是edge对象
        #     # self.sceneItemSelected.emit("edge"+str(item.edge.edge_type), item.edge.id)
        #     pass
        # else:
        #     # self.sceneItemSelected.emit("", 0) # 如果选中的是空对象
        #     pass

        super().mousePressEvent(event)


    def leftMouseButtonRelease(self, event):
        # get item which we release mouse button on

        item = self.getItemAtClick(event)
        # 不管什么操作，只要左键释放，鼠标图标都还原成默认
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        # logic
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return

        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)

                if res: return

        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdges()
            self.cutline.line_points = []
            # 因为每次cutine形状变了，所以要每次都prepareGeometryChange
            self.cutline.prepareGeometryChange()
            self.cutline.update()
            # self.update() # 视图更新，因为缓存，self.cutline.update().并不直接刷新view

            self.mode = MODE_NOOP


            return


        if self.rubberBandDraggingRectangle: #框选
            # self.grScene.scene.history.storeHistory("rubberBandDraggingRectangle Selection changed")
            self.rubberBandDraggingRectangle = False

        super().mouseReleaseEvent(event)



    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)

        if DEBUG:
            if isinstance(item, QDMGraphicsEdge): print('RMB DEBUG:', item.edge, ' connecting sockets:',
                                            item.edge.start_socket, '<-->', item.edge.end_socket)
            if type(item) is QDMGraphicsSocket: print('RMB DEBUG:', item.socket, 'has edges:', item.socket.edges)

            if item is None:
                print('SCENE:')
                print('  Nodes:')
                for node in self.grScene.scene.nodes: print('    ', node)
                print('  Edges:')
                for edge in self.grScene.scene.edges: print('    ', edge)


    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)


    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG: # 如果是拖拽连线操作
            pos = self.mapToScene(event.pos())
            self.drag_edge.grEdge.setDestination(pos.x(), pos.y())
            self.drag_edge.grEdge.update()


        # 如果是切线操作，添加鼠标当前点进入line_points
        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos()) # 移动一下，就添加一个点
            self.cutline.line_points.append(pos)
            # self.update() # 这个函数会触发view里所有的item的paint()函数，但不是触发scene的drawBackGround()
            self.cutline.prepareGeometryChange()
            self.cutline.update()
        self.last_scene_mouse_position = self.mapToScene(event.pos())
        # 这里发射鼠标移动点信号
        self.scenePosChanged.emit(
            int(self.last_scene_mouse_position.x()), int(self.last_scene_mouse_position.y())
        )

        super().mouseMoveEvent(event)
    # 判断cutLine与当前scene中每个edge是否相交，如果相交，就切断相交的edge
    def cutIntersectingEdges(self):
        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix + 1]

            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1, p2):
                    # 删除edge
                    edge.remove()

        self.grScene.scene.history.storeHistory("Delete cutted edges", setModified=True)



    def deleteSelected(self):
        # 选中的只能是gr对象
        for item in self.grScene.selectedItems():
            # 因为edge和node之间可能有耦合，删除node后自动连带删除相连的edge。为了
            # 避免重复删除，删之前，判断锅里还有没有要删的菜
            if item.parent in self.grScene.scene.nodes + self.grScene.scene.edges:
                item.parent.remove()
                  # if isinstance(item, QAbstractGraphicsNode): #hasattr(item, 'node'):  # 如果是grNode对象，具有属性'node'
                #     item.parent.remove()
                # elif isinstance(item, QDMGraphicsEdge): #hasattr(item, 'node'):  # 如果是grNode对象，具有属性'node'
                #     item.parent.remove()
        self.grScene.scene.history.storeHistory("Delete selected", setModified=True)

    def rotateSelected(self, angle):
        # 选中的只能是grnode对象
        for item in self.grScene.selectedItems():
            item.rotateDelata(angle)
            # if isinstance(item, QAbstractGraphicsNode): #hasattr(item, 'node'):  # 如果是grNode对象，具有属性'node'
            #     item.node.rotate(angle)
        self.grScene.scene.history.storeHistory("Rotate selected", setModified=True)

    def scaleSelected(self, scale):
        # 选中的只能是grnode对象
        for item in self.grScene.selectedItems():
            if isinstance(item, QAbstractGraphicsNode):  # hasattr(item, 'node'):  # 如果是grNode对象，具有属性'node'
                # item.node.setRelativeScale(scale)
                item.scaleDelta(scale)
        self.grScene.scene.history.storeHistory("Scale selected", setModified=True)




    def debug_modifiers(self, event):
        out = "MODS: "
        if event.modifiers() & Qt.ShiftModifier: out += "SHIFT "
        if event.modifiers() & Qt.ControlModifier: out += "CTRL "
        if event.modifiers() & Qt.AltModifier: out += "ALT "
        return out

    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj


    def edgeDragStart(self, item):
        if DEBUG: print('View::edgeDragStart ~ Start dragging edge')
        if DEBUG: print('View::edgeDragStart ~   assign Start Socket to:', item.socket)
        self.drag_start_socket = item.socket
        self.drag_edge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_POLYGONAL)
        if DEBUG: print('View::edgeDragStart ~   dragEdge:', self.drag_edge)


    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP

        if DEBUG: print('View::edgeDragEnd ~ End dragging edge')
        self.drag_edge.remove()
        self.drag_edge = None

        if type(item) is QDMGraphicsSocket: # 如果拖到了一个socket之上
            if item.socket != self.drag_start_socket: # 如果拖到了另外一个socket之上
                # if we released dragging on a socket (other then the beginning socket)

                # we wanna keep all the edges comming from target socket
                if not item.socket.is_multi_edges:
                    item.socket.removeAllEdges()

                # we wanna keep all the edges comming from start socket
                if not self.drag_start_socket.is_multi_edges:
                    self.drag_start_socket.removeAllEdges()

                new_edge = Edge(self.grScene.scene, self.drag_start_socket, item.socket, edge_type=EDGE_TYPE_POLYGONAL)
                if DEBUG: print("View::edgeDragEnd ~  created new edge:", new_edge, "connecting", new_edge.start_socket, "<-->", new_edge.end_socket)


                self.grScene.scene.history.storeHistory("Created new edge by dragging", setModified=True)


                return True
        # # 如果拖到一半松手了，drag_start_socket之前被隐藏了，现在必须显示出来
        # else:
        #     if len(self.drag_start_socket.edges) ==0: #如果起始的socket其他edge线链接
        #         self.drag_start_socket.grSocket.linkFlag = False


        if DEBUG: print('View::edgeDragEnd ~ everything done.')
        return False


    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ measures if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > edge_drag_threshold_sq



    def wheelEvent(self, event):
        # calculate our zoom Factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep


        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor) # (x,y)方向上的縮放


    # 拖拽进入事件
    def dragEnterEvent(self, event):
        mineData = event.mimeData() # 获取drop site上的数据

        if mineData.hasFormat("text/plain"):    # 如果拖拽的是文字
            event.accept()
        # elif mineData.hasFormat("text/uri-list"): # 如果是文件
        #     filename = mineData.urls()[0].fileName()
        #     self.grScene.scene.loadFromFile(filename)
        #     print("recevied file: %s " % filename)
        #     event.accept()
        else:
            event.ignore()

    # 下面事件必须要写出来，并accept，不然传不到dropEvent（)无法响应
    def dragLeaveEvent(self, event):
        event.accept()

    # 下面事件必须要写出来，并accept，不然传不到dropEvent（)无法响应
    def dragMoveEvent(self, event):
        event.accept()

    # 拖拽放置事件
    def dropEvent(self, event):
        text = event.mimeData().text() # 获取文本

        # print("x:%d, y: %d" % (event.pos().x(), event.pos().y()))
        # 按照名称创建node对象
        from pyHydraulic.node_graphics_node import componentsLib # 如果在是对象文本
        if text in componentsLib.getSecondList():
            from pyHydraulic.node_node import Node
            node = Node(self.grScene.scene, text) # 按照文本添加node
            pos = self.mapToScene(event.pos())
            node.setPos(pos.x(),pos.y()) # 设置node位置为鼠标落地位置
        event.acceptProposedAction()
