#import kivy module
from audioop import add
from ctypes import GetLastError
from ctypes.wintypes import RGB
from lib2to3.pytree import Node
from optparse import TitledHelpFormatter
from textwrap import indent
from turtle import heading
from xml.etree.ElementTree import tostring
import kivy

   
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
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.clock import *
import os
import sys

my_dir   = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(my_dir)
sys.path.append(os.path.join(root_dir, 'src'))

import pluginplay as pp
from examples import geometry

class Module(Widget):
    def SetName(self, name):
        self.ids.modulebutton.text = name
    

class CallGraphNode(Widget):
    indent_lvl = 0
    child_count = 0

    def UpdateParent(self):
        if(isinstance(self.parent.parent, CallGraphNode)):
            self.parent.parent.height = self.parent.parent.height + 65
            self.parent.parent.y = self.parent.parent.y - 65
            self.parent.parent.UpdateParent()
            
    def GetLastChildY(self):
        if(self.child_count > 0):
            return self.ids.childBody.children[0].top
        return 0

    def SetLabel(self, text):
         self.ids.label.text = text

    def GetLabel(self):
        return self.ids.label.text

    def AddSubModule(self):
        self.child_count += 1
        sub_module = CallGraphNode()
        sub_module.indent_lvl = self.indent_lvl+1
        sub_module.SetLabel(self.GetLabel() + "."+str(self.child_count))
        self.ids.childBody.add_widget(sub_module) 
        self.height = self.height + 65
        self.y = self.y - 65
        self.UpdateParent()
        return sub_module

    def AddSubModuleWithName(self, name):
        self.child_count += 1
        sub_module = CallGraphNode()
        sub_module.indent_lvl = self.indent_lvl+1
        sub_module.SetLabel(name)
        self.ids.childBody.add_widget(sub_module)
        return sub_module

    def OnButtonDropDownPress(self):
        print(self.GetLastChildY())
    
    def OnButtonOptionsPress(self):
        self.AddSubModule()

class Section(Widget):

    def SetTitle(self, title):
        self.ids.title.text = title

    def SetWidth(self, width):
        self.size_hint_x = width
    
    def Body(self):
        return self.ids.body
        pass

class AddModuleButton(Widget):
    callgraph = None
    moduleManager = None
    counter = 0

    def SetCallGraph(self, CallGraphNode):
        self.callgraph = CallGraphNode

    def SetModuleManager(self, ModuleManager):
        self.moduleManager = ModuleManager

    def OnPress(self):
        node = CallGraphNode()
        name = list(self.moduleManager._modules.keys())[self.counter]
        module = self.moduleManager._modules.get(name)
        print(name)
        node.SetLabel(module._state.get("callback_name"))
        self.callgraph.add_widget(node)
        for x in range(0, module._state.get("submods").__len__()):
            n = node.AddSubModule()
            subname = list(self.moduleManager._modules.keys())[x]
            submodule = module._state.get("submods").get(subname)
            n.SetLabel(subname)
        self.counter +=1

class PluginPlay(App):
    
    moduleManager = None
    

    def build(self):

        self.moduleManager = pp.ModuleManager()
        geometry.load_modules(self.moduleManager)
        

        self.title = "Plugin Play"
        grayColor = 0.2
        Window.clearcolor = (grayColor, grayColor, grayColor, 1)
        # To position oriented widgets again in the proper orientation
        # use of vertical orientation to set all widgets 
        superBox = BoxLayout(orientation ='horizontal')

        modulesSection = Section()
        modulesSection.SetTitle("Modules")
        modulesSection.SetWidth(0.6)
        
        for x in range(0, self.moduleManager._modules.keys().__len__()):
            m = Module()
            name = list(self.moduleManager._modules.keys())[x]
            module = self.moduleManager._modules.get(name)
            m.SetName(module._state.get("callback_name"))
            modulesSection.Body().add_widget(m)

        callSection = Section()        
        callSection.SetTitle("CallGraph")

        b = AddModuleButton()
        b.SetCallGraph(callSection.Body())
        b.SetModuleManager(self.moduleManager)
        modulesSection.add_widget(b)

        

        superBox.add_widget(modulesSection)
        superBox.add_widget(callSection)

        return superBox

# creating the object root for BoxLayoutApp() class 
root = PluginPlay()
# run function runs the whole program
# i.e run() method which calls the
# target function passed to the constructor.
root.run()