"""Install packages with pip."""
import os
import subprocess
import shutil
import shlex


def pip(pkg, project_path):
    '''
    Packages installation function.

    Args:
        pkg: True or False
        project_path: absolute path to the project

    Returns:
        Packages installed or not installed
    '''
    if pkg:
        pip_path = shutil.which('pip3')
        os.chdir(project_path)
        pkg = input("\n📦 Packages you want to install: ")
        pkgs = shlex.split(pkg)
        args = [pip_path, 'install']
        freeze = [pip_path, 'freeze', '>', 'requirements.txt']
        for i in range(len(args)):
            pkgs.insert(i, args[i])

        print('\n🔰 Downloading packages...\n')
        subprocess.check_call(pkgs)
        subprocess.check_call(freeze)
    else:
        print("\nNo package downloaded...")
