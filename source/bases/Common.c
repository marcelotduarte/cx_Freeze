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
    #define CX_LIB                      L"lib"
#else
    #define CX_PATH_FORMAT              L"%ls/lib/library.zip:%ls/lib"
#endif

// global variables (used for simplicity)
static wchar_t g_ExecutableName[MAXPATHLEN + 1];
static wchar_t g_ExecutableDirName[MAXPATHLEN + 1];
#if defined(MS_WINDOWS)
static wchar_t g_LibDirName[MAXPATHLEN + 1];
#else
static char *g_argv0;
#endif


//-----------------------------------------------------------------------------
// SetExecutableName()
//   Set the executable name given the value of argv[0]. First, if a path
// separator is not found in the value of argv[0] the PATH environment variable
// is searched to locate the full path of the executable. After that, on
// platforms other than Windows links are followed in order to find the actual
// executable path.
// On Windows platform, the DLL search path is changed here.
//-----------------------------------------------------------------------------
static int SetExecutableName(void)
{
#ifdef MS_WINDOWS
    if (!GetModuleFileNameW(NULL, g_ExecutableName, MAXPATHLEN + 1))
        return FatalError("Unable to get executable name!");
    wcscpy(g_ExecutableDirName, g_ExecutableName);
    PathRemoveFileSpecW(g_ExecutableDirName);

    // set lib directory as default for dll search
    PathCombineW(g_LibDirName, g_ExecutableDirName, CX_LIB);
    if (!SetDllDirectoryW(g_LibDirName))
        return FatalError("Unable to change DLL search path!");

#else
    char executableName[PATH_MAX + 1], *path, *ptr, *tempPtr;
    char tempname[MAXPATHLEN + 1];
    wchar_t *wname, *wptr;
    size_t size, argv0Size;
    struct stat statData;
    int found = 0;

    // check to see if path contains a separator
    if (strchr(g_argv0, SEP)) {
        strcpy(executableName, g_argv0);

    // if not, check the PATH environment variable
    } else {
        path = getenv("PATH");
        if (!path)
            return FatalError("PATH environment variable not defined!");
        ptr = path;
        argv0Size = strlen(g_argv0);
        while (1) {
            tempPtr = strchr(ptr, DELIM);
            size = (tempPtr) ? (size_t) (tempPtr - ptr) : strlen(ptr);
            if (size + argv0Size + 1 <= MAXPATHLEN) {
                strncpy(executableName, ptr, PATH_MAX + 1);
                executableName[size] = SEP;
                executableName[size + 1] = '\0';
                strcat(executableName, g_argv0);
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
    if (!realpath(executableName, tempname))
        return FatalError("Unable to determine absolute path for executable!");
    wname = Py_DecodeLocale(tempname, NULL);
    if (!wname)
        return FatalError("Unable to convert path to string!");
    wcscpy(g_ExecutableName, wname);

    // get directory from executable name
    wptr = wcsrchr(wname, SEP);
    if (!wptr)
        return FatalError("Unable to calculate directory of executable!");
    *wptr = '\0';
    wcscpy(g_ExecutableDirName, wname);
    PyMem_RawFree(wname);
#endif

    return 0;
}


//-----------------------------------------------------------------------------
// InitializePython()
//   Initialize Python on all platforms.
//-----------------------------------------------------------------------------
static int InitializePython(int argc, wchar_t **argv)
{
    wchar_t *wpath;
    size_t size;

    // determine executable name
    if (SetExecutableName() < 0)
        return -1;

    // create sys.path
    size = wcslen(g_ExecutableDirName) * 2 + wcslen(CX_PATH_FORMAT) + 1;
    wpath = PyMem_RawMalloc(sizeof(wchar_t) * size);
    if (!wpath)
        return FatalError("Out of memory creating sys.path!");
    swprintf(wpath, size, CX_PATH_FORMAT,
             g_ExecutableDirName, g_ExecutableDirName);

    // initialize Python
    Py_NoSiteFlag = 1;
    Py_FrozenFlag = 1;
    Py_IgnoreEnvironmentFlag = 1;
    Py_SetProgramName(g_ExecutableName);
    Py_SetPath(wpath);
    Py_Initialize();
#ifdef MS_WINDOWS
    PySys_SetArgv(argc, argv);
#else
    PySys_SetArgvEx(argc, argv, 0);
#endif

    PyMem_RawFree(wpath);

    return 0;
}



//-----------------------------------------------------------------------------
// ExecuteScript()
//   Execute the script found within the file.
//-----------------------------------------------------------------------------
static int ExecuteScript(void)
{
    PyObject *module, *func = NULL, *result = NULL;

    module = PyImport_ImportModule("__startup__");
    if (!module)
        return FatalScriptError();

    func = PyObject_GetAttrString(module, "init");
    if (!func) {
        Py_DECREF(module);
        return FatalScriptError();
    }

    result = PyObject_CallObject(func, NULL);
    Py_DECREF(func);
    if (!result) {
        Py_DECREF(module);
        return FatalScriptError();
    }
    Py_DECREF(result);

    func = PyObject_GetAttrString(module, "run");
    Py_DECREF(module);
    if (!func)
        return FatalScriptError();

    result = PyObject_CallObject(func, NULL);
    Py_DECREF(func);
    if (!result)
        return FatalScriptError();
    Py_DECREF(result);

    return 0;
}
