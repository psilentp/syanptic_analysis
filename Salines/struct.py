#  struct.py
#  
#
#  Created by Theodore Lindsay on 10/2/09.
#  Copyright (c) 2009 University of Oregon. All rights reserved.
#
"""calculate recipe for a volume of saline given the desired concentrations"""

class Struct:
    """general structure class"""
    def __init__ (self, *argv, **argd):
        if len(argd):
            # Update by dictionary                                                                                            
            self.__dict__.update (argd)
        else:
            # Update by position                                                                                              
            attrs = filter (lambda x: x[0:2] != "__", dir(self))
            for n in range(len(argv)):
                setattr(self, attrs[n], argv[n])
