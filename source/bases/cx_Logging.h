//-----------------------------------------------------------------------------
// cx_Logging.h
//   Include file for managing logging.
//-----------------------------------------------------------------------------

#include <Python.h>
#include <osdefs.h>

// define platform specific variables
#ifdef MS_WINDOWS
    #include <windows.h>
    #define LOCK_TYPE CRITICAL_SECTION
    #ifdef __GNUC__
        #ifdef CX_LOGGING_CORE
            #define CX_LOGGING_API(t) __declspec(dllexport) __stdcall t
        #else
            #define CX_LOGGING_API(t) __declspec(dllimport) __stdcall t
        #endif
    #else
        #ifdef CX_LOGGING_CORE
            #define CX_LOGGING_API(t) __declspec(dllexport) t __stdcall
        #else
            #define CX_LOGGING_API(t) __declspec(dllimport) t __stdcall
        #endif
    #endif
#else
    #include <pthread.h>
    #include <semaphore.h>
    #define LOCK_TYPE sem_t
    #define CX_LOGGING_API(t) t
#endif

// define structure for managing exception information
typedef struct {
    char message[MAXPATHLEN + 1024];
} ExceptionInfo;


// define structure for managing logging state
typedef struct {
    FILE *fp;
    char *fileName;
    char *fileNameMask;
    char *prefix;
    unsigned long level;
    unsigned long maxFiles;
    unsigned long maxFileSize;
    unsigned long seqNum;
    int reuseExistingFiles;
    int rotateFiles;
    int fileOwned;
    ExceptionInfo exceptionInfo;
} LoggingState;


// define structure for managing logging state for Python
typedef struct {
    PyObject_HEAD
    LoggingState *state;
    LOCK_TYPE lock;
} udt_LoggingState;


// define logging levels
#define LOG_LEVEL_DEBUG                 10
#define LOG_LEVEL_INFO                  20
#define LOG_LEVEL_WARNING               30
#define LOG_LEVEL_ERROR                 40
#define LOG_LEVEL_CRITICAL              50
#define LOG_LEVEL_NONE                  100


// define defaults
#define DEFAULT_MAX_FILE_SIZE           1024 * 1024
#define DEFAULT_PREFIX                  "%t"


// declarations of methods exported
CX_LOGGING_API(int) StartLogging(const char*, unsigned long, unsigned long,
        unsigned long, const char *);
CX_LOGGING_API(int) StartLoggingEx(const char*, unsigned long, unsigned long,
        unsigned long, const char *, int, int, ExceptionInfo*);
CX_LOGGING_API(int) StartLoggingForPythonThread(const char*, unsigned long,
        unsigned long, unsigned long, const char *);
CX_LOGGING_API(int) StartLoggingForPythonThreadEx(const char*, unsigned long,
        unsigned long, unsigned long, const char *, int, int);
CX_LOGGING_API(int) StartLoggingStderr(unsigned long, const char *);
CX_LOGGING_API(int) StartLoggingStderrEx(unsigned long, const char *,
        ExceptionInfo*);
CX_LOGGING_API(int) StartLoggingStdout(unsigned long, const char *);
CX_LOGGING_API(int) StartLoggingStdoutEx(unsigned long, const char *,
        ExceptionInfo*);
CX_LOGGING_API(int) StartLoggingFromEnvironment(void);
CX_LOGGING_API(void) StopLogging(void);
CX_LOGGING_API(void) StopLoggingForPythonThread(void);
CX_LOGGING_API(int) LogMessage(unsigned long, const char*);
CX_LOGGING_API(int) LogMessageV(unsigned long, const char*, ...);
CX_LOGGING_API(int) LogMessageVaList(unsigned long, const char*, va_list);
CX_LOGGING_API(int) LogMessageForPythonV(unsigned long, const char*, ...);
CX_LOGGING_API(int) WriteMessageForPython(unsigned long, PyObject*);
CX_LOGGING_API(int) LogDebug(const char*);
CX_LOGGING_API(int) LogInfo(const char*);
CX_LOGGING_API(int) LogWarning(const char*);
CX_LOGGING_API(int) LogError(const char*);
CX_LOGGING_API(int) LogCritical(const char*);
CX_LOGGING_API(int) LogTrace(const char*);
CX_LOGGING_API(unsigned long) GetLoggingLevel(void);
CX_LOGGING_API(int) SetLoggingLevel(unsigned long);
CX_LOGGING_API(int) LogPythonObject(unsigned long, const char*, const char*,
        PyObject*);
CX_LOGGING_API(int) LogPythonException(const char*);
CX_LOGGING_API(int) LogPythonExceptionWithTraceback(const char*, PyObject*,
        PyObject*, PyObject*);
CX_LOGGING_API(int) LogConfiguredException(PyObject*, const char*);
CX_LOGGING_API(udt_LoggingState*) GetLoggingState(void);
CX_LOGGING_API(int) SetLoggingState(udt_LoggingState*);
CX_LOGGING_API(int) IsLoggingStarted(void);
CX_LOGGING_API(int) IsLoggingAtLevelForPython(unsigned long);

#if defined MS_WINDOWS && !defined UNDER_CE
CX_LOGGING_API(int) LogWin32Error(DWORD, const char*);
CX_LOGGING_API(int) LogGUID(unsigned long, const char*, const IID*);
#endif

#ifdef MS_WINDOWS
CX_LOGGING_API(int) StartLoggingW(const OLECHAR*, unsigned long, unsigned long,
        unsigned long, const OLECHAR*);
CX_LOGGING_API(int) StartLoggingExW(const OLECHAR*, unsigned long,
        unsigned long, unsigned long, const OLECHAR*, int, int,
        ExceptionInfo*);
CX_LOGGING_API(int) LogMessageW(unsigned long, const OLECHAR*);
CX_LOGGING_API(int) LogDebugW(const OLECHAR*);
CX_LOGGING_API(int) LogInfoW(const OLECHAR*);
CX_LOGGING_API(int) LogWarningW(const OLECHAR*);
CX_LOGGING_API(int) LogErrorW(const OLECHAR*);
CX_LOGGING_API(int) LogCriticalW(const OLECHAR*);
CX_LOGGING_API(int) LogTraceW(const OLECHAR*);
#endif
