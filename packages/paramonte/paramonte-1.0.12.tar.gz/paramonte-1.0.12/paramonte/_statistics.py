#**********************************************************************************************************************************
#**********************************************************************************************************************************
#
#  ParaMonte: plain powerful parallel Monte Carlo library.
#
#  Copyright (C) 2012-present, The Computational Data Science Lab
#
#  This file is part of ParaMonte library.
#
#  ParaMonte is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, version 3 of the License.
#
#  ParaMonte is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with ParaMonte.  If not, see <https://www.gnu.org/licenses/>.
#
#**********************************************************************************************************************************
#**********************************************************************************************************************************

from _AutoCorr import AutoCorr
from _CorCovMat import CorCovMat, CorMat, CovMat

import numpy as _np
import typing as _tp
import pandas as _pd
import weakref as _wref

class _Struct: pass

def getMaxLogFunc( dataFrame : _pd.DataFrame
                 , column    : _tp.Optional[ str ] = "SampleLogFunc"
                 ):
    _offset = dataFrame.columns.get_loc(column) + 1
    maxLogFunc = _Struct()
    maxLogFunc.idrow = dataFrame[[column]].idxmax().values[0]
    maxLogFunc.value = dataFrame[[column]].iat[maxLogFunc.idrow,0]
    maxLogFunc.dfrow = dataFrame.iloc[maxLogFunc.idrow,:]
    maxLogFunc.state = dataFrame.iloc[maxLogFunc.idrow,_offset:]
    return maxLogFunc
