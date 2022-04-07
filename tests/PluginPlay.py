#import kivy module
from audioop import add
from ctypes.wintypes import RGB
from json import tool
from lib2to3.pytree import Node
from optparse import TitledHelpFormatter
from re import sub
from textwrap import indent
from turtle import heading
from weakref import ProxyType
from xml.etree.ElementPath import get_parent_map
from xml.etree.ElementTree import tostring
from xmlrpc.client import getparser
import kivy
import importlib

   
# this restricts the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require("1.9.1")
   
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.clock import *
import os
import sys

my_dir   = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(my_dir)
sys.path.append(os.path.join(root_dir, 'src'))

import pluginplay as pp
from examples import geometry2





moduleManager = pp.ModuleManager()

class Section(Widget):
    def SetTitle(self, title):
        self.ids.title.text = title

    def SetWidth(self, width):
        self.size_hint_x = width
    
    def Body(self):
        return self.ids.body

class ModuleRes(Widget):
    callgraph = None
    module = None
    key = None

    def __init__(self, key, *args, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.module = moduleManager._modules.get(self.key)
        self.SetLabel(key)

    def SetCallGraph(self, CallGraphNode):
        self.callgraph = CallGraphNode

    def OnPress(self):
        node = CallGraphNode(self.key, self.module)
        self.callgraph.add_widget(node)
        submodules = list(self.module.submods())
        for x in submodules:
            n = node.AddSubModule(x,self.module.submods()[x]) 
        self.parent.remove_widget(self)

    def SetLabel(self, name):
        self.ids.modulebutton.text = name

class PopupContent(Widget):
    pass

class RemoveWidget(Widget):
    
    callNode = None

    def __init__(self, CallNode, *args, **kwargs):
        super().__init__(**kwargs)
        self.callNode = CallNode

    def RemoveWidget(self):
        self.callNode.removeModule()



class RunModule(Widget):
    module = None
    ptype = None

    def disableSet(self, disable):
        self.disabled = disable

    def __init__(self, module, ptype, *args, **kwargs):
        super().__init__(**kwargs)
        self.ptype = ptype
        self.module = module

    def GetParam(self, index):
        return float(self.ids.body.children[self.GetParamCount()-1-index].ids.param.text)

    def GetParamCount(self):
        return self.ids.body.children.__len__() -1

    def OnPressRun(self):
        input_count = self.GetParamCount()
        if(input_count == 0):
            print(self.module.run_as(self.ptype))
        if(input_count == 1):
            print(self.module.run_as(self.ptype, self.GetParam(0)))
        if(input_count == 2):
            print(self.module.run_as(self.ptype, self.GetParam(0), self.GetParam(1)))
    
class ParamModule(Widget):
    module = None

    def disableSet(self, disable):
        self.disabled = disable

    def __init__(self, module, *args, **kwargs):
        super().__init__(**kwargs)
        self.module = module
        self.ids.set.disabled = self.module.locked()

    def OnPressSet(self):
        parameters = self.ids.body.children.__len__() -1
        for x in range(0, parameters):
            paramobj = self.ids.body.children[x]
            param_name = paramobj.ids.label.text
            param_value = float(paramobj.ids.param.text)
            self.module.change_input(param_name, param_value)
    
class ParamField(Widget):

    def __init__(self, name, value, *args, **kwargs):
        super().__init__(**kwargs)
        self.ids.label.text = name
        self.ids.param.text = str(value)

    def SetFieldName(self, name):
        pass

    def GetValue(self):
        return float(self.ids.param.text)

class ToolRunAll(Widget):
    container = None

    def SetContainer(self, container):
        self.container = container
    
    def RunAll(self):
        for x in range(0,self.container.children.__len__()):
            self.container.children[x].RunModule()
        

class ToolClearAll(Widget):
    container = None

    def SetContainer(self, container):
        self.container = container
    
    def ClearAll(self):
        for x in range(0,self.container.children.__len__()):
            self.container.children[x].RunModule()

class CallGraphNode(Widget):
    module = None
    indent_lvl = 0
    child_count = 0
    key = None
    optionsdisabled = False
    modulesSection = None
    callSection = None

    def SetSections(self,m,c):
        self.modulesSection = m
        self.callSection = c

    def removeModule(self):
        moduleManager.erase(self.key)
        moduleManager.add_module(self.key,self.module)
        m = ModuleRes(self.key)
        m.SetCallGraph(self.callSection.Body())
        self.modulesSection.Body().add_widget(m)
        self.parent.remove_widget(self)

    def disableOptions(self):
        self.optionsdisabled = True
        for x in range (0,self.child_count):
            self.ids.childBody.children[x].disableOptions()

    def __init__(self, key, module, *args, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.module = module
        self.SetLabel(self.key)
        if isinstance(self.module, pp.Module):
            inputs=list(self.module.inputs())
            for x in range(0, inputs.__len__()):
                self.module.change_input(str(inputs[x]), 0)

    def StartOptionsPopUp(self):
        popup = Popup()
        popup.title = "Options"
        popup.size_hint = (None, None)
        popup.size = (400, 400)
        popupcontent = PopupContent()
        paramModule = ParamModule(self.module)
        paramModule.disableSet(self.optionsdisabled)

        proptypes = list(self.module.property_types())[0]
        inputs = list(self.module.inputs())
        propinputs = proptypes.inputs()

        for x in range(0, propinputs.__len__()):
            propinput = propinputs[x][0]
            inputs.remove(propinput)
        
        for x in range(0, inputs.__len__()):
            inputField1 = ParamField(str(inputs[x]), 0)
            paramModule.ids.body.add_widget(inputField1)

        popupcontent.ids.body.add_widget(paramModule)
        popupcontent.ids.body.add_widget(RemoveWidget(self))
        popup.add_widget(popupcontent)
        popup.open()


    def StartRunModulePopUp(self):
        popup = Popup()
        popup.title = "Options"
        popup.size_hint = (None, None)
        popup.size = (400, 400)
        popupcontent = PopupContent()
        proptypes = list(self.module.property_types())
        

        for ptype in proptypes:
            paramModule = RunModule(self.module, ptype)
            propinputs = ptype.inputs()
            paramModule.ids.label.text = str(ptype.results())
            for x in range(0, propinputs.__len__()):
                inputField1 = ParamField(str(propinputs[x][0]), 0)
                paramModule.ids.body.add_widget(inputField1)
            popupcontent.ids.body.add_widget(paramModule)
        
        popup.add_widget(popupcontent)
        popup.open()
       

    def UpdateParent(self):
        print(self.parent.parent)
        if(isinstance(self.parent.parent, CallGraphNode)):
            self.parent.parent.height = self.parent.parent.height + 65
            self.parent.parent.y = self.parent.parent.y - 65*2
            self.parent.parent.UpdateParent()
            
    def GetLastChildY(self):
        if(self.child_count > 0):
            return self.ids.childBody.children[0].top
        return 0

    def SetLabel(self, name):
        self.ids.label.text = name

    def GetLabel(self):
        return self.ids.label.text

    def AddSubModule(self, key, module):
        self.child_count += 1
        sub_module = CallGraphNode(key, module)
        sub_module.indent_lvl = self.indent_lvl+1
        self.ids.childBody.add_widget(sub_module)
        sub_module.UpdateParent()
        return sub_module
    
    
    def OnButtonOptionsPress(self):
        self.StartOptionsPopUp()

    def OnButtonDropDownPress(self):
       self.StartRunModulePopUp()


class PluginPlay(App):

    def module_loader(self, module):
        plugin = importlib.import_module(f".{module}", package='examples')
        plugin.load_modules(moduleManager)

    def build(self):
        self.module_loader('geometry')
        self.module_loader('geometry2')

        self.title = "Plugin Play"
        grayColor = 0.2
        Window.clearcolor = (grayColor, grayColor, grayColor, 1)
        # To position oriented widgets again in the proper orientation
        # use of vertical orientation to set all widgets 
        superBox = BoxLayout(orientation ='horizontal')
        
        modulesSection = Section()
        callSection = Section()
        
        modulesSection.ids.title.text = "Modules"
        modulesSection.SetWidth(0.6)

        toolSection = Section()
        toolSection.SetTitle("Tools")
        toolSection.SetWidth(0.15)
     
        callSection.SetTitle("CallGraph")
        
        for x in range(0, moduleManager._modules.keys().__len__()):
            key = list(moduleManager._modules.keys())[x]
            m = ModuleRes(key)
            m.SetCallGraph(callSection.Body())
            modulesSection.Body().add_widget(m)

        
        t = ToolRunAll()
        t.SetContainer(callSection.Body())
        toolSection.Body().add_widget(t)
        toolSection.Body().add_widget(ToolClearAll())
        
        superBox.add_widget(modulesSection)
        superBox.add_widget(callSection)
    
        superBox.add_widget(toolSection)

        return superBox

# creating the object root for BoxLayoutApp() class 
root = PluginPlay()

# run function runs the whole program
# i.e run() method which calls the
# target function passed to the constructor.
root.run()
