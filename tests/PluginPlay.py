import kivy

# this restricts the kivy version (below this kivy version you cannot use the app or software)
kivy.require("1.9.1")
   
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
import os
import sys

my_dir   = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(my_dir)
sys.path.append(os.path.join(root_dir, 'src'))

import pluginplay as pp

moduleManager = pp.ModuleManager()

#Name:      module_loader
#Function:  A Function that loads modules into the module manager via the specified filepath and name
#Inputs:    Filename    - The path to the module "C:/etc/etc/parentfolderoffile"
#           Path        - The name of the file to be loaded includeing .py "modulename.py"
def module_loader(filename, path):
    import importlib.util
    try:
        print(path+"\\"+os.path.basename(os.path.normpath(path)))
        spec = importlib.util.spec_from_file_location(os.path.basename(os.path.normpath(path)), filename[0])
        plugin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin)
        plugin.load_modules(moduleManager)
    except AttributeError:
        print("Not a valid module")
    except KeyError:
        print("Module already loaded")


#Name:      Section
#Function:  A BoxLayout with a nametag at the top and a body to display content. 
class Section(Widget):
    def SetTitle(self, title):
        self.ids.title.text = title

    def SetWidth(self, width):
        self.size_hint_x = width
    
    def Body(self):
        return self.ids.body

