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

from setuptools import setup
import txConverter

setup(
    name="txConverter",
    version=txConverter.__version__,
    packages=[
        "tests",
        "tests.elements",
        "txConverter",
        "txConverter.gui",
        "txConverter.gui.widgets",
        "txConverter.elements",
    ],
    scripts=["bin/tx_converter"],
    url="",
    license="Apache License 2.0",
    author="Max Wiklund",
    author_email="info@maxwiklund.com",
    description="GUI for converting images to tx files.",
)
