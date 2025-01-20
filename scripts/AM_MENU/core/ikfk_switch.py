import maya.cmds as mc
import maya.api.OpenMaya as om2
import re
import traceback
from AM_MENU.core.python_utils import  Object
from AM_MENU.extensions.six.moves import xrange



def switch_func(addKey = False , match_relatives = False):
    __Switch.switch( addKey , match_relatives)
    

class __Switch(Object):
    
    IKFK_cls    =   {}
    
             
    @classmethod
    def switch(cls , addKey = False , match_relatives = False):
        
        sel   = mc.ls(sl = True, l=True)
        if not sel:
            return
            
        _input = sel[0]

        if mc.attributeQuery('match_nodes', n= _input ,ex=True):
            
            setting_node_list   = []
            sub_comp            = None
            root_comp           = mc.listConnections('%s.match_nodes' % _input)[0]
            if mc.attributeQuery('componentType', n= root_comp , ex=True): 
                setting_node_list.append( mc.ls(root_comp , l=True)[0] )
            elif mc.attributeQuery('SubComponentType', n= root_comp , ex=True):
                sub_comp = mc.listConnections('%s.match_nodes' % _input)[0]
                setting_node    = mc.ls(sub_comp , l=True)[0]
                comp_name = mc.listConnections('%s.comp_relationship' % setting_node)[0]
                root_comp = mc.ls(comp_name , l=True)[0]
                subType = mc.getAttr(setting_node + '.SubComponentType')
                
                
                if match_relatives:
                    relatives_nodes  = mc.listConnections('%s.comp_relationship' % root_comp)
                    for item in relatives_nodes:
                        if mc.getAttr(item + '.SubComponentType') == subType:
                            sub_setting    = mc.ls(item , l=True)[0]
                            setting_node_list.append( sub_setting )
                    
                else:
                    setting_node_list.append( setting_node )
                    
                
                
            if not setting_node_list:
                raise RuntimeError("Cannot find setting group, make sure you are using original rig.")
            
            for setting_node in setting_node_list:
                getSelNode      = om2.MGlobal.getSelectionListByName(setting_node)
                dag_node        = getSelNode.getDagPath(0)
                node_name       = dag_node.fullPathName()
                
                connector_list = []
                if mc.objExists(node_name + ".connector"):
                    connected = mc.listConnections('%s.connector' % node_name)
                    if connected:
                        for conctor in connected:
                            conctorNode         = om2.MGlobal.getSelectionListByName(conctor)
                            conctordag_node     = conctorNode.getDagPath(0)
                            conctorFullName     = conctordag_node.fullPathName()
                            instance_connector  = cls.IKFK_cls.get(conctorFullName)
                            
                            if not instance_connector :
                                instance_connector              = AM_Switch_IKFK(conctordag_node , cls)
                                cls.IKFK_cls[conctorFullName]   =   instance_connector
                            
                            if node_name not in instance_connector.connector:
                                instance_connector.connector.append(node_name)
                            
                            connector_list.append(conctorFullName)
                            
                instance_switch = cls.IKFK_cls.get(node_name)
                if not instance_switch:
                    instance_switch = AM_Switch_IKFK(dag_node , cls)
                    cls.IKFK_cls[node_name]   = instance_switch
                    
                for comp in connector_list:
                    if comp not in instance_switch.connector:
                        instance_switch.connector.append(comp)
                    
                    
                instance_switch.run(addKey, match_relatives)
            



