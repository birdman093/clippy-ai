# dependencies
import os

import clr
clr.AddReference('System')
clr.AddReference('System.Net')
clr.AddReference('System.Threading')
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
clr.AddReference('PresentationCore')
clr.AddReference('PresentationFramework')
clr.AddReference('System.Windows.Forms')

from Autodesk.Revit.Exceptions import InvalidOperationException
from System.Windows.Controls.Primitives import BulletDecorator
from System.Windows.Media.Imaging import BitmapImage
from System.Windows.Media.Animation import DiscreteObjectKeyFrame
from System.Windows.Controls import Image
from System.Windows import ResourceDictionary
from System import Uri, UriKind

from System import String
from System.Net import WebClient, WebRequest
from System.Text import Encoding
from System.IO import StreamReader
from System.Threading import Thread
from System.Net import WebException

from pyrevit import forms
from pyrevit import UI
from pyrevit import script

import rpw
import os

from custom_functions import clean_code_snippet, clean_response_string


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
        # Set clean state for new window
        self.state = Custom_Window_State()

        # Fix WPF Resource Dictionary - Not needed
        #self.resolve_wpf_resource()
        self.current_dir = os.path.dirname(__file__)
        self.output = script.get_output()
        self.logger = script.get_logger()

    def setup(self):
        self.resolve_images()
        # Fix linked image resources - Not needed
        #self.resolve_browser_paths()
        pass

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
        
        
        gifs = [
            {"xaml_name": "clippy_blink_animation", "folder": "assets/clippy_blink"},
            {"xaml_name": "clippy_blink_animation", "folder": "assets/clippy_blink"},
            {"xaml_name": "clippy_blink_animation", "folder": "assets/clippy_blink"},
        ]

        for gif in gifs:
            folder_path = os.path.join(dir_path, gif["folder"])
            animation_keyframe_collection_name = gif["xaml_name"]
            
            try:
                animation_keyframe_collection = self.FindName(animation_keyframe_collection_name)
                animation_keyframes = animation_keyframe_collection.KeyFrames

                for keyframe in animation_keyframes:
                    print(type(keyframe))
                    if type(keyframe) == DiscreteObjectKeyFrame:
                        hopefully_bitmap = keyframe.Value
                        print(type(hopefully_bitmap))
                        if type(hopefully_bitmap) == BitmapImage:
                            initial_source = hopefully_bitmap.UriSource
                            
                            #end_bits = initial_source.AbsoluteUri.split('/lib/')[1]
                            end_bits_two = str(initial_source.AbsolutePath).split('/lib/')[1]

                            # https://learn.microsoft.com/en-us/dotnet/api/system.windows.media.imaging.bitmapimage.urisource?view=windowsdesktop-7.0#system-windows-media-imaging-bitmapimage-urisource
                            my_new_uri = os.path.join(dir_path, end_bits_two)
                            
                            bi = BitmapImage()
                            bi.BeginInit()
                            bi.UriSource = Uri(my_new_uri, UriKind.RelativeOrAbsolute)
                            bi.EndInit()
                            
                            keyframe.Value = bi
                            #print(my_new_uri)
                            #BitmapImage.UriSource = my_new_uri
            
            except Exception as error:
                # handle the exception
                print("An exception occurred:", error) # An exception occurred: division by zero
            
            else:
                print("Nothing went wrong")
                self.logger.warning("All good")

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
        #print("New state set...")

        self.state = new_state
        #update main display 

        self.render_custom_ui()
        
        # Update the UI
        self.show()

    # ------------------
    # View updaters - Create UI text based on data within this instance
    # ------------------
    def render_custom_ui(self):
        #update debug html
        temphtml_path = os.path.join(self.current_dir, 'temp.html')
        self.output.save_contents(temphtml_path)
        htmlContent = Read_file_incurrent_directory_to_string(temphtml_path)    
        self.DebugDisplay.NavigateToString(htmlContent)

        ds = self.state.data
        
        output_messages = []

        for item in ds:
            (status, message) = item
            output_messages.append(message)

        # Update what the user sees
        formatted_display = '\n'.join(output_messages)

        print(formatted_display)
        self.myTextBlock.Text = formatted_display


    # ------------------
    # UI Functionality - Button Controllers
    # ------------------
    def click_submit(self, sender, e):
        custom_event.raise_event(query_chat_gpt, self)


