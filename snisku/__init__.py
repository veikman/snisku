# -*- coding: utf-8 -*-
"""Files in this directory constitute the source code of Snisku.

Snisku is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Snisku is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Snisku.  If not, see <http://www.gnu.org/licenses/>.

Copyright 2019–2020 Viktor Eikman and Icomera AB.

"""

from typing import Sequence

from . import argparse
from . import exc
from . import kvs
from . import param
from . import types
from . import ui
from . import whitelist  # Deprecated.

__all__: Sequence[str] = ("argparse", "exc", "kvs", "param", "types", "ui",
                          "whitelist")
__version__ = '0.3.0'
