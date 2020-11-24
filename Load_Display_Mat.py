# -*- coding: utf-8 -*-

import os
import sys

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import subprocess
from shiboken2 import wrapInstance
import time
import maya.cmds as cmds
import pymel.core as pm
# import maya.mel as mm
# import maya.utils as mu




import maya_ascii_parser
reload(maya_ascii_parser)
import ui_Load_Display_Mat
reload(ui_Load_Display_Mat)
import ui_Load_Display_Mat


mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)


class LoadDisplayMatWindow(QMainWindow, ui_Load_Display_Mat.Ui_LoadDisplayMatWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, *args, **kwargs):
        super(LoadDisplayMatWindow, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setupUi(self)
    #     self.setup()
    # #
    # def setup(self):
        # self.main_tableWidget.hide()
    #     self.pathlineEdit.setAcceptDrops(True)
    #     # self.pathlineEdit.setDragEnable()
    #     self.pathlineEdit.setText(r'Z:/TSP/Asset/Chars/Chars_01000ab/Mod/default/check/v006/Chars_01000ab_Mod_default.ma')
    #     # self.pathlineEdit.setText(r'S:/Load_Display_Mat/shader.ma')
    #
    #     # self.main_tableWidget.setIconSize(QSize(96, 96))
    #     self.tableworker = tableViewWorker(self.main_tableWidget)
    #     self.tablethread = QThread()
    #     self.tableworker.intReady.connect(self.tableworker_over)
    #     self.tableworker.moveToThread(self.tablethread)
    #     self.tableworker.finished.connect(self.tablethread.quit)
    #     self.tablethread.started.connect(self.tableworker.work)
    #     # 开始tableworker线程
    #     self.tablethread.start()


    # def tableworker_over(self,nodes):
    # 
    #     self.nodes = nodes
    # @Slot()
    # def on_pathlineEdit_editingFinished(self):
    #     try:
    #         self.matfile = self.pathlineEdit.text()
    #         # mat_info = self.parsing_ma(self.matfile, 'matinfo')
    #         # shader_info = self.parsing_ma(self.matfile, 'shaderinfo')
    #         self.filelabel.setText('y')
    #     except Exception, Argument:
    #         print 'repr(Argument):\t\t', str(Argument)
    #     else:
    #         self.filelabel.setText('n')


    @Slot()
    def on_cleanpushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.matfile = self.pathlineEdit.text()
        mat_info = self.parsing_ma(self.matfile, 'matinfo')
        shader_info = self.parsing_ma(self.matfile, 'shaderinfo')

        # ParDepNode = self.get_renderPartition()
        # lLinkDepNode = self.get_lightLinker()
        # rPar_plug = ParDepNode.findPlug('sets', False)
        # lonj_plug = lLinkDepNode.findPlug('link', False)
        # lsh_plug = lLinkDepNode.findPlug('shadowLink', False)

        for sg in mat_info.keys():
            try:
                if mat_info[sg].keys():
                    material = str(pm.shadingNode('lambert', asShader=1, name=mat_info[sg].keys()[0]))
                    mat_attr = mat_info[sg][mat_info[sg].keys()[0]]

                    if mat_attr.has_key('type'):
                        if mat_attr['type'] == 'tex':
                            tex_node = str(
                                pm.shadingNode('file', asTexture=1, isColorManaged=1, name=mat_attr['node'] + '_tex'))

                            pm.setAttr('{}.fileTextureName'.format(tex_node), mat_attr['file'], type="string")
                            pm.connectAttr('{}.outColor'.format(tex_node), '{}.color'.format(material), force=1)

                            uv_node = str(pm.shadingNode('place2dTexture', asUtility=1, name=mat_attr['node'] + '_uv'))
                            pm.setAttr('{}.repeatU'.format(uv_node), mat_attr['attr_re'][0])
                            pm.setAttr('{}.repeatV'.format(uv_node), mat_attr['attr_re'][1])
                            pm.connectAttr('{}.coverage'.format(uv_node), '{}.coverage'.format(tex_node), f=1)
                            pm.connectAttr('{}.translateFrame'.format(uv_node), '{}.translateFrame'.format(tex_node),
                                           f=1)
                            pm.connectAttr('{}.rotateFrame'.format(uv_node), '{}.rotateFrame'.format(tex_node), f=1)
                            pm.connectAttr('{}.mirrorU'.format(uv_node), '{}.mirrorU'.format(tex_node), f=1)
                            pm.connectAttr('{}.mirrorV'.format(uv_node), '{}.mirrorV'.format(tex_node), f=1)
                            pm.connectAttr('{}.stagger'.format(uv_node), '{}.stagger'.format(tex_node), f=1)
                            pm.connectAttr('{}.wrapU'.format(uv_node), '{}.wrapU'.format(tex_node), f=1)
                            pm.connectAttr('{}.wrapV'.format(uv_node), '{}.wrapV'.format(tex_node), f=1)
                            pm.connectAttr('{}.repeatUV'.format(uv_node), '{}.repeatUV'.format(tex_node), f=1)
                            pm.connectAttr('{}.offset'.format(uv_node), '{}.offset'.format(tex_node), f=1)
                            pm.connectAttr('{}.rotateUV'.format(uv_node), '{}.rotateUV'.format(tex_node), f=1)
                            pm.connectAttr('{}.noiseUV'.format(uv_node), '{}.noiseUV'.format(tex_node), f=1)
                            pm.connectAttr('{}.vertexUvOne'.format(uv_node), '{}.vertexUvOne'.format(tex_node), f=1)
                            pm.connectAttr('{}.vertexUvTwo'.format(uv_node), '{}.vertexUvTwo'.format(tex_node), f=1)
                            pm.connectAttr('{}.vertexUvThree'.format(uv_node), '{}.vertexUvThree'.format(tex_node), f=1)
                            pm.connectAttr('{}.vertexCameraOne'.format(uv_node), '{}.vertexCameraOne'.format(tex_node),
                                           f=1)
                            pm.connectAttr('{}.outUV'.format(uv_node), '{}.uv'.format(tex_node))
                            pm.connectAttr('{}.outUvFilterSize'.format(uv_node), '{}.uvFilterSize'.format(tex_node))
                        elif mat_attr['type'] == 'col':
                            pm.setAttr('{}.c'.format(material), mat_attr['attr_diff'][0],mat_attr['attr_diff'][1],mat_attr['attr_diff'][2], type='double3')




                        # pm.hyperShade(assign=tex_node)
                    pm.hyperShade(assign=material)


                    if shader_info[sg].keys():
                        for shape in shader_info[sg].keys():
                            try:
                                new_shape = shape
                                meshlist = pm.ls(type='mesh')
                                for mesh in meshlist:
                                    if not mesh.find('|') == -1 and mesh.split("|")[-1] == shape:
                                        new_shape = mesh

                                if len(shader_info[sg][shape]) == 0:
                                    pm.select(new_shape)
                                    pm.cmds.sets(forceElement=material + "SG", e=1)
                                else:
                                    for f_sets in shader_info[sg][shape]:
                                        pm.select(new_shape + '.' + f_sets.split(".")[1])
                                        pm.cmds.sets(forceElement=material + "SG", e=1)

                            except Exception, Argument:
                                print 'repr(Argument):\t\t', str(Argument)


                # sgDagNode = om.MFnDependencyNode()
                # sgDagNode.create('shadingEngine', sg)
                #
                # sgp_plug = sgDagNode.findPlug('partition', False)
                # sgm_plug = sgDagNode.findPlug('message', True)
                # print sgm_plug.info




                # dg_mod = om.MDGModifier()
                # dg_mod.connect(sgp_plug, rPar_plug.elementByLogicalIndex(-1))
                # dg_mod.doIt()
                #
                # ll_mod = om.MDGModifier()
                # ll_mod.connect(sgm_plug, lonj_plug.elementByLogicalIndex(-1).child(0))
                # ll_mod.doIt()
                #
                # lo_mod = om.MDGModifier()
                # lo_mod.connect(sgm_plug, lonj_plug.elementByLogicalIndex(-2).child(1))
                # lo_mod.doIt()
            except Exception, Argument:
                print 'repr(Argument):\t\t', str(Argument)



    # @Slot()
    # def on_extpushButton_clicked(self):
    #     """
    #     Slot documentation goes here.
    #     """
    #     # TODO: not implemented yet
    #
    #     matfile = self.pathlineEdit.text()
    #     self.loadworker = startWorker(self.nodes, matfile)
    #     self.loadthread = QThread()
    #     self.loadworker.logReady.connect(self.loadthread_logReady)
    #     self.loadworker.existReady.connect(self.loadthread_existReady)
    #     self.loadworker.moveToThread(self.loadthread)
    #     self.loadworker.finished.connect(self.loadthread.quit)
    #     self.loadthread.started.connect(self.loadworker.work)
    #     print 'start'
    #     # 开始tableworker线程
    #     self.loadthread.start()

    # def loadthread_logReady(self,log):
    #     print log
    #     import logging
    #     logging.basicConfig(level=10,
    #                         format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #                         filename=r'D:/work/Load_Display_Mat/text.log')
    #     logging.debug(str(log))

    # def loadthread_existReady(self,num,result):
    #     # print self,num,result
    #     item = QTableWidgetItem(unicode(result))
    #     item.setFlags(Qt.ItemIsEnabled)
    #     self.main_tableWidget.setItem(num, 1, item)


    @Slot()
    def on_lookpushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "choose directory", r"C:", 'ma Files (*.ma)')
        self.pathlineEdit.setText(str(filename))

    # @Slot()
    # def on_cleanpushButton_clicked(self):
    #
    #
    #     self.setup()

    def parsing_ma(self,path,nodetype):

        try:
            madata = maya_ascii_parser.main(path,nodetype)
            return madata

        except Exception, Argument:
            print 'str(Argument):\t\t', str(Argument)
            time.sleep(5)

    # def get_renderPartition(self):
    #     it = om.MItDependencyNodes(om.MFn.kPartition)
    #     partiNodes = om.MObjectArray()
    #     while not it.isDone():
    #         partiNodes.append(it.thisNode())
    #         it.next()
    # 
    #     for parti in partiNodes:
    #         mDagNode = om.MFnDependencyNode(parti)
    #         if mDagNode.absoluteName() == ":renderPartition":
    #             rParDepNode = mDagNode
    # 
    #     return rParDepNode
    # 
    # def get_lightLinker(self):
    #     it = om.MItDependencyNodes(om.MFn.kLightLink)
    #     LightLinkNodes = om.MObjectArray()
    #     while not it.isDone():
    #         LightLinkNodes.append(it.thisNode())
    #         it.next()
    #     mDagNode = om.MFnDependencyNode(LightLinkNodes[0])
    #     return mDagNode



    # def file_path(self):
    #     """
    #     查询当前文件路径
    #
    #     """
    #     action = self.comboBox.currentText()
    #     script = os.path.realpath(__file__)
    #     scripts_dir = os.path.dirname(script)
    #     path = scripts_dir + '/action/{}'.format(action)
    #     return path


