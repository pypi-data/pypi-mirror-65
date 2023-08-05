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


def classpath_string(classpath=""):
  if classpath != "":
    cp_string = " -cp " + classpath + ":" + libs_classpath()
  else:
    cp_string = " -cp " + libs_classpath()
  return cp_string


def libs_classpath():
  libs = common.run_command_in_shell('find lib/java -type f -name "*.jar" -print')[1]
  return ":".join(libs.splitlines())


def list_of_test_classes(test_source_dir):
  test_classes = common.run_command_in_shell('find ' + test_source_dir +  ' -type f -name "*Test.java" -print')[1].splitlines()
  return [test_class.replace(test_source_dir + "/", "").replace(".java", "").replace("/", ".") for test_class in test_classes]
