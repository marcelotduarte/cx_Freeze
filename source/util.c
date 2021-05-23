//-----------------------------------------------------------------------------
// util.c
//   Shared library for use by cx_Freeze.
//-----------------------------------------------------------------------------

#define PY_SSIZE_T_CLEAN

#include <Python.h>
#ifdef MS_WINDOWS
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <imagehlp.h>
#include <Shlwapi.h>

#pragma pack(2)

typedef struct {
    BYTE bWidth;                        // Width, in pixels, of the image
    BYTE bHeight;                       // Height, in pixels, of the image
    BYTE bColorCount;                   // Number of colors in image
    BYTE bReserved;                     // Reserved ( must be 0)
    WORD wPlanes;                       // Color Planes
    WORD wBitCount;                     // Bits per pixel
    DWORD dwBytesInRes;                 // How many bytes in this resource?
    DWORD dwImageOffset;                // Where in the file is this image?
} ICONDIRENTRY;

typedef struct {
    WORD idReserved;                    // Reserved (must be 0)
    WORD idType;                        // Resource Type (1 for icons)
    WORD idCount;                       // How many images?
    ICONDIRENTRY idEntries[0];          // An entry for each image
} ICONDIR;

typedef struct {
    BYTE bWidth;                        // Width, in pixels, of the image
    BYTE bHeight;                       // Height, in pixels, of the image
    BYTE bColorCount;                   // Number of colors in image
    BYTE bReserved;                     // Reserved ( must be 0)
    WORD wPlanes;                       // Color Planes
    WORD wBitCount;                     // Bits per pixel
    DWORD dwBytesInRes;                 // How many bytes in this resource?
    WORD nID;                           // resource ID
} GRPICONDIRENTRY;

typedef struct {
    WORD idReserved;                    // Reserved (must be 0)
    WORD idType;                        // Resource Type (1 for icons)
    WORD idCount;                       // How many images?
    GRPICONDIRENTRY idEntries[0];       // An entry for each image
} GRPICONDIR;
#endif

//-----------------------------------------------------------------------------
// Globals
//-----------------------------------------------------------------------------
#ifdef MS_WINDOWS
static PyObject *g_BindErrorException = NULL;
static PyObject *g_ImageNames = NULL;
#endif

#ifdef MS_WINDOWS
//-----------------------------------------------------------------------------
// BindStatusRoutine()
//   Called by BindImageEx() at various points. This is used to determine the
// dependency tree which is later examined by cx_Freeze.
//-----------------------------------------------------------------------------
static BOOL __stdcall BindStatusRoutine(
    IMAGEHLP_STATUS_REASON reason,      // reason called
    PCSTR imageName,                    // name of image being examined
    PCSTR dllName,                      // name of DLL
    ULONG_PTR virtualAddress,           // computed virtual address
    ULONG_PTR parameter)                // parameter (value depends on reason)
{
    char imagePath[MAX_PATH + 1];
    char fileName[MAX_PATH + 1];

    switch (reason) {
        case BindImportModule:
            strcpy(imagePath, imageName);
            PathRemoveFileSpec(imagePath);
            if (!SearchPath(imagePath, dllName, NULL, sizeof(fileName),
                    fileName, NULL)) {
                if (!SearchPath(NULL, dllName, NULL, sizeof(fileName),
                        fileName, NULL))
                    return FALSE;
            }
            Py_INCREF(Py_None);
            if (PyDict_SetItemString(g_ImageNames, fileName, Py_None) < 0)
                return FALSE;
            break;
        default:
            break;
    }

    return TRUE;
}


