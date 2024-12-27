//-----------------------------------------------------------------------------
// Win32GUI.c
//   Main routine for frozen programs written for the Win32 GUI subsystem.
//-----------------------------------------------------------------------------

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include "pythoncapi_compat.h"

extern PyStatus InitializePython(int argc, wchar_t** argv);
extern int ExecuteScript(void);

//-----------------------------------------------------------------------------
// FatalError()
//   Handle a fatal error.
//-----------------------------------------------------------------------------
static int FatalError(const char* err_msg)
{
    MessageBoxA(NULL, err_msg, "cx_Freeze Fatal Error", MB_ICONERROR);
    Py_Finalize();
    return -1;
}

//-----------------------------------------------------------------------------
// DisplayMessageFromPythonObjects()
//   Display message from Python objects. Returns -1 as a convenience to the
// caller.
//-----------------------------------------------------------------------------
static int DisplayMessageFromPythonObjects(
    PyObject* caption, PyObject* message)
{
    wchar_t *wcaption, *wmessage;
    wcaption = PyUnicode_AsWideCharString(caption, NULL);
    wmessage = PyUnicode_AsWideCharString(message, NULL);
    MessageBoxW(NULL, wmessage, wcaption, MB_ICONERROR);
    PyMem_Free(wcaption);
    PyMem_Free(wmessage);
    return -1;
}

