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

import textool
import numpy as np
import warnings
from textool.downsample2x import downsample2x


def generate_mipmaps(texture, gamma=2.2):
    texture = textool.copy(texture)
    res = textool.inplace_generate_mipmaps(texture, textool.ResizeMode.Nearest, np.uint32(-1))  # preallocate space
    if not res:
        raise RuntimeError('Operation failed')
    v = textool.view(texture, 0, 0)
    img = texture.cast_to_float(v)

    if texture.needs_gamma_correction:
        img = np.power(img, gamma)

    max_val = img.max()
    img /= max_val

    downsample_type = 'bspline'
    if texture.is_power_of_two and texture.dtype == np.float32:
        downsample_type = 'area_average'
        warnings.warn("bspline may produce artifacts with hdr. Texture is POT, so using area_average instead",
                      UserWarning)

    for i in range(1, texture.num_mip_levels):
        img = downsample2x(img, type=downsample_type)
        v = textool.view(texture, i, 0)
        img_to_save = img * max_val
        if texture.needs_gamma_correction:
            img_to_save = np.clip(img_to_save, 0, None)
            img_to_save = np.power(img_to_save, 1.0 / gamma)
        v[:] = texture.cast_from_float(img_to_save)
    return texture
