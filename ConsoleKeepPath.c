//-----------------------------------------------------------------------------
// ConsoleKeepPath.c
//   Main routine for frozen programs which need a Python installation to do
// their work (such as FreezePython). This executable will set the attribute
// sys.dllname on Windows so that no third party modules are required for
// FreezePython to do its work. It will also examine the command line for the
// presence of the arguments -O and -OO and set the optimization flag similar
// to what the Python executable itself does.
//-----------------------------------------------------------------------------

#include <Python.h>
#ifdef __WIN32__
#include <windows.h>
#endif

//-----------------------------------------------------------------------------
// FatalError()
//   Prints a fatal error.
//-----------------------------------------------------------------------------
static int FatalError(
    const char *message)		// message to print
{
    PyErr_Print();
    Py_FatalError(message);
    return -1;
}


//-----------------------------------------------------------------------------
// FatalScriptError()
//   Prints a fatal error in the initialization script.
//-----------------------------------------------------------------------------
static int FatalScriptError(void)
{
    PyErr_Print();
    return -1;
}


#include "Common.c"


//-----------------------------------------------------------------------------
// main()
//   Main routine for frozen programs.
//-----------------------------------------------------------------------------
int main(int argc, char **argv)
{
    const char *fileName;
    int i;

    // determine whether or not to set the optimization flag
    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-O") == 0)
            Py_OptimizeFlag = 1;
        else if (strcmp(argv[i], "-OO") == 0)
            Py_OptimizeFlag = 2;
    }

    // initialize Python
    Py_SetProgramName(argv[0]);
    fileName = Py_GetProgramFullPath();
    Py_Initialize();
    PySys_SetArgv(argc, argv);

    // do the work
    if (ExecuteScript(fileName) < 0)
        return 1;

    Py_Finalize();
    return 0;
}

