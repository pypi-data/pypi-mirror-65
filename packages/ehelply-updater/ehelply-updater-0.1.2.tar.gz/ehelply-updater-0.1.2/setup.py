from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ehelply-updater',
    packages=find_packages(),  # this must be the same as the name above
    version='0.1.2',
    description='eHelply Updater',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Shawn Clake',
    author_email='shawn.clake@gmail.com',
    url='https://github.com/ehelply/Updater',
    keywords=[],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'wheel',

        # Helpful packages (Comment in/out as needed)
        'requests == 2.22.*',
        'python-slugify',

        'pydantic == 0.30.*',

        # Packages for dev or testing (DO NOT comment these out)
        'pytest == 5.0.*',

        # Misc eHelply Packages (Comment in/out as needed)
        'ehelply-logger >= 0.0.8',

        # Required for CLI
        'click',
    ],
    entry_points={
        'console_scripts': [
            'ehelplyupdater=ehelply_updater.ehelply_updater:ehelplyupdater',  # command=package.module:function
        ],
    },

)
