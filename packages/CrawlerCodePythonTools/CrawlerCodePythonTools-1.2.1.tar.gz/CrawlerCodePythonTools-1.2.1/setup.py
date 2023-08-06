from setuptools import setup

def readme():
    with open("README.rst") as f:
        README = f.read()
    return README


TYPE = "CORE"  # "CORE" "GUI" "WEBBOT"

packages = ['pythontools.core', 'pythontools.identity', 'pythontools.sockets', 'pythontools.dev']
install_requires = ["colorama"]
if TYPE == "GUI": packages.append('pythontools.gui') and install_requires.append('PyQt5')
if TYPE == "WEBBOT": packages.append('pythontools.webbot') and install_requires.append('selenium')

setup(
    name='CrawlerCodePythonTools' + ('-Gui' if TYPE == "GUI" else '-WebBot' if TYPE == "WEBBOT" else ''),
    version='1.2.1',
    packages=packages,
    url='https://github.com/CrawlerCode',
    license='',
    author='CrawlerCode',
    author_email='',
    description='',
    long_description=readme(),
    long_description_content_type="text/x-rst",
    include_package_data=True,
    install_requires=install_requires
)
