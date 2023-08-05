import os
import sys

a = input("have you updated conf.py, __init__.py and setup.py with the version"
          "name? (y/n)")
if a == 'y':
    os.system('cmd /k "python setup.py sdist bdist_wheel"')
else:
    print('exiting....')
    sys.exit()

b = input('Check it - all OK? (y/n)')
if b == 'y':
    os.system('cmd /k "twine upload --repository-url https://test.pypi.org/'
              'legacy/ dist/*"')
else:
    print('exiting....')
