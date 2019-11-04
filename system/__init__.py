# Import shared objects 
from .shared import *
from .constants import *

from .interface import Interface
from .gps import GPS

# Application object
gui = Interface()

# GPS object
gps = GPS()