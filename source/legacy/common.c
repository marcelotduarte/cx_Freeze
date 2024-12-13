//-----------------------------------------------------------------------------
// Common.c
//   Routines which are common to running frozen executables.
//-----------------------------------------------------------------------------

#include <compile.h>
#include <osdefs.h>

#if MAXPATHLEN < 1024
#undef MAXPATHLEN
#define MAXPATHLEN 1024
#endif

#if defined(MS_WINDOWS)
#include <libloaderapi.h>
#define PY3_DLLNAME L"python3.dll"
#endif

// global variable (used for simplicity)
#if !defined(MS_WINDOWS)
static char* g_argv0;
#endif

//-----------------------------------------------------------------------------
// get_executable_name()
//   Get the executable name given the value of argv[0]. First, if a path
// separator is not found in the value of argv[0] the PATH environment variable
// is searched to locate the full path of the executable. After that, on
// platforms other than Windows links are followed in order to find the actual
// executable path.
//-----------------------------------------------------------------------------
#ifdef MS_WINDOWS
static wchar_t* get_executable_name(void)
{
    wchar_t exe_fullpath[MAXPATHLEN + 1];
    wchar_t* executable;

    if (!GetModuleFileNameW(NULL, exe_fullpath, MAXPATHLEN + 1)) {
        FatalError("Unable to get executable name!");
        return NULL;
    }
    executable = PyMem_RawMalloc(sizeof(wchar_t) * wcslen(exe_fullpath) + 1);
    if (!executable) {
        FatalError("Out of memory creating executable!");
        return NULL;
    }
    return wcscpy(executable, exe_fullpath);
}

static wchar_t* get_lib_dir(wchar_t* executable)
{
    wchar_t buf_dir[MAXPATHLEN + 1];
    wchar_t *lib_dir, *wptr;

    // make the lib directory from executable name
    wcscpy(buf_dir, executable);
    wptr = wcsrchr(buf_dir, SEP);
    if (!wptr) {
        FatalError("Unable to calculate directory of executable!");
        return NULL;
    }
    wcscpy(++wptr, L"lib");

    lib_dir = PyMem_RawMalloc(sizeof(wchar_t) * wcslen(buf_dir) + 1);
    if (!lib_dir) {
        FatalError("Out of memory creating lib_dir!");
        return NULL;
    }
    return wcscpy(lib_dir, buf_dir);
}

static wchar_t* get_sys_path(wchar_t* lib_dir)
{
    wchar_t filename[MAXPATHLEN + 1], buf_path[MAXPATHLEN + 1], *sys_path;
    char buffer[MAXPATHLEN + 1];
    wchar_t* wbuffer;
    FILE* fp;

    // create sys.path
    wcscpy(buf_path, L"");
    // filename
    wcscpy(filename, lib_dir);
    wcscat(filename, L"\\");
    wcscat(filename, L"library.dat");
    if ((fp = _wfopen(filename, L"rt")) != NULL) {
        size_t i = fread(buffer, sizeof(*buffer), sizeof(buffer), fp);
        buffer[i] = 0;
        fclose(fp);
        wbuffer = Py_DecodeLocale(buffer, NULL);
        if (!wbuffer) {
            FatalError("Unable to convert path to string!");
        } else {
            wcscpy(filename, lib_dir);
            wcscat(filename, L"\\");
            wcscat(filename, wbuffer);
            PyMem_RawFree(wbuffer);
            wcscat(buf_path, filename);
        }
    }
    if (wcslen(buf_path) != 0)
        wcscat(buf_path, L";");
    wcscat(buf_path, lib_dir);

    sys_path = PyMem_RawMalloc(sizeof(wchar_t) * wcslen(buf_path) + 1);
    if (!sys_path) {
        FatalError("Out of memory creating sys_path!");
        return NULL;
    }
    return wcscpy(sys_path, buf_path);
}
#else
static char* get_executable_name(void)
{
    char exe_fullpath[MAXPATHLEN + 1];
    char executable_name[MAXPATHLEN + 1];
    char *executable, *ptr, *path, *temp_ptr;
    size_t size, size_argv0;
    struct stat stat_data;
    int found = 0;

    // check to see if path contains a separator
    if (strchr(g_argv0, SEP)) {
        strcpy(executable_name, g_argv0);

        // if not, check the PATH environment variable
    } else {
        path = getenv("PATH");
        if (!path) {
            FatalError("PATH environment variable not defined!");
            return NULL;
        }
        ptr = path;
        size_argv0 = strlen(g_argv0);
        while (1) {
            temp_ptr = strchr(ptr, DELIM);
            size = (temp_ptr) ? (size_t)(temp_ptr - ptr) : strlen(ptr);
            if (size + size_argv0 + 1 <= MAXPATHLEN) {
                strncpy(executable_name, ptr, MAXPATHLEN);
                executable_name[size] = SEP;
                executable_name[size + 1] = '\0';
                strcat(executable_name, g_argv0);
                if (stat(executable_name, &stat_data) == 0
                    && S_ISREG(stat_data.st_mode)
                    && (stat_data.st_mode & 0111)) {
                    found = 1;
                    break;
                }
            }
            if (!temp_ptr)
                break;
            ptr += size + 1;
        }
        if (!found) {
            FatalError("Unable to locate executable on PATH!");
            return NULL;
        }
    }

    // get absolute path for executable name
    if (!realpath(executable_name, exe_fullpath)) {
        FatalError("Unable to determine absolute path for executable!");
        return NULL;
    }
    executable = PyMem_RawMalloc(sizeof(char) * strlen(exe_fullpath) + 1);
    if (!executable) {
        FatalError("Out of memory creating executable!");
        return NULL;
    }
    return strcpy(executable, exe_fullpath);
}

