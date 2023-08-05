"""Create a project with venv."""
import os
import venv
import sys


def create(pname):
    '''
    Project creation function.

    Args:
        pname: project_name

    Returns:
        Absolute Project Path
    '''
    proj_files = ['__init__', 'main']
    test_files = ['__init__', 'test_main']
    dirs_folders = [f'{pname}/{pname}', f'{pname}/tests']

    current_path = os.getcwd()
    exist_path = os.path.join(current_path, pname)
    project_path = os.path.join(exist_path, pname)
    if os.path.exists(exist_path):
        print("Project {} already exists in {}.\n".format(pname, current_path))
        sys.exit()
    else:
        venv.create(pname)
        os.chdir(exist_path)
        for i in range(len(dirs_folders)):
            os.makedirs(os.path.join(exist_path, dirs_folders[i]))
            for j in range(len(dirs_folders)):
                if i == 0:
                    open(f"{dirs_folders[i]}/{proj_files[j]}.py", 'x').close()
                else:
                    open(f"{dirs_folders[i]}/{test_files[j]}.py", 'x').close()

        print("\n🎉 Project {} created in {}.\n".format(pname, current_path))

    return project_path
