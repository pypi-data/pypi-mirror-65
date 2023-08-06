#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from setuptools import setup
from setuptools import find_packages

packages = find_packages()

setup(
    name = "py-antilibrary",
    version = "0.0.2",
    description = "API Client for antilibrary.xyz, a demo app for thundergolfer/example-bazel-monorepo",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers = ["Programming Language :: Python", "Programming Language :: Python :: 3.5", "Programming Language :: Python :: 3.6", "Programming Language :: Python :: 3.7", "Programming Language :: Python :: 3.8", "License :: OSI Approved :: MIT License", "Intended Audience :: Developers", "Environment :: Console"],
    keywords = "antilibrary apiwrapper apiclient demo",
    url = "https://github.com/thundergolfer/example-bazel-monorepo/",
    author = "Jonathon Belotti",
    author_email = "jonathon.i.belotti@gmail.com",
    license = "MIT",
    packages=packages,
    install_requires=["requests~=2.23.0"],
    zip_safe=False,
)
