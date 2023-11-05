#from pyrevit import script
#from pyrevit.revit import ui
#from user_interface import PdsoControlWindow

#import pdso_classes
#import ui_functions

#from pyrevit.coreutils import Timer

import pdso_fx
import user_interface
from pyrevit import script

logger = script.get_logger()

logger.warning("Running checks")
passed_checks = True

state =user_interface.PdsoControlWindow_State()

if (passed_checks == True):
    (passed_checks, result_state) = pdso_fx.basic_setup_check_for_area_schemes(state)
    state = result_state
logger.warning("1ST CHECK DONE")

if(passed_checks == True):
    print("2nd check starting")
    (passed_checks, result_state) = pdso_fx.basic_setup_check_areas(state)
    state = result_state
logger.warning("2ND CHECK DONE")

if(passed_checks == True):
    (passed_checks, result_state) = pdso_fx.basic_setup_check_area_parameters(state)
    state = result_state
logger.warning("3RD CHECK DONE")

if(passed_checks == True):
    (passed_checks, result_state) = pdso_fx.basic_setup_check_pdsos(state)
    state = result_state
logger.warning("4TH CHECK DONE")

logger.warning("Check complete")
'''
# importing the module
from collections import defaultdict

from attrdict import AttrDict, AttrMap, AttrDefault
from attrdict.merge import merge


# AttrDict Requires full frame
__fullframeengine__ = True
'''

'''
# creating the first dictionary
a = {'foo': 'bar', 'alpha': {'beta': 'a', 'a': 'a'}}
 
# creating the second dictionary
b = {'lorem': 'ipsum', 'alpha': {'bravo': 'b', 'a': 'b'}}
 
# combining the dictionaries, right overwrites left
c = merge(AttrDict(a), AttrDict(b))
 
print(type(c))
print(c)
'''

#attr = defaultdict(dict)
#attr['test']['foo'] = "Mr"

'''
data = AttrMap({
    'test':{
        "foo" : "Miss",
        "bar" : "Broskie"
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

new_data = AttrMap({
    'test':{},
    "basic_setup_checks" : {},
    "area_checks":{},
    "pdso_checks":{}
})

new_data.test.foo = "Working?"

merged_data = data + new_data

print(merged_data)
print("\n\n\n")
'''

'''
timer = Timer()

# SLOWER
timer.restart()
data = data + new_data
time_a = timer.get_time()
print("Time a: " + str(time_a))

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data)
print("\n\n\n")
#Time a: 0.027717590332


# FASTER
timer.restart()
data_b = data + new_data
time_b = timer.get_time()
print("Time b: " + str(time_b))

pp.pprint(data_b)
print("\n\n\n")
#Time b: 0.000999450683594
'''



'''
#This does not work. Cannot add entries like this
more_data = AttrMap()
more_data.test = {}
more_data.test.foo = "Something"
print (more_data)
print("\n\n\n")

#Or like this
diff_data = AttrDefault({})
diff_data.test.foo = "Something else"

a = attrdict.AttrMap({'foo': 'bar'})
print(a["foo"])



print (c.test.foo)
'''