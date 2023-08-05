#  Copyright 2016-2020 Prasanna Pendse <prasanna.pendse@gmail.com>
#
#  This file is part of power-daps.
#
#  power-daps is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  power-daps is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with power-daps.  If not, see <https://www.gnu.org/licenses/>.

import os, setuptools


def dirs_in(dirname, ignore_dirs):
  subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
  subfolders_without_ignore_dirs = []
  for dirname in list(subfolders):
    is_ignore_dir = False
    for ignore_dir in ignore_dirs:
      if ignore_dir in dirname:
        is_ignore_dir = True

    if not is_ignore_dir:
      subfolders_without_ignore_dirs.append(dirname)

    subfolders_without_ignore_dirs.extend(dirs_in(dirname, ignore_dirs))

  return subfolders_without_ignore_dirs

def append_pattern_to_dir_names(dir_names, patterns):
  dir_names_with_appended_patterns = []
  for dir_name in dir_names:
    for pattern in patterns:
      dir_names_with_appended_patterns.append(dir_name + pattern)

  return dir_names_with_appended_patterns

def remove_parent_dir_from_dir_names(dir_names, parent_dir):
  dir_names_without_parent_dir = []
  for dir_name in dir_names:
    dir_names_without_parent_dir.append(dir_name.replace(parent_dir, ""))

  return dir_names_without_parent_dir


def generate_glob_patterns(depth):
  glob_patterns = ["*", ".*"]
  for i in range(depth - 1):
    glob_patterns_to_add = []
    for p in glob_patterns:
      glob_patterns_to_add.append(p + "/*")
      glob_patterns_to_add.append(p + "/.*")
    glob_patterns += glob_patterns_to_add

  return glob_patterns

with open("README.md", "r") as fh:
  long_description = fh.read()

print(setuptools.find_packages(where="src"))
parent_dir = "src/power_daps/python3/templates"
package_data_templates = append_pattern_to_dir_names(
    dirs_in(parent_dir,
           ["__pycache__", "egg-info"]),
           ["/*", "/.*"]
    )

print(str(package_data_templates))
# package_data_patterns = ['*', '.*', "*/*", "*/.*", ".*/*", ".*/.*", "*/*/*", "*/*/*/*"]
package_data_patterns = generate_glob_patterns(4)
# package_data_patterns = ["power_daps/python3/templates/init/test/*"]
# print(str(package_data_patterns))

setuptools.setup(
  name="power-daps-meta-model-python-3",
  version="0.0.3",
  author="Prasanna Pendse",
  author_email="prasanna.pendse@gmail.com",
  description="Python 3 meta-model for power-daps - a build tool that builds apps in multiple languages",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/power-daps/power-daps",
  package_dir={"": "src"},
  packages=setuptools.find_packages(where="src"),
  entry_points={'power_daps.meta_model.actions': [
    'power_daps.python3.actions=power_daps.python3.actions']},
  package_data={
    "power_daps.python3.templates": package_data_patterns,
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
