# Import the necessary Revit and DB modules
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import BuiltInCategory, UnitUtils

# Access the current Revit document
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# Prompt the user to select a single element (a column)
selection = uidoc.Selection.GetElementIds()

if len(selection) == 1:
    # Get the selected element
    element = doc.GetElement(selection[0])

    # Check if the selected element is a column
    if element.Category.Id.IntegerValue == int(BuiltInCategory.OST_StructuralColumns):
        # Get the length parameter
        length_param = element.LookupParameter("Length")

        if length_param:
            # Get the length value in feet
            length_in_feet = length_param.AsDouble()

            # Extract feet and inches
            feet = int(length_in_feet)
            remaining_length_in_inches = (length_in_feet - feet) * 12
            inches = int(remaining_length_in_inches)
            remaining_fractional_inches = (remaining_length_in_inches - inches)
            fractional_inches = round(remaining_fractional_inches * 16)

            print(f"Selected Column Length: {feet}' {inches} {fractional_inches}/16\"")
        else:
            print("The selected column does not have a 'Length' parameter.")
    else:
        print("The selected element is not a column.")
else:
    print("Please select a single column to retrieve its length.")
