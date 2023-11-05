# Import the necessary Revit and DB modules
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI.Selection import ObjectType

# Access the current Revit document
uidoc = __revit__.ActiveUIDocument

# Prompt the user to select a single element (a wall)
# uiapp = __revit__.Application
selection = uidoc.Selection
