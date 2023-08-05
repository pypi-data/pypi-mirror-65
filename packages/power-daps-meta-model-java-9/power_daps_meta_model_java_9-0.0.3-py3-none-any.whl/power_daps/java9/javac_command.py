
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

from dap_core import common
from power_daps.java9 import java_helper

class JavacCommand:
  def __init__(self, source_dir, target_dir, classpath):
    self.source_dir = source_dir
    self.target_dir = target_dir
    self.classpath = classpath

  def run(self):
    cp_string = java_helper.classpath_string(self.classpath)

    common.run_command_in_shell('mkdir -p ' + self.target_dir)

    exit_code, output = common.run_command_in_shell(
      'find ' + self.source_dir + ' ' +
      '-type f -name "*.java" -print | xargs ' + common.which('javac') + ' ' +
      cp_string + " " +
      '-d ' + self.target_dir + ' -sourcepath ' + self.source_dir)
    try:
      output = output.decode()
    except (UnicodeDecodeError, AttributeError):
      pass

    return exit_code, output


