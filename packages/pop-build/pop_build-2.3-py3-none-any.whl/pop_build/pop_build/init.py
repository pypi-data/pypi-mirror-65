# Import python libs
import os
import uuid
import subprocess
import shutil
import tempfile


def __init__(hub):
    hub.pop.sub.load_subdirs(hub.pop_build)
    hub.pop_build.BUILDS = {}
    hub.pop_build.SYSTEMD = ("rhel7", "rhel8", "arch", "debian10")
    hub.pop_build.SYSTEMD_DIR = "usr/lib/systemd/system/"
    hub.pop_build.SYSV = ("rhel5", "rhel6")
    hub.pop_build.SYSV_DIR = "etc/init.d"


def cli(hub):
    """
    Execute the routine from the CLI
    """
    hub.pop.config.load(["pop_build"], cli="pop_build")
    hub.pop_build.init.builder(
        hub.OPT["pop_build"]["name"],
        hub.OPT["pop_build"]["requirements"],
        hub.OPT["pop_build"]["system_site"],
        hub.OPT["pop_build"]["exclude"],
        hub.OPT["pop_build"]["directory"],
        hub.OPT["pop_build"]["dev_pyinstaller"],
        hub.OPT["pop_build"]["pyinstaller_runtime_tmpdir"],
        hub.OPT["pop_build"]["build"],
        hub.OPT["pop_build"]["pkg"],
        hub.OPT["pop_build"]["onedir"],
        hub.OPT["pop_build"]["pyenv"],
        hub.OPT["pop_build"]["run"],
        hub.OPT["pop_build"]["no_clean"],
        hub.OPT["pop_build"]["locale_utf8"],
        hub.OPT["pop_build"]["pkg_tgt"],
        hub.OPT["pop_build"]["pkg_builder"],
        hub.OPT["pop_build"]["srcdir"],
        hub.OPT["pop_build"]["system_copy_in"],
    )


def new(
    hub,
    name,
    requirements,
    sys_site,
    exclude,
    directory,
    dev_pyinst=False,
    pyinstaller_runtime_tmpdir=None,
    build=None,
    pkg=None,
    onedir=False,
    pyenv="system",
    run="run.py",
    locale_utf8=False,
    pkg_tgt=None,
    pkg_builder=None,
    srcdir=None,
    system_copy_in=None,
):
    venv_dir = tempfile.mkdtemp()
    is_win = os.name == "nt"
    if is_win:
        python_bin = os.path.join(venv_dir, "Scripts", "python")
        s_path = os.path.join(venv_dir, "Scripts", name)
    else:
        python_bin = os.path.join(venv_dir, "bin", "python3")
        if locale_utf8:
            s_path = "env PYTHONUTF8=1 LANG=POSIX " + os.path.join(
                venv_dir, "bin", name
            )
        else:
            s_path = os.path.join(venv_dir, "bin", name)
    bname = str(uuid.uuid1())
    requirements = os.path.join(directory, requirements)
    hub.pop_build.BUILDS[bname] = {
        "name": name,
        "build": build,
        "pkg": pkg,
        "pkg_tgt": pkg_tgt,
        "pkg_builder": pkg_builder,
        "binaries": [],
        "is_win": is_win,
        "exclude": exclude,
        "requirements": requirements,
        "sys_site": sys_site,
        "dir": os.path.abspath(directory),
        "srcdir": srcdir,
        "dev_pyinst": dev_pyinst,
        "pyinstaller_runtime_tmpdir": pyinstaller_runtime_tmpdir,
        "system_copy_in": system_copy_in,
        "run": os.path.join(directory, run),
        "spec": os.path.join(directory, f"{name}.spec"),
        "pybin": python_bin,
        "s_path": s_path,
        "venv_dir": venv_dir,
        "vroot": os.path.join(venv_dir, "lib"),
        "onedir": onedir,
        "all_paths": set(),
        "imports": set(),
        "datas": set(),
        "cmd": f"{python_bin} -B -OO -m PyInstaller ",
        "pyenv": pyenv,
        "pypi_args": [
            s_path,
            "--log-level=INFO",
            "--noconfirm",
            "--onedir" if onedir else "--onefile",
            "--clean",
        ],
        "locale_utf8": locale_utf8,
    }
    req = hub.pop_build.init.mk_requirements(bname)
    hub.pop_build.BUILDS[bname]["req"] = req
    return bname


def mk_requirements(hub, bname):
    opts = hub.pop_build.BUILDS[bname]
    req = os.path.join(opts["dir"], "__build_requirements.txt")
    with open(opts["requirements"], "r") as rfh:
        data = rfh.read()
    with open(req, "w+") as wfh:
        wfh.write(data)
    return req


def builder(
    hub,
    name,
    requirements,
    sys_site,
    exclude,
    directory,
    dev_pyinst=False,
    pyinstaller_runtime_tmpdir=None,
    build=None,
    pkg=None,
    onedir=False,
    pyenv="system",
    run="run.py",
    no_clean=False,
    locale_utf8=False,
    pkg_tgt=None,
    pkg_builder=None,
    srcdir=None,
    system_copy_in=None,
):
    bname = hub.pop_build.init.new(
        name,
        requirements,
        sys_site,
        exclude,
        directory,
        dev_pyinst,
        pyinstaller_runtime_tmpdir,
        build,
        pkg,
        onedir,
        pyenv,
        run,
        locale_utf8,
        pkg_tgt,
        pkg_builder,
        srcdir,
        system_copy_in,
    )
    hub.pop_build.venv.create(bname)
    hub.pop_build.data.version(bname)
    hub.pop_build.build.make(bname)
    hub.pop_build.venv.scan(bname)
    hub.pop_build.venv.mk_adds(bname)
    hub.pop_build.inst.mk_spec(bname)
    hub.pop_build.inst.call(bname)
    if pkg_tgt:
        hub.pop_build.pkg.init.build(bname)
    hub.pop_build.post.report(bname)
    if not no_clean:
        hub.pop_build.post.clean(bname)
