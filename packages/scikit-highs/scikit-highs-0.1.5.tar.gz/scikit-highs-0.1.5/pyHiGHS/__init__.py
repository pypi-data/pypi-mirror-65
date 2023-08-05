
import pathlib
from os import chdir
chdir(str(pathlib.Path(__file__).parent))

# Wrappers
from pyHiGHS.highs_wrapper import highs_wrapper

# Constants
from pyHiGHS.highs_wrapper import (
    CONST_I_INF,
    CONST_INF,
)
