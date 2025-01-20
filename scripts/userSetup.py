import maya
import importlib
import AM_MENU
import AM_MENU.core.chbox

maya.utils.executeDeferred(AM_MENU.AM_toolsMenuLoader)
maya.utils.executeDeferred(AM_MENU.UpdateChecker)


