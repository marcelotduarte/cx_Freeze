//-----------------------------------------------------------------------------
// Common.c
//   Routines which are common to running frozen executables.
//-----------------------------------------------------------------------------

#include <compile.h>
#include <eval.h>
#include <osdefs.h>

// define names that will work for both Python 2 and 3
#if PY_MAJOR_VERSION >= 3
    #define cxString_FromString         PyUnicode_FromString
    #define cxWin_GetModuleFileName     GetModuleFileNameW
    #define cxWin_PathRemoveFileSpec    PathRemoveFileSpecW
#else
    #define cxString_FromString         PyString_FromString
    #define cxWin_GetModuleFileName     GetModuleFileNameA
    #define cxWin_PathRemoveFileSpec    PathRemoveFileSpecA
#endif

// global variables (used for simplicity)
#if defined(MS_WINDOWS) && PY_MAJOR_VERSION >= 3
    static wchar_t g_ExecutableName[MAXPATHLEN + 1];
    static wchar_t g_ExecutableDirName[MAXPATHLEN + 1];
#else
    static char g_ExecutableName[MAXPATHLEN + 1];
    static char g_ExecutableDirName[MAXPATHLEN + 1];
#endif

#ifndef MS_WINDOWS
//-----------------------------------------------------------------------------
// FollowLinks()
//   Follow links in order to get the final executable name.
//-----------------------------------------------------------------------------
static int FollowLinks(void)
{
    char linkData[MAXPATHLEN + 1], *ptr;
    size_t linkSize, size, i;
    struct stat statData;

    for (i = 0; i < 25; i++) {
        if (lstat(g_ExecutableName, &statData) < 0)
            return FatalError("unable to stat executable");
        if (!S_ISLNK(statData.st_mode))
            break;
        linkSize = readlink(g_ExecutableName, linkData, sizeof(linkData));
        if (linkSize < 0)
            return FatalError("unable to read link");
        if (linkData[0] == SEP)
            strcpy(g_ExecutableName, linkData);
        else {
            ptr = strrchr(g_ExecutableName, SEP);
            if (!ptr)
                return FatalError("no directory in executable name!");
            size = strlen(g_ExecutableName) - strlen(ptr);
            if (size + linkSize + 1 > MAXPATHLEN)
                return FatalError("cannot dereference link, path too large!");
            strncpy(ptr + 1, linkData, linkSize);
            *(ptr + linkSize + 1) = '\0';
        }
    }

    return 0;
}
#endif


