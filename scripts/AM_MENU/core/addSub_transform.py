import sys
import maya.standalone as std
std.initialize(name='python')
import maya.cmds as cmds
# import pymel.core as pm
filename = sys.argv[1]
ctl_name = sys.argv[2]
deep = sys.argv[3]




def addSub_transform( filename , ctl_name , deep):
    
    deep = int(deep)
    try:
        cmds.file(filename , open=True,  pmt=False , force=True)
        
        parent = getParent(ctl_name , deep)
        child = getParent(ctl_name , deep-1)
        name = ctl_name+'_space_cons'
        _grp = cmds.createNode("transform", n=name)
        mtx = cmds.xform(child, q=True, m=True, ws=True)
        cmds.xform(_grp, m=mtx)
        cmds.parent(_grp, parent)
        cmds.parent(child , _grp)
        
        cmds.file( save=True , force=True )
    
    except Exception, e:
        sys.stderr.write(str(e))
        sys.exit(-1)




def getParent(ctl_name , deep=1 ):
    
    current_parent = None
    ctrl = ctl_name
    for i in range(deep):
        _parent = cmds.listRelatives(ctrl , p=True)
        if _parent:
            current_parent = _parent[0]
            ctrl = current_parent
    if deep == 0:
        current_parent = ctl_name
    
    return current_parent



addSub_transform( filename , ctl_name , deep)









