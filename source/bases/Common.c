//-----------------------------------------------------------------------------
// Common.c
//   Routines which are common to running frozen executables.
//-----------------------------------------------------------------------------

#include <compile.h>
#include <eval.h>
#include <osdefs.h>

// PyEval_EvalCode() takes different parameter types on Python 2 & 3.
#if PY_MAJOR_VERSION >= 3
typedef PyObject EvalCodeType;
#else
typedef PyCodeObject EvalCodeType;
#endif

// global variables (used for simplicity)
static char g_ExecutableName[MAXPATHLEN + 1];
static char g_ExecutableDirName[MAXPATHLEN + 1];
static char g_LibDirName[MAXPATHLEN + 1];
static char g_ZipFileName[MAXPATHLEN + 1];
static char g_InitscriptName[MAXPATHLEN + 1];
static PyObject *g_ExecutableNameObj;
static PyObject *g_ExecutableDirNameObj;
static PyObject *g_LibDirNameObj;
static PyObject *g_ZipFileNameObj;

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
    char *path, *ptr, *tempPtr;
    size_t size, argv0Size;
    struct stat statData;
    int found = 0;

#ifdef MS_WINDOWS
    if (!GetModuleFileName(NULL, g_ExecutableName, MAXPATHLEN + 1))
        return FatalError("Unable to get executable name!");
#else

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
#endif

    // get directory from executable name
    strcpy(g_ExecutableDirName, g_ExecutableName);
    ptr = strrchr(g_ExecutableDirName, SEP);
    if (!ptr)
        return FatalError("Unable to calculate directory of executable!");
    *ptr = '\0';

    // get library directory
#ifdef LIBDIR
    sprintf(g_LibDirName, "%s%c%s", g_ExecutableDirName, SEP, LIBDIR);
#else
    strcpy(g_LibDirName, g_ExecutableDirName);
#endif

    // calculate zip file name
    sprintf(g_ZipFileName, "%s%cpython%d%d.zip", g_LibDirName, SEP,
            PY_MAJOR_VERSION, PY_MINOR_VERSION);

    // calculate initscript name
    ptr = strrchr(g_ExecutableName, SEP);
    strcpy(g_InitscriptName, ptr + 1);
#ifdef MS_WINDOWS
    ptr = strrchr(g_InitscriptName, '.');
    if (ptr)
        *ptr = '\0';
    for (ptr = g_InitscriptName; *ptr; ptr++)
        *ptr = tolower(*ptr);
#endif
    strcat(g_InitscriptName, "__init__");

    return 0;
}


#if PY_MAJOR_VERSION >= 3
//-----------------------------------------------------------------------------
// InitializePython()
//   Initialize Python for Python 3 and higher.
//-----------------------------------------------------------------------------
#ifdef MS_WINDOWS
static int InitializePython(int argc, wchar_t **argv)
{
    wchar_t **wargv, *wExecutableName, *wExecutableDirName;
    char *origLocale;
    size_t size;
    int i;

    // determine executable name
    if (SetExecutableName(NULL) < 0)
        return -1;
#else
static int InitializePython(int argc, char **argv)
{
    wchar_t **wargv, *wExecutableName, *wExecutableDirName;
    char *origLocale;
    size_t size;
    int i;

    // determine executable name
    if (SetExecutableName(argv[0]) < 0)
        return -1;
#endif	
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

#ifdef MS_WINDOWS
	wargv = argv;
#else
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
#endif
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

    // convert strings to Python objects for later injection
    g_ExecutableNameObj = PyUnicode_DecodeFSDefault(g_ExecutableName);
    if (!g_ExecutableNameObj)
        return FatalError("Unable to create Python obj for executable name!");
    g_ExecutableDirNameObj = PyUnicode_DecodeFSDefault(g_ExecutableDirName);
    if (!g_ExecutableDirNameObj)
        return FatalError("Unable to create Python obj for executable dir!");
    g_LibDirNameObj = PyUnicode_DecodeFSDefault(g_LibDirName);
    if (!g_LibDirNameObj)
        return FatalError("Unable to create Python obj for lib dir name!");
    g_ZipFileNameObj = PyUnicode_DecodeFSDefault(g_ZipFileName);
    if (!g_ZipFileNameObj)
        return FatalError("Unable to create Python obj for zip file name!");

    return 0;
}

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

    // convert strings to Python objects for later injection
    g_ExecutableNameObj = PyString_FromString(g_ExecutableName);
    if (!g_ExecutableNameObj)
        return FatalError("Unable to create Python obj for executable name!");
    g_ExecutableDirNameObj = PyString_FromString(g_ExecutableDirName);
    if (!g_ExecutableDirNameObj)
        return FatalError("Unable to create Python obj for executable dir!");
    g_LibDirNameObj = PyString_FromString(g_LibDirName);
    if (!g_LibDirNameObj)
        return FatalError("Unable to create Python obj for lib dir name!");
    g_ZipFileNameObj = PyString_FromString(g_ZipFileName);
    if (!g_ZipFileNameObj)
        return FatalError("Unable to create Python obj for zip file name!");

    return 0;
}

