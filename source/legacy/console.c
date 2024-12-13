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
#include <locale.h>

// disable filename globbing on Windows
#ifdef MS_WINDOWS
int _CRT_glob = 0;
#endif

//-----------------------------------------------------------------------------
// FatalError()
//   Prints a fatal error.
//-----------------------------------------------------------------------------
static int FatalError(const char* message)
{
    if (Py_IsInitialized()) {
        PyErr_Print();
        Py_FatalError(message);
    } else
        fprintf(stderr, "Fatal error: %s\n", message);
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

#include "common.c"

//-----------------------------------------------------------------------------
// main()
//   Main routine for frozen programs.
//-----------------------------------------------------------------------------
#if defined(MS_WINDOWS)
int wmain(int argc, wchar_t** argv)
{
    int status = 0;

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
int main(int argc, char** argv)
{
    int status = 0;
    wchar_t** wargv;
    /* We need a second copy, as Python might modify the first one. */
    wchar_t** wargv2;
    int i;
    char* oldloc;

    oldloc = _PyMem_RawStrdup(setlocale(LC_ALL, NULL));
    if (!oldloc)
        return FatalError("Out of memory!");

    // convert arguments to wide characters, using the system default locale
    setlocale(LC_ALL, "");
    wargv = (wchar_t**)PyMem_RawMalloc(sizeof(wchar_t*) * (argc + 1));
    if (!wargv)
        return FatalError("Out of memory converting arguments!");
    wargv2 = (wchar_t**)PyMem_RawMalloc(sizeof(wchar_t*) * (argc + 1));
    if (!wargv2) {
        PyMem_RawFree(wargv);
        return FatalError("Out of memory converting arguments!");
    }
    for (i = 0; i < argc; i++) {
        wargv[i] = Py_DecodeLocale(argv[i], NULL);
        if (!wargv[i]) {
            status = FatalError("Unable to convert argument to string!");
            argc = i;
            break;
        }
        wargv2[i] = wargv[i];
    }
    wargv2[argc] = wargv[argc] = NULL;

    // global pointer to argv[0] for use in SetExecutableName()
    g_argv0 = argv[0];

    // initialize Python
    if (status == 0) {
        status = InitializePython(argc, wargv);

        // do the work
        if (status == 0)
            status = ExecuteScript();

        Py_Finalize();
    }

    // free the memory
    for (i = 0; i < argc; i++)
        PyMem_RawFree(wargv2[i]);
    PyMem_RawFree(wargv);
    PyMem_RawFree(wargv2);

    setlocale(LC_ALL, oldloc);
    PyMem_RawFree(oldloc);

    return status;
}
#endif
