"""Install packages with pip."""
import os
import subprocess
# import shutil
import shlex


def pip(pkg, root_path, pname):
    '''
    Packages installation function.

    Args:
        pkg: True or False
        project_path: absolute path to the project
        pname: project name

    Returns:
        Packages installed or not installed
    '''
    if pkg:
        os.chdir(root_path)
        pip_path = "bin/pip3"
        # shell_path = os.environ['SHELL']
        # shell = os.path.basename(shell_path)
        # if shell == "bash" or "zsh":
        #     cmd = f"{pname}/bin/activate"
        # elif shell == "csh" or "tcsh":
        #     cmd = f"{pname}/bin/activate.csh"
        # elif shell == "fish":
        #     cmd = f"{pname}/bin/activate.fish"
        # else:
        #     raise OSError("\nUnknown Shell!")
        pkg = input("\n📦 Packages you want to install: ")
        pkgs = shlex.split(pkg)
        args = [pip_path, "install"]
        for i in range(len(args)):
            pkgs.insert(i, args[i])

        # subprocess.run(["source", cmd], shell=True, executable=shell_path)
        # os.chdir(project_path)
        print('\n🔰 Downloading packages...\n')
        subprocess.run(pkgs, check=True)
        return 1
    else:
        print("\nNo package downloaded...")
        return 0
