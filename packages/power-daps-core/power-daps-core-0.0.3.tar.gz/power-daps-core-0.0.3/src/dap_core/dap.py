#!/usr/bin/env python

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

import sys, pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from dap_core import common
from dap_core.meta_model import MetaModel


def run(log_level="info", meta_model_name="power_daps/python3", actions_to_run=["default"]):
  common.set_log_level(log_level)
  meta_model = MetaModel(meta_model_name)
  common.set_meta_model(meta_model_name)

  valid_actions = meta_model.actions()
  valid_action_names = [common.action_name(va) for va in valid_actions]

  common.print_verbose('Actions to run ' + str(actions_to_run))
  common.print_verbose('Valid actions ' + str(valid_action_names))

  for action_to_run in actions_to_run:
    if action_to_run not in valid_action_names:
      common.print_error("Action '" + action_to_run + "' not found.")
      continue
    for valid_action in valid_actions:
      valid_action_name = common.action_name(valid_action)
      if valid_action_name == action_to_run:
        common.stop_if_failed(*valid_action.run())


def main():
  import argparse
  import os
  default_meta_model = common.configured_meta_model()

  parser = argparse.ArgumentParser(description="dap")
  parser.add_argument("-v", "--verbose", dest="log_level",
                      default="info", action="store_const",
                      const="verbose", help="Verbose output")
  parser.add_argument("-q", "--quiet", dest="log_level",
                      default="info", action="store_const",
                      const="error", help="Quiet output. Only errors will be written out.")
  parser.add_argument("-m", "--meta-model", dest="meta_model",
                      default=default_meta_model,
                      help="Use the specified meta-model. Defaults to 'power_daps/python3'")
  parser.add_argument("action",
                      help="List of actions to run. Defaults to 'default' for the given meta-model",
                      default=["default"], nargs="*")

  args = parser.parse_args()

  run(args.log_level, args.meta_model, args.action)
  sys.exit(common.exit_code())


if __name__ == '__main__':
  main()
