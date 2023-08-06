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

# import pypvrtex
#
#
# class Texture:
#     """Generic texture object
#     """
#
#     def __init__(self,
#                  width, height, depth=1,
#                  pixel_format=pypvrtex.PixelFormat.RGBA8888,
#                  channel_type=pypvrtex.ChannelType.UnsignedByteNorm,
#                  colour_space=pypvrtex.ColourSpace.lRGB,
#                  x_flipped=False,
#                  y_flipped=False,
#                  z_flipped=False):
#
#         self.channel_type = channel_type
#         assert self.channel_type.name in getattr(pypvrtex.ChannelType, '__entries')
#         self.colour_space = colour_space
#         assert self.colour_space.name in getattr(pypvrtex.ColourSpace, '__entries')
#
#         if isinstance(pixel_format, str):
#             if pixel_format in pypvrtex.PixelFormat.__entries:
#                 pixel_format = pypvrtex.PixelFormat.__entries[format][0]
#             else:
#                 pixel_format = pypvrtex.format_from_string(format)
#         else:
#             self.pixel_format = pixel_format
#         assert self.pixel_format.name in getattr(pypvrtex.PixelFormat, '__entries')
#         self.width = width
#         self.height = height
#         self.depth = depth
#         assert(all(isinstance(x, int) for x in [self.width, self.height, self.depth]))
#
#     @property
#     def pow_of_2(self):
#         return all(pypvrtex.is_power_of_two(x) for x in input.shape[:-1])
#
#     @property
#     def shape(self):
#         return [self.depth, self.height, self.width, self.channel_count]
#
#     @property
#     def channel_count(self):
#         return
#

