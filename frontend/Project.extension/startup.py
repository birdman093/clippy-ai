"""Example of IronPython script to be executed by pyRevit on extension load

The script filename must end in startup.py

To Test:
- rename file to startup.py
- reload pyRevit: pyRevit will run this script after successfully
  created the DLL for the extension.

pyRevit runs the startup script in a dedicated IronPython engine and output
window. Thus the startup script is isolated and can not hurt the load process.
All errors will be printed to the dedicated output window similar to the way
errors are printed from pyRevit commands.
"""
#pylint: disable=import-error,invalid-name,broad-except,superfluous-parens
#pylint: disable=unused-import,wrong-import-position,unused-argument
#pylint: disable=missing-docstring
#import attrdict
#import attrdict


'''
import os.path as op

from pyrevit import HOST_APP, framework
from pyrevit import revit, DB, UI
from pyrevit import forms
from pyrevit import routes
'''

# add your module paths to the sys.path here
# sys.path.append(r'path/to/your/module')

#sys.path.append(r'C:\Python27\Lib\site-packages')

'''
print('Startup script execution test.')
print('\n'.join(sys.path))
'''

# test imports from same directory and exensions lib
#from attrdict import AttrDict




'''
data = attrdict.AttrMap({
    'test':{
        "foo" : "Miss"
    },
    "basic_setup_checks" : {
        "area_schemes_requested" : ["Mary", "Mack"],    # list of... strings ?
        "area_schemes_found": ["All", "Dressed", "In", "Black"],         # list of... strings?
        "count_of_areas_found" : 0,      # int
        "area_parameters_missing" : ["With", "Silver", "Buttons"],   # list of... strings?
        "pdso_family_name" : "All Down Her Back",          # string
        "pdso_family_is_loaded" : True,     # bool
        "count_of_pdso_instances" : 0,   # int
        "pdso_parameters_missing" : ["And", "An", "Itsie", "Spider"]    # list of... strings?
    },
    "area_checks":{},
    "pdso_checks":{}
})

new_data = attrdict.AttrMap({
    'test':{
        "foo" : "Mr"
    },
})

more_data = attrdict.AttrMap()
more_data.test.foo = "Mx"

#time test this
#data = data + new_data

#vs this
#b = data + new_data

c = data + more_data

a = attrdict.AttrMap({'foo': 'bar'})
print(a["foo"])



print (c.test.foo)

'''

#print('lib/ import works in startup.py')