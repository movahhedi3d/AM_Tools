import maya.api.OpenMaya as om2
import maya.OpenMayaUI as omui
import maya.cmds as mc


def getNamespace(modelName):
    if not modelName:
        return ""
    if len(modelName.split(":")) >= 2:
        nameSpace = ":".join(modelName.split(":")[:-1])
    else:
        nameSpace = ""
    return nameSpace


def getParent(nodeName , deep=1 ):
    
    current_parent = None
    current_node = nodeName
    for i in range(deep):
        _parent = mc.listRelatives(current_node , p=True)
        if _parent:
            current_parent = _parent[0]
            current_node = current_parent
    if deep == 0:
        current_parent = nodeName
    
    return current_parent



def uniqueName(nodeName):
    ctl_name = stripNamespace(nodeName.split("|")[-1])
    listItem = mc.ls(ctl_name)
    if len(listItem) > 1:
        return False
    else:
        return True



def stripNamespace(nodeName):
    return nodeName.split(":")[-1]


def mayaWinUi():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(main_window_ptr), QtWidgets.QMainWindow)


def getMayaVer():
    version = mc.about(apiVersion = True)
    return version
    
def getMayaVer2():
    version = mc.about(version = True)
    return version
    
    

# ===============================================================

def get_MObject(node_name):
    if isinstance(node_name, om2.MObject):
        return node_name
 
    if isinstance(node_name, om2.MDagPath):
        return node_name.node()
 
    slist = om2.MSelectionList()
    try:
        slist.add(node_name)
    except RuntimeError:
        assert False, 'The node: "'+node_name+'" could not be found.'
 
    matches = slist.length()
    assert (matches == 1), 'Multiple nodes found for the same name: '+node_name
 
    obj = slist.getDependNode(0)
    return obj


def get_MPlug(obj, attribute):
    if not isinstance(obj, om2.MObject):
        assert False, "expected MObject"
    dep = om2.MFnDependencyNode(obj)
    plug = om2.MPlug()
    try:
        plug = dep.findPlug( attribute, True)
    except RuntimeError:
        assert False, 'The attribute: "'+attribute+'" could not be found.'
           
    assert (not plug.isNull), 'The attribute: "'+attribute+'" could not be found.'
    return plug

        