//-----------------------------------------------------------------------------
// SetExecutableName()
//   Set the executable name given the value of argv[0]. First, if a path
// separator is not found in the value of argv[0] the PATH environment variable
// is searched to locate the full path of the executable. After that, on
// platforms other than Windows links are followed in order to find the actual
// executable path.
//-----------------------------------------------------------------------------
static int SetExecutableName(
    const char *argv0)                  // script to execute
{
#ifdef MS_WINDOWS
    if (!cxWin_GetModuleFileName(NULL, g_ExecutableName, MAXPATHLEN + 1))
        return FatalError("Unable to get executable name!");
    memcpy(g_ExecutableDirName, g_ExecutableName,
            (MAXPATHLEN + 1) * sizeof(wchar_t));
    cxWin_PathRemoveFileSpec(g_ExecutableDirName);

#else

    char *path, *ptr, *tempPtr;
    size_t size, argv0Size;
    struct stat statData;
    int found = 0;

    // check to see if path contains a separator
    if (strchr(argv0, SEP)) {
        strcpy(g_ExecutableName, argv0);

    // if not, check the PATH environment variable
    } else {
        path = getenv("PATH");
        if (!path)
            return FatalError("PATH environment variable not defined!");
        ptr = path;
        argv0Size = strlen(argv0);
        while (1) {
            tempPtr = strchr(ptr, DELIM);
            if (tempPtr)
                size = tempPtr - ptr;
            else size = strlen(ptr);
            if (size + argv0Size + 1 <= MAXPATHLEN) {
                strncpy(g_ExecutableName, ptr, size);
                g_ExecutableName[size] = SEP;
                g_ExecutableName[size + 1] = '\0';
                strcat(g_ExecutableName, argv0);
                if (stat(g_ExecutableName, &statData) == 0 &&
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

    if (FollowLinks() < 0)
        return -1;

    // get directory from executable name
    strcpy(g_ExecutableDirName, g_ExecutableName);
    ptr = strrchr(g_ExecutableDirName, SEP);
    if (!ptr)
        return FatalError("Unable to calculate directory of executable!");
    *ptr = '\0';
#endif

    return 0;
}


#if PY_MAJOR_VERSION >= 3

#ifdef MS_WINDOWS
//-----------------------------------------------------------------------------
// InitializePython()
//   Initialize Python for Python 3 and higher on Windows.
//-----------------------------------------------------------------------------
static int InitializePython(int argc, wchar_t **argv)
{
    // determine executable name
    if (SetExecutableName(NULL) < 0)
        return -1;

    // initialize Python
    Py_NoSiteFlag = 1;
    Py_FrozenFlag = 1;
    Py_IgnoreEnvironmentFlag = 1;
    Py_SetPythonHome(g_ExecutableDirName);
    Py_SetProgramName(g_ExecutableName);
    Py_Initialize();
    PySys_SetArgv(argc, argv);

    return 0;
}

#else

//-----------------------------------------------------------------------------
// InitializePython()
//   Initialize Python for Python 3 and higher on all other platforms.
//-----------------------------------------------------------------------------
static int InitializePython(int argc, char **argv)
{
    wchar_t **wargv, *wExecutableName, *wExecutableDirName;
    char *origLocale;
    size_t size;
    int i;

    // determine executable name
    if (SetExecutableName(argv[0]) < 0)
        return -1;

    // ensure locale is set consistently
    origLocale = setlocale(LC_ALL, NULL);
    setlocale(LC_ALL, "");

    // convert executable name to wide characters
    size = mbstowcs(NULL, g_ExecutableName, 0);
    if (size < 0)
        return FatalError("Unable to convert executable name to Unicode!");
    wExecutableName = PyMem_Malloc((size + 1) * sizeof(wchar_t));
    if (!wExecutableName)
        return FatalError("Out of memory converting executable name!");
    mbstowcs(wExecutableName, g_ExecutableName, size + 1);

    // convert executable dir name to wide characters
    size = mbstowcs(NULL, g_ExecutableDirName, 0);
    if (size < 0)
        return FatalError("Unable to convert executable dir name to Unicode!");
    wExecutableDirName = PyMem_Malloc((size + 1) * sizeof(wchar_t));
    if (!wExecutableDirName)
        return FatalError("Out of memory converting executable dir name!");
    mbstowcs(wExecutableDirName, g_ExecutableDirName, size + 1);

    // convert arguments to wide characters
    wargv = PyMem_Malloc(sizeof(wchar_t*) * argc);
    if (!wargv)
        return FatalError("Out of memory converting arguments!");
    for (i = 0; i < argc; i++) {
        size = mbstowcs(NULL, argv[i], 0);
        if (size < 0)
            return FatalError("Unable to convert argument to Unicode!");
        wargv[i] = PyMem_Malloc((size + 1) * sizeof(wchar_t));
        if (!wargv[i])
            return FatalError("Out of memory converting argument!");
        mbstowcs(wargv[i], argv[i], size + 1);
    }

    // reset locale
    setlocale(LC_ALL, origLocale);

    // initialize Python
    Py_NoSiteFlag = 1;
    Py_FrozenFlag = 1;
    Py_IgnoreEnvironmentFlag = 1;
    Py_SetPythonHome(wExecutableDirName);
    Py_SetProgramName(wExecutableName);
    Py_Initialize();
    PySys_SetArgv(argc, wargv);

    return 0;
}

#endif

#else

//-----------------------------------------------------------------------------
// InitializePython()
//   Initialize Python for Python 2.x.
//-----------------------------------------------------------------------------
static int InitializePython(int argc, char **argv)
{
    // determine executable name
    if (SetExecutableName(argv[0]) < 0)
        return -1;

    // initialize Python
    Py_NoSiteFlag = 1;
    Py_FrozenFlag = 1;
    Py_IgnoreEnvironmentFlag = 1;
    Py_SetPythonHome(g_ExecutableDirName);
    Py_SetProgramName(g_ExecutableName);
    Py_Initialize();
    PySys_SetArgv(argc, argv);

    return 0;
}

#endif


//-----------------------------------------------------------------------------
// ExecuteScript()
//   Execute the script found within the file.
//-----------------------------------------------------------------------------
static int ExecuteScript(void)
{
    PyObject *name, *module;

    name = cxString_FromString("__startup__");
    if (!name)
        return FatalError("Cannot create string for startup module name!");
    module = PyImport_Import(name);
    if (!module)
        return FatalScriptError();
    Py_DECREF(module);
    Py_DECREF(name);

    return 0;
}

