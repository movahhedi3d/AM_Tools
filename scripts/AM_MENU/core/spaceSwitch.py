# python
import  os , subprocess
import re

# maya
import maya.cmds as mc
import maya.api.OpenMaya as om2


# AM_Tools 
from AM_MENU.core import utils
from AM_MENU.extensions import pyqt
from AM_MENU.extensions.Qt import QtWidgets ,QtGui , QtCore
from AM_MENU.ui import space_initializer_ui
from AM_MENU.ui import space_renamer_ui


# logging
import logging
LOG = logging.getLogger("Am Tools |")


maya_ver = int(utils.getMayaVer2())




class space_initializer(QtWidgets.QDialog, space_initializer_ui.Ui_Dialog):

    def __init__(self, parent=None):
        self.toolName = "space_initializer"
        super(space_initializer, self).__init__(parent=parent)
        self.setupUi(self)

        self.use_translate = True
        self.use_rotate = True
        self.cons_mode = "constraint"
        
        self.create_connections()
        self.setWindowTitle("Space Initializer")

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def create_connections(self):
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)

    def ok(self):
        self.use_translate = self.useTrans_chb.isChecked()
        self.use_rotate = self.useRotate_chb.isChecked()
        if self.by_blnd_rb.isChecked():
            self.cons_mode = "blnd"
        
    def cancel(self):
        LOG.warning("add new space Cancelled")


def exec_space_initializer(*args):

    windw = space_initializer()
    if windw.exec_():
        return windw





class space_renamer(QtWidgets.QDialog, space_renamer_ui.Ui_Dialog):

    def __init__(self, parent= None ):
        self.toolName = "space_renamer"
        super(space_renamer, self).__init__(parent=parent)
        self.setupUi(self)
        self.ctrl = None
        
        self.create_connections()
        self.setWindowTitle("Space Renamer")

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.get_space_item()
    
    
    def get_space_item(self):
        
        sel = mc.ls(sl=True)
        if sel:
            if mc.attributeQuery("space", node= sel[0], exists=True):
                self.ctrl = sel[0]
                enum_string = mc.attributeQuery('space', node= self.ctrl , listEnum=True)[0]
                enum_options = enum_string.split(":")
                
                self.renamerTable.setRowCount(len(enum_options))
                for i , item in enumerate(enum_options):
                    self.renamerTable.setItem( i , 0 , QtWidgets.QTableWidgetItem(item) )
                        
        
        
        
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)

    def ok(self):
        if self.ctrl:
            names_list = [(self.renamerTable.item(i , 0).text()).strip() for i in range(self.renamerTable.rowCount())]
            enum = ":".join(names_list)
            mc.addAttr(self.ctrl+".space" , e =True , enumName = enum)
            
    def cancel(self):
        LOG.warning("space rename Cancelled")



def exec_space_renamer(*args):

    windw = space_renamer(pyqt.maya_main_window())
    windw.show()







