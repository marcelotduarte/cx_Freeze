import os.path
import sys
import subprocess

if sys.version_info[0] >= 3:
    exec("print_ = print")
else:
    exec("def print_(x): print x")
    input = raw_input

class SetupWriter(object):
    name = None
    version = None
    description = None
    exe_name = None
    py_file = None
    base = "Console"
    
    @property
    def need_win32_options(self):
        return self.exe_name or self.base.startswith("Win32")
    
    def write(self, filename):
        f = open(filename, "w")
        try:
            self._write(f)
        finally:
            f.close()
    
    def _write(self, f):
        w = lambda s: f.write(s+"\n")
        w("from cx_Freeze import setup, Executable")
        if self.need_win32_options:
            w("import sys")
        w("")
        
        w("# Dependencies are automatically detected, but it might need fine tuning.")
        w("build_exe_options = {'packages': [], 'excludes': []}")
        w("")
        
        if self.base.startswith("Win32"):
            w("base = None")
        else:
            w("base = %r" % self.base)
        if self.exe_name:
            w("target_name = %r" % self.exe_name)
        
        if self.need_win32_options:
            w("if sys.platform == 'win32':")
            if self.base.startswith("Win32"):
                w("    base = %r" % self.base)
            if self.exe_name:
                w("target_name = %r" % self.exe_name + '.exe')
        w("")
        
        if self.exe_name:
            executables = "[Executable(%r, base = base, targetName=target_name)]"
        else:
            executables = "[Executable(%r, base = base)]"
        executables = executables % self.py_file
        
        w(("setup(name=%r,\n"
           "      version=%r,\n"
           "      description=%r,\n"
           "      options = {'build_exe': build_exe_options},\n"
           "      executables=%s,\n"
           "     )") % (self.name, self.version, self.description, executables))

bases = {"C":"Console", "G": "Win32GUI", "S": "Win32Service"}

def getstr(prompt):
    return input(prompt).strip()

def ask_yn(prompt, default="n"):
    if default == "y":
        prompt += " ([y]/n) "
    elif default == "n":
        prompt += " (y/[n]) "
    else:
        prompt += " (y/n) "
    
    ans = ""
    while ans not in ("y", "n", "yes", "no"):
        ans = getstr(prompt).lower() or default
    
    return ans in ("y", "yes")

def cli_quickstart():
    setup = SetupWriter()
    setup.name = getstr("Project name: ")
    setup.version = getstr("Version [1.0]: ") or "1.0"
    setup.description = getstr("Description: ")
    setup.py_file = getstr("Python file to make executable from: ")
    setup.exe_name = getstr("Executable file name [%s]: " % os.path.splitext(setup.py_file)[0])
    base_prompt = "(C)onsole application, (G)UI application, or (S)ervice? "
    basecode = getstr(base_prompt).upper()
    while basecode not in bases:
        basecode = getstr(base_prompt).upper()
    setup.base = bases[basecode]
    
    setup_file = getstr("Save setup script to [setup.py]: ") or "setup.py"
    can_overwrite = False
    while os.path.exists(setup_file) and not can_overwrite:
        can_overwrite = ask_yn("Overwrite %s?" % setup_file)
        if not can_overwrite:
            setup_file = getstr("Save setup script to: ")
    setup.write(setup_file)
    print("")
    print_("Setup script written to %s; run it as:" % setup_file)
    print_("    python %s build" % setup_file)
    if ask_yn("Run this now?", default="n"):
        from subprocess import call
        call(["python", setup_file, "build"])
