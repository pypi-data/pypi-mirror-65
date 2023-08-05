"""Testing clifold python project"""
import subprocess
import shutil
import os

from clifold import clifold_main


cmd = ['python3', 'clifold/clifold_main.py', 'testing', '-g', '-p', '-i']
output = subprocess.run(cmd, shell=True, executable='/bin/bash')
print(output)
python_path = shutil.which('python3')
# command = [
#     f'{python_path} {clifold_main}.py -g -p -i',
#     f'{python_path} {clifold_main}.py -g -p -i',
#     f'{python_path} {clifold_main}.py -g -p -i',
#     f'{python_path} {clifold_main}.py -g -p -i',
#     f'{python_path} {clifold_main}.py -g -p -i',
#     f'{python_path} {clifold_main}.py -g -p -i',
#     f'{python_path} {clifold_main}.py -g -p -i',
#     f'{python_path} {clifold_main}.py -g -p -i',
# ]

# for i in range(len(command)):
#     print(f"Testing Test {i}...")
#     subprocess.check_output([command[i]])

# subprocess.run(["python3", 'clifold/clifold_main.py',
#                 'testing', '-g', '-np', '-i'], check=True)
# print(output)
# os.chdir('testing')


# def test():
#     '''Hard coded testing'''
#     assert os.path.exists('tests') == True
#     assert os.path.exists('testing') == True
#     assert os.path.exists('bin') == True
#     assert os.path.exists('include') == True
#     assert os.path.exists('lib') == True
#     assert os.path.exists('README.md') == True
#     assert os.path.exists('pyvenv.cfg') == True
#     assert os.path.exists('setup.py') == True
#     assert os.path.exists('src/testing/__init__.py') == True
#     assert os.path.exists('src/testing/main.py') == True
#     assert os.path.exists('tests/__init__.py') == True
#     assert os.path.exists('tests/test_main.py') == True
