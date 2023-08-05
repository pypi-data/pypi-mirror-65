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
from dap_core.base_actions.dap_action_base import DapActionBase
from power_daps.java9 import java_helper
from power_daps.java9.java_command import JavaCommand


class UnitTestAction(DapActionBase):

  def __init__(self, source_dir="test", target_dir="target/test", classpath=".:target/production:target/test"):
    super().__init__()
    self.source_dir = source_dir
    self.target_dir = target_dir
    self.classpath = classpath

  def run(self):
    super().run()

    common.run_command_in_shell('mkdir -p ' + self.target_dir)

    test_classes = java_helper.list_of_test_classes(self.source_dir)
    if not test_classes:
      common.print_verbose("No test classes found. Not running unit tests.")
      return 0, ""
    main_class = 'org.junit.runner.JUnitCore'
    args_to_main_class = test_classes

    return JavaCommand(main_class, args_to_main_class, self.classpath).run()


def action():
  return UnitTestAction()
