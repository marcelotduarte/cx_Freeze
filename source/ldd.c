//-----------------------------------------------------------------------------
// ldd.c
//   Shared library for use by cx_Freeze.
//-----------------------------------------------------------------------------

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <imagehlp.h>
#include <Shlwapi.h>

#define MakePtr( cast, ptr, addValue ) (cast)( (DWORD_PTR)(ptr) + (DWORD)(addValue))

//-----------------------------------------------------------------------------
// ExtGetDependentFiles()
//   Return a list of files that this file depends on.
//-----------------------------------------------------------------------------
static PyObject *ExtGetDependentFiles(
    PyObject *self,                     // passthrough argument
    PyObject *args)                     // arguments
{
    PyObject *path;
    wchar_t *filename;
    HANDLE fhandle, fmap = NULL;
    PVOID mmap = NULL;
    PIMAGE_DOS_HEADER dos_header;
    PIMAGE_NT_HEADERS headers = NULL;
    PIMAGE_OPTIONAL_HEADER opt_header;
    PIMAGE_IMPORT_DESCRIPTOR imp_desc;
    DWORD filesize, last_error = 0;
    BOOL succeeded = TRUE;

    if (!PyArg_ParseTuple(args, "O&", PyUnicode_FSDecoder, &path)) {
        PyErr_Format(PyExc_RuntimeError, "Invalid parameter.");
        return NULL;
    }

    filename = PyUnicode_AsWideCharString(path, NULL);
    if (!filename) {
        return PyErr_NoMemory();
    }

    fhandle = CreateFileW((LPCWSTR) filename,
                          GENERIC_READ,
                          FILE_SHARE_READ,
                          NULL,
                          OPEN_EXISTING,
                          FILE_ATTRIBUTE_NORMAL,
                          NULL);
    if (fhandle == INVALID_HANDLE_VALUE) {
        succeeded = FALSE;
        last_error = GetLastError();
    }
    if (succeeded) {
        filesize = GetFileSize(fhandle, NULL);
        if (filesize == INVALID_FILE_SIZE) {
            succeeded = FALSE;
            last_error = GetLastError();
        }
    }
    if (succeeded) {
        fmap = CreateFileMapping(fhandle, NULL, PAGE_READONLY, 0, 0, NULL);
        if (!fmap) {
            succeeded = FALSE;
            last_error = GetLastError();
        }
    }
    if (succeeded) {
        mmap = MapViewOfFile(fmap, FILE_MAP_READ, 0, 0, 0);
        if (mmap == NULL) {
            succeeded = FALSE;
            last_error = GetLastError();
        }
    }
    if (succeeded) {
        dos_header = (PIMAGE_DOS_HEADER) mmap;
        if (dos_header->e_magic == IMAGE_DOS_SIGNATURE) {
            headers = MakePtr(PIMAGE_NT_HEADERS, dos_header, dos_header->e_lfanew);
            if (headers) {
                opt_header = &headers->OptionalHeader;
                imp_desc = (PIMAGE_IMPORT_DESCRIPTOR) ((BYTE*)mmap + 
                    opt_header->DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress);
            }
        }
        if (headers == NULL) {
            succeeded = FALSE;
            last_error = GetLastError();
        }
    }

    // clean up
    if (mmap)
        UnmapViewOfFile(mmap);
    if (fmap)
        CloseHandle(fmap);
    if (fhandle)
        CloseHandle(fhandle);
    if (filename)
        PyMem_Free(filename);
    if (!succeeded) {
        PyErr_SetExcFromWindowsErrWithFilenameObject(
            PyExc_WindowsError, last_error, path
        );
        Py_DECREF(path);
        return NULL;
    }
    Py_DECREF(path);

    Py_INCREF(Py_None);
    return Py_None;
}


//-----------------------------------------------------------------------------
// Methods
//-----------------------------------------------------------------------------
static PyMethodDef g_ModuleMethods[] = {
    { "GetDependentFiles", ExtGetDependentFiles, METH_VARARGS },
    { NULL }
};


//-----------------------------------------------------------------------------
//   Declaration of module definition for Python 3.x.
//-----------------------------------------------------------------------------
static struct PyModuleDef g_ModuleDef = {
    PyModuleDef_HEAD_INIT,
    "cx_Freeze.ldd",
    NULL,
    -1,
    g_ModuleMethods,                       // methods
    NULL,                                  // m_reload
    NULL,                                  // traverse
    NULL,                                  // clear
    NULL                                   // free
};


//-----------------------------------------------------------------------------
// Entry point for the module.
//-----------------------------------------------------------------------------
PyMODINIT_FUNC PyInit_ldd(void)
{
    PyObject *module;

    module = PyModule_Create(&g_ModuleDef);
    if (!module)
        return NULL;
    /*
    g_BindErrorException = PyErr_NewException("cx_Freeze.util.BindError",
            NULL, NULL);
    if (!g_BindErrorException)
        return NULL;
    if (PyModule_AddObject(module, "BindError", g_BindErrorException) < 0)
        return NULL;
    */
    return module;
}
