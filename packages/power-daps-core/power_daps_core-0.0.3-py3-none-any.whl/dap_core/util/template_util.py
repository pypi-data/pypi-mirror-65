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

import os, sys, pathlib, shutil
from dap_core import common
from dap_core.meta_model import MetaModel


def copy_template_files_to(destination, source_action_name):
  common.print_verbose("Looking for files to copy in: " + str(pathlib.Path(MetaModel(common.meta_model()).template_for_action(source_action_name))))
  files_to_copy = [str(p) for p in pathlib.Path(MetaModel(common.meta_model()).template_for_action(source_action_name)).glob("*")]
  common.print_verbose("Found " + str(len(files_to_copy)) + " files to copy.")
  command_to_run = ['/bin/cp', "-R", *files_to_copy, destination]
  common.run_command(command_to_run)


def find_and_replace_in_file_names_and_content(dir, find_and_replace_dict):
  current_dir = os.getcwd()

  for str_to_find, str_to_replace_with in find_and_replace_dict.items():
    dirs = sorted(common.dirs_in(dir, ["__pycache__", "dist", "build", "egg-info", ".git"]) + ["."], key=len, reverse=True)

    for d in dirs:
      os.chdir(current_dir + "/" + d)

      files_to_rename = [str(p) for p in pathlib.Path(".").glob("*" + str_to_find + "*")]

      for f in files_to_rename:
        common.print_verbose("Renaming " + f + " to " + f.replace(str_to_find, str_to_replace_with))
        rename_command = ['/bin/mv', f, f.replace(str_to_find, str_to_replace_with)]
        common.run_command(rename_command)

    grep_files_command = [shutil.which('find'), ".", "!", "-name", '*.pyc', "!", "-path", '*.git*', "-type", "f", "-exec", shutil.which("grep"), "-l", "PROJECT_NAME", '{}', ";", "-print"]
    files_to_search_and_replace_within = common.run_command(grep_files_command)[1].splitlines()

    for f in files_to_search_and_replace_within:
      sed_command = sed_find_and_replace_command(str_to_find, str_to_replace_with, f)
      common.run_command(sed_command)

  os.chdir(current_dir)


def sed_find_and_replace_command(str_to_find, str_to_replace_with, filename):
  sed_command = [shutil.which('sed'), '-i']
  if sys.platform.startswith('darwin'):
    sed_command += [""]
  sed_command += ['-e', "s/" + str_to_find + "/" + str_to_replace_with + "/g", filename]
  return sed_command


def check_that_name_does_not_have_dashes(name):
  if "-" in name:
    common.exit_with_error_message("Name " + name + " has dashes. Please use underscores as dashes cause problems in the python ecosystem")

