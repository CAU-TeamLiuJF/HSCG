import os
import subprocess


class BashIO:
    def __init__(self, output_file):
        self.initialization = ["#! /bin/bash"]
        self.pre_command = []
        self.core_command = []
        self.output_file = output_file

    def add_pre_command(self, command):
        self.pre_command.append(command)

    def add_core_command(self, command):
        self.core_command.append(command)

    def output_bash(self):
        with open(self.output_file, "w") as wp:
            wp.write("\n".join(self.initialization))
            wp.write("\n\n")
            wp.write("\n".join(self.pre_command))
            wp.write("\n\n")
            wp.write("\n".join(self.core_command))
            wp.write("\n")


def run_bash(module_name, command):
    """
    @ command: list
    """
    result = subprocess.call(command)
    if result != 0:
        print("{} failed !".format(module_name))
        exit(1)
