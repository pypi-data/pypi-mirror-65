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

import os, inspect, sys, importlib, glob, pkg_resources, pathlib, sysconfig, site
from dap_core import common


class MetaModel:
  n = ""

  def __init__(self, name="power_daps/python3"):
    self.n = name

  def name(self):
    return self.n

  def package_name(self):
    pack_name = self.name().replace("/", ".")
    return pack_name

  def load_actions_from_dir(self, dir):

    if os.path.isdir(dir) is not True:
      common.exit_with_error_message("Meta-model '" + self.name() + "' not found in '" + dir + "'")

    elif os.path.isdir(os.path.join(dir, "actions")) is not True:
      common.exit_with_error_message("Meta-model '" + self.name() + "' found but no actions found")

    elif len(self.actions_found_in(dir + "/actions")) == 0:
      common.exit_with_error_message("No actions found in '" + dir + "/actions'")

    if dir not in sys.path:
      sys.path.insert(0, dir)

    actions = []
    #for action in ["default", "deps", "unit_test", "package", "run"]:

    for action in self.actions_found_in(dir + "/actions"):
      sys.path.append(str(pathlib.Path(dir).parent.parent.absolute()))
      action_module = importlib.import_module(self.package_name() + ".actions." + action + "_action")
      actions.append(action_module.action())
    
    return actions


  def actions_dir(self):
    discovered_plugins = {
      entry_point.name: entry_point.load()
      for entry_point
      in pkg_resources.iter_entry_points('power_daps.meta_model.actions')
    }
    # common.print_error(discovered_plugins)
    ret_val = ""
    if not discovered_plugins:
      ret_val = os.path.realpath(
        os.path.abspath(
          os.path.join(
            os.path.split(
              inspect.getfile(
                inspect.currentframe()
              ))[0],
            "../../../meta_models/" + self.name() + "/src/" + self.name())))
    else:
      in_system_sitepackages = sysconfig.get_paths()["purelib"] + "/" + self.name()
      in_user_sitepackages = site.getusersitepackages() + "/" + self.name()
      if os.path.isdir(in_user_sitepackages):
        ret_val = in_user_sitepackages
      elif os.path.isdir(in_system_sitepackages):
        ret_val = in_system_sitepackages
      else:
        ret_val = "."
    return ret_val

  def actions(self):
    return self.load_actions_from_dir(self.actions_dir())

  def actions_found_in(self, dir):
    return [os.path.split(path)[-1].replace("_action.py", "") for path in glob.glob(dir + "/*_action.py")]

  def template_for_action(self, action_name):
    return os.path.join(self.actions_dir(), "templates", action_name)

