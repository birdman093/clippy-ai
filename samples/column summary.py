# Import the necessary Revit and DB modules
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

# Access the current Revit document
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# Create a FilteredElementCollector to retrieve all columns
collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType()

# Initialize a list to store the column lengths
column_lengths = []

# Iterate through the columns and calculate their lengths
for column in collector:
    # Get the length parameter
    length_param = column.LookupParameter("Length")

    if length_param:
        # Get the length value
        length = length_param.AsDouble()
        family_name = column.Symbol.FamilyName
        instance_name = column.Name
        column_lengths.append((family_name, instance_name, length))

# Print the list of column lengths without format strings
for family_name, instance_name, length in column_lengths:
    print("Family: " + family_name + ", Instance: " + instance_name + ", Length: " + str(length) + " feet")