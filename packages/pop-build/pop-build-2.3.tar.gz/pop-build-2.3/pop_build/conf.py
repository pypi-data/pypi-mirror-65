CLI_CONFIG = {
    "config": {"options": ["-c"],},
    "name": {"options": ["-n"],},
    "directory": {"options": ["-D", "--dir"],},
    "run": {"options": ["-R"],},
    "requirements": {"options": ["-r"],},
    "exclude": {"options": ["-e"],},
    "system_site": {"options": ["-S"], "action": "store_true",},
    "dev_pyinstaller": {"options": ["--dev-pyinst"], "action": "store_true",},
    "pyinstaller_runtime_tmpdir": {"options": ["--pyinstaller-runtime-tmpdir"],},
    "onedir": {"action": "store_true",},
    "pyenv": {},
    "no_clean": {"action": "store_true",},
    "locale_utf8": {"options": ["--locale-utf8"], "action": "store_true",},
    "pkg_builder": {},
    "pkg_tgt": {},
    "srcdir": {},
    "system_copy_in": {"nargs": "*",},
}

CONFIG = {
    "config": {
        "default": "",
        "help": "Load extra options from a configuration file, this is useful when the project needs to use more advanced features like compiling c binaries into the environment.",
    },
    "name": {"default": None, "help": "The name of the project to build",},
    "directory": {
        "default": ".",
        "help": "The path to the directory to build from. This denotes the root of the python project souce tree to work from. This directory should have the setup.py and the paths referenced in configurations will assume that this is the root path they are working from.",
    },
    "run": {"default": "run.py", "help": "The location of the project run.py file",},
    "requirements": {
        "default": "requirements.txt",
        "help": "The name of the requirements.txt file to use",
    },
    "exclude": {
        "default": "exclude.txt",
        "help": "The path to the exclude file, these python packages will be uninstalled",
    },
    "system_site": {
        "default": False,
        "help": "Include the system site-packages when building. This is needed for builds from custom minstalls of Python",
    },
    "dev_pyinstaller": {
        "default": False,
        "help": "Use the latest development build of PyInstaller. This can fix issues on newer versions of python not yet supported by mainline releases.",
    },
    "pyinstaller_runtime_tmpdir": {
        "default": None,
        "help": "Pyinstaller rumtime tmpdir",
    },
    "onedir": {
        "default": False,
        "help": "Instead of producing a single binary produce a directory with all components",
    },
    "pyenv": {
        "default": "system",
        "help": 'Set the python version to build with, if not present the system python will be used. Only use CPython versions, to see available versions run `pyenv install --list | grep " 3\.[6789]"`',
    },
    "no_clean": {
        "default": False,
        "help": "Don't run the clean up sequence, this will leave the venv, spec file and other artifacts. Only use this for debugging.",
    },
    "locale_utf8": {
        "default": False,
        "help": "Use the UTF-8 locale with PyInstaller, as in PEP538 and PEP540. This enables UTF-8 on systems which only provide C or POSIX locales.",
    },
    "build": {
        "default": False,
        "help": """Enter in commands to build a non-python binary into the deployed binary.
            The build options are set on a named project basis. This allows for multiple shared
            binaries to be embedded into the final build:

            build:
              libsodium:
                make:
                   - wget libsodium
                   - tar xvf libsodium*
                   - cd libsodium
                   - ./configure
                   - make
                src: libsodium/libsodium.so
                dest: lib64/
                """,
    },
    "pkg": {"default": {}, "help": "Options for building packages"},
    "pkg_builder": {
        "default": "fpm",
        "help": "Select what package builder plugin to use.",
    },
    "pkg_tgt": {
        "defualt": "pacman",
        "help": "Specify the os/distribution target to build the package against.",
    },
    "srcdir": {
        "default": None,
        "help": "Instead of reading in a requirements.txt file, install all of the python package sources and/or wheels found in the specific directory",
    },
    "system_copy_in": {
        "default": None,
        "help": "A list of directories to copy into the build venv that are not otherwise detected",
    },
}
SUBCOMMANDS = {}
DYNE = {
    "pop_build": ["pop_build"],
}