def main():
    import sys

    # app = QtWidgets.QApplication(sys.argv)
    ui = LoadDisplayMatWindow()

    ui.show()
    # sys.exit(app.exec_())
    return ui






# #tableView线程
# class tableViewWorker(QObject):
#     finished = Signal()
#     intReady = Signal(list)
#     def __init__(self,main_tableWidget):
#         super(tableViewWorker, self).__init__()
# 
#         self.main_tableWidget = main_tableWidget
# 
#         # self.work()
#     def work(self):
#         if self.Query_node_exist(om.MFn.kTransform, 'Mod_Grp'):
#             pNode = self.nameToNode('Mod_Grp')
#             meshNodes = self.Query_node_list(om.MFn.kMesh,pNode)
# 
# 
#         self.lay_main_tableWidget_HeaderLabels()
#         self.lay_main_tableWidget(meshNodes)
# 
# 
# 
# 
#         self.intReady.emit(meshNodes)
# 
#     def lay_main_tableWidget_HeaderLabels(self):
#         self.main_tableWidget.clear()
#         self.main_tableWidget.setColumnCount(3)
#         self.main_tableWidget.setHorizontalHeaderLabels(['node', '存在', '材质'])
#         self.main_tableWidget.setColumnWidth(0, 150)
#         self.main_tableWidget.setColumnWidth(1, 30)
#         self.main_tableWidget.setColumnWidth(2, 80)
# 
# 
#     def lay_main_tableWidget(self,Nodes):
#         for i in xrange(len(Nodes)):
# 
#             row_count = self.main_tableWidget.rowCount()
# 
#             self.main_tableWidget.insertRow(row_count)
#             mDagNode = om.MFnDagNode(Nodes[i])
# 
#             mesh_item = QTableWidgetItem(unicode(mDagNode.getPath()))
#             mesh_item.setFlags(Qt.ItemIsEnabled)
#             self.main_tableWidget.setItem(i, 0, mesh_item)
# 
# 
#     def Query_node_exist(self,nodetype,nodestring):
#         #返回指定对象是否存在
#         it = om.MItDependencyNodes(nodetype)
#         transformNodes = om.MObjectArray()
#         while not it.isDone():
#             transformNodes.append(it.thisNode())
#             it.next()
#         result = False
#         for transformNode in transformNodes:
#             mDagNode = om.MFnDagNode(transformNode)
#             transformName = mDagNode.fullPathName()
#             if transformName.find(nodestring):
#                 result = True
#                 break
#         return result
# 
#     def Query_node_list(self, nodetype, pNode):
#         # 返回指定父对象下的nodetype节点
#         it = om.MItDependencyNodes(nodetype)
#         meshNodes = om.MObjectArray()
# 
# 
#         while not it.isDone():
#             mDagNode = om.MFnDagNode(it.thisNode())
#             if mDagNode.hasParent(pNode) == True:
#                 meshNodes.append(it.thisNode())
#                 mDagNode = om.MFnDagNode(it.thisNode())
#                 # print mDagNode
#                 Node = mDagNode.fullPathName()
#                 # print Node
#             it.next()
#         # Nodes = om.MObjectArray()
#         # for meshNode in meshNodes:
#         #     mDagNode = om.MFnDagNode(meshNode)
#         #     Node = mDagNode.fullPathName()
#         #     print Node
#         #     if mDagNode.hasParent(pNode) == True:
#         #         Nodes.append(meshNode)
#         return meshNodes
# 
#     def nameToNode(self,name):
#         selectionList = om.MSelectionList()
#         selectionList.add(name)
#         node = selectionList.getDependNode(0)
#         return node
# 
# 
#     def kill_thread(self):
#         self.terminate()
# 
# 
# 
# 
# 
# 
# class startWorker(QObject):
#     logReady = Signal(str)
#     existReady = Signal(int, bool)
#     finished = Signal()
#     intReady = Signal(str,int,int,int)
# 
#     def __init__(self,nodes,matfile):
#         super(startWorker, self).__init__()
# 
#         self.matfile = matfile
#         self.nodes = nodes
#         # for i in nodes:
#         #     mDagNode = om.MFnDagNode(i)
#         #     # print mDagNode
#         #     Node = mDagNode.fullPathName()
#         #     print Node
# 
#             # self.printing = Node
#             # mu.executeDeferred(self.p)
# 
#         self.exist_nodes = []
# 
#         # self.work()
#     # def p(self):
#     #     print self.printing
#     def work(self):  # A slot takes no params
#         on_create_mesh = self.parsing_ma(self.matfile, 'mesh')
# 
#         for meshNode in self.nodes:
#             mDagNode = om.MFnDagNode(meshNode)
#             nodeName = mDagNode.getPath()
#             # nodePathName =mDagNode.fullPathName()
# 
#             if unicode(nodeName)in on_create_mesh:
#                 # slist = om.MSelectionList()
#                 # slist.add(meshNode)
#                 # om.MGlobal.setActiveSelectionList(slist)
#                 #
#                 # self.set_mesh_iod(unicode(nodeName))
#                 self.exist_nodes.append({'node': meshNode, 'num': list(self.nodes).index(meshNode)})
#                 result = True
#             else:
#                 result = False
# 
#             self.existReady.emit(list(self.nodes).index(meshNode), result)
# 
#         mat_info = self.parsing_ma(self.matfile, 'matinfo')
# 
#         ParDepNode = self.get_renderPartition()
#         lLinkDepNode = self.get_lightLinker()
#         rPar_plug = ParDepNode.findPlug('sets', False)
#         lonj_plug = lLinkDepNode.findPlug('link', False)
#         lsh_plug = lLinkDepNode.findPlug('shadowLink', False)
# 
# 
#         for sg in mat_info.keys():
#             try:
# 
#                 sgDagNode= om.MFnDependencyNode()
#                 sgDagNode.create('shadingEngine', sg)
# 
#                 sgp_plug = sgDagNode.findPlug('partition', False)
#                 sgm_plug = sgDagNode.findPlug('message', True)
# 
# 
#                 dg_mod = om.MDGModifier()
#                 dg_mod.connect(sgp_plug, rPar_plug.elementByLogicalIndex(-1))
#                 dg_mod.doIt()
# 
#                 ll_mod = om.MDGModifier()
#                 ll_mod.connect(sgm_plug, lonj_plug.elementByLogicalIndex(-1).child(0))
#                 ll_mod.doIt()
# 
#                 lo_mod = om.MDGModifier()
#                 lo_mod.connect(sgm_plug, lonj_plug.elementByLogicalIndex(-2).child(1))
#                 lo_mod.doIt()
# 
# 
#             # dg_mod = om.MDGModifier()
#             # dg_mod.connect(sgm_plug, lonj_plug.elementByLogicalIndex(-1).child(1))
# 
#             # try:
#             # print lonj_plug.elementByLogicalIndex(-1).child(1)
#             # ll_mod = om.MDGModifier()
#             # ll_mod.connect(sgm_plug, lonj_plug.elementByLogicalIndex(-1).child(1))
#             # ll_mod.doIt()
#             # # except Exception, Argument:
#             # #         print 'repr(Argument):\t\t', str(Argument)
#             # #         time.sleep(3)
#             #
#             # ls_mod = om.MDGModifier()
#             # ls_mod.connect(sgm_plug, lsh_plug.elementByLogicalIndex(-2).child(1))
#             # ls_mod.doIt()
# 
#             # if mat_info[sg].keys():
#             #     self.logReady.emit(mat_info[sg].keys())
#             #
#             #     try:
#             #         mat_name = pm.shadingNode('lambert', asShader=1, name=mat_info[sg].keys()[0])
#             #
#             #         sg_name = pm.sets(renderable=True, empty=True, noSurfaceShader=True, name=sg)
#             #         cmds.connectAttr('{}.outColor'.format(mat_name), '{}.surfaceShader'.format(sg_name).format(tex_node) , f=1)
#             #
#             except Exception, Argument:
#                     print 'repr(Argument):\t\t', str(Argument)
#                     self.finished.emit()
# 
# 
#                 # matDagNode = om.MFnDependencyNode()
#                 # matDagNode.create('lambert', mat_info[sg].keys()[0])
#                 #
#                 # # "// Assign new material\n",
#                 # # "shadingNode -asShader lambert -n ", material, ";\n",
#                 # # "sets -renderable true -noSurfaceShader true -empty -name ", materialSG, ";\n",
#                 # # "connectAttr -f ", material, ".outColor ", materialSG, ".surfaceShader;\n",
#                 # # "assignCreatedShader \"lambert\" \"\" ", material, " \"", object, "\";\n",
#                 # # "sets -e -forceElement ", materialSG, ";\n",
#                 # mat_plug = matDagNode.findPlug('outColor', False)
#                 # sg_plug = sgDagNode.findPlug('surfaceShader', False)
# 
#                 # dg_mod = om.MDGModifier()
#                 # dg_mod.connect(mat_plug, sg_plug)
#                 # dg_mod.doIt()
#         self.finished.emit()
# 
# 
# 
# 
#     def parsing_ma(self,path,nodetype):
# 
#         try:
#             madata = maya_ascii_parser.main(path,nodetype)
#             return madata
# 
#         except Exception, Argument:
#             print 'str(Argument):\t\t', str(Argument)
#             time.sleep(5)
# 
# 
# 
# 
#     def readInChunks(self,fileObj, chunkSize=1024 * 1024):
#         """
#         Lazy function to read a file piece by piece.
#         Default chunk size: 4kB.
#         """
#         while 1:
#             data = fileObj.read(chunkSize)
#             if not data:
#                 break
#             yield data
# 
#     def check_dir(self,des_path):
#         my_dir = os.path.exists(des_path)
#         if my_dir == True:
#             return 0
#         else:
#             os.makedirs(des_path.replace('\\','/'))
# 
# 
#     def kill_thread(self):
#         self.terminate()