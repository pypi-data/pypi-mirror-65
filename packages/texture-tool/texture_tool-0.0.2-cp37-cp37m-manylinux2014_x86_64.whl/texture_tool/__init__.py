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

from texture_tool._pvrtex_loader import *
from texture_tool.imread import imread
from texture_tool.describe import describe as _describe
from texture_tool import utils
from texture_tool.downsample2x import downsample2x
from texture_tool.generate_mipmaps import generate_mipmaps
from texture_tool.transcode import transcode
from texture_tool.cubemap_from_equirectangular import cubemap_from_equirectangular


def parse_bin_format(pixel_format):
    pixel_format = np.uint64(pixel_format)
    compressed = (pixel_format & np.uint64(0xFFFFFFFF00000000)) == 0
    if compressed:
        return compressed, None, None
    byte_list = []
    for i in range(8):
        byte_list.append(int(pixel_format & np.uint64(0xff)))
        pixel_format = pixel_format >> np.uint64(8)

    channels = byte_list[:4]
    sizes = byte_list[4:]
    channels = filter(lambda x: x != 0, channels)
    channels = [chr(x) for x in channels]
    sizes = filter(lambda x: x != 0, sizes)
    return compressed, channels, sizes


@property
def channel_count(self):
    compressed, channels, sizes = parse_bin_format(np.uint64(self.pixel_format))
    return len(channels)


@property
def pixel_format_str(self):
    compressed, channels, sizes = parse_bin_format(np.uint64(self.pixel_format))
    if compressed:
        return 'compressed'
    return "".join(channels) + "".join([str(x) for x in sizes])


@property
def shape(self):
    s = [self.get_height(0), self.get_width(0), self.channel_count]
    if self.get_depth() > 1:
        return tuple([self.get_depth()] + s)
    return tuple(s)


@property
def is_compressed(self):
    compressed, channels, sizes = parse_bin_format(np.uint64(self.pixel_format))
    return compressed != 0


@property
def dtype(self):
    _, _, sizes = parse_bin_format(np.uint64(self.pixel_format))
    if self.channel_type == ChannelType.Float:
        assert all(x == 32 for x in sizes)
        return np.float32

    if self.channel_type == ChannelType.Float:
        assert all(x == 32 for x in sizes)
        return np.float32

    if self.channel_type == ChannelType.UnsignedByteNorm or self.channel_type == ChannelType.UnsignedByte:
        return np.uint8

    if self.channel_type == ChannelType.SignedByteNorm or self.channel_type == ChannelType.SignedByte:
        return np.int8

    if self.channel_type == ChannelType.UnsignedShortNorm or self.channel_type == ChannelType.UnsignedShort:
        return np.uint16

    if self.channel_type == ChannelType.SignedShortNorm or self.channel_type == ChannelType.SignedShort:
        return np.int16

    if self.channel_type == ChannelType.UnsignedIntegerNorm or self.channel_type == ChannelType.UnsignedInteger:
        return np.uint32

    if self.channel_type == ChannelType.SignedIntegerNorm or self.channel_type == ChannelType.SignedInteger:
        return np.int32

    return None


def cast_to_float(self, x):
    if self.dtype == np.float32:
        return x.astype(np.float64)

    if self.dtype == np.uint8:
        return x.astype(np.float64) / 255.0

    if self.dtype == np.int8:
        return x.astype(np.float64) / 127.0

    if self.dtype == np.uint16:
        return x.astype(np.float64) / 65535.0

    if self.dtype == np.int16:
        return x.astype(np.float64) / 32767.0

    if self.dtype == np.int32 or self.dtype == np.uint32:
        return x.astype(np.float64)


def cast_from_float(self, x):
    if self.dtype == np.float32:
        return x.astype(self.dtype)

    if self.dtype == np.uint8:
        return np.clip(x * 255.0, 0, 255).astype(self.dtype)

    if self.dtype == np.int8:
        return np.clip(x * 127.0, -128, 127).astype(self.dtype)

    if self.dtype == np.uint16:
        return np.clip(x * 65535, 0, 65535).astype(self.dtype)

    if self.dtype == np.int16:
        return np.clip(x * 32767, -32768, 32767).astype(self.dtype)

    if self.dtype == np.int32 or self.dtype == np.uint32:
        return x.astype(self.dtype)


def view(texture, mipmap=0, face=0):
    return np.array(texture.open_view(mipmap, face), copy=False)


def is_power_of_two(n):
    """Return True if n is a power of two."""

    if isinstance(n, list) or isinstance(n, tuple):
        return all(is_power_of_two(x) for x in n)
    if n <= 0:
        return False
    else:
        return n & (n - 1) == 0


@property
def _is_power_of_two(self):
    return is_power_of_two(self.shape[:-1])


@property
def needs_gamma_correction(self):
    return self.dtype == np.uint8 or self.dtype == np.uint16 or self.dtype == np.uint32


PVRTexture.__str__ = _describe
PVRTexture.channel_count = channel_count
PVRTexture.is_compressed = is_compressed
PVRTexture.pixel_format_str = pixel_format_str
PVRTexture.shape = shape
PVRTexture.dtype = dtype
PVRTexture.view = view
PVRTexture.cast_to_float = cast_to_float
PVRTexture.cast_from_float = cast_from_float
PVRTexture.is_power_of_two = _is_power_of_two
PVRTexture.needs_gamma_correction = needs_gamma_correction