//-----------------------------------------------------------------------------
// GetFileData()
//   Return the data for the given file.
//-----------------------------------------------------------------------------
static int GetFileData(
    LPCWSTR filename,                   // name of file to read
    char **data)                        // pointer to data (OUT)
{
    DWORD numberOfBytesRead, dataSize;
    HANDLE file;

    file = CreateFileW(filename, GENERIC_READ, FILE_SHARE_READ, NULL,
            OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (file == INVALID_HANDLE_VALUE)
        return -1;
    dataSize = GetFileSize(file, NULL);
    if (dataSize == INVALID_FILE_SIZE) {
        CloseHandle(file);
        return -1;
    }
    *data = PyMem_Malloc(dataSize);
    if (!*data) {
        CloseHandle(file);
        return -1;
    }
    if (!ReadFile(file, *data, dataSize, &numberOfBytesRead, NULL)) {
        CloseHandle(file);
        return -1;
    }
    CloseHandle(file);
    return 0;
}


//-----------------------------------------------------------------------------
// CreateGroupIconResource()
//   Return the group icon resource given the icon file data.
//-----------------------------------------------------------------------------
static GRPICONDIR *CreateGroupIconResource(
    ICONDIR *iconDir,                   // icon information
    DWORD *resourceSize)                // size of resource (OUT)
{
    GRPICONDIR *groupIconDir;
    int i;

    *resourceSize = sizeof(GRPICONDIR) +
            sizeof(GRPICONDIRENTRY) * iconDir->idCount;
    groupIconDir = PyMem_Malloc(*resourceSize);
    if (!groupIconDir)
        return NULL;
    groupIconDir->idReserved = iconDir->idReserved;
    groupIconDir->idType = iconDir->idType;
    groupIconDir->idCount = iconDir->idCount;
    for (i = 0; i < iconDir->idCount; i++) {
        groupIconDir->idEntries[i].bWidth = iconDir->idEntries[i].bWidth;
        groupIconDir->idEntries[i].bHeight = iconDir->idEntries[i].bHeight;
        groupIconDir->idEntries[i].bColorCount =
                iconDir->idEntries[i].bColorCount;
        groupIconDir->idEntries[i].bReserved = iconDir->idEntries[i].bReserved;
        groupIconDir->idEntries[i].wPlanes = iconDir->idEntries[i].wPlanes;
        groupIconDir->idEntries[i].wBitCount = iconDir->idEntries[i].wBitCount;
        groupIconDir->idEntries[i].dwBytesInRes =
                iconDir->idEntries[i].dwBytesInRes;
        groupIconDir->idEntries[i].nID = i + 1;
    }

    return groupIconDir;
}


//-----------------------------------------------------------------------------
// ExtAddIcon()
//   Add the icon as a resource to the specified file.
//-----------------------------------------------------------------------------
static PyObject *ExtAddIcon(
    PyObject *self,                     // passthrough argument
    PyObject *args)                     // arguments
{
    char *data, *iconData;
    PyObject *executable, *icon;
    LPWSTR executableName, iconName;
    GRPICONDIR *groupIconDir;
    DWORD resourceSize;
    ICONDIR *iconDir;
    BOOL succeeded;
    HANDLE handle;
    int i;

    succeeded = TRUE;
    handle = NULL;
    data = NULL;
    groupIconDir = NULL;
    executableName = NULL;
    iconName = NULL;

    if (!PyArg_ParseTuple(args, "UU", &executable, &icon)) {
        succeeded = FALSE;
        PyErr_Format(
            PyExc_RuntimeError, "Invalid parameters."
        );
    }

    if (succeeded) {
        executableName = (LPWSTR)PyUnicode_AsWideCharString(executable, NULL);
        iconName = (LPWSTR)PyUnicode_AsWideCharString(icon, NULL);
        if (!executableName || !iconName) {
            succeeded = FALSE;
            PyErr_NoMemory();
        }
    }

    // begin updating the executable
    if (succeeded) {
        handle = BeginUpdateResourceW(executableName, FALSE);
        if (!handle) {
            succeeded = FALSE;
            PyErr_SetExcFromWindowsErrWithFilenameObject(
                PyExc_WindowsError, GetLastError(), executable
            );
        }
    }

    // first attempt to get the data from the icon file
    if (succeeded) {
        if (GetFileData(iconName, &data) < 0)
            succeeded = FALSE;
    }

    // check for valid icon
    if (succeeded) {
        iconDir = (ICONDIR*) data;
        if (iconDir->idType != 1) {
            PyErr_Format(
                PyExc_RuntimeError, "Icon filename '%S' has invalid type.", icon
            );
            succeeded = FALSE;
        }
    }

    // next, attempt to add a group icon resource
    if (succeeded) {
        groupIconDir = CreateGroupIconResource(iconDir, &resourceSize);
        if (groupIconDir)
            succeeded = UpdateResource(handle, RT_GROUP_ICON,
                    MAKEINTRESOURCE(1),
                    MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL),
                    groupIconDir, resourceSize);
        else succeeded = FALSE;
    }

    // next, add each icon as a resource
    if (succeeded) {
        for (i = 0; i < iconDir->idCount; i++) {
            iconData = &data[iconDir->idEntries[i].dwImageOffset];
            resourceSize = iconDir->idEntries[i].dwBytesInRes;
            succeeded = UpdateResource(handle, RT_ICON,
                    MAKEINTRESOURCE(i + 1),
                    MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL), iconData,
                    resourceSize);
            if (!succeeded)
                break;
        }
    }

    // finish writing the resource (or discarding the changes upon an error)
    if (handle) {
        if (!EndUpdateResourceW(handle, !succeeded)) {
            if (succeeded) {
                succeeded = FALSE;
                PyErr_SetExcFromWindowsErrWithFilenameObject(
                    PyExc_WindowsError, GetLastError(), executable
                );
            }
        }
    }

    // clean up
    if (executableName)
        PyMem_Free(executableName);
    if (iconName)
        PyMem_Free(iconName);
    if (groupIconDir)
        PyMem_Free(groupIconDir);
    if (data)
        PyMem_Free(data);
    if (!succeeded)
        return NULL;

    Py_INCREF(Py_None);
    return Py_None;
}


