# code to show how to use nested boxlayouts.
 
# import kivy module
from audioop import add
from ctypes.wintypes import RGB
from lib2to3.pytree import Node
from optparse import TitledHelpFormatter
from textwrap import indent
from turtle import heading
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


class PayLoad():
    pass

class CallGraphNode(Widget):
    indent_lvl = 0
    child_count = 0

    def ChildBody(self):
        return self.ids.childBody

    def AddSubModule(self):
        self.child_count += 1
        sub_module = CallGraphNode()
        #sub_module.ids.node_label.text = "child"
        sub_module.SetIndentLvl(self.indent_lvl+1)
        self.ChildBody().add_widget(sub_module)
        return sub_module

    def SetIndentLvl(self, level):
        self.indent_lvl = level

    pass

class TargetNode(Widget):  
    dragging = False

    def SetDragging(self, drag):
        self.dragging = drag

    def set_bgcolor(self,r,b,g,a,*args):
        self.canvas.after.clear()
        with self.canvas.after:
            Color(r,g,b,a)
            Rectangle(pos=self.pos,size=self.size)

    def on_touch_move(self, touch):
        self.set_bgcolor(0,0,0,0)
        if(self.dragging):
            if(touch.x > self.x and touch.x< self.x+self.width and self.dragging):
                if(touch.y > self.y and touch.y< self.y +self.height):
                    self.set_bgcolor(1,0,0,1)
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if(self.dragging):
            if(touch.x > self.x and touch.x< self.x+self.width and self.dragging):
                if(touch.y > self.y and touch.y< self.y +self.height):
                    self.set_bgcolor(1,1,0,1)
        else:
            self.set_bgcolor(0,0,0,0)
        return super().on_touch_up(touch)   


class Section(Widget):

    def SetTitle(self, title):
        self.ids.title.text = title

    def SetWidth(self, width):
        self.size_hint_x = width
    
    def Body(self):
        return self.ids.body
    pass


class SourceNode(Widget):
    drag = False
    defaultPosX = 0
    defaultPosY = 0

    def IsDragging(self):
        return self.drag

    def on_touch_up(self, touch):
        self.x = self.defaultPosX
        self.y = self.defaultPosY
        self.drag = False
        DragActive = False
        return super().on_touch_up(touch)      
    
    def on_touch_move(self, touch):
        if self.drag:
            self.x = touch.x
            self.y = touch.y
        return super().on_touch_move(touch)
    

    def on_touch_down(self, touch):
        self.defaultPosX = self.x
        self.defaultPosY = self.y
        if(touch.x > self.x and touch.x< self.x+self.width):
            if(touch.y > self.y and touch.y< self.y +self.height):
                  self.drag = True
                  
                  DragActive = True
        return super().on_touch_move(touch)

# class in which we are creating the button by using boxlayout
# defining the App class
class PluginPlay(App):
    
    callSection = None
    modulesSection = None
    dragging = False  

    def update(self,dt):
        self.dragging = False
       # for x in range(0,3):
        #    if(self.modulesSection.Body().children[x].IsDragging()):
        #        self.dragging = True
        #self.callSection.Body().children[2].SetDragging(self.dragging)    
        

    def start(self):
        Clock.schedule_interval(self.update, 0.01) 

    def build(self):
        self.title = "Plugin Play"
        grayColor = 0.2
        Window.clearcolor = (grayColor, grayColor, grayColor, 1)
        # To position oriented widgets again in the proper orientation
        # use of vertical orientation to set all widgets 
        superBox = BoxLayout(orientation ='horizontal')

        self.modulesSection = Section()
        self.modulesSection.SetTitle("Modules")
        self.modulesSection.SetWidth(0.6)
        
  

        self.callSection = Section()        
        self.callSection.SetTitle("CallGraph")
        call1 = CallGraphNode()
        call4 = CallGraphNode()
        call5 = call4.AddSubModule()
        call4.AddSubModule()
        call5.AddSubModule()
        call2 = call1.AddSubModule()
        call1.AddSubModule()

        self.callSection.Body().add_widget(call1)
        self.callSection.Body().add_widget(call4)

        

        self.callSection

        superBox.add_widget(self.modulesSection)
        superBox.add_widget(self.callSection)

        return superBox

# creating the object root for BoxLayoutApp() class 
root = PluginPlay()
root.start()
# run function runs the whole program
# i.e run() method which calls the
# target function passed to the constructor.
root.run()