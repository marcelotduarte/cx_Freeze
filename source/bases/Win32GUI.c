//-----------------------------------------------------------------------------
// Win32GUI.c
//   Main routine for frozen programs written for the Win32 GUI subsystem.
//-----------------------------------------------------------------------------

#include <Python.h>
#include <locale.h>
#include <windows.h>
#include <shlwapi.h>

// define PyInt_* macros for Python 3.x
#ifndef PyInt_Check
#define PyInt_Check             PyLong_Check
#define PyInt_AsLong            PyLong_AsLong
#endif


// define methods for manipulating strings
#if PY_MAJOR_VERSION >= 3
    #define cxString_Check              PyUnicode_Check
    #define cxString_Format             PyUnicode_Format
    #define cxString_FromAscii(str) \
        PyUnicode_DecodeASCII(str, strlen(str), NULL)
    #define cxString_Join               PyUnicode_Join
    #define cxSTR                       wchar_t
    #define cx__argv                    __wargv
    #define cxMain                      wWinMain
#else
    #define cxString_Check              PyString_Check
    #define cxString_Format             PyString_Format
    #define cxString_FromAscii(str)     PyString_FromString(str)
    #define cxString_Join               _PyString_Join
    #define cxSTR                       char
    #define cx__argv                    __argv
    #define cxMain                      WinMain
#endif


//-----------------------------------------------------------------------------
// FatalError()
//   Handle a fatal error.
//-----------------------------------------------------------------------------
static int FatalError(
    char *a_Message)                    // message to display
{
    MessageBoxA(NULL, a_Message, "cx_Freeze Fatal Error", MB_ICONERROR);
    Py_Finalize();
    return -1;
}


//-----------------------------------------------------------------------------
// DisplayMessageFromPythonObjects()
//   Display message from Python objects. The Python objects are expected to be
// of the correct type (Unicode for Python 3.x and string for Python 2.x). The
// method returns -1 as a convenience to the caller.
//-----------------------------------------------------------------------------
static int DisplayMessageFromPythonObjects(
    PyObject *caption,                  // caption
    PyObject *message)                  // message
{
#if PY_MAJOR_VERSION >= 3
    MessageBoxW(NULL, PyUnicode_AS_UNICODE(message),
            PyUnicode_AS_UNICODE(caption), MB_ICONERROR);
#else
    MessageBox(NULL, PyString_AS_STRING(message), PyString_AS_STRING(caption),
            MB_ICONERROR);
#endif
    return -1;
}


//-----------------------------------------------------------------------------
// ArgumentValue()
//   Return a suitable argument value by replacing NULL with Py_None.
//-----------------------------------------------------------------------------
static PyObject *ArgumentValue(
    PyObject *object)                   // argument to massage
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
    PyObject *origValue,                // exception value
    char *contextMessage)               // context message to display
{
    PyObject *contextMessageObj, *message, *format, *formatArgs, *caption;
    PyObject *type, *value, *traceback;

    // create caption and message objects
    PyErr_Fetch(&type, &value, &traceback);
    PyErr_NormalizeException(&type, &value, &traceback);
    contextMessageObj = cxString_FromAscii(contextMessage);
    if (!contextMessageObj)
        return FatalError("Cannot create context message string object.");
    format = cxString_FromAscii("%s\nException: %s\nOriginal Exception: %s");
    if (!format)
        return FatalError("Cannot create format string object.");
    formatArgs = PyTuple_New(3);
    if (!formatArgs)
        return FatalError("Cannot create format args tuple.");
    PyTuple_SET_ITEM(formatArgs, 0, ArgumentValue(contextMessageObj));
    PyTuple_SET_ITEM(formatArgs, 1, ArgumentValue(value));
    PyTuple_SET_ITEM(formatArgs, 2, ArgumentValue(origValue));
    message = cxString_Format(format, formatArgs);
    if (!message)
        return FatalError("Cannot format exception values.");
    caption = cxString_FromAscii("cx_Freeze: Python error in main script "
            "(traceback unavailable)");
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
    int exitCode = 0;

    PyErr_Fetch(&type, &value, &traceback);
    PyErr_NormalizeException(&type, &value, &traceback);
    caption = PyObject_GetAttrString(value, "caption");
    if (!caption || !cxString_Check(caption)) {
        PyErr_Clear();
        caption = cxString_FromAscii("cx_Freeze: Application Terminated");
        if (!caption)
            return FatalError("Cannot create caption string object.");
    }

    code = PyObject_GetAttrString(value, "code");
    if (!code)
        PyErr_Clear();
    else {
        value = code;
        if (value == Py_None)
            Py_Exit(0);
    }
    if (PyInt_Check(value))
        exitCode = PyInt_AsLong(value);
    else {
        message = PyObject_Str(value);
        if (!message)
            return FatalError("Cannot get string representation of messsage.");
        DisplayMessageFromPythonObjects(caption, message);
        exitCode = 1;
    }
    Py_Exit(exitCode);
    return -1;
}


//-----------------------------------------------------------------------------
// FatalScriptError()
//   Handle a fatal Python error with traceback.
//-----------------------------------------------------------------------------
static int FatalScriptError()
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
            return FatalPythonErrorNoTraceback(value,
                    "Error in sys.excepthook.");
        return -1;
    }

    // import the traceback module
    module = PyImport_ImportModule("traceback");
    if (!module)
        return FatalPythonErrorNoTraceback(value,
                "Cannot import traceback module.");

    // get the format_exception method
    method = PyObject_GetAttrString(module, "format_exception");
    if (!method)
        return FatalPythonErrorNoTraceback(value,
              "Cannot get format_exception method.");

    // call the format_exception method
    result = PyObject_CallObject(method, argsTuple);
    if (!result)
        return FatalPythonErrorNoTraceback(value,
                "Exception raised when calling format_exception.");

    // convert to string
    emptyString = cxString_FromAscii("");
    if (!emptyString)
        return FatalPythonErrorNoTraceback(value,
                "Cannot create empty string object.");
    message = cxString_Join(emptyString, result);
    if (!message)
        return FatalPythonErrorNoTraceback(value,
                "Cannot join exception strings.");

    // acquire caption
    caption = PyObject_GetAttrString(value, "caption");
    if (!caption || !cxString_Check(caption)) {
        PyErr_Clear();
        caption = cxString_FromAscii("cx_Freeze: Python error in main script");
        if (!caption)
            return FatalPythonErrorNoTraceback(value,
                    "Cannot create default caption string.");
    }

    // display message box
    return DisplayMessageFromPythonObjects(caption, message);
}


#include "Common.c"


//-----------------------------------------------------------------------------
// WinMain()
//   Main routine for the executable in Windows.
//-----------------------------------------------------------------------------
int WINAPI cxMain(
    HINSTANCE instance,                 // handle to application
    HINSTANCE prevInstance,             // previous handle to application
    cxSTR *commandLine,                 // command line
    int showFlag)                       // show flag
{
    int status = 0;

    // initialize Python
    if (InitializePython(__argc, cx__argv) < 0)
        status = 1;

    // do the work
    if (status == 0 && ExecuteScript() < 0)
        status = 1;
    Py_Finalize();
    return status;
}

