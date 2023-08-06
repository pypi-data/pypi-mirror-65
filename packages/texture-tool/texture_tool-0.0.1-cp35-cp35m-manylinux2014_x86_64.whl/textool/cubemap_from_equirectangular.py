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

import numpy as np
from textool.coordinate_transform import cube_to_equirectangular
import textool
import warnings
from textool.downsample2x import downsample2x
import scipy.ndimage
#import matplotlib.pyplot as plt


def cubemap_from_equirectangular(texture, cubemap_size=None, gamma=2.2):
    v = textool.view(texture, 0, 0)
    img = texture.cast_to_float(v)

    if cubemap_size is None:
        cubemap_size = int(texture.get_width(0) / 4)

    cube_texture = textool.new_texture(texture.pixel_format, cubemap_size, cubemap_size, 1, 1, 1, 6, texture.colour_space, texture.channel_type, False)

    if texture.needs_gamma_correction:
        img = np.power(img, gamma)

    max_val = img.max()
    img /= max_val

    width = cubemap_size
    height = cubemap_size
    grid = np.stack([np.repeat(np.arange(width)[None, ...], height, axis=0), np.repeat(np.arange(height)[..., None], width, axis=1)], axis=2).astype(np.float64)
    grid[:, :, 0] = (grid[:, :, 0] + 0.5) / height
    grid[:, :, 1] = (grid[:, :, 1] + 0.5) / width

    for face in range(6):
        r = []
        g = cube_to_equirectangular(grid, face)
        g = np.stack([g[:, :, 1] * img.shape[0], g[:, :, 0] * img.shape[1]])

        for plane in range(img.shape[-1]):
            _img = img[..., plane]
            r.append(scipy.ndimage.map_coordinates(_img, g, order=1, mode='mirror'))
        cube_face = np.stack(r, axis=-1)

        #plt.subplot(611 + face)
        #plt.imshow(cube_face * max_val)

        v = textool.view(cube_texture, 0, face)
        img_to_save = cube_face * max_val
        if texture.needs_gamma_correction:
            img_to_save = np.clip(img_to_save, 0, None)
            img_to_save = np.power(img_to_save, 1.0 / gamma)
        v[:] = cube_texture.cast_from_float(img_to_save)
    #plt.show()
    return cube_texture
