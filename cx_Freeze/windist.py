import distutils.command.bdist_msi
from distutils import log
import importlib
import msilib
import os
import re
import shutil
import sysconfig

__all__ = ["bdist_msi"]

# force the remove existing products action to happen first since Windows
# installer appears to be braindead and doesn't handle files shared between
# different "products" very well
sequence = msilib.sequence.InstallExecuteSequence
for index, info in enumerate(sequence):
    if info[0] == "RemoveExistingProducts":
        sequence[index] = (info[0], info[1], 1450)


class bdist_msi(distutils.command.bdist_msi.bdist_msi):
    user_options = distutils.command.bdist_msi.bdist_msi.user_options + [
        ("add-to-path=", None, "add target dir to PATH environment variable"),
        ("upgrade-code=", None, "upgrade code to use"),
        ("initial-target-dir=", None, "initial target directory"),
        ("target-name=", None, "name of the file to create"),
        ("directories=", None, "list of 3-tuples of directories to create"),
        ("environment-variables=", None, "list of environment variables"),
        (
            "data=",
            None,
            "dictionary of data indexed by table name, and each value is a "
            "tuple to include in table",
        ),
        (
            "summary-data=",
            None,
            "Dictionary of data to include in msi summary data stream. "
            'Allowed keys are "author", "comments", "keywords".',
        ),
        ("product-code=", None, "product code to use"),
        ("install-icon=", None, "icon path to add/remove programs "),
        ("all-users=", None, "installation for all users (or just me)"),
        ("extensions=", None, "Extensions for which to register Verbs"),
    ]
    x = y = 50
    width = 370
    height = 300
    title = "[ProductName] Setup"
    modeless = 1
    modal = 3
    _binary_columns = {
        "Binary": 1,
        "Icon": 1,
        "Patch": 4,
        "SFPCatalog": 1,
        "MsiDigitalCertificate": 1,
        "MsiPatchHeaders": 1,
    }

    def add_config(self, fullname):
        if self.add_to_path:
            path = "Path"
            if self.all_users:
                path = "=-*" + path
            msilib.add_data(
                self.db,
                "Environment",
                [("E_PATH", path, r"[~];[TARGETDIR]", "TARGETDIR")],
            )
        if self.directories:
            msilib.add_data(self.db, "Directory", self.directories)
        if self.environment_variables:
            msilib.add_data(self.db, "Environment", self.environment_variables)
        # This is needed in case the AlwaysInstallElevated policy is set.
        # Otherwise installation will not end up in TARGETDIR.
        msilib.add_data(
            self.db,
            "Property",
            [("SecureCustomProperties", "TARGETDIR;REINSTALLMODE")],
        )
        msilib.add_data(
            self.db,
            "CustomAction",
            [
                (
                    "A_SET_TARGET_DIR",
                    256 + 51,
                    "TARGETDIR",
                    self.initial_target_dir,
                ),
                (
                    "A_SET_REINSTALL_MODE",
                    256 + 51,
                    "REINSTALLMODE",
                    "amus",
                ),
            ],
        )
        msilib.add_data(
            self.db,
            "InstallExecuteSequence",
            [
                ("A_SET_TARGET_DIR", 'TARGETDIR=""', 401),
                ("A_SET_REINSTALL_MODE", 'REINSTALLMODE=""', 402),
            ],
        )
        msilib.add_data(
            self.db,
            "InstallUISequence",
            [
                ("PrepareDlg", None, 140),
                ("A_SET_TARGET_DIR", 'TARGETDIR=""', 401),
                ("A_SET_REINSTALL_MODE", 'REINSTALLMODE=""', 402),
                ("SelectDirectoryDlg", "not Installed", 1230),
                (
                    "MaintenanceTypeDlg",
                    "Installed and not Resume and not Preselected",
                    1250,
                ),
                ("ProgressDlg", None, 1280),
            ],
        )
        for idx, executable in enumerate(self.distribution.executables):
            if (
                executable.shortcut_name is not None
                and executable.shortcut_dir is not None
            ):
                base_name = os.path.basename(executable.target_name)
                msilib.add_data(
                    self.db,
                    "Shortcut",
                    [
                        (
                            f"S_APP_{idx}",
                            str(executable.shortcut_dir),
                            executable.shortcut_name,
                            "TARGETDIR",
                            f"[TARGETDIR]{base_name}",
                            None,
                            None,
                            None,
                            None,
                            None,
                            None,
                            "TARGETDIR",
                        )
                    ],
                )
        for table_name, data in self.data.items():
            col = self._binary_columns.get(table_name)
            if col is not None:
                data = [
                    (*row[:col], msilib.Binary(row[col]), *row[col + 1 :])
                    for row in data
                ]
            msilib.add_data(self.db, table_name, data)

        # If provided, add data to MSI's summary information stream
        if len(self.summary_data) > 0:
            for k in self.summary_data:
                if k not in ["author", "comments", "keywords"]:
                    raise Exception(
                        f"Unknown key provided in summary-data: {k!r}"
                    )

            summary_info = self.db.GetSummaryInformation(5)
            if "author" in self.summary_data:
                summary_info.SetProperty(
                    msilib.PID_AUTHOR, self.summary_data["author"]
                )
            if "comments" in self.summary_data:
                summary_info.SetProperty(
                    msilib.PID_COMMENTS, self.summary_data["comments"]
                )
            if "keywords" in self.summary_data:
                summary_info.SetProperty(
                    msilib.PID_KEYWORDS, self.summary_data["keywords"]
                )
            summary_info.Persist()

    def add_cancel_dialog(self):
        dialog = msilib.Dialog(
            self.db,
            "CancelDlg",
            50,
            10,
            260,
            85,
            3,
            self.title,
            "No",
            "No",
            "No",
        )
        dialog.text(
            "Text",
            48,
            15,
            194,
            30,
            3,
            "Are you sure you want to cancel [ProductName] installation?",
        )
        button = dialog.pushbutton("Yes", 72, 57, 56, 17, 3, "Yes", "No")
        button.event("EndDialog", "Exit")
        button = dialog.pushbutton("No", 132, 57, 56, 17, 3, "No", "Yes")
        button.event("EndDialog", "Return")

    def add_error_dialog(self):
        dialog = msilib.Dialog(
            self.db,
            "ErrorDlg",
            50,
            10,
            330,
            101,
            65543,
            self.title,
            "ErrorText",
            None,
            None,
        )
        dialog.text("ErrorText", 50, 9, 280, 48, 3, "")
        for text, x in [
            ("No", 120),
            ("Yes", 240),
            ("Abort", 0),
            ("Cancel", 42),
            ("Ignore", 81),
            ("Ok", 159),
            ("Retry", 198),
        ]:
            button = dialog.pushbutton(text[0], x, 72, 81, 21, 3, text, None)
            button.event("EndDialog", f"Error{text}")

    def add_exit_dialog(self):
        dialog = distutils.command.bdist_msi.PyDialog(
            self.db,
            "ExitDialog",
            self.x,
            self.y,
            self.width,
            self.height,
            self.modal,
            self.title,
            "Finish",
            "Finish",
            "Finish",
        )
        dialog.title("Completing the [ProductName] installer")
        dialog.back("< Back", "Finish", active=False)
        dialog.cancel("Cancel", "Back", active=False)
        dialog.text(
            "Description",
            15,
            235,
            320,
            20,
            0x30003,
            "Click the Finish button to exit the installer.",
        )
        button = dialog.next("Finish", "Cancel", name="Finish")
        button.event("EndDialog", "Return")

    def add_fatal_error_dialog(self):
        dialog = distutils.command.bdist_msi.PyDialog(
            self.db,
            "FatalError",
            self.x,
            self.y,
            self.width,
            self.height,
            self.modal,
            self.title,
            "Finish",
            "Finish",
            "Finish",
        )
        dialog.title("[ProductName] installer ended prematurely")
        dialog.back("< Back", "Finish", active=False)
        dialog.cancel("Cancel", "Back", active=False)
        dialog.text(
            "Description1",
            15,
            70,
            320,
            80,
            0x30003,
            "[ProductName] setup ended prematurely because of an error. "
            "Your system has not been modified. To install this program "
            "at a later time, please run the installation again.",
        )
        dialog.text(
            "Description2",
            15,
            155,
            320,
            20,
            0x30003,
            "Click the Finish button to exit the installer.",
        )
        button = dialog.next("Finish", "Cancel", name="Finish")
        button.event("EndDialog", "Exit")

    def add_files(self):
        db = self.db
        cab = msilib.CAB("distfiles")
        feature = msilib.Feature(
            db,
            "default",
            "Default Feature",
            "Everything",
            1,
            directory="TARGETDIR",
        )
        feature.set_current()
        rootdir = os.path.abspath(self.bdist_dir)
        root = msilib.Directory(
            db, cab, None, rootdir, "TARGETDIR", "SourceDir"
        )
        db.Commit()
        todo = [root]
        while todo:
            directory = todo.pop()
            for file in os.listdir(directory.absolute):
                sep_comp = self.separate_components.get(
                    os.path.relpath(
                        os.path.join(directory.absolute, file),
                        self.bdist_dir,
                    )
                )
                if sep_comp is not None:
                    restore_component = directory.component
                    directory.start_component(
                        component=sep_comp,
                        flags=0,
                        feature=feature,
                        keyfile=file,
                    )
                    directory.add_file(file)
                    directory.component = restore_component
                elif os.path.isdir(os.path.join(directory.absolute, file)):
                    short_file = directory.make_short(file)
                    new_dir = msilib.Directory(
                        db, cab, directory, file, file, f"{short_file}|{file}"
                    )
                    todo.append(new_dir)
                else:
                    directory.add_file(file)
        cab.commit(db)

    def add_files_in_use_dialog(self):
        dialog = distutils.command.bdist_msi.PyDialog(
            self.db,
            "FilesInUse",
            self.x,
            self.y,
            self.width,
            self.height,
            19,
            self.title,
            "Retry",
            "Retry",
            "Retry",
            bitmap=False,
        )
        dialog.text(
            "Title", 15, 6, 200, 15, 0x30003, r"{\DlgFontBold8}Files in Use"
        )
        dialog.text(
            "Description",
            20,
            23,
            280,
            20,
            0x30003,
            "Some files that need to be updated are currently in use.",
        )
        dialog.text(
            "Text",
            20,
            55,
            330,
            50,
            3,
            "The following applications are using files that need to be "
            "updated by this setup. Close these applications and then "
            "click Retry to continue the installation or Cancel to exit it.",
        )
        dialog.control(
            "List",
            "ListBox",
            20,
            107,
            330,
            130,
            7,
            "FileInUseProcess",
            None,
            None,
            None,
        )
        button = dialog.back("Exit", "Ignore", name="Exit")
        button.event("EndDialog", "Exit")
        button = dialog.next("Ignore", "Retry", name="Ignore")
        button.event("EndDialog", "Ignore")
        button = dialog.cancel("Retry", "Exit", name="Retry")
        button.event("EndDialog", "Retry")

    def add_maintenance_type_dialog(self):
        dialog = distutils.command.bdist_msi.PyDialog(
            self.db,
            "MaintenanceTypeDlg",
            self.x,
            self.y,
            self.width,
            self.height,
            self.modal,
            self.title,
            "Next",
            "Next",
            "Cancel",
        )
        dialog.title("Welcome to the [ProductName] Setup Wizard")
        dialog.text(
            "BodyText",
            15,
            63,
            330,
            42,
            3,
            "Select whether you want to repair or remove [ProductName].",
        )
        group = dialog.radiogroup(
            "RepairRadioGroup",
            15,
            108,
            330,
            60,
            3,
            "MaintenanceForm_Action",
            "",
            "Next",
        )
        group.add("Repair", 0, 18, 300, 17, "&Repair [ProductName]")
        group.add("Remove", 0, 36, 300, 17, "Re&move [ProductName]")
        dialog.back("< Back", None, active=False)
        button = dialog.next("Finish", "Cancel")
        button.event(
            "[REINSTALL]", "ALL", 'MaintenanceForm_Action="Repair"', 5
        )
        button.event(
            "[Progress1]", "Repairing", 'MaintenanceForm_Action="Repair"', 6
        )
        button.event(
            "[Progress2]", "repairs", 'MaintenanceForm_Action="Repair"', 7
        )
        button.event("Reinstall", "ALL", 'MaintenanceForm_Action="Repair"', 8)
        button.event("[REMOVE]", "ALL", 'MaintenanceForm_Action="Remove"', 11)
        button.event(
            "[Progress1]", "Removing", 'MaintenanceForm_Action="Remove"', 12
        )
        button.event(
            "[Progress2]", "removes", 'MaintenanceForm_Action="Remove"', 13
        )
        button.event("Remove", "ALL", 'MaintenanceForm_Action="Remove"', 14)
        button.event(
            "EndDialog", "Return", 'MaintenanceForm_Action<>"Change"', 20
        )
        button = dialog.cancel("Cancel", "RepairRadioGroup")
        button.event("SpawnDialog", "CancelDlg")

    def add_prepare_dialog(self):
        dialog = distutils.command.bdist_msi.PyDialog(
            self.db,
            "PrepareDlg",
            self.x,
            self.y,
            self.width,
            self.height,
            self.modeless,
            self.title,
            "Cancel",
            "Cancel",
            "Cancel",
        )
        dialog.text(
            "Description",
            15,
            70,
            320,
            40,
            0x30003,
            "Please wait while the installer prepares to guide you through "
            "the installation.",
        )
        dialog.title("Welcome to the [ProductName] installer")
        text = dialog.text(
            "ActionText", 15, 110, 320, 20, 0x30003, "Pondering..."
        )
        text.mapping("ActionText", "Text")
        text = dialog.text("ActionData", 15, 135, 320, 30, 0x30003, None)
        text.mapping("ActionData", "Text")
        dialog.back("Back", None, active=False)
        dialog.next("Next", None, active=False)
        button = dialog.cancel("Cancel", None)
        button.event("SpawnDialog", "CancelDlg")

    def add_progress_dialog(self):
        dialog = distutils.command.bdist_msi.PyDialog(
            self.db,
            "ProgressDlg",
            self.x,
            self.y,
            self.width,
            self.height,
            self.modeless,
            self.title,
            "Cancel",
            "Cancel",
            "Cancel",
            bitmap=False,
        )
        dialog.text(
            "Title",
            20,
            15,
            200,
            15,
            0x30003,
            r"{\DlgFontBold8}[Progress1] [ProductName]",
        )
        dialog.text(
            "Text",
            35,
            65,
            300,
            30,
            3,
            "Please wait while the installer [Progress2] [ProductName].",
        )
        dialog.text("StatusLabel", 35, 100, 35, 20, 3, "Status:")
        text = dialog.text(
            "ActionText", 70, 100, self.width - 70, 20, 3, "Pondering..."
        )
        text.mapping("ActionText", "Text")
        control = dialog.control(
            "ProgressBar",
            "ProgressBar",
            35,
            120,
            300,
            10,
            65537,
            None,
            "Progress done",
            None,
            None,
        )
        control.mapping("SetProgress", "Progress")
        dialog.back("< Back", "Next", active=False)
        dialog.next("Next >", "Cancel", active=False)
        button = dialog.cancel("Cancel", "Back")
        button.event("SpawnDialog", "CancelDlg")

    def add_properties(self):
        metadata = self.distribution.metadata
        props = [
            ("DistVersion", metadata.get_version()),
            ("DefaultUIFont", "DlgFont8"),
            ("ErrorDialog", "ErrorDlg"),
            ("Progress1", "Install"),
            ("Progress2", "installs"),
            ("MaintenanceForm_Action", "Repair"),
            ("ALLUSERS", "2"),
        ]

        if not self.all_users:
            props.append(("MSIINSTALLPERUSER", "1"))
        email = metadata.author_email or metadata.maintainer_email
        if email:
            props.append(("ARPCONTACT", email))
        if metadata.url:
            props.append(("ARPURLINFOABOUT", metadata.url))
        if self.upgrade_code is not None:
            if not _is_valid_guid(self.upgrade_code):
                raise ValueError("upgrade-code must be in valid GUID format")
            props.append(("UpgradeCode", self.upgrade_code.upper()))
        if self.install_icon:
            props.append(("ARPPRODUCTICON", "InstallIcon"))
        msilib.add_data(self.db, "Property", props)
        if self.install_icon:
            msilib.add_data(
                self.db,
                "Icon",
                [("InstallIcon", msilib.Binary(self.install_icon))],
            )

    def add_select_directory_dialog(self):
        dialog = distutils.command.bdist_msi.PyDialog(
            self.db,
            "SelectDirectoryDlg",
            self.x,
            self.y,
            self.width,
            self.height,
            self.modal,
            self.title,
            "Next",
            "Next",
            "Cancel",
        )
        dialog.title("Select destination directory")
        dialog.back("< Back", None, active=False)
        button = dialog.next("Next >", "Cancel")
        button.event("SetTargetPath", "TARGETDIR", ordering=1)
        button.event("SpawnWaitDialog", "WaitForCostingDlg", ordering=2)
        button.event("EndDialog", "Return", ordering=3)
        button = dialog.cancel("Cancel", "DirectoryCombo")
        button.event("SpawnDialog", "CancelDlg")
        dialog.control(
            "DirectoryCombo",
            "DirectoryCombo",
            15,
            70,
            272,
            80,
            393219,
            "TARGETDIR",
            None,
            "DirectoryList",
            None,
        )
        dialog.control(
            "DirectoryList",
            "DirectoryList",
            15,
            90,
            308,
            136,
            3,
            "TARGETDIR",
            None,
            "PathEdit",
            None,
        )
        dialog.control(
            "PathEdit",
            "PathEdit",
            15,
            230,
            306,
            16,
            3,
            "TARGETDIR",
            None,
            "Next",
            None,
        )
        button = dialog.pushbutton("Up", 306, 70, 18, 18, 3, "Up", None)
        button.event("DirectoryListUp", "0")
        button = dialog.pushbutton("NewDir", 324, 70, 30, 18, 3, "New", None)
        button.event("DirectoryListNew", "0")

    def add_text_styles(self):
        msilib.add_data(
            self.db,
            "TextStyle",
            [
                ("DlgFont8", "Tahoma", 9, None, 0),
                ("DlgFontBold8", "Tahoma", 8, None, 1),
                ("VerdanaBold10", "Verdana", 10, None, 1),
                ("VerdanaRed9", "Verdana", 9, 255, 0),
            ],
        )

    def add_ui(self):
        self.add_text_styles()
        self.add_error_dialog()
        self.add_fatal_error_dialog()
        self.add_cancel_dialog()
        self.add_exit_dialog()
        self.add_user_exit_dialog()
        self.add_files_in_use_dialog()
        self.add_wait_for_costing_dialog()
        self.add_prepare_dialog()
        self.add_select_directory_dialog()
        self.add_progress_dialog()
        self.add_maintenance_type_dialog()

    def add_upgrade_config(self, sversion):
        if self.upgrade_code is not None:
            msilib.add_data(
                self.db,
                "Upgrade",
                [
                    (
                        self.upgrade_code,
                        None,
                        sversion,
                        None,
                        513,
                        None,
                        "REMOVEOLDVERSION",
                    ),
                    (
                        self.upgrade_code,
                        sversion,
                        None,
                        None,
                        257,
                        None,
                        "REMOVENEWVERSION",
                    ),
                ],
            )

    def add_user_exit_dialog(self):
        dialog = distutils.command.bdist_msi.PyDialog(
            self.db,
            "UserExit",
            self.x,
            self.y,
            self.width,
            self.height,
            self.modal,
            self.title,
            "Finish",
            "Finish",
            "Finish",
        )
        dialog.title("[ProductName] installer was interrupted")
        dialog.back("< Back", "Finish", active=False)
        dialog.cancel("Cancel", "Back", active=False)
        dialog.text(
            "Description1",
            15,
            70,
            320,
            80,
            0x30003,
            "[ProductName] setup was interrupted. Your system has not "
            "been modified. To install this program at a later time, "
            "please run the installation again.",
        )
        dialog.text(
            "Description2",
            15,
            155,
            320,
            20,
            0x30003,
            "Click the Finish button to exit the installer.",
        )
        button = dialog.next("Finish", "Cancel", name="Finish")
        button.event("EndDialog", "Exit")

    def add_wait_for_costing_dialog(self):
        dialog = msilib.Dialog(
            self.db,
            "WaitForCostingDlg",
            50,
            10,
            260,
            85,
            self.modal,
            self.title,
            "Return",
            "Return",
            "Return",
        )
        dialog.text(
            "Text",
            48,
            15,
            194,
            30,
            3,
            "Please wait while the installer finishes determining your "
            "disk space requirements.",
        )
        button = dialog.pushbutton(
            "Return", 102, 57, 56, 17, 3, "Return", None
        )
        button.event("EndDialog", "Exit")

    def _append_to_data(self, table, *line):
        rows = self.data.setdefault(table, [])
        line = tuple(line)
        if line not in rows:
            rows.append(line)

    def finalize_options(self):
        distutils.command.bdist_msi.bdist_msi.finalize_options(self)
        name = self.distribution.get_name()
        fullname = self.distribution.get_fullname()
        platform = sysconfig.get_platform().replace("win-amd64", "win64")
        if self.initial_target_dir is None:
            if platform == "win64" or platform.startswith("mingw_x86_64"):
                program_files_folder = "ProgramFiles64Folder"
            else:
                program_files_folder = "ProgramFilesFolder"
            self.initial_target_dir = fr"[{program_files_folder}]\{name}"
        if self.add_to_path is None:
            self.add_to_path = False
        if self.target_name is None:
            self.target_name = fullname
        if not self.target_name.lower().endswith(".msi"):
            self.target_name = f"{self.target_name}-{platform}.msi"
        if not os.path.isabs(self.target_name):
            self.target_name = os.path.join(self.dist_dir, self.target_name)
        if self.directories is None:
            self.directories = []
        if self.environment_variables is None:
            self.environment_variables = []
        if self.data is None:
            self.data = {}
        if not isinstance(self.summary_data, dict):
            self.summary_data = {}
        self.separate_components = {}
        for idx, executable in enumerate(self.distribution.executables):
            base_name = os.path.basename(executable.target_name)
            # Trying to make these names unique from any directory name
            self.separate_components[base_name] = msilib.make_id(
                f"_cx_executable{idx}_{executable}"
            )
        if self.extensions is None:
            self.extensions = []
        for extension in self.extensions:
            try:
                ext = extension["extension"]
                verb = extension["verb"]
                executable = extension["executable"]
            except KeyError:
                raise ValueError(
                    "Each extension must have at least extension, verb, "
                    "and executable"
                )
            try:
                component = self.separate_components[executable]
            except KeyError:
                raise ValueError(
                    "Executable must be the base target name of one of the "
                    "distribution's executables"
                )
            progid = msilib.make_id(
                "{}.{}.{}".format(
                    self.distribution.get_name(),
                    os.path.splitext(executable)[0],
                    self.distribution.get_version(),
                )
            )
            mime = extension.get("mime", None)
            # "%1" a better default for argument?
            argument = extension.get("argument", None)
            context = extension.get("context", f"{fullname} {verb}")
            # Add rows via self.data to safely ignore duplicates
            self._append_to_data(
                "ProgId",
                progid,
                None,
                None,
                self.distribution.get_description(),
                None,
                None,
            )
            self._append_to_data(
                "Extension", ext, component, progid, mime, "default"
            )
            self._append_to_data("Verb", ext, verb, 0, context, argument)
            if mime is not None:
                self._append_to_data("MIME", mime, ext, "None")
            # Registry entries that allow proper display of the app in menu
            self._append_to_data(
                "Registry",
                f"{progid}-name",
                -1,
                fr"Software\Classes\{progid}",
                "FriendlyAppName",
                self.distribution.get_name(),
                component,
            )
            self._append_to_data(
                "Registry",
                f"{progid}-verb-{verb}",
                -1,
                fr"Software\Classes\{progid}\shell\{verb}",
                "FriendlyAppName",
                self.distribution.get_name(),
                component,
            )
            self._append_to_data(
                "Registry",
                f"{progid}-author",
                -1,
                fr"Software\Classes\{progid}\Application",
                "ApplicationCompany",
                self.distribution.get_author(),
                component,
            )

    def initialize_options(self):
        distutils.command.bdist_msi.bdist_msi.initialize_options(self)
        self.upgrade_code = None
        self.product_code = None
        self.add_to_path = None
        self.initial_target_dir = None
        self.target_name = None
        self.directories = None
        self.environment_variables = None
        self.data = None
        self.summary_data = None
        self.install_icon = None
        self.all_users = False
        self.extensions = None

    def run(self):
        if not self.skip_build:
            self.run_command("build")
        install = self.reinitialize_command("install", reinit_subcommands=1)
        bdist_dir = self.bdist_dir
        install.prefix = bdist_dir
        install.skip_build = self.skip_build
        install.warn_dir = 0
        log.info(f"installing to {bdist_dir}")
        install.ensure_finalized()
        install.run()
        self.mkpath(self.dist_dir)
        fullname = self.distribution.get_fullname()
        if os.path.exists(self.target_name):
            os.unlink(self.target_name)
        metadata = self.distribution.metadata
        author = metadata.author or metadata.maintainer or "UNKNOWN"
        version = metadata.get_version()
        sversion = ".".join(
            str(x) for x in distutils.version.LooseVersion(version).version
        )

        # msilib is reloaded in order to reset the "_directories" global member
        # in that module.  That member is used by msilib to prevent any two
        # directories from having the same logical name.  _directories might
        # already have contents due to msilib having been previously used in
        # the current instance of the python interpreter -- if so, it could
        # prevent the root from getting the logical name TARGETDIR, breaking
        # the MSI.
        importlib.reload(msilib)

        if self.product_code is None:
            self.product_code = msilib.gen_uuid()
        self.db = msilib.init_database(
            self.target_name,
            msilib.schema,
            self.distribution.metadata.name,
            self.product_code,
            sversion,
            author,
        )
        msilib.add_tables(self.db, msilib.sequence)
        self.add_properties()
        self.add_config(fullname)
        self.add_upgrade_config(sversion)
        self.add_ui()
        self.add_files()
        self.db.Commit()
        self.distribution.dist_files.append(
            ("bdist_msi", sversion or "any", self.target_name)
        )

        if not self.keep_temp:
            log.info(f"removing '{bdist_dir}' (and everything under it)")
            if not self.dry_run:
                try:
                    shutil.rmtree(bdist_dir)
                except OSError as exc:
                    log.warn(f"error removing {bdist_dir}: {exc}")

        # Cause the MSI file to be released. Without this, then if bdist_msi
        # is run programmatically from within a larger script, subsequent
        # editting of the MSI is blocked.
        self.db = None


def _is_valid_guid(code):
    pattern = re.compile(
        r"^\{[0-9A-F]{8}-([0-9A-F]{4}-){3}[0-9A-F]{12}\}$", re.IGNORECASE
    )
    return isinstance(code, str) and pattern.match(code) is not None
