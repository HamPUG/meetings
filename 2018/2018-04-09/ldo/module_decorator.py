#+
# How to construct a nested module in the absence of direct Python
# syntax for same: build it as a class and then use the contents
# of that to populate a module object.
#-

import types

def module(cłass) :
    result = types.ModuleType(cłass.__name__, cłass.__doc__)
    allnames = []
    for name in dir(cłass) :
        if not name.startswith("__") :
            setattr(result, name, getattr(cłass, name))
            allnames.append(name)
        #end if
    #end for
    result.__all__ = allnames
    return \
        result
#end module

@module
class test_module :
    "this is a module built from a class."

    def func() :
        "this function is not a class method."
        print("hi there!")
    #end func

#end test_module