//-----------------------------------------------------------------------------
// ExtBeginUpdateResource()
//   Wrapper for BeginUpdateResource().
//-----------------------------------------------------------------------------
static PyObject *ExtBeginUpdateResource(
    PyObject *self,                     // passthrough argument
    PyObject *args)                     // arguments
{
    BOOL deleteExistingResources;
    char *fileName;
    HANDLE handle;

    deleteExistingResources = TRUE;
    if (!PyArg_ParseTuple(args, "s|i", &fileName, &deleteExistingResources))
        return NULL;
    handle = BeginUpdateResource(fileName, deleteExistingResources);
    if (!handle) {
        PyErr_SetExcFromWindowsErrWithFilename(PyExc_WindowsError,
                GetLastError(), fileName);
        return NULL;
    }
    return PyLong_FromLongLong(handle);
}


//-----------------------------------------------------------------------------
// ExtUpdateResource()
//   Wrapper for UpdateResource().
//-----------------------------------------------------------------------------
static PyObject *ExtUpdateResource(
    PyObject *self,                     // passthrough argument
    PyObject *args)                     // arguments
{
    int resourceType, resourceId, resourceDataSize;
    char *resourceData;
    HANDLE handle;

    if (!PyArg_ParseTuple(args, "iiis#", &handle, &resourceType, &resourceId,
            &resourceData, &resourceDataSize))
        return NULL;
    if (!UpdateResource(handle, MAKEINTRESOURCE(resourceType),
            MAKEINTRESOURCE(resourceId),
            MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL), resourceData,
            resourceDataSize)) {
        PyErr_SetExcFromWindowsErr(PyExc_WindowsError, GetLastError());
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}