def add_new_space( *args ):
    
    cons_items = args[0]
    cons_nodes = cons_items
    ctrl = cons_nodes[-1]
    drivers = cons_nodes[:-1]
    
    cons_grp = get_space_cons_grp(ctrl)
    if not cons_grp:
        LOG.warning("cannot find Space group , first add Space group then try again")
        return
    
    if not mc.attributeQuery("consNode", node= cons_grp , exists=True):
        LOG.warning("not find consNode attribute ")
        return
        
    
    for item in ['tx','ty','tz','rx','ry','rz']:
        mc.setAttr(cons_grp+".%s"%item , l=False)
        
    
    
    space_atr = get_space_attr(ctrl)
    space_Options = [opt for opt in space_atr[1] if opt != "None"]
    space_idx = len(space_Options) 
    

    
    blend , cons_mode = get_constraint_node( cons_grp )
    
    if not blend :
        init_space = exec_space_initializer()
        if not init_space:
            return
        
        
        if init_space.cons_mode == "blnd":
            if int(maya_ver) < 2020 :
                cons_mode = "constraint"
                LOG.warning("Driver Node changed to Parent Constraint. blend matrix just available for mara 2020 and higher")
            else:
                cons_mode = init_space.cons_mode
        else:
            cons_mode = init_space.cons_mode
            
        
    
    if cons_mode == "blnd":
        
        if not blend :
            use_translate = init_space.use_translate
            use_rotate = init_space.use_rotate
            
            blend = mc.createNode("blendMatrix")
            m = mc.getAttr(cons_grp+".offsetParentMatrix")
            mc.setAttr(blend+".inputMatrix" , m , type="matrix")
            mc.connectAttr( blend+".message" , cons_grp+".consNode" , f=True)
            
        if not mc.attributeQuery("spaceUseTranslate", node= ctrl , exists=True):
            mc.addAttr(ctrl, ln="spaceUseTranslate", at="bool", defaultValue = use_translate, k=False)
        
        
        if not mc.attributeQuery("spaceUseRotate", node= ctrl , exists=True):
            mc.addAttr(ctrl , ln = "spaceUseRotate" , at="bool" , defaultValue = use_rotate , k=False )
        
        
        parent = utils.getParent(cons_grp)
        
        for i in range(1,50):
            targetMatrix_connection = mc.connectionInfo(blend+".target[{}].targetMatrix".format(i) , sfd = True)
            weight_connection = mc.connectionInfo(blend+".target[{}].weight".format(i) , sfd = True)
            if not targetMatrix_connection and not weight_connection:
                curent_blnd_index = i
                break
        
        
        enum_string = mc.attributeQuery('space', node= space_atr[0] , listEnum=True)[0]
        currentEnumNames = enum_string.split(":")
        
        newEnumNames        = currentEnumNames + [item.split("|")[-1] for item in drivers]
        enum = ":".join(newEnumNames )
        mc.addAttr(space_atr[0]+".space" , e =True , enumName = enum)
        
        
        
        for i , driver in enumerate(drivers):
            
            enum_idx = len(currentEnumNames) + i
            blnd_idx = curent_blnd_index + i
            
            connect_matrix_driver(blend, cons_grp , driver , blnd_idx , parent )
            
            target_attr = blend+".target[{}]".format(blnd_idx) 
            
            node_name = mc.createNode("condition")
            mc.connectAttr(space_atr[0]+".space" , node_name + ".firstTerm")
            mc.setAttr(node_name + ".secondTerm", enum_idx )
            mc.setAttr(node_name + ".operation", 0 )
            mc.setAttr(node_name + ".colorIfTrueR", 1)
            mc.setAttr(node_name + ".colorIfFalseR", 0)
            mc.connectAttr(node_name + ".outColorR", target_attr+".weight")
    
            mc.connectAttr(ctrl+".spaceUseTranslate" , target_attr+".useTranslate" )
            mc.connectAttr(ctrl+".spaceUseRotate" , target_attr+".useRotate" )
            
            
        if not mc.connectionInfo(cons_grp+".offsetParentMatrix" , sfd = True):
            mc.connectAttr( blend+".outputMatrix" , cons_grp+".offsetParentMatrix" ) 
            
            
            
    elif cons_mode == "constraint":
        
        customOpt = {"maintainOffset":True}
        connection = {}
        cons_t = mc.xform(cons_grp , q=True, m=True, ws=True)
        
        if blend:
            for item in ["t", "r"]:
                for x in ["x", "y", "z"]:
                    
                    con = mc.listConnections(cons_grp+".{}{}".format(item , x), p=True , s=True , d=False)
                    connection["{}{}".format(item , x)] = con
                    
                    if item == "t":
                        src_atr = mc.connectionInfo(cons_grp+".t{}".format(x) , sfd = True)
                        if src_atr:
                            mc.disconnectAttr( src_atr , cons_grp+".t{}".format(x))
                            mc.connectAttr(blend+".constraintTranslate{}".format( x.capitalize() ) , cons_grp+".t{}".format(x) , f=True)
                            
                    if item == "r":
                        src_atr = mc.connectionInfo(cons_grp+".r{}".format(x) , sfd = True)
                        if src_atr:
                            mc.disconnectAttr( src_atr , cons_grp+".r{}".format(x))
                            mc.connectAttr(blend+".constraintRotate{}".format( x.capitalize() ) , cons_grp+".r{}".format(x) , f=True)
                            
        else:
            if not init_space.use_translate:
                customOpt["skipTranslate"] = ["x", "y", "z"]
            if not init_space.use_rotate:
                customOpt["skipRotate"] = ["x", "y", "z"]
            
        
        
        cons_list = drivers + [cons_grp]
        cns_node = mc.parentConstraint(*cons_list , **customOpt )
        cns_attr = mc.parentConstraint(cns_node[0], query=True, weightAliasList=True)
        add_new_indx = len(cns_attr) - space_idx
        mc.connectAttr( cns_node[0]+'.message' , cons_grp+".consNode" , f=True )
        
        alias_list = [att.split(re.search(r'W\d+' , att).group())[0]  for att in cns_attr[add_new_indx*-1:]]
        enum = ":".join(space_atr[1] + alias_list)
        mc.addAttr(space_atr[0]+".space" , e =True , enumName = enum)
        
        
        if connection:
            for item , conct in connection.items():
                src_atr = mc.connectionInfo(cons_grp+".%s"%item , sfd = True)
                if src_atr:
                    mc.disconnectAttr( src_atr , cons_grp+".%s"%item )
                if conct:
                    mc.connectAttr(conct[0] , cons_grp+".%s"%item , f=True)
                    
            mc.xform(cons_grp , m= cons_t , ws=True)
            
        
        i = len(space_atr[1])
        for att in cns_attr[add_new_indx*-1:]:
            node_name = mc.createNode("condition")
            mc.connectAttr(space_atr[0]+".space" , node_name + ".firstTerm")
            mc.setAttr(node_name + ".secondTerm", i)
            mc.setAttr(node_name + ".operation", 0)
            mc.setAttr(node_name + ".colorIfTrueR", 1)
            mc.setAttr(node_name + ".colorIfFalseR", 0)
            mc.connectAttr(node_name + ".outColorR", att )
            i +=1
            
        mc.select(ctrl)
        
        
        




