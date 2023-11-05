# dependencies
import custom_functions
from pyrevit import forms
from pyrevit import UI
from pyrevit import script
import rpw
from Autodesk.Revit.Exceptions import InvalidOperationException
from System.Windows.Controls.Primitives import BulletDecorator
from System.Windows.Controls import Image
from System.Windows import ResourceDictionary
from System import Uri
import os
import clr

clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
clr.AddReference('PresentationCore')
clr.AddReference('PresentationFramework')
clr.AddReference('System.Windows.Forms')


# ----------------------------
# Magic
# ----------------------------
'''
Code borrowed from: 
https://github.com/CyrilWaechter/pyRevitMEP/blob/master/pyRevitMEP.tab/Samples.panel/Samples.pulldown/FormExternalEventHandler.pushbutton/script.py
'''


class CustomizableEvent:
    def __init__(self):
        """ An instance of this class need to be created before any modeless operation.
        You can then call the raise_event method to perform any modeless operation.
        Any modification to Revit DB need to be performed inside a valid Transaction.
        This Transaction needs to be open inside the function_or_method, NOT before calling raise_event.
        """
        # Create an handler instance and his associated ExternalEvent
        custom_handler = _CustomHandler()
        custom_handler.customizable_event = self
        self.custom_event = UI.ExternalEvent.Create(custom_handler)

        # Initialise raise_event variables
        self.function_or_method = None
        self.args = ()
        self.kwargs = {}

    def _raised_method(self):
        """ !!! DO NOT USE THIS METHOD IN YOUR SCRIPT !!!
        Method executed by IExternalEventHandler.Execute when ExternalEvent is raised by ExternalEvent.Raise.
        """
        self.function_or_method(*self.args, **self.kwargs)

    def raise_event(self, function_or_method, *args, **kwargs):
        """
        Method used to raise an external event with custom function and parameters
        Example :
        >>> customizable_event = CustomizableEvent()
        >>> customizable_event.raise_event(rename_views, views_and_names)
        """
        self.args = args
        self.kwargs = kwargs
        self.function_or_method = function_or_method
        self.custom_event.Raise()


class _CustomHandler(UI.IExternalEventHandler):
    """ Subclass of IExternalEventHandler intended to be used in CustomizableEvent class
    Input : function or method. Execute input in a IExternalEventHandler"""

    def __init__(self):
        self.customizable_event = None

    # Execute method run in Revit API environment.
    # noinspection PyPep8Naming, PyUnusedLocal
    def Execute(self, application):
        try:
            self.customizable_event._raised_method()
        except InvalidOperationException:
            # If you don't catch this exeption Revit may crash.
            print("InvalidOperationException catched")

    # noinspection PyMethodMayBeStatic, PyPep8Naming
    def GetName(self):
        return "Execute an function or method in a IExternalHandler"


custom_event = CustomizableEvent()

# ----------------------------
# Custom UI Window
# ----------------------------


class CustomWindow(forms.WPFWindow):
    def __init__(self):
        # Fix WPF Resource Dictionary
        self.resolve_wpf_resource()

        # Set clean state for new window
        self.state = Custom_Window_State()

        self.logger = script.get_logger()

    def setup(self):
        # Fix linked image resources
        self.resolve_browser_paths()

    def resolve_wpf_resource(self):
        """Function to add WPF resources."""
        dir_path = os.path.dirname(__file__)
        path_styles = os.path.join(dir_path, './resources/WPF_styles.xaml')
        r = ResourceDictionary()
        r.Source = Uri(path_styles)
        self.Resources = r

        return None

    def resolve_images(self):
        """Add assets folder too"""
        dir_path = os.path.dirname(__file__)

        images = [
            {"xaml_name": "clippy_gif", "relative_path": "./assets/clippy_gif.gif"},
        ]

        for image in images:
            path_to_asset = os.path.join("file:///", dir_path, image["relative_path"])
            wpf_img_element = getattr(self, image["xaml_name"])
            self.set_image_source(wpf_img_element, path_to_asset)

        return None

    def resolve_browser_paths(self):
        """Add assets folder too"""
        dir_path = os.path.dirname(__file__)

        paths = [
            {"xaml_name": "clippy_gif", "relative_path": "./assets/clippy_gif.gif"},
        ]

        for path in paths:
            path_to_asset = os.path.join("file:///", dir_path, path["relative_path"])
            wpf_img_element = getattr(self, path["xaml_name"])

            wpf_img_element.Source = path_to_asset
            print(path_to_asset)
            
        return None

    def update_state(self, new_state):
        self.logger.warning("New state set...")

        self.state = new_state

        # Convert
        self.render()

        # Update the UI
        self.show()

    # ------------------
    # View updaters - Create UI text based on data within this instance
    # ------------------
    def render_test(self, defer_ui_refresh=False):
        ds = self.state.data["test"]
        self.ui_test_result.Text = ds["foo"]

    # ------------------
    # UI Functionality - Button Controllers
    # ------------------
    def tab_next(self, sender, args):
        self.tabControl.SelectedIndex = self.tabControl.SelectedIndex + 1

    def click_test(self, sender, e):
        custom_event.raise_event(run_checks, self, "String arg")


class Custom_Window_State():
    def __init__(self):
        self.data = {
            "test": {
                "foo": None
            }
        }


# ----------------------------
# Functions called by UI buttons
# ----------------------------
def run_checks(window, text_string_prefix):
    # EACH CHECK CAN MAP TO UPDATING ONE DATA VALUE?
    window.logger.warning("Running checks")
    passed_checks = True

    state = window.state

    if (passed_checks == True):
        (passed_checks, result_state) = custom_functions.basic_setup_check_for_area_schemes(state)
        state = result_state

    window.logger.warning("Check complete")
    window.update_state(state)