class AM_Switch_IKFK(Object):
    
    def __init__(self, node_dag , __Switch):
        
        self.__Switch               = __Switch
        self.node_dag               = node_dag
        self.blend_attr             = None
        self.comp_root              = None
        self.comp_setting           = None
        self.ctrl_setting           = None
        self.clavicle_control       = None
        
        
        self.fk_control_list        = []
        self.fk_match_list          = []
        self.fk_sec_list            = []
        
        self.ik_control_list        = []
        self.ik_match_list          = []
        self.ik_sec_list            = []
        
        self.mutual_control_list    = []
        self.mutual_match_list      = []
        self.mutual_sec_list        = []
        
        self.ik_foot_control_list   = []
        self.key_ctrlList           = []
        self.connector              = []
        
        self.gather_node_info()
        

    def gather_node_info(self):
        
        
        # |  general data ---------------------------------------------------------------
        
        
        self.comp_setting   = self.node_dag.fullPathName()
        
        if mc.attributeQuery('componentType', n= self.comp_setting , ex=True): 
            self.comp_root      = self.comp_setting
        elif mc.attributeQuery('SubComponentType', n= self.comp_setting , ex=True):
            comp_name = mc.listConnections('%s.comp_relationship' % self.comp_setting)[0]
            self.comp_root      = mc.ls(comp_name , l=True)[0]
        
        
        self.ctrl_setting   = mc.listConnections('%s.setting_ctrl' % self.comp_root)[0]
        
        blend_attr_name = 'ikFkBlend'
        if mc.attributeQuery('tag',n= self.comp_setting ,ex=True):
            tag = mc.getAttr(self.comp_setting + '.tag')
            blend_attr_name = tag+'_ikFkBlend'
            
        for attr in mc.listAttr(self.ctrl_setting ,userDefined=True,keyable=True) or []:
            if (not attr.endswith(blend_attr_name) or mc.addAttr("{}.{}".format(self.ctrl_setting, attr),query=True, usedAsProxy=True)):
                continue
                
            self.blend_attr = attr
            break
        
        
        # |  valid Item  ---------------------------------------------------------------
        match_nodes_full_path_list  = mc.listConnections('%s.match_nodes' % self.comp_setting )
        match_nodes_name_list       = [node.split('|')[-1].split(':')[-1] for node in match_nodes_full_path_list]
        
                    
        
        if mc.objExists(self.comp_setting + ".fkControls"):
            param_fk_control_list   = eval(mc.getAttr(self.comp_setting + '.fkControls'))
            fk_control_list         = [match_nodes_full_path_list[match_nodes_name_list.index(node)] for node in param_fk_control_list if node in match_nodes_name_list]
            self.fk_sec_list        = [ item for item in fk_control_list if mc.attributeQuery('Am_secCtrl',n=item ,ex=True)]
            self.fk_control_list    = [ item for item in fk_control_list if item not in self.fk_sec_list]
            self.key_ctrlList.append(fk_control_list)
            
            if mc.objExists(self.comp_setting + ".fkMatchTransforms"):
                param_fk_match_list     = eval(mc.getAttr(self.comp_setting + '.fkMatchTransforms'))
                self.fk_match_list = [match_nodes_full_path_list[match_nodes_name_list.index(node)] for node in param_fk_match_list if node in match_nodes_name_list]
                
            
            
        if mc.objExists(self.comp_setting + ".ikControls"):
            param_ik_control_list   = eval(mc.getAttr(self.comp_setting + '.ikControls'))
            ik_control_list         = [match_nodes_full_path_list[match_nodes_name_list.index(node)] for node in param_ik_control_list if node in match_nodes_name_list]
            self.ik_sec_list        = [ item for item in ik_control_list if mc.attributeQuery('Am_secCtrl',n=item ,ex=True)]
            self.ik_control_list    = [ item for item in ik_control_list if item not in self.ik_sec_list]
            self.key_ctrlList.append(ik_control_list)
            
            if mc.objExists(self.comp_setting + ".ikMatchTransforms"):
                param_ik_match_list     = eval(mc.getAttr(self.comp_setting + '.ikMatchTransforms'))
                self.ik_match_list = [match_nodes_full_path_list[match_nodes_name_list.index(node)] for node in param_ik_match_list if node in match_nodes_name_list]
                


        if mc.objExists(self.comp_setting + ".mutual_ikfkControls"):
            param_mutual_control_list   = eval(mc.getAttr(self.comp_setting + '.mutual_ikfkControls'))
            mutual_control_list         = [match_nodes_full_path_list[match_nodes_name_list.index(node)] for node in param_mutual_control_list if node in match_nodes_name_list]
            self.mutual_sec_list        = [ item for item in mutual_control_list if mc.attributeQuery('Am_secCtrl',n=item ,ex=True)]
            self.mutual_control_list    = [ item for item in mutual_control_list if item not in self.mutual_sec_list]
            self.key_ctrlList.append(mutual_control_list)
            
            if mc.objExists(self.comp_setting + ".mutualMatchTransforms"):
                param_mutual_match_list     = eval(mc.getAttr(self.comp_setting + '.mutualMatchTransforms'))
                mutual_match_list           = [match_nodes_full_path_list[match_nodes_name_list.index(node)] for node in param_mutual_match_list if node in match_nodes_name_list]
                self.mutual_match_list      = [item for item in mutual_match_list if item not in self.mutual_sec_list ]
                
            
            
        if mc.objExists(self.comp_setting + ".footIkControls"):
            param_ik_foot_control_list = eval(mc.getAttr(self.comp_setting + '.footIkControls'))
            self.ik_foot_control_list = [match_nodes_full_path_list[match_nodes_name_list.index(node)] for node in
                                     param_ik_foot_control_list if node in match_nodes_name_list]
            for item in self.ik_foot_control_list :
                self.ik_sec_list.append(item)


        if mc.objExists(self.comp_setting + ".clavicleCtrl"):
            clavicle_control_name = mc.getAttr(self.comp_setting + ".clavicleCtrl")
            if clavicle_control_name in match_nodes_name_list:
                self.clavicle_control = match_nodes_full_path_list[match_nodes_name_list.index(clavicle_control_name)]
                self.key_ctrlList.append(self.clavicle_control)
                

    

    # | SWITCH  ::::::::: STEP 1 :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # | get transform and reset to defult secondary ctrl 
    
    def switch_step_1(self , value , add_key ):
        

        self.scaleValues            =   []
        self.ik_match_transform     =   []
        self.fk_match_transform     =   []
        self.mutual_transform       =   []
        
        
        if self.clavicle_control:
            self.clavicle_trans = mc.xform(self.clavicle_control, q=True, ws=True, matrix=True)
        
        if mc.objExists(self.comp_setting + ".ref_stretchTop"):
            self.scaleValues = [mc.getAttr('%s.%s' % (self.comp_setting , atr)) for atr in ['ref_stretchTop' , 'ref_stretchBottom']]
        
        
        mutual_list = []
        if self.mutual_match_list : 
            mutual_list = self.mutual_match_list
        elif self.mutual_control_list : 
            mutual_list = self.mutual_control_list

        if mutual_list:
            for item in mutual_list :
                self.mutual_transform.append( mc.xform(item , q=True, ws=True, matrix=True) )
                
            for item in self.mutual_sec_list:
                self.set_default_value( item )
            
        
        if value == 1:
            fkControls = self.fk_control_list
            for node in self.fk_match_list :
                self.fk_match_transform.append(mc.xform(node, q=True, ws=True, rotation =True))
            
            
            # |  set defult ctrls ---------------------------------------------------------------
            self.set_default_value(self.fk_sec_list)
            self.set_default_value(fkControls , ['tx','ty','tz','sx','sy','sz'])
        
        
        
        elif value == 0:
            
            if self.ik_control_list and self.ik_match_list :
                
                self.set_default_value(self.ik_control_list[1] , ['softStretch','pvPin','twist'])
                normal        = self.getPlaneNormal(self.ik_match_list[:3])
                newPvPos      = self.getPvPosition( self.ik_match_list[:3] , normal)
                ik_ctrl_pos   = mc.xform(self.ik_match_list[2], q=True, ws=True, matrix=True)
                
                self.ik_match_transform.append(newPvPos)
                self.ik_match_transform.append(ik_ctrl_pos)
                
                # get transform from other part in the limb , except of 3 main transform
                for item in self.ik_match_list[3:]:
                    tra = mc.xform( item , q=True, ws=True, matrix=True)
                    self.ik_match_transform.append(tra)
                    
                
            # |  set defult ctrls ---------------------------------------------------------------
            self.set_default_value(self.ik_sec_list)

        if add_key:
            self.addKeyframe( 1 )


   
    # | SWITCH  ::::::::: STEP 2 :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # | switch and set transform based on before step data
    
    def switch_step_2 (self , value ):
        
        if value == 1:
            mc.setAttr("%s.%s" % (self.ctrl_setting , self.blend_attr), 0)
            mc.getAttr("%s.%s" % (self.ctrl_setting , self.blend_attr))
            mc.setAttr("%s.%s" % (self.ctrl_setting , self.blend_attr), 0)
        
            
            if self.scaleValues:
                attrList = ('stretchTop', 'stretchBottom')
                for scaleValue , attr in zip(self.scaleValues , attrList):
                    mc.setAttr(self.ctrl_setting + '.' + attr , scaleValue)
                    
            if self.clavicle_control:
                if mc.objExists( self.clavicle_control + ".autoClav"):
                    for i in xrange(20):
                        # limb
                        for t , ctrl in zip(self.fk_match_transform , self.fk_control_list[:3]):
                            mc.xform(ctrl, ws=True, rotation = t )
                        # clav
                        mc.xform(self.clavicle_control, ws=True, matrix = self.clavicle_trans )
                else:
                    for t , ctrl in zip(self.fk_match_transform , self.fk_control_list[:3]):
                        mc.xform(ctrl, ws=True, rotation = t )
            else:
                for t , ctrl in zip(self.fk_match_transform , self.fk_control_list[:3]):
                    mc.xform(ctrl, ws=True, rotation = t )
        
            
            
        # |  To ik   ---------------------------------------------------------------
        elif value == 0:
            
            mc.setAttr("%s.%s" % (self.ctrl_setting , self.blend_attr), 1)
            mc.getAttr("%s.%s" % (self.ctrl_setting , self.blend_attr))
            mc.setAttr("%s.%s" % (self.ctrl_setting , self.blend_attr), 1)
            
            if self.scaleValues :
                attrList = ('stretchTop', 'stretchBottom')
                for scaleValue, attr in zip( self.scaleValues , attrList ):
                    mc.setAttr(self.ctrl_setting + '.' + attr , scaleValue)
            
            if self.ik_control_list:
                mc.xform("%s" % (self.ik_control_list[1]), ws=True, matrix= self.ik_match_transform[1] )
                mc.xform("%s" % (self.ik_control_list[0]), ws=True, t = self.ik_match_transform[0] )
            
            # Match Clav
            if self.clavicle_control:
                if mc.objExists(self.clavicle_control + ".autoClav" ):
                    for i in xrange(10):
                        mc.xform(self.clavicle_control, ws=True, matrix= self.clavicle_trans )
                        mc.xform("%s" % (self.ik_control_list[0]), ws=True, t= self.ik_match_transform[0] )
                else:
                    mc.xform(self.clavicle_control, ws=True, matrix= self.clavicle_trans )
                    mc.xform("%s" % (self.ik_control_list[0]), ws=True, t= self.ik_match_transform[0] )
                    
        
        if self.mutual_transform:
            for item , t in zip(self.mutual_control_list , self.mutual_transform) :
                mc.xform(item , ws=True , matrix = t )
        
    
    
    
    # | SWITCH  ::::::::: STEP 3 :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # | switch and set other transform (except of 3 main fk control in the limb) based on step 2
    
    def switch_step_3 (self , value , revrs = True ):
        
        if value == 1:
            for t , ctrl in zip(self.fk_match_transform[3:] , self.fk_control_list[3:]):
                mc.xform(ctrl, ws=True, rotation = t )
            
        
        if value == 0:
            
            match_tra = self.ik_match_transform[2:]
            ctrl_item = self.ik_control_list[2:]
            
            if revrs:
                match_tra = match_tra[::-1]
                ctrl_item = ctrl_item[::-1]
                
            for tra , ctrl in zip(match_tra , ctrl_item ):
                mc.xform(ctrl, ws=True, matrix = tra )
                
            
            
            
    
    
    def addKeyframe(self , Stage = 1 ):
        key_list = self.key_ctrlList
        key_list.append( "%s.%s" % (self.ctrl_setting , self.blend_attr) )
        key_list.append( "%s.stretchTop" % (self.ctrl_setting ) )
        key_list.append( "%s.stretchBottom" % (self.ctrl_setting ) )

        if Stage == 1 :
            [mc.setKeyframe( elem , time=(mc.currentTime(query=True) - 1.0)) for elem in key_list]
        elif Stage == 2 :
            [mc.setKeyframe( elem , time=(mc.currentTime(query=True))) for elem in key_list]




    def getPvPosition(self , match_list , normal):
        
        if len(match_list) != 3:
            raise RuntimeError("{0} must be a lenght of three and a list.".format(match_list))
        
        size = 5.0
        if mc.attributeQuery('pv_distance', n= self.ik_control_list[0] ,ex=True):
            size = mc.getAttr(self.ik_control_list[0] + '.pv_distance')
        
        match1Pos = mc.xform(match_list[0], q=True, ws=True, t=True)
        match2Pos = mc.xform(match_list[1], q=True, ws=True, t=True)
        match3Pos = mc.xform(match_list[2], q=True, ws=True, t=True)
        
        vector1 = om2.MVector(*match1Pos)
        vector2 = om2.MVector(*match2Pos)
        vector3 = om2.MVector(*match3Pos)
        
        v = vector3 - vector1
        v = normal ^ v
        v.normalize()
        v *= size
        v += vector2
        
        return v
    
    
    def getPlaneNormal(self , match_list):
        
        if len(match_list) != 3:
            raise RuntimeError("{0} must be a length of three and a list.".format(match_list))
        mid_vec = om2.MVector(*mc.xform(match_list[1], q=True, ws=True, t=True))
        first_node_vec = om2.MVector(*mc.xform(match_list[0], q=True, ws=True, t=True))
        last_node_vec = om2.MVector(*mc.xform(match_list[-1], q=True, ws=True, t=True))
        vector0 = mid_vec - first_node_vec
        vector1 = last_node_vec - first_node_vec
        vector0.normalize()
        vector1.normalize()
        normal = vector1 ^ vector0
        
        return normal
    
    
    def set_default_value(self , objs , attribute=  [ "tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]):
        
        if not objs:
            return
            
        if not isinstance(objs, list):
            objs = [objs]
        
        for item in objs:
            for atr in attribute:
                if not mc.attributeQuery(atr , n= item , ex=True):
                    continue
                
                dv = mc.attributeQuery(atr , node= item , listDefault=True)[0]
                try:
                    mc.setAttr("%s.%s" % (item, atr ), dv )
                except RuntimeError:
                    pass
    
    
    
    
    def run(self , addKey = False , match_relatives = False):
        
        SubComp = None
        comp_type           = mc.getAttr(self.comp_root + '.componentType')
        comp_vers           = mc.getAttr(self.comp_root + '.componentVersion')
        if mc.attributeQuery('SubComponentType', n= self.comp_setting , ex=True):
            SubComp = mc.getAttr(self.comp_setting + '.SubComponentType')
            
            
        
        if mc.attributeQuery('is_AmRig2', n= self.comp_root , ex=True):
            match_operation     = self.AmRig2_match_func(comp_type , comp_vers , SubComp)
        else:
            match_operation     = self.match_func(comp_type)
            
        if match_operation:
            eval("self.%s" %match_operation )(addKey)
            
        

        
    @staticmethod
    def match_func(comp_type):
        if re.search(r'leg2__03' , comp_type ):
            return 'switchStyle_1'
            
        elif re.search(r'arm__\d{2}' , comp_type ) or re.search(r'leg2__\d{2}' , comp_type ):
            return 'standard_Switch'
        
        elif re.search(r'hand__\d{2}' , comp_type ) or re.search(r'foot__01' , comp_type ):
            return 'switchStyle_2'
            
        else:
            return None
    
    
    @staticmethod
    def AmRig2_match_func(comp_type , ver, SubComp= None):
        
        comp_type = SubComp if SubComp else comp_type
        
        vers_list = [int(i) for i in ver.split(",")]
            
        if re.search(r'arm_\d{2}' , comp_type ):
            if vers_list[1] == 1:
                return 'standard_Switch'
                
        elif re.search(r'leg2_\d{2}' , comp_type ):
            if vers_list[1] == 2:
                return 'standard_Switch'
            
        elif re.search(r'finger' , comp_type ):
            if vers_list[1] == 2:
                return 'standard_Switch'
            
        elif re.search(r'hand_01' , comp_type ) :
            if vers_list[1] == 1 or vers_list[1] == 2:
                return 'switchStyle_2'
            
        elif re.search(r'foot_01' , comp_type ):
            if vers_list[1] == 1:
                return 'switchStyle_2'
        
        else:
            return None
    
    
    
    
    
    def standard_Switch(self , addKey=False):
        
        mc.undoInfo(openChunk=1)
        try:
            value = mc.getAttr("%s.%s" % (self.ctrl_setting , self.blend_attr))
            if not value in [0, 1]:
                return
            
            self.switch_step_1(value , addKey)
            if self.connector:
                for comp in self.connector:
                    _cls = self.__Switch.IKFK_cls.get(comp)
                    if _cls:
                        _cls.switch_step_1(value , addKey)
            
            self.switch_step_2( value )
            if addKey:
                self.addKeyframe( 2 )
                
                
            if self.connector:
                for comp in self.connector:
                    _cls = self.__Switch.IKFK_cls.get(comp)
                    if _cls:
                        _cls.switch_step_2(value )
                        if addKey:
                            _cls.addKeyframe( 2 )
            
        except:
            traceback.print_exc()
        mc.undoInfo(closeChunk=1)
        
    
    

        
    
    def switchStyle_1(self , addKey=False):
        '''
        this func use for:
            leg2__03
            
        '''
        mc.undoInfo(openChunk=1)
        try:
            value = mc.getAttr("%s.%s" % (self.ctrl_setting , self.blend_attr))
            if not value in [0, 1]:
                return
            
            self.switch_step_1(value , addKey)
            if self.connector:
                for comp in self.connector:
                    _cls = self.__Switch.IKFK_cls.get(comp)
                    if _cls:
                        _cls.switch_step_1(value , addKey)
            
            self.switch_step_2( value )
            self.switch_step_3( value , revrs = True)
            self.switch_step_2( value )
            
            if addKey:
                self.addKeyframe( 2 )
                
            if self.connector:
                for comp in self.connector:
                    _cls = self.__Switch.IKFK_cls.get(comp)
                    if _cls:
                        _cls.switch_step_2(value )
                        if addKey:
                            _cls.addKeyframe( 2 )
            
        except:
            traceback.print_exc()
        mc.undoInfo(closeChunk=1)


        
        
    
    def switchStyle_2(self , addKey=False):
        '''
        this func use for:
            hand__01
            foot__01
        '''
        
        mc.undoInfo(openChunk=1)
        try:
            value = mc.getAttr("%s.%s" % (self.ctrl_setting , self.blend_attr))
            if not value in [0, 1]:
                return
            
            if self.connector:
                for comp in self.connector:
                    _cls = self.__Switch.IKFK_cls.get(comp)
                    if _cls:
                        _cls.switch_step_1(value , addKey)
            self.switch_step_1(value , addKey)
            
            if self.connector:
                for comp in self.connector:
                    _cls = self.__Switch.IKFK_cls.get(comp)
                    _cls.switch_step_2(value )
                    if addKey:
                        _cls.addKeyframe( 2 )
                    
                    
            self.switch_step_2( value )
            if addKey:
                self.addKeyframe( 2 )
            
        except:
            traceback.print_exc()
        mc.undoInfo(closeChunk=1)
        

    