def switch_space_func(*args):
    
    auto_clav = None
    switch_control = args[0].split("|")[-1]
    switch_idx = args[1]
    
    autokey = mc.listConnections("{}.space".format(switch_control), type="animCurve")
    if autokey:
        mc.setKeyframe(switch_control , time=(mc.currentTime(query=True) - 1.0))
        
        if mc.attributeQuery( 'hasAutoClav', node=switch_control , exists=True ) :
            try:
                clav_ctrl = mc.listConnections(switch_control+'.hasAutoClav')[0]
                if clav_ctrl+".autoClav" != 0:
                    mc.setKeyframe(clav_ctrl , time=(mc.currentTime(query=True) - 1.0))
                    auto_clav = clav_ctrl
            except:
                pass
        
        
    
    changeSpace(switch_control ,  switch_idx )
    
    if autokey:
        mc.setKeyframe(switch_control ,time=(mc.currentTime(query=True)))
        if auto_clav:
            mc.setKeyframe(auto_clav ,time=(mc.currentTime(query=True)))
            




def changeSpace( ctl_name , cnsIndex ):
    
    namespace = utils.getNamespace(ctl_name)
    
    if namespace:
        ctl = namespace + ":" + stripNamespace(ctl_name)
    else:
        ctl = ctl_name
    
    
    if mc.attributeQuery("hasAutoClav" , n= ctl , exists=True):
        try:
            clav = mc.listConnections(ctl+".hasAutoClav" )[0]
            clavWM = mc.xform(clav , q=True, m=True , ws=True)
            sWM = mc.xform(ctl , q=True, m=True , ws=True)
            mc.setAttr(ctl+".space" , cnsIndex )
            
            if mc.getAttr( clav+".autoClav" ) == 0:
                mc.xform(ctl, m=sWM , ws=True)
            else:
                for i in xrange(5):
                    mc.xform(clav, m=clavWM , ws=True)
                    mc.xform(ctl, m=sWM , ws=True)
        except:
            pass
    else:
        sWM = mc.xform(ctl , q=True, m=True , ws=True)
        mc.setAttr(ctl+".space" , cnsIndex )
        mc.xform(ctl, m=sWM , ws=True)







def get_constraint_node( cons_grp ):
    cons_mode = ""
    blend = None
    consNodeList = mc.listConnections(cons_grp+".consNode", p=True , s=True , d=False)
    
    if not consNodeList:
        
        if mc.attributeQuery("offsetParentMatrix" , n= cons_grp , exists=True) and \
        mc.connectionInfo(cons_grp+".offsetParentMatrix" , sfd = True):
            blnd_node = mc.listConnections(cons_grp+".offsetParentMatrix", s=True , d=False)
            if blnd_node and mc.objectType(blnd_node[0]) == "blendMatrix" :
                blend = blnd_node[0]
                mc.connectAttr( blend+".message", cons_grp+".consNode", f=True )
                cons_mode = "blnd"
                
        else:
            for item in ["tx","ty","tz","rx","ry","rz"]:
                const = mc.listConnections(cons_grp+".%s"%item , s=True , d=False )
                if const and mc.objectType(const[0]) == "parentConstraint" :
                    blend = const[0]
                    mc.connectAttr( blend+".message", cons_grp+".consNode", f=True )
                    cons_mode = "constraint"
                    break
                    
    else:
        
        blend = mc.listConnections(cons_grp+".consNode", s=True , d=False)[0]
        if mc.objectType(blend) == "parentConstraint":
            cons_mode = "constraint"
        elif mc.objectType(blend) == "blendMatrix":
            cons_mode = "blnd"
        
    return blend , cons_mode
        
        






