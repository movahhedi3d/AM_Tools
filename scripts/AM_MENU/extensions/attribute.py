import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel

def addAttribute(node,
                 longName,
                 attributeType,
                 value=None,
                 niceName=None,
                 shortName=None,
                 minValue=None,
                 maxValue=None,
                 keyable=True,
                 readable=True,
                 storable=True,
                 writable=True,
                 channelBox=False):
    """Add attribute to a node

    Arguments:
        node (dagNode): The object to add the new attribute.
        longName (str): The attribute name.
        attributeType (str): The Attribute Type. Exp: 'string', 'bool',
            'long', etc..
        value (float or int): The default value.
        niceName (str): The attribute nice name. (optional)
        shortName (str): The attribute short name. (optional)
        minValue (float or int): minimum value. (optional)
        maxValue (float or int): maximum value. (optional)
        keyable (bool): Set if the attribute is keyable or not. (optional)
        readable (bool): Set if the attribute is readable or not. (optional)
        storable (bool): Set if the attribute is storable or not. (optional)
        writable (bool): Set if the attribute is writable or not. (optional)
        channelBox (bool): Set if the attribute is in the channelBox or not,
            when the attribute is not keyable. (optional)

    Returns:
        str: The long name of the new attribute
    """
    if cmds.attributeQuery( longName , n=node , ex=True ):
        om.MGlobal.displayError("Attribute already exists")
        return

    data = {}

    if shortName is not None:
        data["shortName"] = shortName
    if niceName is not None:
        data["niceName"] = niceName
    if attributeType == "string":
        data["dataType"] = attributeType
    else:
        data["attributeType"] = attributeType

    if minValue is not None and minValue is not False:
        data["minValue"] = minValue
    if maxValue is not None and maxValue is not False:
        data["maxValue"] = maxValue

    data["keyable"] = keyable
    data["readable"] = readable
    data["storable"] = storable
    data["writable"] = writable

    if value is not None and attributeType not in ["string"]:
        data["defaultValue"] = value
    
    cmds.addAttr(node, longName= longName , **data )
    attr = node+".%s"%longName

    if value is not None:
        if attributeType == "matrix":
            cmds.setAttr(attr , value , type = "matrix")
        else:
            cmds.setAttr(attr , value )
        
    if channelBox:
        cmds.setAttr(attr , channelBox=True)
        
    return longName


def addColorAttribute(node,
                      longName,
                      value=False,
                      keyable=True,
                      readable=True,
                      storable=True,
                      writable=True,
                      niceName=None,
                      shortName=None):
    """
    Add a color attribute to a node

    Arguments:
        node (dagNode): The object to add the new attribute.
        longName (str): The attribute name.
        value (list of flotat): The default value in a list for RGB.
            exp [1.0, 0.99, 0.13].
        keyable (bool): Set if the attribute is keyable or not. (optional)
        readable (bool): Set if the attribute is readable or not. (optional)
        storable (bool): Set if the attribute is storable or not. (optional)
        writable (bool): Set if the attribute is writable or not. (optional)
        niceName (str): The attribute nice name. (optional)
        shortName (str): The attribute short name. (optional)

    Returns:
        str: The long name of the new attribute

    """
    if cmds.attributeQuery( longName , n=node , ex=True ):
        om.MGlobal.displayError("Attribute already exists")
        return

    data = {}

    data["attributeType"] = "float3"
    if shortName is not None:
        data["shortName"] = shortName
    if niceName is not None:
        data["niceName"] = niceName

    data["usedAsColor"] = True
    data["keyable"] = keyable
    data["readable"] = readable
    data["storable"] = storable
    data["writable"] = writable

    # child nested attr
    dataChild = {}
    dataChild["attributeType"] = 'float'
    dataChild["parent"] = longName
    
    
    cmds.addAttr(node, longName= longName , **data )
    cmds.addAttr(node, longName= longName + "_r", **dataChild )
    cmds.addAttr(node, longName= longName + "_g", **dataChild )
    cmds.addAttr(node, longName= longName + "_b", **dataChild )
    

    if value:
        
        cmds.setAttr(node+".%s_r"%longName , value[0])
        cmds.setAttr(node+".%s_g"%longName , value[1])
        cmds.setAttr(node+".%s_b"%longName , value[2])
        
    return longName








