'''Testing clifold python project'''
# from clifold.clifold import main
import subprocess
import shutil
import os


python_path = shutil.which('python3')
# command = [f'{python_path} clifold_main.py -g -p -i', f'{python_path} clifold_main.py -ng -np -ni',
#            f'{python_path} clifold_main.py -ng -p -i', f'{python_path} clifold_main.py -ng -np -i',
#            f'{python_path} clifold_main.py -g -np -ni', f'{python_path} clifold_main.py -ng -p -ni',
#            f'{python_path} clifold_main.py -g -np -i', f'{python_path} clifold_main.py -g -p -ni'
#            ]

# for i in range(len(command)):
#     print(f"Testing Test {i}...")
#     subprocess.run([command[i]], check=True)

subprocess.run([python_path, 'clifold/clifold_main.py', 'testing', '-g', '-np', '-i'], check=True)
os.chdir('testing')


def test():
    '''Hard coded testing'''
    assert os.path.exists('src') == True
    assert os.path.exists('tests') == True
    assert os.path.exists('src/testing') == True
    assert os.path.exists('bin') == True
    assert os.path.exists('include') == True
    assert os.path.exists('lib') == True
    assert os.path.exists('README.md') == True
    assert os.path.exists('pyvenv.cfg') == True
    assert os.path.exists('setup.py') == True
    assert os.path.exists('src/testing/__init__.py') == True
    assert os.path.exists('src/testing/main.py') == True
    assert os.path.exists('tests/__init__.py') == True
    assert os.path.exists('tests/test_main.py') == True
