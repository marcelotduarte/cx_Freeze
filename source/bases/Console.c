//-----------------------------------------------------------------------------
// Console.c
//   Main routine for frozen programs which run in a console.
//-----------------------------------------------------------------------------

#include <Python.h>
#ifdef MS_WINDOWS
#include <windows.h>
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
#ifndef MS_WINDOWS
    #if PY_MAJOR_VERSION >= 3
#include "3.0/M__abcoll.c"
#include "3.0/M__weakrefset.c"
#include "3.0/M_abc.c"
#include "3.0/M_codecs.c"
#include "3.0/M_copyreg.c"
#include "3.0/M_encodings.c"
#include "3.0/M_encodings__aliases.c"
#include "3.0/M_encodings__latin_1.c"
#include "3.0/M_encodings__utf_8.c"
#include "3.0/M_genericpath.c"
#include "3.0/M_io.c"
#include "3.0/M_os.c"
#include "3.0/M_posixpath.c"
#include "3.0/M_stat.c"

static struct _frozen _PyImport_FrozenModules[] = {
        {"_abcoll", M__abcoll, 27173},
        {"_weakrefset", M__weakrefset, 10014},
        {"abc", M_abc, 6951},
        {"codecs", M_codecs, 41294},
        {"copyreg", M_copyreg, 5609},
        {"encodings", M_encodings, -4471},
        {"encodings.aliases", M_encodings__aliases, 8494},
        {"encodings.latin_1", M_encodings__latin_1, 2996},
        {"encodings.utf_8", M_encodings__utf_8, 2494},
        {"genericpath", M_genericpath, 3653},
        {"io", M_io, 79868},
        {"os", M_os, 25518},
        {"posixpath", M_posixpath, 12445},
        {"stat", M_stat, 2963},
        {0, 0, 0}
};
    #endif
#endif


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
    Py_NoSiteFlag = 1;
    Py_FrozenFlag = 1;
    Py_IgnoreEnvironmentFlag = 1;
#if PY_MAJOR_VERSION >= 3
#ifndef MS_WINDOWS
    PyImport_FrozenModules = _PyImport_FrozenModules;
#endif
    Py_SetPythonHome(L"");
    wargv = PyMem_Malloc(sizeof(wchar_t*) * argc);
    if (!wargv)
        return 2;
    for (i = 0; i < argc; i++) {
        size = strlen(argv[i]);
        wargv[i] = PyMem_Malloc(sizeof(wchar_t) * (size + 1));
        if (!wargv[i])
            return 2;
        mbstowcs(wargv[i], argv[i], size + 1);
    }
    Py_SetProgramName(wargv[0]);
    wfileName = Py_GetProgramFullPath();
    wcstombs(fileName, wfileName, MAXPATHLEN);
    Py_Initialize();
    PySys_SetArgv(argc, wargv);
#else
    Py_SetPythonHome("");
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

