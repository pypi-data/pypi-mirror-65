"""A reduced version of the Open Babel chemical toolbox to work with
ManipulateAggregates
"""

# Copyright (C) 2020 by Torsten Sachse
# All rights reserved.
#
# This file is part of MaAg-bel.
# The contents of this file are covered by the terms of the GPL v2 license,
# see the file COPYING in the root if the repository for the license.
#
# MaAg-bel is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation version 2 of the License.
#
# MaAg-bel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MaAg-bel. If not, see <http://www.gnu.org/licenses/>.

import os

# Set some environment variables needed by the library if not yet set
__MAABEL_PATH = os.path.dirname(os.path.realpath(__file__))
# The path to some data files needed by the forcefields
__DATA_PATH = os.path.join(__MAABEL_PATH, "data")
if os.environ.get("BABEL_DATADIR", None) is None:
    os.environ["BABEL_DATADIR"] = __DATA_PATH
# Import the C++ functionality
from .cpp import *
