import sys

sys.stdout.write("Hello from cx_Freeze\n\n")

sys.stdout.write("Executable: %r\n" % sys.executable)
sys.stdout.write("Prefix: %r\n" % sys.prefix)
sys.stdout.write("File system encoding: %r\n\n" % sys.getfilesystemencoding())

sys.stdout.write("ARGUMENTS:\n")
for a in sys.argv:
    sys.stdout.write("%s\n" % a)
sys.stdout.write("\n")

sys.stdout.write("PATH:\n")
for p in sys.path:
    sys.stdout.write("%s\n" % p)
sys.stdout.write("\n")

