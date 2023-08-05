"""
Social-Ecological-System Motif Analyser (SMA).

The module provides the following main functions:
    - reading SES from CSV files
    - analysing SES', especially counting 3- and 4-motifs with or without
      taking nodal attributes into account
    - generating random SES'
    - exchanging information with R (using statnet on the R side)

"""

from .properties import *
from .helper import *
from .io import *
from .classify import *
from .iterate import *
from .analyse import *
from .analyse_triangles import *
from .analyse_cooccurrence import *
from .analyse_distribution import *
from .generate import *
from .draw import *

from .rbridge import *