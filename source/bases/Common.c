//-----------------------------------------------------------------------------
// Common.c
//   Routines which are common to running frozen executables.
//-----------------------------------------------------------------------------

#include <compile.h>
#include <eval.h>
#include <osdefs.h>

// define format for sys.path
// this consists of <dir>/lib/library.zip and <dir>/lib
// where <dir> refers to the directory in which the executable is found
#if defined(MS_WINDOWS)
    #define CX_PATH_FORMAT              L"%ls\\lib\\library.zip;%ls\\lib"
#else
    #define CX_PATH_FORMAT              "%s/lib/library.zip:%s/lib"
#endif

// global variables (used for simplicity)
#if defined(MS_WINDOWS)
    static wchar_t g_ExecutableName[MAXPATHLEN + 1];
    static wchar_t g_ExecutableDirName[MAXPATHLEN + 1];
#else
    static char g_ExecutableName[MAXPATHLEN + 1];
    static char g_ExecutableDirName[MAXPATHLEN + 1];
#endif


//-----------------------------------------------------------------------------
// SetExecutableName()
//   Set the executable name given the value of argv[0]. First, if a path
// separator is not found in the value of argv[0] the PATH environment variable
// is searched to locate the full path of the executable. After that, on
// platforms other than Windows links are followed in order to find the actual
// executable path.
//-----------------------------------------------------------------------------
static int SetExecutableName(const char *argv0)
{
#ifdef MS_WINDOWS
    if (!GetModuleFileNameW(NULL, g_ExecutableName, MAXPATHLEN + 1))
        return FatalError("Unable to get executable name!");
    memcpy(g_ExecutableDirName, g_ExecutableName,
            (MAXPATHLEN + 1) * sizeof(wchar_t));
    PathRemoveFileSpecW(g_ExecutableDirName);

#else

    char executableName[PATH_MAX + 1], *path, *ptr, *tempPtr;
    size_t size, argv0Size;
    struct stat statData;
    int found = 0;

    // check to see if path contains a separator
    if (strchr(argv0, SEP)) {
        strcpy(executableName, argv0);

    // if not, check the PATH environment variable
    } else {
        path = getenv("PATH");
        if (!path)
            return FatalError("PATH environment variable not defined!");
        ptr = path;
        argv0Size = strlen(argv0);
        while (1) {
            tempPtr = strchr(ptr, DELIM);
            size = (tempPtr) ? (size_t) (tempPtr - ptr) : strlen(ptr);
            if (size + argv0Size + 1 <= MAXPATHLEN) {
                strncpy(executableName, ptr, PATH_MAX + 1);
                executableName[size] = SEP;
                executableName[size + 1] = '\0';
                strcat(executableName, argv0);
                if (stat(executableName, &statData) == 0 &&
                        S_ISREG(statData.st_mode) &&
                        (statData.st_mode & 0111)) {
                    found = 1;
                    break;
                }
            }
            if (!tempPtr)
                break;
            ptr += size + 1;
        }
        if (!found)
            return FatalError("Unable to locate executable on PATH!");
    }

    // get absolute path for executable name
    if (!realpath(executableName, g_ExecutableName))
        return FatalError("Unable to determine absolute path for executable!");

    // get directory from executable name
    strcpy(g_ExecutableDirName, g_ExecutableName);
    ptr = strrchr(g_ExecutableDirName, SEP);
    if (!ptr)
        return FatalError("Unable to calculate directory of executable!");
    *ptr = '\0';
#endif

    return 0;
}


