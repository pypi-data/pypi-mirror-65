# Copyright 2020 Stanislav Pidhorskyi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import sys
import os

_here = os.path.abspath(__file__)
_here = os.path.dirname(_here)


def _load_libpvr():
    import platform
    import ctypes
    lib_name = 'libPVRTexLib' + ('.dylib' if platform.system() == 'Darwin' else '.so')
    lib_path = os.path.join(_here, '../', lib_name)
    ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)


# if running debug session
if os.path.exists("cmake-build-debug/"):
    print('Debugging!')
    sys.path.insert(0, "cmake-build-debug/")
    # sys.path.insert(0, "cmake-build-release/")
else:
    _load_libpvr()

del os
del sys


from _pypvrtex import *
