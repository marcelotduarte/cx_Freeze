//-----------------------------------------------------------------------------
// console.c
//   Main routine for frozen programs which run in a console.
//-----------------------------------------------------------------------------

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#ifdef MS_WINDOWS
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#endif

// disable filename globbing on Windows
#ifdef MS_WINDOWS
int _CRT_glob = 0;
#endif

#ifdef MS_WINDOWS
extern PyStatus InitializePython(int argc, wchar_t** argv);
#else
extern PyStatus InitializePython(int argc, char** argv);
#endif
extern int ExecuteScript(void);

//-----------------------------------------------------------------------------
// FatalScriptError()
//   Prints a fatal error in the initialization script.
//-----------------------------------------------------------------------------
int FatalScriptError(void)
{
    PyErr_Print();
    return -1;
}

//-----------------------------------------------------------------------------
// main()
//   Main routine for frozen programs.
//-----------------------------------------------------------------------------
#ifdef MS_WINDOWS
int wmain(int argc, wchar_t** argv)
#else
int main(int argc, char** argv)
#endif
{
    PyStatus status;
    int exitcode;

    status = InitializePython(argc, argv);
    if (PyStatus_Exception(status))
        Py_ExitStatusException(status);

    // do the work
    exitcode = ExecuteScript();

    if (Py_FinalizeEx() < 0) {
        exitcode = 120;
    }
    return exitcode;
}
