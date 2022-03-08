# code to show how to use nested boxlayouts.
 
# import kivy module
from ctypes.wintypes import RGB
import kivy
   
# this restricts the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require("1.9.1")
   
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.behaviors import DragBehavior

class CallNode(Widget): 
    pass

class DragNode(DragBehavior, Label): 
    pass

# class in which we are creating the button by using boxlayout
# defining the App class
class PluginPlay(App):
       
    def build(self):
        self.title = "Plugin Play"
        grayColor = 0.2
        Window.clearcolor = (grayColor, grayColor, grayColor, 1)
        # To position oriented widgets again in the proper orientation
        # use of vertical orientation to set all widgets 
        superBox = BoxLayout(orientation ='vertical')

        
        
        
        #Titles
        titleBox = BoxLayout(orientation ='horizontal')
        titleBox.size_hint_y = (0.1)
        moduleTitle = Button(text ="Modules")
        moduleTitle.size_hint_x = (0.6)
        moduleTitle.disabled = True
        callGraphTitle = Button(text ="Call Graph")
        callGraphTitle.disabled = True        
        titleBox.add_widget(moduleTitle)
        titleBox.add_widget(callGraphTitle)
        superBox.add_widget(titleBox)
        
        horizBox = BoxLayout(orientation ='horizontal')

        # modulesbox
        modulesBox = BoxLayout(orientation = 'vertical')
        modulesBox.size_hint_x = (0.6)


        #moduleSelection
        scrollBox  = BoxLayout(orientation = 'vertical')
        scrollBox.padding = [15,15,15,15]
        scrollBox.spacing = 5

        for x in range(1,12):
            scrollBox.add_widget(DragNode())

        #moudleSaveLoad
        saveLoadBox  = BoxLayout(orientation = 'horizontal')
        saveLoadBox.size_hint_y = (0.2)
        saveLoadBox.padding = [15,15,15,15]
        saveLoadBox.spacing = 5
        saveLoadBox.add_widget(Button(text ="Save"))
        saveLoadBox.add_widget(Button(text ="Load"))


        #Call Graph Section
        callgraphBox = BoxLayout(orientation = 'vertical')
        callgraphBox.padding = [15,15,15,15]
        callgraphBox.spacing = 5
        #CallNode
        for x in range(1,12):
           callgraphBox.add_widget(CallNode())
    

        modulesBox.add_widget(scrollBox)
        modulesBox.add_widget(saveLoadBox)
        horizBox.add_widget(modulesBox)
        horizBox.add_widget(callgraphBox)
        superBox.add_widget(horizBox)
        
    
        return superBox
 
# creating the object root for BoxLayoutApp() class 
root = PluginPlay()
   
# run function runs the whole program
# i.e run() method which calls the
# target function passed to the constructor.
root.run()