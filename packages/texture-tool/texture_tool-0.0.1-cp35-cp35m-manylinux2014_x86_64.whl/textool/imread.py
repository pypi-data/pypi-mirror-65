# Copyright 2019-2020 Stanislav Pidhorskyi
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

import imageio as io
import numpy as np
import textool


def imread(filename):
    if textool.check_if_pvr(filename):
        tex = textool.load_pvr(filename)
    if textool.check_if_dds(filename):
        tex = textool.load_dds(filename)
    img = io.imread(filename)
    if len(img.shape) != 3 and len(img.shape) != 4:
        raise RuntimeError('Wrong shape, must be 3-dimensional for 2D textures and 4-dimensional for 3D textures')
    if img.shape[-1] > 4:
        raise RuntimeError('Wrong number of channels. Expected 1, 2, 3 or 4, but got %f' % img.shape[-1])
    if img.shape[-1] == 1:
        img = np.concatenate([img, np.zeros_like(img[:, :, :1])], axis=2)
    if img.shape[-1] == 2:
        img = np.concatenate([img, np.zeros_like(img[:, :, :1])], axis=2)
    if img.shape[-1] == 3:
        img = np.concatenate([img, 255 * np.ones_like(img[:, :, :1])], axis=2)
    return textool.from_numpy(img)
