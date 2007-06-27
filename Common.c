//-----------------------------------------------------------------------------
// Common.c
//   Routines which are common to running frozen executables.
//-----------------------------------------------------------------------------

#include <compile.h>
#include <eval.h>
#include <osdefs.h>

//-----------------------------------------------------------------------------
// ExecuteScript()
//   Execute the script found within the file.
//-----------------------------------------------------------------------------
static int ExecuteScript(
    const char *fileName)		// name of file containing Python code
{
    PyObject *module, *importer, *code, *dict, *pathList, *temp;
    char dirName[MAXPATHLEN + 1];
    int result;
    size_t i;

#ifdef __WIN32__
    char dllName[MAXPATHLEN + 1];
    HMODULE handle;

    // set the attribute sys.dllname on Windows so that FreezePython can know
    // which DLL needs to be copied without requiring the presence of the
    // win32api module
    temp = PySys_GetObject("dllhandle");
    if (!temp)
        return FatalError("cannot get dll handle");
    handle = (HMODULE) PyInt_AsLong(temp);
    Py_DECREF(temp);
    if (PyErr_Occurred())
        return FatalError("dll handle is not an integer");
    if (!GetModuleFileName(handle, dllName, sizeof(dllName)))
        return FatalError("cannot get name of Python DLL");
    temp = PyString_FromString(dllName);
    if (!temp)
        return FatalError("cannot get Python string for DLL name");
    PySys_SetObject("dllname", temp);
    Py_DECREF(temp);
    if (PyErr_Occurred())
        return FatalError("cannot set dll name in module sys");
#endif

    // calculate the directory in which the file is located
    strcpy(dirName, fileName);
    for (i = strlen(dirName); i > 0 && dirName[i] != SEP; --i);
    dirName[i] = '\0';

    // add the file to sys.path
    pathList = PySys_GetObject("path");
    if (!pathList)
        return FatalError("cannot acquire sys.path");
    temp = PyString_FromString(dirName);
    if (!temp)
        return FatalError("cannot create Python string for directory name");
    result = PyList_Insert(pathList, 0, temp);
    Py_DECREF(temp);
    if (result < 0)
        return FatalError("cannot insert directory name in sys.path");
    temp = PyString_FromString(fileName);
    if (!temp)
        return FatalError("cannot create Python string for file name");
    result = PyList_Insert(pathList, 0, temp);
    Py_DECREF(temp);
    if (result < 0)
        return FatalError("cannot insert file name in sys.path");

    // load and execute initscript
    module = PyImport_ImportModule("zipimport");
    if (!module)
        return FatalError("cannot import zipimport module");
    importer = PyObject_CallMethod(module, "zipimporter", "s", fileName);
    Py_DECREF(module);
    if (!importer)
        return FatalError("cannot get zipimporter instance");
    code = PyObject_CallMethod(importer, "get_code", "s", "cx_Freeze__init__");
    Py_DECREF(importer);
    if (!code)
        return FatalError("unable to locate initialization module");
    dict = PyDict_New();
    if (!dict)
        return FatalError("unable to create temporary dictionary");
    if (PyDict_SetItemString(dict, "__builtins__", PyEval_GetBuiltins()) < 0)
        return FatalError("unable to set builtins for initialization module");
    temp = PyEval_EvalCode( (PyCodeObject*) code, dict, dict);
    Py_DECREF(code);
    Py_DECREF(dict);
    if (!temp)
        return FatalScriptError();
    Py_DECREF(temp);

    return 0;
}

