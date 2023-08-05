import os
import json
from collections import OrderedDict
from .utils import dumpException
from .node_serializable import Serializable
from .node_graphics_scene import QDMGraphicsScene
from .node_node import Node
from .node_edge import Edge
from .node_scene_history import SceneHistory
from .node_scene_clipboard import SceneClipboard
from PyQt5.QtCore import Qt


class InvalidFile(Exception): pass

DEBUG = False
class Scene(Serializable):
    def __init__(self):
        super().__init__()
        # 所有nodes和edges集合
        self.nodes = []
        self.edges = []

        self.scene_width = 640000
        self.scene_height = 640000

        self._has_been_modified = False # 有历史记录，则该值被改变为True
        self._has_been_modified_listeners = [] #界面改变事件回调函数集合

        self.initUI()
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)


    @property
    def has_been_modified(self):
        return self._has_been_modified

    # 属性赋值的时候，会自动调用callback()集
    @has_been_modified.setter
    def has_been_modified(self, value):
        if not self._has_been_modified and value: # 只有上一次没改变，这次改变了，才触发整个界面改变事件回调函数
            self._has_been_modified = value

            # call all registered listeners
            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified = value

    # 添加callback()集
    def addHasBeenModifiedListener(self, callback):
        self._has_been_modified_listeners.append(callback)

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        if node in self.nodes: self.nodes.remove(node)
        else: print("!W:", "Scene::removeNode", "wanna remove node", node, "from self.nodes but it's not in the list!")

    def removeEdge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
        else:
            print("!W:", "Scene::removeEdge", "wanna remove edge", edge, "from self.edges but it's not in the list!")

    # 删除所有nodes
    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

        self.has_been_modified = False


    def saveToFile(self, filename):
        with open(filename, "w") as file:
            file.write( json.dumps( self.serialize(), indent=4 ) )
            print("saving to", filename, "was successfull.")

            self.has_been_modified = False

    def loadFromFile(self, filename):
        with open(filename, "r", encoding='utf-8', errors='ignore') as file:
            raw_data = file.read()
            try:
                data = json.loads(raw_data, encoding='utf-8')
                self.deserialize(data)
                self.has_been_modified = False
            except json.JSONDecodeError:
                raise InvalidFile("%s is not a valid JSON file" % os.path.basename(filename))
            except Exception as e:
                dumpException(e)

    def setBackgroundColor(self, color=Qt.lightGray, grid_on = True):
        self.grScene._color_background = color
        self.grScene.setBackgroundBrush(color)
        self.grScene._grid_enble = grid_on

    # 序列化所有的nodes和edges
    def serialize(self):
        nodes, edges = [], []  # 存放序列化后的字符串list
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        self.clear() # 撤销的时候，先全部删除界面里所有元素
        hashmap = {}  # hashmap存放的是id:对象集合，通过寻找id就能得到node和socket对象，为以后恢复连线做准备

        if restore_id: self.id = data['id'] # scene的id

        # create nodes 在scene层创建node，以及还原node

        for nodeDataDict in data['nodes']: # node_data 为单个node的描述字典
            node = Node(self, nodeDataDict["type"])
            for (property, propertyValue) in nodeDataDict.items():
                if hasattr(node.grItem, property):  # 检查类是否有属性
                    try:
                        setattr(node.grItem, property, propertyValue) # 因为有的属性是只读属性，所以有可能失败
                    except Exception as e:
                        pass
                        # print("写属性失败"+property)
            hashmap[nodeDataDict['id']] = node  # 4.在对象字典添加单个node的对象和id
            node.deserialize(nodeDataDict, hashmap, restore_id)  # 4.把单个node的数据传递到下一级，解析socket数据


        # for node_data in data['nodes']:
            # node = Node(self, node_type=node_data["node_type"])   # 1.先还原创建的node对象, 默认没有socket, socket的创建是在下一层
            # node.setPos(node_data['pos_x'], node_data['pos_y'])   # 2.再还原node的位置
            # node.setRotation(node_data["rotation"])     # 3.还原绝对位置角度（顺时针）
            # node.setAbsoluteScale(node_data["scale"])
            # node.name = node_data["name"]
            # node.grNode.unit = node_data["unit"]
            # node.grNode.value = node_data["value"]
            # node.grNode.maxValue = node_data["maxValue"]
            # node.grNode.minValue = node_data["minValue"]
            # node.grNode.text = node_data["text"]
            # if restore_id: node.id = node_data['id']    # 4.再还原node的id
            #
            # hashmap[node_data['id']] = node  # 4.在对象字典添加单个node的对象和id

            # node.deserialize(node_data, hashmap, restore_id)  # 4.把单个node的数据传递到下一级，解析socket数据


        # create edges
        for edge_data in data['edges']:
            edge = Edge(self)
            edge.deserialize(edge_data, hashmap, restore_id) # 创建edge时候，自动添加到grScene中
            if DEBUG:
                print("edge is created. id is %d" % edge.id)

        return True