class Custom_Window_State():
    def __init__(self):
        self.data = []
        


# ----------------------------
# Functions called by UI buttons
# ----------------------------

def Read_file_incurrent_directory_to_string(file_path):
     try:
          with open(file_path, 'r') as file:
               html_code = file.read()
          return html_code
     
     except Exception as e:
        print ("Error reading file: {e}")
        return None

def query_chat_gpt(window):    
    state = Custom_Window_State()

 
    input_string = window.MyTextBox.Text


    if input_string == "enter prompt...":
        window.FindName("myTextBlock").Text = "CANT USE DEFAULT STRING"
        return

    window.FindName("myTextBlock").Text = "HELLO"
 
    try:
        x=('Message', 'Query hitting')
        print(x)
        state.data.append(x)
        
        output = []
        for status, message in state.data:
            output.append(message)
            formatted_display = '\n'.join(output)

            window.FindName("myTextBlock").Text = formatted_display
        
        
        #window.update_state(state)
        
        print(state)


        x = ('successful', 'Test')
        state.data.append(x)
        window.update_state(state)

    except Exception as error:
        # handle the exception
        window.logger.error("An exception occurred:", error) # An exception occurred: division by zero

    max_attempts = 3
    counter = 1
    context = ""
    url = 'http://127.0.0.1:8080/'

    client = WebClient()


    while counter <= max_attempts:
        json_data = '{{"client": "{0}. {1}."}}'.format(input_string, context)
        data = Encoding.UTF8.GetBytes(json_data)
        client.Headers.Add("Content-Type", "application/json; charset=utf-8")
        
        print("Info", "Sending data to server: {0}".format(json_data))  # Check the JSON structure
        #window.update_state(state)

        try:
            responseBytes = client.UploadData(url, "POST", data)
            responseString = Encoding.UTF8.GetString(responseBytes)
            if "MISSING" in responseString:
                x = ('missing', responseString.split("-")[1])
                state.data.append(x)
                window.update_state(state)
                return # unsuccessful

            clean_code = clean_code_snippet(responseString)
            print("Code response: ", clean_code)
            exec(clean_code)

            x = ('successful', '')
            state.data.append(x)
            window.update_state(state)
            return  # Successful execution, exit the loop
        
        except WebException as webEx:
            if webEx.Response is not None:
                responseStream = webEx.Response.GetResponseStream()
                if responseStream is not None:
                    reader = StreamReader(responseStream)
                    errorMessage = reader.ReadToEnd()
                    response_exception = clean_response_string(errorMessage)
                    x = ('exception', "Server error response: {0}".format(response_exception))
                    state.data.append(x)
                    window.update_state(state)
            else:
                x = ('exception', "WebException without response: : {0}".format(webEx.Message))
                state.data.append(x)
                window.update_state(state)
        
        except Exception as e:
            response_exception = clean_response_string(str(e))
            print("Exception: ", response_exception)
            x = ('exception', "Exception: {0}".format(response_exception))
            state.data.append(x)
            window.update_state(state)
        
        finally:
            context = "Consider this error: {0}".format(response_exception)
            counter += 1
            x = ('attempt', "Attempt: {0}".format(counter))
            state.data.append(x)
            window.update_state(state)
            if counter > max_attempts:
                print("Maximum attempts reached. Exiting.")
                x = ('failure', "Maximum attempts reached. Exiting.")
                state.data.append(x)
                break  # Ensure to break out of the loop

        