# -*- coding: utf-8 -*-

import os
import sys

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from maya import OpenMayaUI as omui
import maya.api.OpenMaya as om
import subprocess
from shiboken2 import wrapInstance
import time
import maya.cmds as cmds
import maya.mel as mm
import maya.utils as mu
import json



import maya_ascii_parser
reload(maya_ascii_parser)
import ui_Load_Mat
reload(ui_Load_Mat)



mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)


class LoadMatWindow(QMainWindow, ui_Load_Mat.Ui_LoadMatWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, *args, **kwargs):
        super(LoadMatWindow, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.pathlineEdit.setAcceptDrops(True)
        # self.pathlineEdit.setDragEnable()
        self.pathlineEdit.setText(r'Z:/TSP/Asset/Chars/Chars_01000ab/Mod/default/check/v005/Chars_01000ab_Mod_default_Mat.srn')


    @Slot()
    def on_pathlineEdit_editingFinished(self):
        path = self.pathlineEdit.text()
        self.srnpath = path.replace('\\', '/')
        self.matpath = self.srnpath.replace('.srn', '.ma')
        if os.path.exists(self.matpath) and os.path.exists(self.srnpath) == True:
            self.filelabel.setText('y')
        else:
            self.filelabel.setText('n')



    def tableworker_over(self,nodes):

        self.nodes = nodes

    @Slot()
    def on_extpushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet

        matfile = self.pathlineEdit.text()
        self.loadworker = startWorker(self.nodes, matfile)
        self.loadthread = QThread()
        self.loadworker.logReady.connect(self.loadthread_logReady)
        self.loadworker.existReady.connect(self.loadthread_existReady)
        self.loadworker.moveToThread(self.loadthread)
        self.loadworker.finished.connect(self.loadthread.quit)
        self.loadthread.started.connect(self.loadworker.work)
        print 'start'
        # 开始tableworker线程
        self.loadthread.start()

    def loadthread_logReady(self,log):
        print log
        import logging
        logging.basicConfig(level=10,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            filename=r'D:/work/Load_Display_Mat/text.log')
        logging.debug(str(log))

    def loadthread_existReady(self,num,result):
        # print self,num,result
        item = QTableWidgetItem(unicode(result))
        item.setFlags(Qt.ItemIsEnabled)
        self.main_tableWidget.setItem(num, 1, item)


    @Slot()
    def on_lookpushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "choose directory", r"C:", 'ma Files (*.srn)')
        self.pathlineEdit.setText(str(filename))

    @Slot()
    def on_cleanpushButton_clicked(self):
        with open(self.srnpath, 'r') as load_f:
            self.load_dict = json.load(load_f)

        # self.load_matfile()
        self.Query_node_exist()
        self.load_mat()

    def load_matfile(self):
        cmds.file(self.matpath,ignoreVersion=1, type="mayaAscii", namespace="temp_load_mat", i=1, ra=1,mergeNamespacesOnClash=False, options="v=0;",pr=1,importTimeRange="combine")
        # self.setup()

    def load_mat(self):

        print self.meshObjs
        print self.meshNames
        for sg in self.load_dict.keys():
            sgdict = self.load_dict[sg]
            shapelist = self.load_dict[sg].keys()
            for shape in shapelist:
                if not list(set([Name.find(shape) for Name in self.meshNames])) == [-1]:
                    if sgdict[shape]:
                        for face in sgdict[shape]:
                            cmds.select(face, r=1)
                        print shape, sgdict[shape]
                    else:
                        cmds.select(shape, r=1)
                    cmds.sets(forceElement='temp_load_mat:{}'.format(sg), e=1)



        # cmds.sets(forceElement='temp_load_mat:Chars_01000ab_Mod_ShaderNode_28', e=1)

    def Query_node_exist(self):
        # 返回指定对象是否存在
        it = om.MItDependencyNodes(om.MFn.kMesh)
        self.meshNodes = om.MObjectArray()
        self.meshObjs = []
        self.meshNames = []
        while not it.isDone():
            self.meshNodes.append(it.thisNode())
            it.next()
        for meshNode in self.meshNodes:
            self.meshObjs.append(meshNode)
            mDagNode = om.MFnDagNode(meshNode)
            meshName = mDagNode.fullPathName()
            self.meshNames.append(meshName)





def main():

    ui = LoadMatWindow()

    ui.show()

    return ui













