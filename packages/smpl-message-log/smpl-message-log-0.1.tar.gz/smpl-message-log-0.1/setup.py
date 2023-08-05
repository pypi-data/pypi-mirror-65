import setuptools
from os.path import join, dirname

import smpl_message_log

setuptools.setup(
    name='smpl-message-log',
    packages=setuptools.find_packages(),
    version=smpl_message_log.__version__,
    license='MIT',
    url='https://github.com/ilya-muhortov/smpl-message-log',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown"
)
