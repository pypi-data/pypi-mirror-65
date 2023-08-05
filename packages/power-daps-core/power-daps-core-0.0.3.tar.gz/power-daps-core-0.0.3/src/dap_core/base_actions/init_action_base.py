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

import os
from dap_core import common
from dap_core.util import str_util, template_util, git_util
from dap_core.base_actions.dap_action_base import DapActionBase


class InitActionBase(DapActionBase):

  def __init__(self, pre_copy_commands=[], additional_find_and_replace_dict={}):
    super().__init__()
    self.project_dir = '.'
    self.project_name = os.getcwd().split('/')[-1]

    self.find_and_replace_dict = {
      "PROJECT_NAME": self.project_name,
      "PROJECT_CAMELIZED_NAME": str_util.camelize(self.project_name)}

    additional_find_and_replace_dict.update(self.find_and_replace_dict)
    self.pre_copy_commands = pre_copy_commands

  def run(self):
    super().run()

    template_util.check_that_name_does_not_have_dashes(self.project_name)

    for pre_copy_command in self.pre_copy_commands:
      pre_copy_command.run()

    template_util.copy_template_files_to(self.project_dir, common.action_name(self))
    template_util.find_and_replace_in_file_names_and_content(self.project_dir, self.find_and_replace_dict)
    git_util.git_init_or_add(self.project_dir)
    common.print_raw("Initialized new " + common.meta_model() + " application.")

    return 0, ""
