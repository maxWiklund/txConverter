# Copyright (C) 2020  Max Wiklund
#
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from txConverter.elements import image_element
import PyImageSequence
import unittest


class TestReleasableImageElement(unittest.TestCase):
    def test_get_command_list(self):
        seq = PyImageSequence.ImageElement("/mock/file.%04d.exr")
        seq.frames = [1001]
        e = image_element.ReleasableImageElement(seq)

        expected_result = ["maketx -v /mock/file.1001.exr -o /mock/file.1001.tx"]
        self.assertEqual(e.get_command_list(), expected_result)

    def test_get_command_list_gamma(self):
        seq = PyImageSequence.ImageElement("/mock/file.1009.exr")
        e = image_element.ReleasableImageElement(seq)
        e.gamma = True
 
        expected_result = ["maketx -v /mock/file.1009.exr --colorconvert sRGB linear -o /mock/file.1009.tx"]
        self.assertEqual(e.get_command_list(), expected_result)

    def test_get_command_list_multiple_frames(self):
        seq = PyImageSequence.ImageElement("/mock/file.%04d.exr")
        seq.frames = [1001, 1002, 1003]
        e = image_element.ReleasableImageElement(seq)

        expected_result = [
            "maketx -v /mock/file.1001.exr -o /mock/file.1001.tx",
            "maketx -v /mock/file.1002.exr -o /mock/file.1002.tx",
            "maketx -v /mock/file.1003.exr -o /mock/file.1003.tx"
        ]
        self.assertEqual(e.get_command_list(), expected_result)

    def test_get_command_list_no_frames(self):
        seq = PyImageSequence.ImageElement("/mock/file.exr")
        e = image_element.ReleasableImageElement(seq)

        expected_result = ["maketx -v /mock/file.exr -o /mock/file.tx"]
        self.assertEqual(e.get_command_list(), expected_result)