#ifdef MS_WINDOWS
//-----------------------------------------------------------------------------
// InitializePython()
//   Initialize Python for Python 3 and higher on Windows.
//-----------------------------------------------------------------------------
static int InitializePython(int argc, wchar_t **argv)
{
    wchar_t *wPath;
    size_t size;

    // determine executable name
    if (SetExecutableName(NULL) < 0)
        return -1;

    // create sys.path
    size = wcslen(g_ExecutableDirName) * 2 + wcslen(CX_PATH_FORMAT) + 1;
    wPath = PyMem_RawMalloc(sizeof(wchar_t) * size);
    if (!wPath)
        return FatalError("Out of memory creating sys.path!");
    swprintf(wPath, size, CX_PATH_FORMAT, g_ExecutableDirName,
            g_ExecutableDirName);

    // initialize Python
    Py_NoSiteFlag = 1;
    Py_FrozenFlag = 1;
    Py_IgnoreEnvironmentFlag = 1;
    Py_SetProgramName(g_ExecutableName);
    Py_SetPath(wPath);
    Py_Initialize();
    PySys_SetArgv(argc, argv);

    return 0;
}

#else

//-----------------------------------------------------------------------------
// InitializePython()
//   Initialize Python on all other platforms.
//-----------------------------------------------------------------------------
static int InitializePython(int argc, char **argv)
{
    wchar_t **wargv, *wpath;
    PyObject *executable;
    size_t size;
    char *path;
    int i;

    // determine executable name
    if (SetExecutableName(argv[0]) < 0)
        return -1;

    // create sys.path before Py_Initialize for compatibility with
    // some versions of python in mac
    size = strlen(g_ExecutableDirName) * 2 + strlen(CX_PATH_FORMAT) + 1;
    path = PyMem_RawMalloc(sizeof(char) * size);
    if (!path)
        return FatalError("Out of memory creating sys.path!");
    PyOS_snprintf(path, size, CX_PATH_FORMAT,
                  g_ExecutableDirName, g_ExecutableDirName);
    wpath = Py_DecodeLocale(path, NULL);
    if (!wpath) {
        PyMem_RawFree(path);
        return FatalError("Unable to convert path to string!");
    }

    // set initialization flags prior Py_SetPath
    Py_NoSiteFlag = 1;
    Py_FrozenFlag = 1;
    Py_IgnoreEnvironmentFlag = 1;

    Py_SetPath(wpath);
    PyMem_RawFree(wpath);

    // initialize Python
    Py_Initialize();

    // set sys.executable
    executable = PyUnicode_FromString(g_ExecutableName);
    if (!executable)
        return FatalError("Unable to convert executable name to string!");
    if (PySys_SetObject("executable", executable) < 0)
        return FatalError("Unable to set executable name!");
    Py_DECREF(executable);

    // recreate sys.path after Py_Initialize to eliminate surrogatescapes
    // in Py_DecodeLocale
    wpath = Py_DecodeLocale(path, NULL);
    PyMem_RawFree(path);
    if (!wpath)
        return FatalError("Unable to convert path to string!");
    PySys_SetPath(wpath);
    PyMem_RawFree(wpath);

    // convert arguments to wide characters
    wargv = PyMem_RawMalloc(sizeof(wchar_t*) * argc);
    if (!wargv)
        return FatalError("Out of memory converting arguments!");
    for (i = 0; i < argc; i++) {
        wargv[i] = Py_DecodeLocale(argv[i], NULL);
        if (!wargv[i])
            return FatalError("Unable to convert argument to string!");
    }
    PySys_SetArgvEx(argc, wargv, 0);
    for (i = 0; i < argc; i++)
        PyMem_RawFree(wargv[i]);
    PyMem_RawFree(wargv);

    return 0;
}

#endif


//-----------------------------------------------------------------------------
// ExecuteScript()
//   Execute the script found within the file.
//-----------------------------------------------------------------------------
static int ExecuteScript(void)
{
    PyObject *module, *function, *result;

    module = PyImport_ImportModule("__startup__");
    if (!module)
        return FatalScriptError();

    function = PyObject_GetAttrString(module, "run");
    if (!function)
        return FatalScriptError();

    result = PyObject_CallObject(function, NULL);
    if (!result)
        return FatalScriptError();

    Py_DECREF(result);
    Py_DECREF(function);
    Py_DECREF(module);

    return 0;
}
