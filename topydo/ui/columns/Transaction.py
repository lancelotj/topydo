# Topydo - A todo.txt client written in Python.
# Copyright (C) 2017 Bram Schoenmakers <bram@topydo.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from topydo.lib.MultiCommand import MultiCommand


class Transaction(object):
    """
    This class implements basic handling of executing any subcommand on multiple
    todo items.
    """
    def __init__(self, p_subcommand=None, p_env_args=(), p_todo_ids=None):
        self._multi = issubclass(p_subcommand, MultiCommand)
        self._cmd = lambda op: p_subcommand(op, *p_env_args)
        self._todo_ids = p_todo_ids
        self._operations = []

    def prepare(self, p_args):
        """
        Prepares list of operations to execute based on p_args, list of
        todo items contained in _todo_ids attribute and _subcommand
        attribute.
        """
        if self._todo_ids:
            id_position = p_args.index('{}')

            # Not using MultiCommand abilities would make EditCommand awkward
            if self._multi:
                p_args[id_position:id_position + 1] = self._todo_ids
                self._operations.append(p_args)
            else:
                for todo_id in self._todo_ids:
                    operation_args = p_args[:]
                    operation_args[id_position] = todo_id
                    self._operations.append(operation_args)
        else:
            self._operations.append(p_args)

    def execute(self):
        """
        Executes each operation from _operations attribute.
        """
        last_operation = len(self._operations) - 1
        for i, operation in enumerate(self._operations):
            command = self._cmd(operation)

            if command.execute() is False:
                return False
            elif i == last_operation:
                return True
