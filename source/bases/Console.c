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
#else
int main(int argc, char **argv)
{
    size_t status = 0;
    wchar_t **wargv;
    int i;

    // convert arguments to wide characters, using the system default locale
    setlocale(LC_ALL, "");
    wargv = PyMem_RawMalloc(sizeof(wchar_t*) * argc);
    if (!wargv)
        return FatalError("Out of memory converting arguments!");
    for (i = 0; i < argc; i++) {
        wargv[i] = Py_DecodeLocale(argv[i], NULL);
        if (!wargv[i])
            return FatalError("Unable to convert argument to string!");
    }

    // initialize Python
    if (InitializePython(argc, wargv) < 0)
        status = 1;

    // do the work
    if (status == 0 && ExecuteScript() < 0)
        status = 1;

    // free the memory
    for (i = 0; i < argc; i++)
        PyMem_RawFree(wargv[i]);
    PyMem_RawFree(wargv);

    Py_Finalize();
    return status;
}
#endif
