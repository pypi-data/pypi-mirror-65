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

import os, sys, re
import urllib.request
from distutils.version import LooseVersion
from xml.etree import ElementTree
from shutil import which
from dap_core import common


class CommandLineInstaller:
  def __init__(self, command_base):
    self.command_base = command_base
    return

  def install(self, dep_name, dep_version, details):
    exit_code, output = common.run_command(self.command_base + [dep_name])
    common.stop_if_failed(exit_code, output)


class PipInstaller:
  NOT_INSTALLED = 0
  SAME_VERSION_INSTALLED = 1
  OLDER_VERSION_INSTALLED = 2
  NEWER_VERSION_INSTALLED = 3

  def __init__(self):
    return

  def install(self, dep_name, dep_version="latest", details={}):
    package_name = dep_name
    if not dep_version == "latest":
      package_name = dep_name + "==" + str(dep_version)

    status = self.is_already_installed(dep_name, dep_version)
    if status == PipInstaller.NOT_INSTALLED:
      common.print_verbose(dep_name + " not installed. Installing.")
      command_to_run = [which('pip3'), '-q', 'install', package_name]
      exit_code, output = common.run_command(command_to_run)
      common.stop_if_failed(exit_code, output)

    elif status == PipInstaller.OLDER_VERSION_INSTALLED:
      common.print_verbose(dep_name + " is already installed. Upgrading to " + dep_version + " version.")

      command_to_run = [which('pip3'), '-q', 'install', '--upgrade', package_name]
      exit_code, output = common.run_command(command_to_run)
      common.stop_if_failed(exit_code, output)

    elif status == PipInstaller.NEWER_VERSION_INSTALLED:
      common.print_verbose("Newer version of " + dep_name + " installed. Uninstalling and installing " + dep_version + " version.")

      command_to_run = [which('pip3'), '-q', 'uninstall', package_name]
      exit_code, output = common.run_command(command_to_run)
      common.stop_if_failed(exit_code, output)

      command_to_run = [which('pip3'), '-q', 'install', package_name]
      exit_code, output = common.run_command(command_to_run)
      common.stop_if_failed(exit_code, output)
    else:
      common.print_verbose(dep_name + ", " + dep_version + " is already installed. Doing nothing.")

  def is_already_installed(self, dep_name, dep_version):
    exit_code, output = common.run_command_in_shell("pip3 list --format=columns | grep -i " + dep_name)
    if not output:
      return PipInstaller.NOT_INSTALLED
    else:
      installed_version = re.sub(' +', ' ', output).split(" ")[1]

      if dep_version == "latest":
        # Assume older version so dap will try to upgrade automatically
        return PipInstaller.OLDER_VERSION_INSTALLED
      elif LooseVersion(installed_version) == LooseVersion(dep_version):
        return PipInstaller.SAME_VERSION_INSTALLED
      elif LooseVersion(installed_version) < LooseVersion(dep_version):
        return PipInstaller.OLDER_VERSION_INSTALLED
      elif LooseVersion(installed_version) > LooseVersion(dep_version):
        return PipInstaller.NEWER_VERSION_INSTALLED


class SysInstaller:
  def __init__(self):
    return

  def install(self, dep_name, dep_version="latest", details={}):
    install_command = [self.installer(), "install", self.dependency_with_version(dep_name, dep_version, self.installer())]
    common.print_raw(install_command)

  def dependency_with_version(self, dep_name, dep_version, sys_installer):
    if dep_version == "latest":
      return dep_name
    elif sys_installer == "brew":
      return dep_name + "@" + dep_version
    elif sys_installer == "apt-get":
      return dep_name + "=" + dep_version
    elif sys_installer == "yum":
      return dep_name + "-" + dep_version
    else:
      return ""

  def installer(self):
    if sys.platform.startswith('darwin'):
      return 'brew'
    elif sys.platform.startswith('linux'):
      if self.linux_distribution().startswith('debian'):
        return 'apt-get'
      elif self.linux_distribution().startswith('rhel'):
        return 'yum'
      else:
        common.print_error("Cannot install system dependencies because /etc/os-release does not exist. It is required to determine linux distribution.")
    else:
      common.exit_with_error_message("Sorry, only Linux (Ubuntu, CentOS) and Mac OS X are currently supported")

  def linux_distribution(self):
    exit_code, output = common.run_command([which('grep'), 'ID_LIKE', '/etc/os-release'])
    return output.split("=")[1].rstrip()


