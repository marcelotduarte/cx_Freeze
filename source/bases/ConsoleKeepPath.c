//-----------------------------------------------------------------------------
// ConsoleKeepPath.c
//   Main routine for frozen programs which need a Python installation to do
// their work.
//-----------------------------------------------------------------------------

#include <Python.h>
#include <locale.h>
#ifdef __WIN32__
#include <windows.h>
#endif

// disable filename globbing on Windows
#ifdef MS_WINDOWS
int _CRT_glob = 0;
#endif

//-----------------------------------------------------------------------------
// FatalError()
//   Prints a fatal error.
//-----------------------------------------------------------------------------
static int FatalError(
    const char *message)                // message to print
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
#if PY_MAJOR_VERSION >= 3
    char fileName[MAXPATHLEN + 1];
    wchar_t **wargv, *wfileName;
    int i, size;
#else
    const char *fileName;
#endif
    int status;

    // initialize Python
#if PY_MAJOR_VERSION >= 3
    setlocale(LC_CTYPE, "");
    wargv = PyMem_Malloc(sizeof(wchar_t*) * argc);
    if (!wargv)
        return 2;
    for (i = 0; i < argc; i++) {
        size = strlen(argv[i]);
        wargv[i] = PyMem_Malloc(sizeof(wchar_t) * (size + 1));
        if (!wargv[i])
            return 2;
        status = mbstowcs(wargv[i], argv[i], size + 1);
        if (status < 0)
            return 3;
    }
    Py_SetProgramName(wargv[0]);
    wfileName = Py_GetProgramFullPath();
    wcstombs(fileName, wfileName, MAXPATHLEN);
    Py_Initialize();
    PySys_SetArgv(argc, wargv);
#else
    Py_SetProgramName(argv[0]);
    fileName = Py_GetProgramFullPath();
    Py_Initialize();
    PySys_SetArgv(argc, argv);
#endif

    // do the work
    status = 0;
    if (ExecuteScript(fileName) < 0)
        status = 1;

    Py_Finalize();
    return status;
}

