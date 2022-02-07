This sample shows how to register a program as handling some file types on windows, using msi features, with minimal supplement of direct registry modifications.

There’s a single option to modify, with a list of dicts, one per file-type association, each comprised of:
1. a file type (extension without leading .)
2. an executable
3. a verb, e.g. “open”
4. optionally arguments, e.g. `"%1"` for proper quoting, but any other program arguments can be passed (see sample),
5. optionally a context menu display name for the association, defaults to `{program name} {verb}`
6. optionally a mime type associated with the extension

Building & installing the sample from this directory modifies the context menu for the specified extensions / file types `.log` and `.txt`:
- it primarily adds an entry the « Open With » submenu for these files,
- when the program is selected as default handler for the file type, it also modifies the top options of the context menu (one per verb for the extension)

The executable + argument are called with the file when an action is selected.

This works for all-users (`all_users=True` in bdist_msi options) as well as current-user installs.


---

Under the hood, cx_Freeze populates MSI tables: extension, verb, mime, progid, and slightly modifies components.

**Component**: Executables are bundled into separate `Component`s (with the executable as its `keyfile`), meaning 1 per directory + 1 per executable. There is a tiny risk of Component id clashes (if there are directories named `_cx_executable{N}_{executable base name}`).

**ProgId**: The `progId` are generated and as close as possible to [recommendations](https://docs.microsoft.com/en-us/windows/win32/shell/fa-progids), which are `[Vendor or Application].[Component].[Version]`.

Additionally, 2 types of registry keys are added, which are needed:
- `FriendlyAppName`: to set a display name other than the executable’s file name (`Hello Program` instead of `hello.exe` in the Open With submenu)
- `ApplicationCompany`: to have the application show directly in the « Open With » submenu rather than only in the « Choose another program » dialog from the « Open With » submenu.
