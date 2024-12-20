//-----------------------------------------------------------------------------
// _common.c
//   Routines which are common to running frozen executables.
//-----------------------------------------------------------------------------

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#ifdef MS_WINDOWS
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#endif
#include <compile.h>
#include <osdefs.h>

#if (!defined(MAXPATHLEN) || MAXPATHLEN < 1024)
#undef MAXPATHLEN
#define MAXPATHLEN 1024
#endif

#ifdef MS_WINDOWS
#include <libloaderapi.h>
#define PY3_DLLNAME L"python3.dll"
#endif

extern int FatalScriptError(void);

//-----------------------------------------------------------------------------
// get_program_name()
//   Get the executable name given the value of argv[0]. First, if a path
// separator is not found in the value of argv[0] the PATH environment variable
// is searched to locate the full path of the executable. After that, on
// platforms other than Windows links are followed in order to find the actual
// executable path.
//-----------------------------------------------------------------------------
#ifdef MS_WINDOWS

PyStatus get_program_name(wchar_t** ptr_str, wchar_t* argv0)
{
    wchar_t* program_name;

    program_name = PyMem_RawMalloc(sizeof(wchar_t) * (MAXPATHLEN + 1));
    if (!program_name) {
        return PyStatus_Error("Out of memory creating executable!");
    }

    if (!GetModuleFileNameW(NULL, program_name, MAXPATHLEN)) {
        PyMem_RawFree(program_name);
        return PyStatus_Error("Unable to get executable path!");
    }
    *ptr_str = program_name;
    return PyStatus_Ok();
}

static PyStatus get_prefix(wchar_t** ptr_str, wchar_t* program_name)
{
    wchar_t *prefix, *wptr;

    prefix = PyMem_RawMalloc(sizeof(wchar_t) * (MAXPATHLEN + 1));
    if (!prefix) {
        return PyStatus_Error("Out of memory creating prefix!");
    }

    // get the directory of the executable
    wcscpy(prefix, program_name);
    wptr = wcsrchr(prefix, SEP);
    if (!wptr) {
        PyMem_RawFree(prefix);
        return PyStatus_Error("Unable to calculate directory of executable!");
    }
    *(wptr++) = 0;
    *ptr_str = prefix;
    return PyStatus_Ok();
}

static PyStatus get_platlib(wchar_t** ptr_str, wchar_t* prefix)
{
    wchar_t* platlib;

    platlib = PyMem_RawMalloc(sizeof(wchar_t) * (MAXPATHLEN + 1));
    if (!platlib) {
        return PyStatus_Error("Out of memory creating platlib!");
    }

    // make the lib directory from executable dir
    wcscpy(platlib, prefix);
    wcscat(platlib, L"\\");
    wcscat(platlib, L"lib");
    *ptr_str = platlib;
    return PyStatus_Ok();
}

static PyStatus get_library_zip(wchar_t** ptr_str, wchar_t* platlib)
{
    wchar_t *filename, *wbuffer, *wptr;
    char* buffer;
    size_t i;
    FILE* fp;

    filename = PyMem_RawMalloc(sizeof(wchar_t) * (MAXPATHLEN + 1));
    if (!filename) {
        return PyStatus_Error("Out of memory creating shared zip filename!");
    }

    // open the library.dat to get the zip filename
    wcscpy(filename, platlib);
    wcscat(filename, L"\\");
    wptr = filename + wcslen(filename);
    wcscat(filename, L"library.dat");
    if ((fp = _wfopen(filename, L"rt")) == NULL) {
        PyMem_RawFree(filename);
        return PyStatus_Ok(); // ok if 'library.dat' does not exist
    }
    buffer = PyMem_RawMalloc(sizeof(char) * (MAXPATHLEN + 1));
    if (!buffer) {
        PyMem_RawFree(filename);
        return PyStatus_Error("Out of memory creating buffer!");
    }
    i = fread(buffer, sizeof(char), MAXPATHLEN, fp);
    buffer[i] = 0;
    fclose(fp);
    wbuffer = Py_DecodeLocale(buffer, NULL);
    PyMem_RawFree(buffer);
    if (!wbuffer) {
        PyMem_RawFree(filename);
        return PyStatus_Error("Unable to convert path to string!");
    }
    wcscpy(wptr, wbuffer);
    PyMem_RawFree(wbuffer);

    *ptr_str = filename;
    return PyStatus_Ok();
}

#else

