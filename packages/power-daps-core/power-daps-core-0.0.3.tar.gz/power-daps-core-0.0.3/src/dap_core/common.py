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

import os, sys, subprocess, inspect, yaml, shutil


LOG_LEVEL = "info"
FAILED = 1
SUCCESS = 0
saved_exit_code = SUCCESS
saved_meta_model = None


def run_command(command):
    """Run the specified command"""

    subprocess_exit_code = SUCCESS
    output = ""
    if not str(command):
        print_error("Trying to run None")

    print_verbose("Running command " + str(command))
    try:
        output = subprocess.check_output(command).decode("utf-8")
        if output:
            print_verbose("Output:\n" + output)
    except FileNotFoundError as err:
        subprocess_exit_code = err.errno
        output = err.strerror
        print_error("Exit code: " + str(subprocess_exit_code))
        print_error(output)
    except subprocess.CalledProcessError as err:
        subprocess_exit_code = err.returncode
        print_error("Exit code: " + str(subprocess_exit_code))
        if output:
            print_error(output)
    return subprocess_exit_code, output


def run_command_in_shell_without_output(command):
  """Run the specified command but do not show any output or errors unless you are in verbose mode"""

  subprocess_exit_code = SUCCESS
  output = ""
  if not str(command):
    print_error("Trying to run None")

  print_verbose("Running command " + str(command))
  try:
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    if output:
      print_verbose("Output:\n" + output)
  except FileNotFoundError as err:
    subprocess_exit_code = err.errno
    output = err.strerror
    print_verbose("Exit code: " + str(subprocess_exit_code))
    print_verbose(output)
  except subprocess.CalledProcessError as err:
    subprocess_exit_code = err.returncode
    print_verbose("Exit code: " + str(subprocess_exit_code))
    if output:
      print_verbose(output)
  return subprocess_exit_code, output


def action_name(a):
  return a.name() if callable(a.name) else a.name


def run_command_in_shell(command):
  """Run the specified command in a shell"""

  subprocess_exit_code = SUCCESS
  output = ""
  if not str(command):
    print_error("Trying to run None")

  print_verbose("Running command " + str(command))
  try:
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    if output:
      print_verbose(output)
  except FileNotFoundError as err:
    subprocess_exit_code = err.errno
    output = err.strerror
    print_error("Exit code: " + str(subprocess_exit_code))
    print_error(output)
  except subprocess.CalledProcessError as err:
    subprocess_exit_code = err.returncode
    output = err.stdout
    print_error("Exit code: " + str(subprocess_exit_code))
    if output:
      print_error(output.decode())

  try:
    output = output.decode()
  except (UnicodeDecodeError, AttributeError):
    pass

  return subprocess_exit_code, output


def print_warning(warning):
    global LOG_LEVEL
    if LOG_LEVEL == "verbose" or LOG_LEVEL == "info" or LOG_LEVEL == "warning":
        print_raw("WARNING: " + str(warning))


def print_error(error):
    if LOG_LEVEL == "verbose" or LOG_LEVEL == "info" or LOG_LEVEL == "warning" or LOG_LEVEL == "error":
        print_raw("ERROR: " + str(error))


def print_info(info):
    if LOG_LEVEL == "verbose" or LOG_LEVEL == "info":
        print_raw("INFO: " + str(info))


def print_raw(s):
    print(s)


def print_info_no_eol(info):
    sys.stdout.write(info)


def print_verbose(verbose_info):
    if LOG_LEVEL == "verbose":
        print_raw("VERBOSE: " + verbose_info)


def print_verbose_no_eol(verbose_info):
    if LOG_LEVEL == "verbose":
        sys.stdout.write(verbose_info)


def stop_if_failed(subprocess_exit_code=SUCCESS, error_message=""):
    if subprocess_exit_code != SUCCESS:
        print_error("FAILED " + error_message)
        sys.exit(FAILED)


def continue_if_failed(subprocess_exit_code=SUCCESS, error_message=""):
    global saved_exit_code
    if subprocess_exit_code != SUCCESS:
        saved_exit_code = FAILED


def exit_code():
    return saved_exit_code


def set_log_level(log_level_to_set):
    global LOG_LEVEL
    LOG_LEVEL = log_level_to_set


def set_meta_model(mm):
    global saved_meta_model
    saved_meta_model = mm
    print_verbose("Meta Model: " + str(saved_meta_model))


def meta_model():
    global saved_meta_model
    if saved_meta_model is None:
      saved_meta_model = configured_meta_model()
    return saved_meta_model


def configured_meta_model():
    configuration = config()
    if 'power_daps_meta_model' in configuration:
      return str(configuration['power_daps_meta_model'])
    return os.getenv("POWER_DAPS_META_MODEL", "power_daps/python3")


def config():
    config_file_location = "config/dap_config.yml"
    configuration = {}
    if os.path.exists(config_file_location):
      config_file_contents = ""
      try:
        with open(config_file_location) as f:
          config_file_contents = f.read()
        f.closed
      except (OSError, IOError) as e:
        print_warning("Config file could not be read from " + config_file_location)
      configuration = yaml.load(config_file_contents, Loader=yaml.SafeLoader)
    return configuration


def power_daps_dir():
    return os.path.dirname(os.path.abspath(__file__)) + "/../../../../"


def app_dir():
    return power_daps_dir() + "apps/dap/"


def dependencies_file_location():
    return os.getcwd() + "/dependencies.yml"


def actions_file_location():
    default_actions_file_location = power_daps_dir() + "actions.yml"
    local_actions_file_location = os.getcwd() + "/actions.yml"
    if os.path.exists(local_actions_file_location):
      return local_actions_file_location
    else:
      return default_actions_file_location


def actions_dir():
    ret_val = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../meta_models/" + meta_model() + "/src")))
    return ret_val


def exit_with_error_message(error_message):
    print_error(error_message)
    sys.exit(1)


def dirs_in(dirname, ignore_dirs=[]):
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


def is_installed(command_name):
  if shutil.which(command_name):
    return True
  return False


def stop_if_not_installed(command_name, additional_error_message=""):
  if is_installed(command_name):
    return
  else:
    error_message = "'" + command_name + "' not found in PATH. " + additional_error_message
    print_error("FAILED " + error_message)
    sys.exit(FAILED)


def which(command_name):
  stop_if_not_installed(command_name)
  return shutil.which(command_name)


if __name__ == '__main__':
    print_error("This module " + __file__ + " cannot be run as a stand alone command")
    sys.exit(1)

