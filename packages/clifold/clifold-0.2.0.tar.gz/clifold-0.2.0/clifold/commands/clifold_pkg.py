"""Install packages with pip."""
import os
import subprocess
import shutil
import shlex


def pip(pkg, project_path, pname):
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
        pip_path = shutil.which('pip3')
        shell_path = os.environ['SHELL']
        shell = os.path.basename(shell_path)
        if shell == 'bash' or 'zsh':
            cmd = ['source', f'{pname}/bin/activate']
        elif shell == 'csh' or 'tcsh':
            cmd = ['source', f'{pname}/bin/activate.csh']
        elif shell == 'fish':
            cmd = ['.', f'{pname}/bin/activate.fish']
        pkg = input("\n📦 Packages you want to install: ")
        pkgs = shlex.split(pkg)
        args = [pip_path, 'install']
        for i in range(len(args)):
            pkgs.insert(i, args[i])

        subprocess.run(cmd, shell=True, executable=shell_path)
        os.chdir(project_path)
        print('\n🔰 Downloading packages...\n')
        subprocess.check_call(pkgs)
        return 1
    else:
        print("\nNo package downloaded...")
        return 0