static char* get_lib_dir(char* executable)
{
    char buf_dir[MAXPATHLEN + 1];
    char *lib_dir, *ptr;

    // make the lib directory from executable name
    strcpy(buf_dir, executable);
    ptr = strrchr(buf_dir, SEP);
    if (!ptr) {
        FatalError("Unable to calculate directory of executable!");
        return NULL;
    }
    strcpy(++ptr, "lib");

    lib_dir = PyMem_RawMalloc(sizeof(char) * strlen(buf_dir) + 1);
    if (!lib_dir) {
        FatalError("Out of memory creating lib_dir!");
        return NULL;
    }
    return strcpy(lib_dir, buf_dir);
}

static char* get_sys_path(char* lib_dir)
{
    char filename[MAXPATHLEN + 1], buf_path[MAXPATHLEN + 1], *sys_path;
    char buffer[MAXPATHLEN + 1];
    FILE* fp;

    // create sys.path
    strcpy(buf_path, "");
    // filename
    strcpy(filename, lib_dir);
    strcat(filename, "/");
    strcat(filename, "library.dat");
    if ((fp = fopen(filename, "r")) != NULL) {
        size_t i = fread(buffer, sizeof(*buffer), sizeof(buffer), fp);
        buffer[i] = 0;
        fclose(fp);
        strcpy(filename, lib_dir);
        strcat(filename, "/");
        strcat(filename, buffer);
        strcat(buf_path, filename);
    }
    if (strlen(buf_path) != 0)
        strcat(buf_path, ":");
    strcat(buf_path, lib_dir);

    sys_path = PyMem_RawMalloc(sizeof(char) * strlen(buf_path) + 1);
    if (!sys_path) {
        FatalError("Out of memory creating sys_path!");
        return NULL;
    }
    return strcpy(sys_path, buf_path);
}
#endif

#ifdef MS_WINDOWS
//-----------------------------------------------------------------------------
// LoadPython3dll()
//   Load python3.dll if it is on the target dir.
//-----------------------------------------------------------------------------
static int LoadPython3dll(void)
{

#ifndef __MINGW32__
    if (LoadLibraryExW(PY3_DLLNAME, NULL, LOAD_LIBRARY_SEARCH_APPLICATION_DIR)
        == NULL)
        return -1; // FatalError("Unable to load python3.dll!");
#endif
    return 0;
}
#endif

//-----------------------------------------------------------------------------
// InitializePython()
//   Initialize Python on all platforms.
//-----------------------------------------------------------------------------
static int InitializePython(int argc, wchar_t** argv)
{
#ifdef MS_WINDOWS
    wchar_t *executable, *lib_dir, *sys_path;
#else
    char *executable, *lib_dir, *sys_path;
#endif
    wchar_t *wexecutable, *wpath;

    // determine executable name, lib directory and sys.path
    if ((executable = get_executable_name()) == NULL)
        return -1;
    if ((lib_dir = get_lib_dir(executable)) == NULL)
        return -1;
    if ((sys_path = get_sys_path(lib_dir)) == NULL)
        return -1;

#ifdef MS_WINDOWS
    LoadPython3dll();
    // On Windows platform, the DLL search path is changed here.
    if (AddDllDirectory(lib_dir) == 0)
        return FatalError("Unable to change DLL search path!");

    wexecutable = executable;
    wpath = sys_path;
#else
    wexecutable = Py_DecodeLocale(executable, NULL);
    if (!wexecutable)
        return FatalError("Unable to convert path to string!");
    PyMem_RawFree(executable);

    wpath = Py_DecodeLocale(sys_path, NULL);
    if (!wpath)
        return FatalError("Unable to convert path to string!");
    PyMem_RawFree(sys_path);
#endif

    // initialize Python
    Py_NoSiteFlag = 1;
    Py_FrozenFlag = 1;
    Py_IgnoreEnvironmentFlag = 1;
    Py_SetProgramName(wexecutable);
    Py_SetPath(wpath);
    Py_Initialize();
    PySys_SetArgvEx(argc, argv, 0);

    PyMem_RawFree(wexecutable);
    PyMem_RawFree(wpath);
    PyMem_RawFree(lib_dir);

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
