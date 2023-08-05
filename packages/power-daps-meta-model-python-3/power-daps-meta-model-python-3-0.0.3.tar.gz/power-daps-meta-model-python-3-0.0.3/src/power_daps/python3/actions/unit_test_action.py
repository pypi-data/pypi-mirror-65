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

import glob, os, sys
from shutil import which
from dap_core import common

class UnitTestAction():
  name = "unit_test"

  def __init__(self):
    return

  def run(self):
    common.print_info("Running " + self.name + " action")
    exit_code = 0
    for test_dir in glob.iglob('**/test', recursive=True):
      original_working_directory = os.getcwd()
  
      run_directory = os.path.join(original_working_directory, str(test_dir))
      common.print_info("Running tests in " + str(run_directory))
      common.print_verbose("Changing directory to " + str(run_directory))
      os.chdir(run_directory)
  
      tests = []
      for filename in glob.iglob('**/*.py', recursive=True):
          tests.append(filename)
      command = [which('python3'), '-m', 'unittest']
      command.extend(tests)
      subprocess_exit_code, output = common.run_command(command)
      if subprocess_exit_code != common.SUCCESS:
        exit_code = common.FAILED
      common.print_verbose(output)
      common.continue_if_failed(subprocess_exit_code, output)
  
      common.print_verbose("Changing directory to " + str(original_working_directory))
      os.chdir(original_working_directory) 
    
    return exit_code, ""

def action():
   return UnitTestAction()