static PyStatus get_program_name(char** ptr_str, const char* argv0)
{
    char *executable_name, *program_name, *ptr, *path, *temp_ptr;
    size_t size, size_argv0;
    struct stat stat_data;
    int found = 0;

    executable_name = PyMem_RawMalloc(sizeof(char) * (MAXPATHLEN + 1));
    if (!executable_name) {
        return PyStatus_Error("Out of memory creating executable_name!");
    }

    // check to see if path contains a separator
    if (strchr(argv0, SEP)) {
        strcpy(executable_name, argv0);
    } else {
        // if not, check the PATH environment variable
        path = getenv("PATH");
        if (!path) {
            return PyStatus_Error("PATH environment variable not defined!");
        }
        ptr = path;
        size_argv0 = strlen(argv0);
        while (1) {
            temp_ptr = strchr(ptr, DELIM);
            size = (temp_ptr) ? (size_t)(temp_ptr - ptr) : strlen(ptr);
            if (size + size_argv0 + 1 <= MAXPATHLEN) {
                strncpy(executable_name, ptr, MAXPATHLEN);
                executable_name[size] = SEP;
                executable_name[size + 1] = '\0';
                strcat(executable_name, argv0);
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
            PyMem_RawFree(executable_name);
            return PyStatus_Error("Unable to locate executable on PATH!");
        }
    }

    // get absolute path for executable name
    program_name = PyMem_RawMalloc(sizeof(char) * (MAXPATHLEN + 1));
    if (!program_name) {
        PyMem_RawFree(executable_name);
        return PyStatus_Error("Out of memory creating executable!");
    }
    if (!realpath(executable_name, program_name)) {
        PyMem_RawFree(executable_name);
        return PyStatus_Error(
            "Unable to determine absolute path for executable!");
    }
    PyMem_RawFree(executable_name);

    *ptr_str = program_name;
    return PyStatus_Ok();
}

static PyStatus get_prefix(char** ptr_str, const char* program_name)
{
    char *prefix, *ptr;

    prefix = PyMem_RawMalloc(sizeof(char) * (MAXPATHLEN + 1));
    if (!prefix) {
        return PyStatus_Error("Out of memory creating prefix!");
    }

    // get the directory of the executable
    strcpy(prefix, program_name);
    ptr = strrchr(prefix, SEP);
    if (!ptr) {
        PyMem_RawFree(prefix);
        return PyStatus_Error("Unable to calculate directory of executable!");
    }
    *(ptr++) = 0;
    *ptr_str = prefix;
    return PyStatus_Ok();
}

static PyStatus get_platlib(char** ptr_str, const char* prefix)
{
    char* platlib;

    platlib = PyMem_RawMalloc(sizeof(char) * (MAXPATHLEN + 1));
    if (!platlib) {
        return PyStatus_Error("Out of memory creating platlib!");
    }

    // make the lib directory from executable dir
    strcpy(platlib, prefix);
    strcat(platlib, "/");
    strcat(platlib, "lib");
    *ptr_str = platlib;
    return PyStatus_Ok();
}

static PyStatus get_library_zip(char** ptr_str, const char* platlib)
{
    char *filename, *ptr;
    size_t dir_len, i;
    FILE* fp;

    filename = PyMem_RawMalloc(sizeof(wchar_t) * (MAXPATHLEN + 1));
    if (!filename) {
        return PyStatus_Error("Out of memory creating shared zip filename!");
    }

    // open the library.dat to get the zip filename
    strcpy(filename, platlib);
    strcat(filename, "/");
    dir_len = strlen(filename);
    ptr = filename + dir_len;
    strcat(filename, "library.dat");
    if ((fp = fopen(filename, "rt")) == NULL) {
        PyMem_RawFree(filename);
        return PyStatus_Ok(); // ok if 'library.dat' does not exist
    }
    i = fread(ptr, sizeof(char), MAXPATHLEN - dir_len, fp);
    ptr[i] = 0;
    fclose(fp);
    *ptr_str = filename;
    return PyStatus_Ok();
}
#endif

//-----------------------------------------------------------------------------
// InitializePython()
//   Main routine for configuration of frozen programs using PEP 587.
//-----------------------------------------------------------------------------
static PyStatus PreInitializePython(void)
{
    PyPreConfig preconfig;

    // pre config - set utf8 mode
    PyPreConfig_InitIsolatedConfig(&preconfig);
    preconfig.utf8_mode = 1;
    // set memory allocator only on Python 3.13
#ifdef PYMEM_ALLOCATOR_MIMALLOC
    preconfig.allocator = PYMEM_ALLOCATOR_MIMALLOC;
#endif
    return Py_PreInitialize(&preconfig);
}

//-----------------------------------------------------------------------------
// PostInitializePython()
//   Adds the lib directory to the search path used to locate DLLs.
//   Load python3.dll if it is on the target dir.
//-----------------------------------------------------------------------------
#ifdef MS_WINDOWS
static PyStatus PostInitializePython(wchar_t* platlib)
{
    PyStatus status = PyStatus_Ok();

    // clang-format off
    Py_BEGIN_ALLOW_THREADS
    if (AddDllDirectory(platlib) == NULL)
        status = PyStatus_Error("Unable to change DLL search path!");
    Py_END_ALLOW_THREADS

#ifndef __MINGW32__
    if (!PyStatus_IsError(status)) {
        Py_BEGIN_ALLOW_THREADS
        // Ignore the error if the dll does not exist.
        LoadLibraryExW(PY3_DLLNAME, NULL, LOAD_LIBRARY_SEARCH_APPLICATION_DIR);
        // status = PyStatus_Error("Unable to load python3.dll!");
        Py_END_ALLOW_THREADS
    }
#endif
    // clang-format on
    return status;
}
#endif

#ifdef MS_WINDOWS
PyStatus InitializePython(int argc, wchar_t** argv)
{
    wchar_t *program_name = NULL, *prefix = NULL, *platlib = NULL,
            *library_zip = NULL;
#else
PyStatus InitializePython(int argc, char** argv)
{
    char *program_name = NULL, *prefix = NULL, *platlib = NULL,
         *library_zip = NULL;
#endif
    PyStatus status;
    PyConfig config;

    // pre config
    status = PreInitializePython();
    if (!PyStatus_Exception(status)) {

        // config
        PyConfig_InitIsolatedConfig(&config);
        config.site_import = 0;
        config.module_search_paths_set = 1;
    }

    // set argv and use it to calculate program name, executable, prefix, etc
#ifdef MS_WINDOWS
    if (!PyStatus_Exception(status))
        status = PyConfig_SetArgv(&config, argc, argv);
    if (!PyStatus_Exception(status)) {
        status = get_program_name(&program_name, argv[0]);
        if (!PyStatus_Exception(status))
            status = PyConfig_SetString(
                &config, &config.program_name, program_name);
    }
    if (!PyStatus_Exception(status)) {
        status = get_prefix(&prefix, program_name);
        if (!PyStatus_Exception(status)) {
            status = PyConfig_SetString(&config, &config.exec_prefix, prefix);
            if (!PyStatus_Exception(status))
                status = PyConfig_SetString(&config, &config.prefix, prefix);
        }
    }
    if (!PyStatus_Exception(status)) {
        // module_search_paths (sys.path)
        status = get_platlib(&platlib, prefix);
        if (!PyStatus_Exception(status)) {
            status = PyWideStringList_Append(
                &config.module_search_paths, platlib);
            if (!PyStatus_Exception(status)) {
                status = get_library_zip(&library_zip, platlib);
                if (library_zip)
                    status = PyWideStringList_Insert(
                        &config.module_search_paths, 0, library_zip);
            }
        }
    }
#else
    if (!PyStatus_Exception(status))
        status = PyConfig_SetBytesArgv(&config, argc, argv);
    if (!PyStatus_Exception(status)) {
        status = get_program_name(&program_name, argv[0]);
        if (!PyStatus_Exception(status))
            status = PyConfig_SetBytesString(
                &config, &config.program_name, program_name);
    }
    if (!PyStatus_Exception(status)) {
        status = get_prefix(&prefix, program_name);
        if (!PyStatus_Exception(status)) {
            status = PyConfig_SetBytesString(
                &config, &config.exec_prefix, prefix);
            if (!PyStatus_Exception(status))
                status
                    = PyConfig_SetBytesString(&config, &config.prefix, prefix);
        }
    }
    if (!PyStatus_Exception(status)) {
        // module_search_paths (sys.path)
        status = get_platlib(&platlib, prefix);
        if (!PyStatus_Exception(status)) {
            wchar_t* wplatlib = Py_DecodeLocale(platlib, NULL);
            if (wplatlib) {
                status = PyWideStringList_Append(
                    &config.module_search_paths, wplatlib);
                PyMem_RawFree(wplatlib);
                if (!PyStatus_Exception(status)) {
                    status = get_library_zip(&library_zip, platlib);
                    if (library_zip) {
                        wchar_t* wlibrary_zip
                            = Py_DecodeLocale(library_zip, NULL);
                        if (wlibrary_zip) {
                            status = PyWideStringList_Insert(
                                &config.module_search_paths, 0, wlibrary_zip);
                            PyMem_RawFree(wlibrary_zip);
                        } else
                            status = PyStatus_NoMemory();
                    }
                }
            } else {
                status = PyStatus_NoMemory();
            }
        }
    }
#endif

    // Read all configuration at once and initialize
    if (!PyStatus_Exception(status)) {
        status = PyConfig_Read(&config);
        if (!PyStatus_Exception(status)) {
            status = Py_InitializeFromConfig(&config);
        }
    }

#ifdef MS_WINDOWS
    if (!PyStatus_Exception(status)) {
        status = PostInitializePython(platlib);
    }
#endif

    // release
    PyConfig_Clear(&config);
    PyMem_RawFree(program_name);
    PyMem_RawFree(prefix);
    PyMem_RawFree(platlib);
    PyMem_RawFree(library_zip);
    return status;
}

//-----------------------------------------------------------------------------
// ExecuteScript()
//   Execute the startup script.
//-----------------------------------------------------------------------------
int ExecuteScript(void)
{
    PyObject *module, *func = NULL, *result = NULL;

    module = PyImport_ImportModule("__startup__");
    if (!module)
        return FatalScriptError();

    // __startup__.init()
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

    // __startup__.run()
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