def connect_matrix_driver(blend, cons_grp, driver, blnd_idx, parent):
    
    mult = mc.createNode("multMatrix")
    
    cons_wm = mc.xform(cons_grp , q=True, m=True , ws=True)
    cons_m = mc.xform(cons_grp , q=True, m=True )
    driver_wm = mc.xform(driver , q=True, m=True , ws=True)
    
    cons_wmo = om2.MMatrix(cons_wm)
    cons_mo = om2.MMatrix(cons_m)
    driver_wmo = om2.MMatrix(driver_wm)
    
    offset = cons_wmo * cons_mo.inverse() * driver_wmo.inverse()
    mc.setAttr(mult+".matrixIn[0]", offset , type="matrix" )
    mc.connectAttr(driver+".worldMatrix[0]", mult+".matrixIn[1]" )
    
    if parent:
        mc.connectAttr(parent+".worldInverseMatrix[0]" , mult+".matrixIn[2]" , f=True )
    mc.connectAttr( mult+".matrixSum" , blend+".target[{}].targetMatrix".format(blnd_idx))
        
    


def get_space_attr(ctrl):
    
    if mc.attributeQuery("space", node=ctrl, exists=True):
        enum_string = mc.attributeQuery('space', node= ctrl , listEnum=True)[0]
        enum_options = enum_string.split(":")
    else:
        enum = "None"
        attr = mc.addAttr(ctrl , ln = 'space' , at="enum" ,en =enum , k=True)
        enum_options = ["None"]
    
    return ctrl , enum_options
    




def get_space_cons_grp(ctrl_name):
    
    ctrl = ctrl_name
    cons_grp = None
    i = 1
    while i < 10:
        parent = utils.getParent(ctrl , i)
        if not parent:
            break
            
        if ctrl.split("|")[-1] +'_space_cons' in parent.split("|")[-1] :
            cons_grp = parent
            break
        i += 1
    
    
    if cons_grp:
        if not mc.attributeQuery("consNode", node=cons_grp, exists=True):
            mc.addAttr(cons_grp , ln='consNode' , at="message", hidden=True )
    
    return cons_grp

    
    

def add_space_group( *args ):
    
    ctl_name = args[0]
    deep = 1
    if not mc.referenceQuery( ctl_name , inr=True):
        ctrl = ctl_name
        parent = utils.getParent(ctrl)
        child = utils.getParent(ctrl, deep-1)
        name = '%s_space_cons'%ctrl
        sub_trans = mc.createNode("transform", n=name)
        mtx = mc.xform(child, q=True, m=True, ws=True)
        mc.xform(sub_trans, m=mtx)
        if parent:
            mc.parent(sub_trans, parent)
        mc.parent(child , sub_trans)
        
    else:
        file_path   = (mc.referenceQuery( ctl_name ,filename=True,unresolvedName=True).replace('//' , '/'))
        refNode     = mc.referenceQuery(ctl_name ,referenceNode=True)
        _ctl_name   = ctl_name.split(':')[-1]
        add_subprocess_trans(file_path , _ctl_name, str(deep) )
        mc.file(referenceNode=refNode,loadReference=True)
        
        
        


    
def add_subprocess_trans(file_path , ctl_name, deep):
    
    scriptPath   = os.path.normpath(os.path.join(relativePath , "core" , "addSub_transform.py"))
    mayapy   = os.path.normpath(os.path.join(os.getcwd() , "mayapy.exe")).replace('\\' , '/')
    
    maya = subprocess.Popen(mayapy +' '+scriptPath +' '+ file_path +' '+ ctl_name+' '+deep ,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = maya.communicate()
    exitcode = maya.returncode
    if str(exitcode) != '0':
        LOG.error(err)
        LOG.error('error opening file: {}'.format(file_path))
    else:
        LOG.info('Successful create data for {}'.format(file_path))
        
       
       
       
       






