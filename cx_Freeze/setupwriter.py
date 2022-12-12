from __future__ import annotations

import os
import subprocess


class SetupWriter:
    bases = {"C": "console", "G": "Win32GUI", "S": "Win32Service"}

    @property
    def base(self):
        return self.bases[self.base_code]

    @property
    def default_executable_name(self):
        return os.path.splitext(self.script)[0]

    def __init__(self):
        self.name = self.description = self.script = ""
        self.executable_name = self.default_executable_name
        self.setup_file_name = "setup.py"
        self.version = "1.0"
        self.base_code = "C"

    def get_boolean_value(self, label, default=False):
        default_response = "y" if default else "n"
        while True:
            response = self.get_value(
                label, default_response, separator="? "
            ).lower()
            if response in ("y", "n", "yes", "no"):
                break
        return response in ("y", "yes")

    def get_value(self, label, default="", separator=": "):
        if default:
            label += " [%s]" % default
        return input(label + separator).strip() or default

    def populate_from_command_line(self):
        self.name = self.get_value("Project name", self.name)
        self.version = self.get_value("Version", self.version)
        self.description = self.get_value("Description", self.description)
        self.script = self.get_value(
            "Python file to make executable from", self.script
        )
        self.executable_name = self.get_value(
            "Executable file name", self.default_executable_name
        )
        bases_prompt = "(C)onsole application, (G)UI application, or (S)ervice"
        while True:
            self.base_code = self.get_value(bases_prompt, "C")
            if self.base_code in self.bases:
                break
        while True:
            self.setup_file_name = self.get_value(
                "Save setup script to", self.setup_file_name
            )
            if not os.path.exists(self.setup_file_name):
                break
            if self.get_boolean_value("Overwrite %s" % self.setup_file_name):
                break

    def write(self):
        with open(self.setup_file_name, "w", encoding="UTF-8") as output:
            w = lambda s: output.write(s + "\n")  # noqa

            w("from cx_Freeze import setup, Executable")
            w("")

            w("# Dependencies are automatically detected, but it might need")
            w("# fine tuning.")
            w("build_options = {'packages': [], 'excludes': []}")
            w("")

            if self.base.startswith("Win32"):
                w("import sys")
                w("base = %r if sys.platform=='win32' else None" % self.base)
            else:
                w("base = %r" % self.base)
            w("")

            w("executables = [")
            if self.executable_name != self.default_executable_name:
                w(
                    "    Executable(%r, base=base, target_name = %r)"
                    % (self.script, self.executable_name)
                )
            else:
                w("    Executable(%r, base=base)" % self.script)
            w("]")
            w("")

            w(
                (
                    "setup(name=%r,\n"
                    "      version = %r,\n"
                    "      description = %r,\n"
                    "      options = {'build_exe': build_options},\n"
                    "      executables = executables)"
                )
                % (self.name, self.version, self.description)
            )


def main():
    writer = SetupWriter()
    writer.populate_from_command_line()
    writer.write()
    print("")
    print("Setup script written to %s; run it as:" % writer.setup_file_name)
    print("    python %s build" % writer.setup_file_name)
    if writer.get_boolean_value("Run this now"):
        subprocess.call(["python", writer.setup_file_name, "build"])
