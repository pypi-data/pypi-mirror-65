import setuptools
from lsoft_oss_pytools.version import Version

setuptools.setup(
    name='lsoft-oss-pytools',
    url='https://gitlab.com/lsoft-oss/pytools',
    license='GNU General Public License v3.0',
    author='Marco Bartel',
    author_email='bartel@electronic-shop.lu',
    version=Version('0.2.0').number,
    description='General purpose tool functions and classes',
    long_description=open('README.md').read().strip(),
    long_description_content_type="text/markdown",
    py_modules=['lsoft_oss_pytools'],
    install_requires=[],
    zip_safe=False,
    keywords='lsoft-oss pytools base36',
)
