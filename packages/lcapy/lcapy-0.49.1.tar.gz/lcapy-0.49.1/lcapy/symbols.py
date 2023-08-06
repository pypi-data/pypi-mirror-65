"""This file defines special symbols f, s, t, and omega.

Copyright 2014--2020 Michael Hayes, UCECE

"""

# The following are Lcapy expressions.  For example, f is an fExpr
# object wrapping the fsym symbol.
from .fexpr import f
from .texpr import t
from .sexpr import s
from .omegaexpr import omega

# Ipmort common SymPy symbols.
from .sym import pi, j, oo, inf

jomega = j * omega
