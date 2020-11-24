# -*- coding: UTF-8 -*-
# .@FileName:start
# .@Date:2020-11-17:15:18
# .@Aurhor:LuoOu
# cmds.sets()
import sys

G_ext_plugin_path = r'S:/Load_Display_Mat'
if G_ext_plugin_path not in sys.path:
    sys.path.append(G_ext_plugin_path)

if __name__ == '__main__':
    try:

        import Load_Display_Mat

        reload(Load_Display_Mat)
        Load_Display_Mat.main()
    except Exception, Argument:
        print 'str(Argument):\t\t', str(Argument)



