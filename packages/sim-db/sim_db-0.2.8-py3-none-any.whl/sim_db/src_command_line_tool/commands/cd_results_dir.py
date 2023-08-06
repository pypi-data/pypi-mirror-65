#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Changes the current working directory to the 'results_dir' of a simulation."""
# Copyright (C) 2020 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_package_root_to_path

import sim_db.src_command_line_tool.commands.helpers as helpers
import sim_db.src_command_line_tool.commands.get as get
import argparse
import subprocess
import sys
import os.path


def command_line_arguments_parser(name_command_line_tool="sim_db",
                                  name_command="cd_results_dir"):
    parser = argparse.ArgumentParser(
            description=("Change the current working directory to the "
                "'results_dir' of the specified simulation or the last entry "
                "if not specified. (This is done by creating a new subshell, "
                "so '$ exit' can be used to return to the original directory "
                "and shell instance.)"),
            prog="{0} {1}".format(name_command_line_tool, name_command))
    parser.add_argument(
            '--id',
            '-i',
            type=int,
            help="'ID' of the simulation in the 'sim.db' database.")
    parser.add_argument(
            '-n',
            type=int,
            help="n'th last entry in the 'sim.db' database.")

    return parser


def cd_results_dir(name_command_line_tool="sim_db", 
                   name_command="cd_results_dir", argv=None):
    args = command_line_arguments_parser(name_command_line_tool,
                                         name_command).parse_args(argv)
    res_dir = get.get(name_command_line_tool, name_command, 
            ["results_dir"] + argv)

    source_shell_config_file = ""
    shell_config_file = os.path.expandvars("$HOME/.bashrc")
    if os.path.isfile(shell_config_file):
        source_shell_config_file = "source {0};".format(shell_config_file)
    shell_config_file = os.path.expandvars("$HOME/.bash_profile")
    if os.path.isfile(shell_config_file):
        source_shell_config_file = "source {0};".format(shell_config_file)

    subprocess.Popen("cd {0}; {1}exec $SHELL".format(res_dir, 
            source_shell_config_file), shell=True).wait()


if __name__ == '__main__':
    cd_results_dir("", sys.argv[0], sys.argv[1:])
