from setuptools import setup

try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except:
    with open("README.md", "r") as f:
        long_description = f.read()

setup(
    name='toggle-admin',
    version='0.2',
    packages=['toggle_admin', 'toggle_admin.src', 'toggle_admin.http'],
    url='https://github.com/zpodushkin/toggle-admin',
    license='GPL-3.0',
    author='zpodushkin',
    author_email='',
    description='Asynchronous module for issuing admin permissions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=['aiohttp', 'vkbottle']
)