//-----------------------------------------------------------------------------
// ArgumentValue()
//   Return a suitable argument value by replacing NULL with Py_None.
//-----------------------------------------------------------------------------
static PyObject* ArgumentValue(PyObject* object)
{
    if (object) {
        Py_INCREF(object);
        return object;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

//-----------------------------------------------------------------------------
// FatalPythonErrorNoTraceback()
//   Handle a fatal Python error without traceback.
//-----------------------------------------------------------------------------
static int FatalPythonErrorNoTraceback(
    PyObject* origValue, char* contextMessage)
{
    PyObject *contextMessageObj, *message, *format, *formatArgs, *caption;
    PyObject *type, *value, *traceback;

    // create caption and message objects
    PyErr_Fetch(&type, &value, &traceback);
    PyErr_NormalizeException(&type, &value, &traceback);
    contextMessageObj = PyUnicode_FromString(contextMessage);
    if (!contextMessageObj)
        return FatalError("Cannot create context message string object.");
    format = PyUnicode_FromString("%s\nException: %s\nOriginal Exception: %s");
    if (!format)
        return FatalError("Cannot create format string object.");
    formatArgs = PyTuple_New(3);
    if (!formatArgs)
        return FatalError("Cannot create format args tuple.");
    PyTuple_SET_ITEM(formatArgs, 0, ArgumentValue(contextMessageObj));
    PyTuple_SET_ITEM(formatArgs, 1, ArgumentValue(value));
    PyTuple_SET_ITEM(formatArgs, 2, ArgumentValue(origValue));
    message = PyUnicode_Format(format, formatArgs);
    if (!message)
        return FatalError("Cannot format exception values.");
    caption = PyUnicode_FromString(
        "cx_Freeze: Python error in main script (traceback unavailable)");
    if (!caption)
        return FatalError("Cannot create caption string object.");

    // display message box
    return DisplayMessageFromPythonObjects(caption, message);
}

//-----------------------------------------------------------------------------
// HandleSystemExitException()
//   Handles a system exit exception differently. If an integer value is passed
// through then that becomes the exit value; otherwise the string value of the
// value passed through is displayed in a message box.
//-----------------------------------------------------------------------------
static int HandleSystemExitException()
{
    PyObject *caption, *message, *type, *value, *traceback, *code;
    int exitcode = 0;

    PyErr_Fetch(&type, &value, &traceback);
    PyErr_NormalizeException(&type, &value, &traceback);
    caption = PyObject_GetAttrString(value, "caption");
    if (!caption || !PyUnicode_Check(caption)) {
        PyErr_Clear();
        caption = PyUnicode_FromString("cx_Freeze: Application Terminated");
        if (!caption)
            return FatalError("Cannot create caption string object.");
    }

    code = PyObject_GetAttrString(value, "code");
    if (!code)
        PyErr_Clear();
    else {
        value = code;
        if (Py_IsNone(value))
            Py_Exit(0);
    }
    if (PyLong_Check(value))
        exitcode = PyLong_AsLong(value);
    else {
        message = PyObject_Str(value);
        if (!message)
            return FatalError("Cannot get string representation of messsage.");
        DisplayMessageFromPythonObjects(caption, message);
        exitcode = 1;
    }
    Py_Exit(exitcode);
    return -1;
}

//-----------------------------------------------------------------------------
// FatalScriptError()
//   Handle a fatal Python error with traceback.
//-----------------------------------------------------------------------------
int FatalScriptError()
{
    PyObject *type, *value, *traceback, *argsTuple, *module, *method, *result;
    PyObject *caption, *hook, *origHook, *emptyString, *message;

    // if a system exception, handle it specially
    if (PyErr_ExceptionMatches(PyExc_SystemExit))
        return HandleSystemExitException();

    // get the exception details
    PyErr_Fetch(&type, &value, &traceback);
    PyErr_NormalizeException(&type, &value, &traceback);
    argsTuple = PyTuple_New(3);
    if (!argsTuple)
        return FatalPythonErrorNoTraceback(value, "Cannot create args tuple.");
    PyTuple_SET_ITEM(argsTuple, 0, ArgumentValue(type));
    PyTuple_SET_ITEM(argsTuple, 1, ArgumentValue(value));
    PyTuple_SET_ITEM(argsTuple, 2, ArgumentValue(traceback));

    // call the exception hook
    hook = PySys_GetObject("excepthook");
    origHook = PySys_GetObject("__excepthook__");
    if (hook && hook != origHook) {
        result = PyObject_CallObject(hook, argsTuple);
        if (!result)
            return FatalPythonErrorNoTraceback(
                value, "Error in sys.excepthook.");
        return -1;
    }

    // import the traceback module
    module = PyImport_ImportModule("traceback");
    if (!module)
        return FatalPythonErrorNoTraceback(
            value, "Cannot import traceback module.");

    // get the format_exception method
    method = PyObject_GetAttrString(module, "format_exception");
    if (!method)
        return FatalPythonErrorNoTraceback(
            value, "Cannot get format_exception method.");

    // call the format_exception method
    result = PyObject_CallObject(method, argsTuple);
    if (!result)
        return FatalPythonErrorNoTraceback(
            value, "Exception raised when calling format_exception.");

    // convert to string
    emptyString = PyUnicode_FromString("");
    if (!emptyString)
        return FatalPythonErrorNoTraceback(
            value, "Cannot create empty string object.");
    message = PyUnicode_Join(emptyString, result);
    if (!message)
        return FatalPythonErrorNoTraceback(
            value, "Cannot join exception strings.");

    // acquire caption
    caption = PyObject_GetAttrString(value, "caption");
    if (!caption || !PyUnicode_Check(caption)) {
        PyErr_Clear();
        caption
            = PyUnicode_FromString("cx_Freeze: Python error in main script");
        if (!caption)
            return FatalPythonErrorNoTraceback(
                value, "Cannot create default caption string.");
    }

    // display message box
    return DisplayMessageFromPythonObjects(caption, message);
}

//-----------------------------------------------------------------------------
// WinMain()
//   Main routine for the executable in Windows.
//-----------------------------------------------------------------------------
int WINAPI wWinMain(HINSTANCE instance, HINSTANCE prevInstance,
    wchar_t* commandLine, int showFlag)
{
    PyStatus status;
    int exitcode;

    // initialize Python
    status = InitializePython(__argc, __wargv);
    if (PyStatus_Exception(status)) {
        FatalError(status.err_msg);
        Py_ExitStatusException(status);
    }

    // do the work
    exitcode = ExecuteScript();

    if (Py_FinalizeEx() < 0) {
        exitcode = 120;
    }
    return exitcode;
}
