# Import the necessary Revit and DB modules
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI.Selection import ObjectType

# Access the current Revit document
uidoc = __revit__.ActiveUIDocument

# Prompt the user to select a single element (a wall)
# uiapp = __revit__.Application
selection = uidoc.Selection.GetElementIds()

# print(selection)

selected_element = doc.GetElement(selection[0])

# print(selected_element)

wall_location = selected_element.Location
wall_curve = wall_location.Curve

# Get the length of the wall in feet
wall_length = wall_curve.Length

print(f"Selected Wall Length: {wall_length:.2f} feet")