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

# IMPORT STANDARD LIBRARIES
import copy

# IMPORT THIRD-PARTY LIBRARIES
import PyImageSequence


class ReleasableImageElement(object):
    """Row data class."""

    def __init__(self, imSeq: PyImageSequence.ImageElement) -> None:
        """Initialize class and do nothing.

        Args:
            imSeq: Image sequence object.

        """
        super(ReleasableImageElement, self).__init__()
        self.input_element = imSeq
        self.output_element = copy.copy(imSeq)
        self.output_element.ext = ".tx"
        self.enabled = True
        self.gamma = False
        self.duplicated = False
        self.name = self.input_element.basename()

    @property
    def tool_tip(self) -> str:
        """str: Get element tooltip."""
        if self.duplicated:
            return "Element is a duplicate and can't be converted."
        return "File path: {}".format(self.input_element.getFilePath())

    @property
    def output(self):
        """str: Image name."""
        return self.output_element.name

    @output.setter
    def output(self, value):
        self.output_element.name = value

    def build_command(self, input_path, output_path) -> str:
        """Build conversion command.
 
        Args:
            input_path: Source file path.
            output_path: Destination file path.

        Returns:
            Command for converting image to tx file.

        """
        command = ["maketx"]  # Name of executable.
        command.append("-v")  # Verbose mode.
        command.append(input_path)  # File to convert.
        if self.gamma:
            command.extend(["--colorconvert", "sRGB", "linear"])
        command.extend(["-o", output_path])
        return " ".join(command)

    def get_command_list(self) -> [str]:
        """Generate commands for converting image sequence to tx.
        
        Returns:
            Conversion commands.

        """
        convert_commands = []
        for path_in, path_out in zip(self.input_element.getPaths(), self.output_element.getPaths()):
            convert_commands.append(self.build_command(path_in, path_out))

        return convert_commands
