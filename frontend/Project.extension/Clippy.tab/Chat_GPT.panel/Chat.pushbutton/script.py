# -*- coding: utf-8 -*-
from pyrevit import script
from pyrevit.revit import ui
from user_interface import CustomWindow
import time

if __name__ == "__main__":

    # log = script.get_logger()

    # Get the Revit window
    revit_window = ui.get_mainwindow()

    # Look through the windows owned by the Revit window to try and find an instance of the custom UI window
    custom_ui_window = next(
        (x for x in revit_window.OwnedWindows if x.Uid == "ClippyAIWindow"), None)

    if custom_ui_window != None:
        # If the custom UI window is already opened, show it with .Activate()
        custom_ui_window.Activate()

    else:
        # If the custom UI window is currently open, create a new instance
        custom_ui_window = script.load_ui(CustomWindow(), 'MainWindow.xaml')
        #custom_ui_window = script.load_ui(CustomWindow(), 'MainWindow_bouncy_clippy.xaml')

        custom_ui_window.show()

        custom_ui_window.Owner = revit_window

    