#endif


//-----------------------------------------------------------------------------
// GetImporter()
//   Return the importer which will be used for importing the initialization
// script from the zip file.
//-----------------------------------------------------------------------------
static int GetImporter(
    PyObject **importer)                // importer (OUT)
{
    PyObject *module;

    module = PyImport_ImportModule("zipimport");
    if (!module)
        return FatalError("cannot import zipimport module");
    *importer = PyObject_CallMethod(module, "zipimporter", "O",
            g_ZipFileNameObj);
    Py_DECREF(module);
    if (!*importer)
        return FatalError("cannot get zipimporter instance");
    return 0;
}


//-----------------------------------------------------------------------------
// PopulateInitScriptDict()
//   Return the dictionary used by the initialization script.
//-----------------------------------------------------------------------------
static int PopulateInitScriptDict(
    PyObject *dict)                     // dictionary to populate
{
    if (!dict)
        return FatalError("unable to create temporary dictionary");
    if (PyDict_SetItemString(dict, "__builtins__", PyEval_GetBuiltins()) < 0)
        return FatalError("unable to set __builtins__");
    if (PyDict_SetItemString(dict, "FILE_NAME", g_ExecutableNameObj) < 0)
        return FatalError("unable to set FILE_NAME");
    if (PyDict_SetItemString(dict, "DIR_NAME", g_ExecutableDirNameObj) < 0)
        return FatalError("unable to set DIR_NAME");
    if (PyDict_SetItemString(dict, "LIB_DIR_NAME", g_LibDirNameObj) < 0)
        return FatalError("unable to set LIB_DIR_NAME");
    if (PyDict_SetItemString(dict, "INITSCRIPT_ZIP_FILE_NAME",
            g_ZipFileNameObj) < 0)
        return FatalError("unable to set INITSCRIPT_ZIP_FILE_NAME");
    return 0;
}


//-----------------------------------------------------------------------------
// ExecuteScript()
//   Execute the script found within the file.
//-----------------------------------------------------------------------------
static int ExecuteScript(void)
{
    PyObject *importer, *dict, *code, *temp;

    // get zip importer object
    importer = NULL;
    if (GetImporter(&importer) < 0)
        return -1;

    // create and populate dictionary for initscript module
    dict = PyDict_New();
    if (PopulateInitScriptDict(dict) < 0) {
        Py_XDECREF(dict);
        Py_DECREF(importer);
        return -1;
    }

    // locate and execute script
    code = PyObject_CallMethod(importer, "get_code", "s", g_InitscriptName);
    Py_DECREF(importer);
    if (!code)
        return FatalError("unable to locate initialization module");
    temp = PyEval_EvalCode( (EvalCodeType*) code, dict, dict);
    Py_DECREF(code);
    Py_DECREF(dict);
    if (!temp)
        return FatalScriptError();
    Py_DECREF(temp);

    return 0;
}

