//-----------------------------------------------------------------------------
// Console.c
//   Main routine for frozen programs which run in a console.
//-----------------------------------------------------------------------------

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <locale.h>
#ifdef MS_WINDOWS
#include <windows.h>
#include <shlwapi.h>
#endif

// disable filename globbing on Windows
#ifdef MS_WINDOWS
int _CRT_glob = 0;
#endif

//-----------------------------------------------------------------------------
// FatalError()
//   Prints a fatal error.
//-----------------------------------------------------------------------------
static int FatalError(const char *message)
{
    if (Py_IsInitialized()) {
        PyErr_Print();
        Py_FatalError(message);
    } else fprintf(stderr, "Fatal error: %s\n", message);
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
#if defined(MS_WINDOWS)
int wmain(int argc, wchar_t **argv)
#else
int main(int argc, char **argv)
#endif
{
    size_t status = 0;

    // initialize Python
    if (InitializePython(argc, argv) < 0)
        status = 1;

    // do the work
    if (status == 0 && ExecuteScript() < 0)
        status = 1;
    Py_Finalize();
    return status;
}
