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

from dap_core import common


class CargoCommand:
  def __init__(self, command):
    self.command = command

  def run(self):
    common.stop_if_not_installed('cargo', "Is rust installed?\nYou can install it with:\n    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
    cmd = common.which('cargo') + ' ' + self.verbose_flag() + ' ' + self.command
    exit_code, output = common.run_command_in_shell(cmd)
    common.print_verbose("Returning " + str(exit_code))
    return exit_code, output

  def verbose_flag(self):
    if(common.LOG_LEVEL == "verbose"):
      return "-v"
    else:
      return ""