#Name:      ModuleResource
#Function:  A Clickable Button that stores a module key. 
#           OnPress adds the module to the callgraph, and removes it from the list of available modules.
#Inputs:    Key - The module key this Module Resource represents.
class ModuleResource(Widget):
    callgraph = None
    moduleSection = None
    key = None

    def __init__(self, key, *args, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.SetLabel(key)

    def SetSections(self, ModuleSection, CallGraphNode):
        self.moduleSection = ModuleSection
        self.callgraph = CallGraphNode

    def OnPress(self):
        module = moduleManager._modules.get(self.key)
        node = CallGraphNode(self.key, module)
        node.SetSections(self.moduleSection, self.callgraph)
        self.callgraph.Body().add_widget(node)
        submodules = list(module.submods())
        for x in submodules:
            n = node.AddSubModule(x,module.submods()[x]) 
        self.parent.remove_widget(self)

    def SetLabel(self, name):
        self.ids.modulebutton.text = name

#Name:      PopupContentRegion
#Function:  Provide a scrollable box layout for Popups
class PopupContentRegion(Widget):
    pass

#Name:      RemoveCallNodeButton
#Function:  A Clickable Button that stores a CallGraphNode.
#           OnPress calls the RemoveModule() function on the stored CallGraphNode
#Inputs:    CallNode - The CallGraphNode to remove
class RemoveCallNodeButton(Widget):
    callNode = None

    def __init__(self, CallNode, popup, *args, **kwargs):
        super().__init__(**kwargs)
        self.popup = popup
        self.callNode = CallNode

    def RemoveWidget(self):
        self.callNode.RemoveModule()
        self.popup.dismiss()


#Name:      RunModuleButton
#Function:  A Clickable Button that runs the specified module with the given parameters and ptype.
#Inputs:    module  - The Module to run when pressed
#           ptype   - The Property Type to run the module as
class RunModuleButton(Widget):
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
    

#Name:      ParameterModule
#Function:  A module that provides inputs to set the fixed inputs of a module
#Inputs:    module  - The Module to change fixed inputs
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
    
#Name:      ParameterField
#Function:  A module that provides a label and a text input to provide the data for a fixed input
#Inputs:    name  - The name of the input
#           value  - The value of the input
class ParamField(Widget):

    def __init__(self, name, value, *args, **kwargs):
        super().__init__(**kwargs)
        self.ids.label.text = name
        self.ids.param.text = str(value)

    def SetFieldName(self, name):
        pass

    def GetValue(self):
        return float(self.ids.param.text)

#Name:      ToolClearAll
#Function:  A button that removes all the modules in the call graph
#Inputs:    container  - The module that contains the callgraph
class ToolClearAll(Widget):
    container = None

    def SetContainer(self, container):
        self.container = container
    
    def ClearAll(self):
        print(self.container.children.__len__())
        for x in range(0, self.container.children.__len__()):
            self.container.children[0].RemoveModule()
        pass


#Name:      ToolOpenModule
#Function:  A button that opens the open module popup
class ToolOpenModule(Widget):
    moduleSection = None
    callSection = None

    def __init__(self, moduleSection, callSection, *args, **kwargs):
        super().__init__(**kwargs)
        self.moduleSection = moduleSection
        self.callSection = callSection

    def OpenModule(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, path, filename):
        module_loader(filename, path)

        self.moduleSection.Body().clear_widgets()

        for x in range(0, moduleManager._modules.keys().__len__()):
            key = list(moduleManager._modules.keys())[x]
            m = ModuleResource(key)
            m.SetSections(self.moduleSection,self.callSection)
            self.moduleSection.Body().add_widget(m)

        self.dismiss_popup()

#Name:      CallGraphNode
#Function:  A button that removes all the modules in the call graph
#Inputs:    key  - The key to the module represented by this node
#           module  - The module represented by this node
class CallGraphNode(Widget):
    module = None
    indent_lvl = 0
    child_count = 0
    key = None
    optionsdisabled = False
    modulesSection = None
    callSection = None

    def __init__(self, key, module, *args, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.module = module
        self.SetLabel(self.key)
        if isinstance(self.module, pp.Module):
            inputs=list(self.module.inputs())
        #    for x in range(0, inputs.__len__()):
        #        self.module.change_input(str(inputs[x]), 0)

    def SetSections(self,m,c):
        self.modulesSection = m
        self.callSection = c

    def RemoveModule(self):
        m = ModuleResource(self.key)
        m.SetSections(self.modulesSection, self.callSection)
        self.modulesSection.Body().add_widget(m)
        self.parent.remove_widget(self)

    def disableOptions(self):
        self.optionsdisabled = True
        for x in range (0,self.child_count):
            self.ids.childBody.children[x].disableOptions()

    def StartOptionsPopUp(self):
        popup = Popup()
        popup.title = "Options"
        popup.size_hint = (None, None)
        popup.size = (400, 400)
        popupcontent = PopupContentRegion()
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
        popupcontent.ids.body.add_widget(RemoveCallNodeButton(self,popup))
        popup.add_widget(popupcontent)
        popup.open()


    def StartRunModulePopUp(self):
        popup = Popup()
        popup.title = "Options"
        popup.size_hint = (None, None)
        popup.size = (400, 400)
        popupcontent = PopupContentRegion()
        proptypes = list(self.module.property_types())
        

        for ptype in proptypes:
            paramModule = RunModuleButton(self.module, ptype)
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
        sub_module.SetSections(self.modulesSection, self.callSection)
        self.ids.childBody.add_widget(sub_module)
        sub_module.UpdateParent()
        return sub_module
    
    
    def OnButtonOptionsPress(self):
        self.StartOptionsPopUp()

    def OnButtonDropDownPress(self):
       self.StartRunModulePopUp()

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class PluginPlay(App):
    def build(self):
        self.title = "Plugin Play"
        Window.clearcolor = (0.2, 0.2, 0.2, 1)

        superBox = BoxLayout(orientation ='horizontal')
        
        callSection = Section()
        callSection.SetTitle("CallGraph")
        
        modulesSection = Section()
        modulesSection.ids.title.text = "Modules"
        modulesSection.SetWidth(0.6)

        
        toolSection = Section()
        toolSection.SetTitle("Tools")
        toolSection.SetWidth(0.15)
        toolSection.Body().add_widget(ToolOpenModule(moduleSection = modulesSection, callSection=callSection))
        clearAll = ToolClearAll()
        clearAll.SetContainer(callSection.Body())
        toolSection.Body().add_widget(clearAll)
        
        superBox.add_widget(modulesSection)
        superBox.add_widget(callSection)
        superBox.add_widget(toolSection)

        return superBox


#Create an instance of the Plugin Play Application and run it
root = PluginPlay()
root.run()
