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

import sys, platform, yaml
from shutil import which
from dap_core import common
from dap_core.dependency_installers import CommandLineInstaller, MavenCentralInstaller, PipInstaller, SysInstaller


class Dependencies():
  def __init__(self, dependencies_file_contents):
    self.dependencies_file_contents = dependencies_file_contents
    self.dependencies = dict()
    dependencies_yaml = yaml.load(self.dependencies_file_contents, Loader=yaml.SafeLoader)
    if not dependencies_yaml:
      common.print_verbose("No dependencies found")
      return

    for stage in dependencies_yaml.items():
      stage_name_from_yaml = stage[0]

      # No stages defined
      if stage_name_from_yaml not in self.dependencies:
        self.dependencies[stage_name_from_yaml] = list()

      # Stage is defined but not dependencies listed for the stage
      stage_dependencies_from_yaml = stage[1] if stage[1] else dict()

      for dependency in stage_dependencies_from_yaml.items():
        dep_name = dependency[0]
        dep_version = dependency[1]["version"]
        dep_installer = dependency[1]["installer"]
        dep_details = dict(dependency[1])
        del dep_details["version"]
        del dep_details["installer"]
        self.dependencies[stage_name_from_yaml].append(\
          Dependency(name=dependency[0], version=dep_version, installer=dep_installer, details=dep_details))

    return

  def dependencies_for(self, stage_name):
    return self.dependencies.get(stage_name, list())


class Dependency:

  def __init__(self, name, version, installer, details=dict()):
    self.name = name
    self.version = str(version)
    self.installer_type = installer
    if len(details) > 0:
      self.details = details
    else:
      self.details = None
    return

  def __eq__(self, other):
      """Overrides the default implementation"""
      if isinstance(self, other.__class__):
          return self.__dict__ == other.__dict__
      return NotImplemented

  def __ne__(self, other):
      """Overrides the default implementation (unnecessary in Python 3)"""
      x = self.__eq__(other)
      if x is not NotImplemented:
          return not x
      return NotImplemented

  def __hash__(self):
      """Overrides the default implementation"""
      return hash(tuple(sorted(self.__dict__.items())))

  def installer(self):
    installers = dict()
    installers["npm"] = CommandLineInstaller(['/usr/local/bin/npm', 'install', '--save-dev'])
    installers["pip3"] = PipInstaller()
    installers["system"] = SysInstaller()
    installers["brew_cask"] = CommandLineInstaller([which('brew'), 'cask', 'install'])
    installers["jar"] = MavenCentralInstaller()
    installers["cargo"] = CommandLineInstaller([which('cargo'), 'install'])

    return installers[self.installer_type]

  def install(self):
    common.print_verbose("Installing '" + self.name + "', " + self.version + " version via " + self.installer_type)
    self.installer().install(self.name, self.version, self.details)