//-----------------------------------------------------------------------------
// ExtEndUpdateResource()
//   Wrapper for EndUpdateResource().
//-----------------------------------------------------------------------------
static PyObject *ExtEndUpdateResource(
    PyObject *self,                     // passthrough argument
    PyObject *args)                     // arguments
{
    BOOL discardChanges;
    HANDLE handle;

    discardChanges = FALSE;
    if (!PyArg_ParseTuple(args, "i|i", &handle, &discardChanges))
        return NULL;
    if (!EndUpdateResource(handle, discardChanges)) {
        PyErr_SetExcFromWindowsErr(PyExc_WindowsError, GetLastError());
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}


//-----------------------------------------------------------------------------
// ExtGetDependentFiles()
//   Return a list of files that this file depends on.
//-----------------------------------------------------------------------------
static PyObject *ExtGetDependentFiles(
    PyObject *self,                     // passthrough argument
    PyObject *args)                     // arguments
{
    PyObject *results;
    char *imageName;

    if (!PyArg_ParseTuple(args, "s", &imageName))
        return NULL;
    g_ImageNames = PyDict_New();
    if (!g_ImageNames)
        return NULL;
    if (!BindImageEx(BIND_NO_BOUND_IMPORTS | BIND_NO_UPDATE | BIND_ALL_IMAGES,
                imageName, NULL, NULL, BindStatusRoutine)) {
        Py_DECREF(g_ImageNames);
        PyErr_SetExcFromWindowsErrWithFilename(g_BindErrorException,
                GetLastError(), imageName);
        return NULL;
    }
    results = PyDict_Keys(g_ImageNames);
    Py_DECREF(g_ImageNames);
    return results;
}


//-----------------------------------------------------------------------------
// ExtGetSystemDir()
//   Return the Windows system directory (C:\Windows\system for example).
//-----------------------------------------------------------------------------
static PyObject *ExtGetSystemDir(
    PyObject *self,                     // passthrough argument
    PyObject *args)                     // arguments (ignored)
{
    OLECHAR dir[MAX_PATH + 1];
    if (GetSystemDirectoryW(dir, sizeof(dir)))
        return PyUnicode_FromWideChar(dir, -1);
    PyErr_SetExcFromWindowsErr(PyExc_RuntimeError, GetLastError());
    return NULL;
}


//-----------------------------------------------------------------------------
// ExtGetWindowsDir()
//   Return the Windows directory (C:\Windows for example).
//-----------------------------------------------------------------------------
static PyObject *ExtGetWindowsDir(
    PyObject *self,                     // passthrough argument
    PyObject *args)                     // arguments (ignored)
{
    OLECHAR dir[MAX_PATH + 1];
    if (GetWindowsDirectoryW(dir, sizeof(dir)))
        return PyUnicode_FromWideChar(dir, -1);
    PyErr_SetExcFromWindowsErr(PyExc_RuntimeError, GetLastError());
    return NULL;
}
#endif


//-----------------------------------------------------------------------------
// ExtUpdateCheckSum()
//   Update the CheckSum into the specified executable.
//-----------------------------------------------------------------------------
static PyObject *ExtUpdateCheckSum(
    PyObject *self,                     // passthrough argument
    PyObject *args)                     // arguments
{
    PyObject *executable, *results, *value;
    wchar_t *filename;
    HANDLE fhandle, fmap = NULL;
    PVOID mmap = NULL;
    DWORD filesize, header_sum, check_sum, last_error = 0;
    PIMAGE_NT_HEADERS headers;
    BOOL succeeded = TRUE;

    if (!PyArg_ParseTuple(args, "U", &executable)) {
        PyErr_Format(
            PyExc_RuntimeError, "Invalid parameter."
        );
        return NULL;
    }

    filename = PyUnicode_AsWideCharString(executable, NULL);
    if (!filename) {
        return PyErr_NoMemory();
    }

    fhandle = CreateFileW((LPWSTR) filename,
                          GENERIC_READ | GENERIC_WRITE,
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
        fmap = CreateFileMapping(fhandle, NULL, PAGE_READWRITE, 0, 0, NULL);
        if (!fmap) {
            succeeded = FALSE;
            last_error = GetLastError();
        }
    }
    if (succeeded) {
        mmap = MapViewOfFile(fmap, FILE_MAP_WRITE, 0, 0, 0);
        if (mmap == NULL) {
            succeeded = FALSE;
            last_error = GetLastError();
        }
    }
    if (succeeded) {
        headers = CheckSumMappedFile(mmap, filesize, &header_sum, &check_sum);
        if (headers == NULL) {
            succeeded = FALSE;
            last_error = GetLastError();
        } else if (header_sum != 0 && header_sum != check_sum) {
            headers->OptionalHeader.CheckSum = check_sum;
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
            PyExc_WindowsError, last_error, executable
        );
        return NULL;
    }

    // return a Tuple[int, int] (so we can check the values)
    results = PyTuple_New(2);
    if (results) {
        value = PyLong_FromLong(header_sum);
        if (value)
            PyTuple_SET_ITEM(results, 0, value);
        value = PyLong_FromLong(check_sum);
        if (value)
            PyTuple_SET_ITEM(results, 1, value);
        return results;
    }
    Py_INCREF(Py_None);
    return Py_None;
}


//-----------------------------------------------------------------------------
// Methods
//-----------------------------------------------------------------------------
static PyMethodDef g_ModuleMethods[] = {
#ifdef MS_WINDOWS
    { "BeginUpdateResource", ExtBeginUpdateResource, METH_VARARGS },
    { "UpdateResource", ExtUpdateResource, METH_VARARGS },
    { "EndUpdateResource", ExtEndUpdateResource, METH_VARARGS },
    { "AddIcon", ExtAddIcon, METH_VARARGS },
    { "GetDependentFiles", ExtGetDependentFiles, METH_VARARGS },
    { "GetSystemDir", ExtGetSystemDir, METH_NOARGS },
    { "GetWindowsDir", ExtGetWindowsDir, METH_NOARGS },
    { "UpdateCheckSum", ExtUpdateCheckSum, METH_VARARGS },
#endif
    { NULL }
};


//-----------------------------------------------------------------------------
//   Declaration of module definition for Python 3.x.
//-----------------------------------------------------------------------------
static struct PyModuleDef g_ModuleDef = {
    PyModuleDef_HEAD_INIT,
    "cx_Freeze.util",
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
PyMODINIT_FUNC PyInit_util(void)
{
    PyObject *module;

    module = PyModule_Create(&g_ModuleDef);
    if (!module)
        return NULL;
#ifdef MS_WINDOWS
    g_BindErrorException = PyErr_NewException("cx_Freeze.util.BindError",
            NULL, NULL);
    if (!g_BindErrorException)
        return NULL;
    if (PyModule_AddObject(module, "BindError", g_BindErrorException) < 0)
        return NULL;
#endif
    return module;
}
