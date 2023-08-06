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

import texture_tool


def describe(self):
    assert isinstance(self, texture_tool.PVRTexture)
    s = '<' + '\n'
    members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
    for attr in members:
        s += '\t' + attr + ': ' + str(getattr(self, attr)) + '\n'
    s += '\t' + str('Flipped X: ' + str(self.get_orientation(texture_tool.Axis.x))) + '\n'
    s += '\t' + str('Flipped Y: ' + str(self.get_orientation(texture_tool.Axis.y))) + '\n'
    s += '\t' + str('Width: ' + str(self.get_width())) + '\n'
    s += '\t' + str('Height: ' + str(self.get_height())) + '\n'
    s += '\t' + str('Depth: ' + str(self.get_depth())) + '\n'
    s += '\t' + str('dtype: ' + str(self.dtype)) + '\n'
    s += '>'
    return s