class MavenCentralInstaller:
  # https://search.maven.org/remotecontent?filepath=
  def __init__(self, url_base="https://repo1.maven.org/maven2/", lib_dir="lib"):
    self.url_base = url_base
    self.lib_dir = lib_dir
    return

  def install(self, name, version, details):
    if not self.has_already_been_downloaded(details["group_id"], name, version, "jar"):
      self.install_file(name, version, details, "jar")
      self.install_file(name, version, details, "pom")
      self.install_transitive_dependencies(name, version, details, "pom")

  def install_transitive_dependencies(self, name, version, details, extension):
    if self.local_pom_exists(details["group_id"], name, version):
      namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}
      tree = ElementTree.parse(self.local_location(details["group_id"], name, version, "pom"))
      root = tree.getroot()
      deps = root.findall("./xmlns:dependencies/xmlns:dependency", namespaces=namespaces)
      for d in deps:
        version = "latest"
        groupId = d.find("xmlns:groupId", namespaces=namespaces).text
        artifactId = d.find("xmlns:artifactId", namespaces=namespaces).text
        version_elem = d.find("xmlns:version", namespaces=namespaces)
        if version_elem is not None:
          version = version_elem.text
        self.install(artifactId, version, {"group_id": groupId})

  def install_file(self, name, version, details, extension):
    remote_loc = self.remote_location(details["group_id"], name, version, extension)
    local_lib_dir = self.local_lib_directory(details["group_id"], name, version)
    local_loc = self.local_location(details["group_id"], name, version, extension)
    if not self.has_already_been_downloaded(details["group_id"], name, version, extension):
      common.print_info("Downloading " + remote_loc + " to " + local_loc)
      common.run_command(["mkdir", "-p", local_lib_dir])
      self.fetch(remote_loc, local_loc)
    else:
      common.print_verbose("Dependency found at " + local_loc)
    return 0, ""

  def remote_location(self, group_id, artifact_id, version, file_extension):
    group_id_with_slashes = group_id.replace(".", "/")

    if version != "latest":
      return self.url_base + "/".join([group_id_with_slashes, artifact_id, version, artifact_id]) + "-" + version + "." + file_extension
    else:
      metadata_file = self.metadata_local_location(group_id, artifact_id)
      #TODO: If metadata file is present, don't fetch again
      metadata_url = self.url_base + "/".join([group_id_with_slashes, artifact_id]) + "/maven-metadata.xml"
      self.fetch(metadata_url, metadata_file)
      #TODO: Parse metadata file and return the latest version.
      namespaces = {'xmlns' : ''}
      tree = ElementTree.parse(metadata_file)
      root = tree.getroot()
      latest_version = root.find(".//latest").text
      return self.url_base + "/".join([group_id_with_slashes, artifact_id, latest_version, artifact_id]) + "-" + latest_version + "." + file_extension

  def metadata_local_location(self, group_id, artifact_id):
    group_id_with_slashes = group_id.replace(".", "/")
    return "lib/java/" + "/".join([group_id_with_slashes, artifact_id]) + \
           "/" + "maven-metadata.xml"

  def local_location(self, group_id, artifact_id, version, file_extension):
    return self.local_lib_directory(group_id, artifact_id, version) + \
           "/" + artifact_id + "-" + version + "." + file_extension

  def local_lib_directory(self, group_id, artifact_id, version):
    group_id_with_slashes = group_id.replace(".", "/")
    return "lib/java/" + "/".join([group_id_with_slashes, artifact_id, version])

  def fetch(self, remote_loc, local_loc):
    urllib.request.urlretrieve(remote_loc, local_loc)

  def has_already_been_downloaded(self, group_id, artifact_id, version, file_extension):
    return os.path.exists(self.local_location(group_id, artifact_id, version, file_extension))

  def local_pom_exists(self, group_id, artifact_id, version):
    return os.path.exists(self.local_location(group_id, artifact_id, version, "pom"))
