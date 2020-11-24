# -*- coding: UTF-8 -*-
import sys
import os
import json
import glob




class MayaAsciiError(ValueError):
    pass



class MayaAsciiParser(object):

    def __init__(self, stream):
        super(MayaAsciiParser, self).__init__()
        self.__stream = stream
        # self.__command_handlers = {
        #     "requires": self._exec_requires,
        #     "fileInfo": self._exec_file_info,
        #     "file": self._exec_file,
        #     "createNode": self._exec_create_node,
        #     "setAttr": self._exec_set_attr,
        # }

    def parse(self,nodetype):
        self.file_reference = []
        self.connect_attr = []
        self.create_shadingEngine = []
        self.create_lambert = []
        self.create_RedshiftMaterial = []
        self.create_mesh = []
        self.create_file = []

        self.create_lambertAttr = []
        self.create_RedshiftMaterialAttr = []
        self.create_meshAttr = []
        self.create_fileAttr = []
        self.create_place2dTextureAttr = []

        self.get_matinfo = {}

        self.lambertattrList = []
        self.RedshiftMaterialattrList = []
        self.meshattrList = []
        self.fileattrList = []
        self.place2dTextureattrList = []
        self.attrkey = ''
        # if nodetype == 'file':
        #     return
        while self.__parse_next_command():
            pass
        # for i in self.attrList:
        #     print i

        if nodetype == 'reference':
            return self.file_reference

        elif nodetype == 'connectAttr':
            return self.connect_attr

        elif nodetype == 'shadingEngine':
            return self.create_shadingEngine

        elif nodetype == 'lambert':
            return self.create_lambert

        elif nodetype == 'RedshiftMaterial':
            return self.create_RedshiftMaterial

        elif nodetype == 'mesh':
            return self.create_mesh
        elif nodetype == 'file':
            return self.create_file

        elif nodetype == 'meshAttr':
            self.on_create_meshAttr(self.meshattrList)
            # print self.create_meshAttr
            return self.create_meshAttr

        elif nodetype == 'fileAttr':
            self.on_create_fileAttr(self.fileattrList)
            return self.create_fileAttr

        elif nodetype == 'place2dTextureAttr':
            self.on_create_place2dTextureAttr(self.place2dTextureattrList)
            return self.create_place2dTextureAttr

        elif nodetype == 'lambertAttr':
            return self.create_lambertAttr

        elif nodetype == 'RedshiftMaterialAttr':
            return self.create_RedshiftMaterialAttr

        elif nodetype ==  'matinfo':
            self.get_mat_info()
            return self.get_matinfo

        elif nodetype ==  'shaderinfo':
            self.get_shader_info()
            return self.get_shaderinfo




    def __parse_next_command(self):
        lines = []

        line = self.__stream.readline()


        while True:
            if not line:
                break
            elif line.startswith("//"):
                self.on_comment(line[2:].strip())

            else:
                line = line.rstrip("\r\n")
                if line and line.endswith(";"):
                    lines.append(line[:-1])
                    break
                elif line:
                    lines.append(line)
            line = self.__stream.readline()
            # if line.find('clothLow_6Shape') == -1:
            #     print line
        
        if lines:


            self.__parse_command_lines(lines)
            # self.__parse_command_lines_setAttr(lines)
            return True

        return False
    def on_comment(self, value):
        pass

    def register_handler(self, command, handler):
        self.__command_handlers[command] = handler

    def exec_command(self, command, args):
        handler = self.__command_handlers.get(command, None)
        if handler is not None:
            handler(args)

    # def has_command(self, command):
    #     return command in self.__command_handlers

    # def _exec_requires(self, args):
    #     if args[0] == "maya":
    #         self.on_requires_maya(args[1])
    #     else:
    #         self.on_requires_plugin(args[0], args[1])

    # def _exec_file_info(self, args):
    #     self.on_file_info(args[0], args[1])

    # def _exec_file(self, args):
    #     # print args
    #
    #     reference = False
    #     reference_depth_info = None
    #     namespace = None
    #     defer_reference = False
    #     reference_node = None
    #
    #     argptr = 0
    #     while argptr < len(args):
    #         arg = args[argptr]
    #         if arg in ("-r", "--reference"):
    #             reference = True
    #             argptr += 1
    #             self.on_file_reference(args[-1])
    #         elif arg in ("-rdi", "--referenceDepthInfo"):
    #             reference_depth_info = int(args[argptr + 1])
    #             argptr += 2
    #         elif arg in ("-ns", "--namespace"):
    #             namespace = args[argptr + 1]
    #             argptr += 2
    #         elif arg in ("-dr", "--deferReference"):
    #             defer_reference = bool(int(args[argptr + 1]))
    #             argptr += 2
    #         elif arg in ("-rfn", "--referenceNode"):
    #             reference_node = args[argptr + 1]
    #             argptr += 2
    #         elif arg in ('-op'):
    #             argptr += 2
    #         else:
    #             break
    #
    #     if argptr < len(args):
    #         path = args[argptr]
    #         # self.on_file_reference(path)

    # def _exec_create_node(self, args):
    #     nodetype = args[0]
    #
    #     name = None
    #     parent = None
    #
    #     argptr = 1
    #     while argptr < len(args):
    #         arg = args[argptr]
    #         if arg in ("-n", "--name"):
    #             name = args[argptr + 1]
    #             argptr += 2
    #         elif arg in ("-p", "--parent"):
    #             parent = args[argptr + 1]
    #             argptr += 2
    #         elif arg in ("-s", "--shared"):
    #             argptr += 1
    #         else:
    #             raise MayaAsciiError("Unexpected argument: %s" % arg)
    #
    #     self.on_create_node(nodetype, name, parent)

    # def _exec_set_attr(self, args):
    #     name = args.pop(0)[1:]
    #     attrtype = None
    #     value = None
    #
    #     argptr = 1
    #     while argptr < len(args):
    #         arg = args[argptr]
    #         if arg in ("-type", "--type"):
    #             attrtype = args[argptr + 1]
    #             value = args[argptr + 2:]
    #             argptr += 2
    #         else:
    #             # FIXME this is a catch-all; explicitly support flags
    #             argptr += 1
    #
    #     if not value:
    #         value = args[-1]
    #
    #     if not attrtype:
    #         # Implicitly convert between Python types
    #         # FIXME this isn't particularly safe?
    #         types = {
    #             str: "string",
    #             float: "double",
    #             int: "integer"
    #         }
    #
    #         try:
    #             attrtype = types[type(json.loads(value))]
    #
    #         except KeyError:
    #             attrtype = "string"
    #
    #         except ValueError:
    #             attrtype = types.get(type(value), "string")
    #
    #     self.on_set_attr(name, value, attrtype)
    def __parse_command_lines(self, lines):
        # Pop command name from the first line
        command, _, lines[0] = lines[0].partition(" ")
        command = command.lstrip()



        if command == 'connectAttr':
            self.on_connect_attr(lines[0])

        elif command == 'createNode':
            l = lines[0].split(" ")
            nodetype = l[0]
            nodename = l[int(l.index('-n') + 1)]
            # nodetype, _, content = lines[0].partition(" ")
            # pr, _, nodename = content.partition(" ")
            # print pr, _, nodename
            if nodetype == 'shadingEngine':
                self.on_create_shadingEngine(nodename)

            elif nodetype == 'lambert':
                self.on_create_lambert(nodename)

            elif nodetype == 'RedshiftMaterial':
                self.on_create_RedshiftMaterial(nodename)

            elif nodetype == 'mesh':
                self.on_create_mesh(nodename)

            elif nodetype == 'file':
                self.on_create_file(nodename)
        #mesh的面
        if command == 'createNode':
            l = lines[0].split(" ")
            nodetype = l[0]
            nodename = eval(l[int(l.index('-n')+1)])
            self.meshattrDict = {'name': nodename,'type':nodetype, 'setAttr_iog':[]}
            self.meshattrList.append(self.meshattrDict)


        elif command == 'setAttr':
            if not lines[0].find('.iog') == -1:
                self.meshattrDict['setAttr_iog'].append(lines[0])

        # file的文件路径
        if command == 'createNode':
            l = lines[0].split(" ")
            nodetype = l[0]
            nodename = eval(l[int(l.index('-n')+1)])
            self.fileattrDict = {'name': nodename,'type':nodetype, 'setAttr_ftn':[]}

            self.fileattrList.append(self.fileattrDict)

        elif command == 'setAttr':
            if not lines[0].find('.ftn') == -1:
                self.fileattrDict['setAttr_ftn'].append(lines[0])

        # place2dTexture的uv缩放
        if command == 'createNode':
            l = lines[0].split(" ")
            nodetype = l[0]
            nodename = eval(l[int(l.index('-n')+1)])
            self.place2dTextureattrDict = {'name': nodename,'type':nodetype, 'setAttr_re':[]}

            self.place2dTextureattrList.append(self.place2dTextureattrDict)

        elif command == 'setAttr':
            if not lines[0].find('.re') == -1:
                self.place2dTextureattrDict['setAttr_re'].append(lines[0])

        # lambert的color
        if command == 'createNode':
            l = lines[0].split(" ")
            nodetype = l[0]
            nodename = eval(l[int(l.index('-n')+1)])
            self.lambertattrDict = {'name': nodename,'type':nodetype, 'setAttr_c':[]}

            self.lambertattrList.append(self.lambertattrDict)

        elif command == 'setAttr':
            if not lines[0].find('.c') == -1:
                self.lambertattrDict['setAttr_c'].append(lines[0])

        # RedshiftMaterial的color
        if command == 'createNode':
            l = lines[0].split(" ")
            nodetype = l[0]
            nodename = eval(l[int(l.index('-n') + 1)])
            self.RedshiftMaterialattrDict = {'name': nodename, 'type': nodetype, 'setAttr_diff': []}

            self.RedshiftMaterialattrList.append(self.RedshiftMaterialattrDict)


        elif command == 'setAttr':
            if not lines[0].find('.diffuse_color') == -1:
                self.RedshiftMaterialattrDict['setAttr_diff'].append(lines[0])









         # print self.attrDict






        # Only process arguments if we handle this command
        # if self.has_command(command):
        #
        #     # Tokenize arguments
        #     args = []
        #     for line in lines:
        #         while True:
        #             line = line.strip()
        #             if not line:
        #                 break
        #
        #             # Handle strings
        #             if line[0] in "'\"":
        #                 string_delim = line[0]
        #                 escaped = False
        #                 string_end = len(line)
        #
        #                 for i in range(1, len(line)):
        #
        #                     # Check for end delimeter
        #                     if not escaped and line[i] == string_delim:
        #                         string_end = i
        #                         break
        #
        #                     # Check for start of escape sequence
        #                     elif not escaped and line[i] == "\\":
        #                         escaped = True
        #
        #                     # End escape sequence
        #                     else:
        #                         escaped = False
        #
        #                 # Partition string argument from the remainder
        #                 # of the command line.
        #                 arg, line = line[1:string_end], line[string_end + 1:]
        #
        #             # Handle other arguments
        #             # These, unlike strings, may be tokenized by whitespace
        #             else:
        #                 arg, _, line = line.partition(" ")
        #
        #             args.append(arg)
        #     self.exec_command(command, args)

    # def __parse_command_lines_setAttr(self, lines):
    #     # Pop command name from the first line
    #     command, _, lines[0] = lines[0].partition(" ")
    #
    #     command = command.lstrip()
    #     print command
    #
    #     if command == 'createNode':
    #
    #         nodetype, _, content = lines[0].partition(" ")
    #         pr, _, nodename = content.partition(" ")
    #
    #
    #         if nodetype == 'shadingEngine':
    #             self.on_create_shadingEngine(nodename)
    #
    #         elif nodetype == 'lambert':
    #             self.on_create_lambert(nodename)
    #
    #         elif nodetype == 'mesh':
    #             self.on_create_mesh(nodename)


    def on_requires_maya(self, version):
        pass

    def on_requires_plugin(self, plugin, version):
        pass
    def on_file_info(self, key, value):
        pass
    def on_create_file(self, name):
        self.create_file.append(unicode(eval(name)))

    def on_current_unit(self, angle, linear, time):
        pass

    def on_file_reference(self, path):
        self.file_reference.append(unicode(path))

    def on_create_shadingEngine(self, name):
        self.create_shadingEngine.append(unicode(eval(name)))

    def on_create_lambert(self, name):
        self.create_lambert.append(unicode(eval(name)))

    def on_create_RedshiftMaterial(self, name):
        self.create_RedshiftMaterial.append(unicode(eval(name)))



    def on_create_mesh(self, name):
        self.create_mesh.append(eval(unicode(name)))

    def on_create_meshAttr(self, attrList):
        for i in attrList:
            if i['type'] == 'mesh':
                self.create_meshAttr.append(i)
    def on_create_fileAttr(self, attrList):
        for i in attrList:
            if i['type'] == 'file':
                self.create_fileAttr.append(i)

    def on_create_place2dTextureAttr(self, attrList):
        for i in attrList:
            if i['type'] == 'place2dTexture':
                self.create_place2dTextureAttr.append(i)

    def on_create_lambertAttr(self, attrList):
        for i in attrList:
            if i['type'] == 'lambert':
                self.create_lambertAttr.append(i)

    def on_create_RedshiftMaterialAttr(self, attrList):
        for i in attrList:
            if i['type'] == 'RedshiftMaterial':
                self.create_RedshiftMaterialAttr.append(i)


    def on_select(self, name):
        pass

    def on_add_attr(self, node, name):
        pass

    def on_set_attr(self, name, value, type):
        pass

    def on_set_attr_flags(self, plug, keyable=None, channelbox=None, lock=None):
        pass

    def on_connect_attr(self, plug):
        self.connect_attr.append(unicode(plug))

    def get_mat_info(self):
        self.on_create_fileAttr(self.fileattrList)
        self.on_create_place2dTextureAttr(self.place2dTextureattrList)

        self.on_create_lambertAttr(self.lambertattrList)
        self.on_create_RedshiftMaterialAttr(self.RedshiftMaterialattrList)
        # print self.create_place2dTextureAttr
        self.get_matinfo = {}
        for sg in self.create_shadingEngine:
            # print self.create_RedshiftMaterial
            self.get_matinfo[sg] = {}
            for cot in self.connect_attr:
                cotlist = cot.split(" ")
                # 如果lambert
                if eval(cotlist[0]) in [m + ".oc" for m in self.create_lambert] and eval(cotlist[1]) == sg + ".ss":  # 如果lambert材质链接着着色组
                    c_connect = [c for c in self.connect_attr if not c.find(eval(cotlist[0]).split(".")[0] + ".c") == -1] #材质链接贴图的链接列表
                    # print c_connect
                    if c_connect:
                        c_file = [s_ftn for s_ftn in self.create_fileAttr if eval(c_connect[0].split(" ")[0]) == s_ftn['name'] + ".oc"][0]  # 获取材质diff链接的贴图文件的节点信息
                        connect_place2d = [p_f.split(" ") for p_f in self.connect_attr if eval(p_f.split(" ")[1]) == c_file['name']+".re"][0]  # 获取place2d链接的贴图文件节点的节点信息
                        if connect_place2d:
                            c_place2d = [s_re for s_re in self.create_place2dTextureAttr if s_re['name'] == eval(connect_place2d[0]).split(".")[0]][0]
                            if c_place2d['setAttr_re']:
                                c_place2d_re = [	float(c_place2d['setAttr_re'][0].split(" ")[-3]),	float(c_place2d['setAttr_re'][0].split(" ")[-2])]
                            else:
                                c_place2d_re = [1,1]
                        else:
                            c_place2d_re = [1,1]

                        self.get_matinfo[sg][eval(cotlist[0]).split(".")[0]] = {"file": eval(c_file['setAttr_ftn'][0].split(" ")[3]), "node": c_file['name'],"type":'tex','attr_re':c_place2d_re}
                    else:
                        # print eval(cotlist[0]).split(".")[0]
                        # print self.create_lambertAttr
                        c_attr =  [c for c in self.create_lambertAttr if eval(cotlist[0]).split(".")[0] == c['name']][0]['setAttr_c']
                        if c_attr:
                            setAttr_c = [float(c_attr[0].split(" ")[-4]),float(c_attr[0].split(" ")[-3]),float(c_attr[0].split(" ")[-2])]#['setAttr_c']
                        else:
                            setAttr_c =[0.5,0.5,0.5]
                        self.get_matinfo[sg][eval(cotlist[0]).split(".")[0]] = {"type": 'col', 'attr_diff': setAttr_c}

                elif eval(cotlist[0]) in [m + ".oc" for m in self.create_RedshiftMaterial] and eval(cotlist[1]) == sg + ".ss":  # 如果RedshiftMaterial材质链接着着色组
                    c_connect = [c for c in self.connect_attr if not c.find(eval(cotlist[0]).split(".")[0] + ".diffuse_color") == -1] #RedshiftMaterial材质链接贴图的链接列表
                    if c_connect:
                        # print c_connect
                        c_file = [s_ftn for s_ftn in self.create_fileAttr if eval(c_connect[0].split(" ")[0]) == s_ftn['name'] + ".oc"][0]  # 获取材质diff链接的贴图文件的节点信息
                        connect_place2d = [p_f.split(" ") for p_f in self.connect_attr if eval(p_f.split(" ")[1]) == c_file['name'] + ".re"][0]  # 获取place2d链接的贴图文件节点的节点信息
                        if connect_place2d:
                            c_place2d = [s_re for s_re in self.create_place2dTextureAttr if s_re['name'] == eval(connect_place2d[0]).split(".")[0]][0]
                            if c_place2d['setAttr_re']:
                                c_place2d_re = [float(c_place2d['setAttr_re'][0].split(" ")[-3]),float(c_place2d['setAttr_re'][0].split(" ")[-2])]
                            else:
                                c_place2d_re = [1, 1]
                        else:
                            c_place2d_re = [1, 1]

                        self.get_matinfo[sg][eval(cotlist[0]).split(".")[0]] = { "file": eval(c_file['setAttr_ftn'][0].split(" ")[3]), "node": c_file['name'], "type": 'tex','attr_re': c_place2d_re}
                    else:
                        c_attr =  [c for c in self.create_RedshiftMaterialAttr if eval(cotlist[0]).split(".")[0] == c['name']][0]['setAttr_diff']
                        if c_attr:
                            setAttr_c = [float(c_attr[0].split(" ")[-4]),float(c_attr[0].split(" ")[-3]),float(c_attr[0].split(" ")[-2])]#['setAttr_c']
                        else:
                            setAttr_c =[0.5,0.5,0.5]
                        self.get_matinfo[sg][eval(cotlist[0]).split(".")[0]] = {"type": 'col', 'attr_diff': setAttr_c}


    def get_shader_info(self):
        self.on_create_meshAttr(self.meshattrList)
        self.get_shaderinfo = {}
        for sg in self.create_shadingEngine:
            # print sg
            self.get_shaderinfo[sg] = {}
            for cot in self.connect_attr:
                cotlist = cot.split(" ")

                if eval(cotlist[1]) == sg+'.dsm':
                    # print eval(cotlist[0]).split(".")
                    # print eval(cotlist[0]).split(".")[1]
                    # print eval(cotlist[0]).split(".")[0]
                    # print cotlist
                    self.get_shaderinfo[sg][eval(cotlist[0]).split(".")[0]] = []

                    # if len(eval(cotlist[0]).split(".")) == 2 and eval(cotlist[0]).split(".")[1] =="iog":
                    if len(eval(cotlist[0]).split(".")) == 3 and eval(cotlist[0]).split(".")[1] =="iog" and eval(cotlist[0]).split(".")[0] in self.create_mesh:
                        f_list = []
                        if [f for f in [mesh['setAttr_iog'] for mesh in self.create_meshAttr if mesh['name'] == eval(cotlist[0]).split(".")[0]][0] if not f.find('.iog[0].og[{}].gcl'.format(eval(cotlist[0]).split(".")[2][3])) == -1]:
                            for face in [f for f in [mesh['setAttr_iog'] for mesh in self.create_meshAttr if mesh['name'] == eval(cotlist[0]).split(".")[0]][0] if not f.find('.iog[0].og[{}].gcl'.format(eval(cotlist[0]).split(".")[2][3])) == -1][0].split(" "):
                                if not face.find('f[') == -1:
                                    f_list.append(eval(face))

                        # f_list = [eval(face) ]
                        if f_list:
                            for f_set in f_list:
                                self.get_shaderinfo[sg][eval(cotlist[0]).split(".")[0]].append('{}.{}'.format(eval(cotlist[0]).split(".")[0],f_set))



def main(path,nodetyoe):

    with open(path, "r") as f:
        parser = MayaAsciiParser(f)

        return parser.parse(nodetyoe)
        if f:
            f.close()





# print main('S:/Load_Display_Mat/shader.ma','fileAttr')
# print main('S:/Load_Display_Mat/shader.ma','meshAttr')
# print main('S:/Load_Display_Mat/shader.ma','file')
# print main('S:/Load_Display_Mat/shader.ma','shaderinfo')
# print main('S:/Load_Display_Mat/shader.ma','matinfo')
# print main(r'Z:/TSP/Asset/Chars/Chars_01000ab/Rig/default/check/v005/Chars_01000ab_Rig_default.ma', 'matinfo')
# print main(r'Z:/TSP/Asset/Chars/Chars_01000ab/Rig/default/check/v005/Chars_01000ab_Rig_default.ma', 'shaderinfo')
# print main(r'Z:/TSP/Asset/Chars/Chars_01000ab/Mod/default/check/v006/Chars_01000ab_Mod_default.ma', 'matinfo')
# print main(r'Z:/TSP/Asset/Chars/Chars_01000ab/Mod/default/check/v006/Chars_01000ab_Mod_default_geo.ma', 'shaderinfo')