def lockAttribute(node,
                  attributes=["tx", "ty", "tz",
                              "rx", "ry", "rz",
                              "sx", "sy", "sz",
                              "v"]):
    """Lock attributes of a node.

    By defaul will lock the rotation, scale and translation.

    Arguments:
        node(dagNode): The node with the attributes to lock.
        attributes (list of str): The list of the attributes to lock.

    Example:
        >>> att.lockAttribute(self.root_ctl, ["sx", "sy", "sz", "v"])

    """
    _lockUnlockAttribute(node, attributes, lock=True, keyable=False)
    
    
    
    

def unlockAttribute(node,
                    attributes=["tx", "ty", "tz",
                                "rx", "ry", "rz",
                                "sx", "sy", "sz",
                                "v"]):
    """Unlock attributes of a node.

    By defaul will unlock the rotation, scale and translation.

    Arguments:
        node(dagNode): The node with the attributes to unlock.
        attributes (list of str): The list of the attributes to unlock.

    Example:
        >>> att.unlockAttribute(self.root_ctl, ["sx", "sy", "sz", "v"])

    """
    _lockUnlockAttribute(node, attributes, lock=False, keyable=True)



def _lockUnlockAttribute(node, attributes, lock, keyable):
    """Lock or unlock attributes of a node.

    Arguments:
        node(dagNode): The node with the attributes to lock/unlock.
        attributes (list of str): The list of the attributes to lock/unlock.

    """
    if not isinstance(attributes, list):
        attributes = [attributes]

    for attr_name in attributes:
        cmds.setAttr(node+".%s"%attr_name , lock=lock , keyable=keyable )





def get_default_value(node, attribute):
    """Get the default attribute value

    Args:
        node (str, PyNode): The object with the attribute
        attribute (str): The attribute to get the value

    Returns:
        variant: The attribute value
    """
    return cmds.attributeQuery(attribute,
                             node=node,
                             listDefault=True)[0]


def set_default_value(node, attribute):
    """Set the default value to the attribute

    Args:
        node (str, PyNode): The object with the attribute to reset
        attribute (str): The attribute to reset
    """

    defVal = get_default_value(node, attribute)
    try:
        cmds.setAttr(node+".%s"%attribute , defVal)
    except RuntimeError:
        pass


def reset_selected_channels_value(objects=None, attributes=None):
    """Reset the the selected channels if not attribute is provided

    Args:
        objects (None, optional): The objects to reset the channels
        attribute (list, optional): The attribute to reset
    """
    if not objects:
        objects = cmds.ls(selection=True)
    if not attributes:
        attributes = getSelectedChannels()

    for obj in objects:
        for attr in attributes:
            set_default_value(obj, attr)


def reset_SRT(objects=None,
              attributes=["tx", "ty", "tz",
                          "rx", "ry", "rz",
                          "sx", "sy", "sz",
                          "v"]):
    """Reset Scale Rotation and translation attributes to default value

    Args:
        objects (None, optional): The objects to reset the channels
        attribute (list): The attribute to reset
    """
    reset_selected_channels_value(objects, attributes)


def smart_reset(*args):
    """Reset the SRT or the selected channels

    Checks first if we have channels selected. If not, will try to reset SRT

    Args:
        *args: Dummy
    """
    attributes = getSelectedChannels()
    if attributes:
        reset_selected_channels_value(objects=None, attributes=attributes)
    else:
        reset_SRT()



def get_channelBox():
    """Get the channel box

    Returns:
        str: channel box path
    """
    mel_str = 'global string $gChannelBoxName; $temp=$gChannelBoxName;'
    channelBox = mel.eval(mel_str)
    return channelBox




def getSelectedChannels():
    """Get the selected channels on the channel box

    Arguments:
        userDefine (bool, optional): If True, will return only the user
            defined channels. Other channels will be skipped.

    Returns:
        list: The list of selected channels names

    """
    # fetch core's main channelbox
    attrs = cmds.channelBox(get_channelBox(), q=True, sma=True)

    return attrs





def connectSet(source, target, testInstance):
    """Connect or set attributes

    Connects or set attributes depending if is instance of a instance check

    Args:
        source (str or Attr): Striname of the attribute or PyNode attribute
        target (str or Attr): Striname of the attribute or PyNode attribute
        testInstance (tuple): Tuple of types to check
    """
    if not isinstance(testInstance, tuple):
        testInstance = tuple(testInstance)

    if isinstance(source, testInstance):
        cmds.connectAttr(source, target)
    else:
        cmds.setAttr(target, source)




def toggle_bool_attr(node , attr):
    
    _attr = node+".%s"%attr
    if cmds.getAttr(_attr):
        cmds.setAttr(_attr , False)
    else:
        cmds.setAttr(_attr , True)








