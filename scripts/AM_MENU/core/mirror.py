import re
import maya.cmds as mc
from AM_MENU.core import  utils
import maya.api.OpenMaya as om


def mirrorPose(flip=False , nodes=None):
    
    if nodes is None:
        nodes = mc.ls(sl=True)
        
    
    
    mc.undoInfo(ock=1)
    try:
        nameSpace = False
        if nodes:
            nameSpace = utils.getNamespace(nodes[0])

        mirrorEntries = []
        for oSel in nodes:
            mirrorEntries.extend(gatherMirrorData(nameSpace, oSel, flip))

        for dat in mirrorEntries:
            if dat["attr"] in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]:
                applyMirror(nameSpace, dat)
    except Exception as e:
        om.MGlobal.displayWarning("Flip/Mirror pose fail")
        import traceback
        traceback.print_exc()
        print(e)
    finally:
        mc.undoInfo(cck=1)








def applyMirror(nameSpace, mirrorEntry):
    
    node = mirrorEntry["target"]
    attr = mirrorEntry["attr"]
    val = mirrorEntry["val"]
    
    try:
        _lock = mc.getAttr(node+".%s"%attr , l=True)
        if (mc.attributeQuery(attr, node=node, shortName=True, exists=True) and not _lock ):
            mc.setAttr(node+".%s"%attr , val )
            
    except RuntimeError as e:
        pass




def gatherMirrorData(nameSpace, node, flip):
    
    if isSideNode(node):
        nameParts = swapSideLabelNode(node)
        nameTarget = ":".join([nameSpace, nameParts])
        return calculateMirrorData(node, nameTarget, flip=flip)
    else:
        return calculateMirrorData(node, node, flip=False)




def swapSideLabelNode(node):
    
    name = utils.stripNamespace(node)
    sw_name = swapSideLabel(name)
    if name != sw_name:
        return sw_name
    
    if mc.attributeQuery("side_meta", n=node, exists=True):
        data = get_side_data(node)
        side = data["side"]
        if side in "LR":
            cm_side = ""
            if side == "L":
                cm_side = data["R_label"]
            elif side == "R":
                cm_side = data["L_label"]
            return utils.stripNamespace(node).replace(data["C_label"], cm_side)
        else:
            return utils.stripNamespace(node)
            
    else:
        return swapSideLabel(utils.stripNamespace(node))




def isSideNode(node):
    if mc.attributeQuery("side_meta", n=node, exists=True):
        data = get_side_data(node)
        if data["side"] in "LR":
            return True
        else:
            return False
    else:
        return isSideElement(node)




def isSideElement(name):
    if "L_" in name or "R_" in name:
        return True
    else:
        return False
        


def get_side_data(node):
    data = mc.getAttr( node+".side_meta").split("|")
    dict_data = {
        "side":data[0],
        "L_label":data[1],
        "R_label":data[2],
        "C_label":data[3],
    }
    return dict_data

        


def calculateMirrorData(srcNode, targetNode, flip=False):
    results = []

    for attrName in listAttrForMirror(srcNode):
        invCheckName = "inv{0}".format(attrName.lower().capitalize())
        if not mc.attributeQuery(invCheckName, node=srcNode, shortName=True, exists=True):
            inv = 1
        else:
            inv = -1 if mc.getAttr(srcNode+".%s"%invCheckName) else 1
            
        invAttrName = swapSideLabel(attrName) if isSideElement(attrName) else attrName

        if flip:
            atr_val = mc.getAttr('%s.%s' %(targetNode, attrName))
            results.append({"target": srcNode, "attr": invAttrName, "val": atr_val * inv})
        
        atr_val = mc.getAttr('%s.%s' %(srcNode, attrName))
        results.append({"target": targetNode, "attr": invAttrName, "val": atr_val * inv})
        
    return results



def listAttrForMirror(node):
    res = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]
    res.extend(mc.listAttr(node, userDefined=True, shortNames=True))
    res = list([x for x in res if not x.startswith("inv")])
    res = list([x for x in res if mc.attributeQuery( x , node= node, attributeType=True ) 
                not in ["message", "string"]])
    return res





def swapSideLabel(name):
    for part in name.split("_"):
        if re.compile("L").match(part):
            try:
                return re.compile("L_").sub(r"R_", name)
            except:
                return re.compile("_L").sub(r"_R", name)
                
        if re.compile("R").match(part):
            try:
                return re.compile("R_").sub(r"L_", name)
            except:
                return re.compile("_R").sub(r"_L", name)
                
    else:
        if "_L_" in name:
            return name.replace("_L_", "_R_")
        elif "_R_" in name:
            return name.replace("_R_", "_L_")
        else:
            return name









    
    
    