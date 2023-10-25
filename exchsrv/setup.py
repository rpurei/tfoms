from setuptools import setup
from distutils.dir_util import copy_tree
from Cython.Build import cythonize
import os
import os.path
import shutil

exclude_files_list = ['uwsgi.py', 'setup.py', 'config.py', '__init__.py', 'mek.py', 'nsifoms.py', 'tfoms_statuses.py']

try:
    if os.path.exists('build'):
        shutil.rmtree('build')
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in [f for f in filenames if f.endswith('.py')]:
            if filename not in exclude_files_list :
                setup(ext_modules=cythonize(os.path.join(dirpath, filename)),
                      options={'compiler_directives': {'always_allow_keywords': True, 'language_level': '3'}},)
                print(f'Cythonize "{os.path.join(dirpath, filename)}"')

    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in [f for f in filenames if f.endswith('.c')]:
            if os.path.exists(os.path.join(dirpath, filename)):
                os.remove(os.path.join(dirpath, filename))
                print(f'File "{os.path.join(dirpath, filename)}" removed')

    copy_tree('app/templates', 'build/lib.linux-x86_64-3.9/app/templates')
    print(f'Dir "templates" copied')
    copy_tree('app/static', 'build/lib.linux-x86_64-3.9/app/static')
    print(f'Dir "static" copied')
    copy_tree('app/opt', 'build/lib.linux-x86_64-3.9/app/opt')
    print(f'Dir "opt" copied')
    shutil.copyfile('requirements.txt', 'build/lib.linux-x86_64-3.9/requirements.txt')
    print(f'File "requirements.txt" copied')
    shutil.copyfile('uwsgi.py', 'build/lib.linux-x86_64-3.9/uwsgi.py')
    print(f'File "requirements.txt" copied')
    shutil.copyfile('app/config.py', 'build/lib.linux-x86_64-3.9/app/config.py')
    print(f'File "config.py" copied')
    shutil.copyfile('app/__init__.py', 'build/lib.linux-x86_64-3.9/app/__init__.py')
    shutil.copyfile('app/auth/__init__.py', 'build/lib.linux-x86_64-3.9/app/auth/__init__.py')
    shutil.copyfile('app/models/__init__.py', 'build/lib.linux-x86_64-3.9/app/models/__init__.py')
    shutil.copyfile('app/tasks/__init__.py', 'build/lib.linux-x86_64-3.9/app/tasks/__init__.py')
    shutil.copyfile('app/tasks/tfoms_statuses.py', 'build/lib.linux-x86_64-3.9/app/tasks/tfoms_statuses.py')
    shutil.copyfile('app/utils/__init__.py', 'build/lib.linux-x86_64-3.9/app/utils/__init__.py')
    shutil.copyfile('app/views/__init__.py', 'build/lib.linux-x86_64-3.9/app/views/__init__.py')
    shutil.rmtree('build/temp.linux-x86_64-3.9')
except Exception as err:
    print(f'Error: {str(err)}')
