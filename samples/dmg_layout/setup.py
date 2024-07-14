"""A very simple setup script to create a single executable.

hello.py is a very simple 'Hello, world' type script which also displays the
environment in which the script runs.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the script without Python
"""

from cx_Freeze import Executable, setup

executables = [
    Executable(
        script="hello.py",
        # You can also specify an icon for the executable that will be reused for the dmg
        # only the first executable is used for the icon
        # icon="../../cx_Freeze/icons/python.icns" #noqa: ERA001
    ),
    Executable(script="hello2.py"),
]

setup(
    name="hello",
    version="0.1.2.3",
    description="Sample cx_Freeze script",
    executables=executables,
    options={
        "bdist_mac": {
            "bundle_name": "hello",
        },
        "bdist_dmg": {
            "applications_shortcut": True,
            "volume_label": "Howdy Yall",
            # from the svg color list, but all of these work too https://dmgbuild.readthedocs.io/en/latest/settings.html#background
            "background": "darkviolet",
            "show_status_bar": True,
            "show_tab_view": True,
            "show_path_bar": True,
            "show_sidebar": True,
            "sidebar_width": 150,
            "silent": False,
            "default_view": "icon-view",
            "list_icon_size": 48,
            "list_text_size": 12,
            "list_scroll_position": (0, 0),
            "list_columns": ["name", "size"],
            "list_column_widths": {"name": 200, "size": 100},
            "list_column_sort_directions": {
                "name": "ascending",
                "size": "ascending",
            },
        },
    },
)
