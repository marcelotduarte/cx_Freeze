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
    #define CX_PATH_FORMAT              "%ls\\lib\\library.zip;%ls\\lib"
    #define CX_LIB                      L"lib"
#else
    #define CX_PATH_FORMAT              "%ls/lib/library.zip:%ls/lib"
#endif

// global variables (used for simplicity)
static wchar_t g_ExecutableName[MAXPATHLEN + 1];
static wchar_t g_ExecutableDirName[MAXPATHLEN + 1];
#if defined(MS_WINDOWS)
static wchar_t g_LibDirName[MAXPATHLEN + 1];
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
static int SetExecutableName(const wchar_t *wargv0)
{
#ifdef MS_WINDOWS
    if (!GetModuleFileNameW(NULL, g_ExecutableName, MAXPATHLEN + 1))
        return FatalError("Unable to get executable name!");
    memcpy(g_ExecutableDirName, g_ExecutableName,
            (MAXPATHLEN + 1) * sizeof(wchar_t));
    PathRemoveFileSpecW(g_ExecutableDirName);

    // set lib directory as default for dll search
    PathCombineW(g_LibDirName, g_ExecutableDirName, CX_LIB);
    if (!SetDllDirectoryW(g_LibDirName))
        return FatalError("Unable to change DLL search path!");

#else

    char executableName[PATH_MAX + 1], *path, *ptr, *tempPtr;
    char tempname[MAXPATHLEN + 1];
    wchar_t *wname;
    size_t size, argv0Size;
    struct stat statData;
    int found = 0;
    char *argv0;

    argv0 = Py_EncodeLocale(wargv0, NULL);
    if (!argv0)
        return FatalError("Unable to convert argument to bytes!");

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
    if (!realpath(executableName, tempname))
        return FatalError("Unable to determine absolute path for executable!");
    wname = Py_DecodeLocale(tempname, NULL);
    if (!wname)
        return FatalError("Unable to convert path to string!");
    wcscpy(g_ExecutableName, wname);
    PyMem_RawFree(wname);

    // get directory from executable name
    ptr = strrchr(tempname, SEP);
    if (!ptr)
        return FatalError("Unable to calculate directory of executable!");
    *ptr = '\0';
    wname = Py_DecodeLocale(tempname, NULL);
    if (!wname)
        return FatalError("Unable to convert path to string!");
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
    char *path;
    wchar_t *wpath;
    size_t size;

    // determine executable name
    if (SetExecutableName(argv[0]) < 0)
        return -1;

    // create sys.path
    size = sizeof(g_ExecutableDirName) * 2 + strlen(CX_PATH_FORMAT) + 1;
    path = PyMem_RawMalloc(sizeof(char) * size);
    if (!path)
        return FatalError("Out of memory creating sys.path!");
    PyOS_snprintf(path, size, CX_PATH_FORMAT,
                  g_ExecutableDirName, g_ExecutableDirName);
    wpath = Py_DecodeLocale(path, NULL);
    PyMem_RawFree(path);
    if (!wpath)
        return FatalError("Unable to convert path to string!");

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
