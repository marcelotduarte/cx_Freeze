import sys

sys.stdout.write("Hello from cx_Freeze\n\n")

sys.stdout.write("sys.executable %s\n" % sys.executable)
sys.stdout.write("sys.prefix %s\n\n" % sys.prefix)

sys.stdout.write("ARGUMENTS:\n")
for a in sys.argv:
    sys.stdout.write("%s\n" % a)
sys.stdout.write("\n")

sys.stdout.write("PATH:\n")
for p in sys.path:
    sys.stdout.write("%s\n" % p)
sys.stdout.write("\n")

