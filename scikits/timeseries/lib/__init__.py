"""
:author: Pierre GF Gerard-Marchant & Matt Knox
:contact: pierregm_at_uga_dot_edu - mattknox_ca_at_hotmail_dot_com
:version: $Id: __init__.py 1232 2008-08-27 00:22:43Z pierregm $
"""
__author__ = "Pierre GF Gerard-Marchant & Matt Knox ($Author: pierregm $)"
__revision__ = "$Revision: 1232 $"
__date__     = '$Date: 2008-08-27 02:22:43 +0200 (Wed, 27 Aug 2008) $'


import interpolate
from interpolate import *
import moving_funcs
from moving_funcs import *

__all__ = []
__all__ += interpolate.__all__
__all__ += moving_funcs.__all__
