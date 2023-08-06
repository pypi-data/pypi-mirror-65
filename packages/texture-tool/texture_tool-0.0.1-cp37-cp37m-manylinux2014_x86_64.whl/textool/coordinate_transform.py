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


def cube_to_direction(uv, face):
    _uv = uv
    uv = _uv.reshape(np.prod(_uv.shape[:-1]), 2)
    v = np.zeros([uv.shape[0], 3], dtype=_uv.dtype)

    if face == 0:
        v[:, 0] = 1.0
        v[:, 2] = 1.0 - 2.0 * uv[:, 0]
        v[:, 1] = 1.0 - 2.0 * uv[:, 1]
    elif face == 1:
        v[:, 0] = -1.0
        v[:, 2] = 2.0 * uv[:, 0] - 1.0
        v[:, 1] = 1.0 - 2.0 * uv[:, 1]
    elif face == 2:
        v[:, 1] = 1.0
        v[:, 0] = 2.0 * uv[:, 0] - 1.0
        v[:, 2] = 2.0 * uv[:, 1] - 1.0
    elif face == 3:
        v[:, 1] = -1.0
        v[:, 0] = 2.0 * uv[:, 0] - 1.0
        v[:, 2] = 1.0 - 2.0 * uv[:, 1]
    elif face == 4:
        v[:, 2] = 1.0
        v[:, 0] = 2.0 * uv[:, 0] - 1.0
        v[:, 1] = 1.0 - 2.0 * uv[:, 1]
    elif face == 5:
        v[:, 2] = -1.0
        v[:, 0] = 1.0 - 2.0 * uv[:, 0]
        v[:, 1] = 1.0 - 2.0 * uv[:, 1]

    # v /= np.linalg.norm(v, axis=1, keepdims=True)
    return v.reshape(list(_uv.shape)[:-1] + [3])


def direction_to_equirectangular(v):
    _v = v
    v = _v.reshape(np.prod(_v.shape[:-1]), 3)
    uv = np.zeros([v.shape[0], 2], dtype=_v.dtype)

    longitude = np.arctan2(v[:, 2], v[:, 0])
    latitude = np.arctan2(v[:, 1], (v[:, 0] ** 2.0 + v[:, 2] ** 2) ** 0.5)

    u = (longitude + np.pi) / (2.0 * np.pi)
    v = (np.pi / 2.0 - latitude) / np.pi
    uv[:, 0] = u
    uv[:, 1] = v
    return uv.reshape(list(_v.shape)[:-1] + [2])


def cube_to_equirectangular(uv, face):
    return direction_to_equirectangular(cube_to_direction(uv, face))

